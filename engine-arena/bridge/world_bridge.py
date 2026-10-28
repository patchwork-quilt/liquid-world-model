#!/usr/bin/env python3
"""world_bridge: the Luanti arena, exposed in the farm's idiom.

SuperInstance — Orin engine arena.

One process, two faces:

* Engine side: file IPC with the `arena` mod inside the Luanti
  dedicated server (bridge_state.json / bridge_action.json in the
  world directory, atomic renames both ways). The mod polls the
  action file ~every 0.15 s; an act() round trip is that poll plus
  the walk itself (a region step is a real walk across the room).

* Client side: an HTTP API on 127.0.0.1:8797 shaped exactly like the
  liquid framework's World protocol, plus a scorer-only /truth:

    GET  /health            {ok, state_age_s, busy}
    GET  /observe           framework Observation (place = perceptual
                            signature; never a true region name)
    GET  /actions           [direction, ...]
    POST /act   {"action": "north"}   -> Observation after the step
    POST /reset {"day": 1}            -> Observation at the start cell
    GET  /truth             SCORING ONLY: {region, pos, holding, day}

  and a farm-style CLI, mirroring farm.py's call(name, input):

    python3 world_bridge.py serve [--world-dir DIR] [--port 8797]
    python3 world_bridge.py call observe
    python3 world_bridge.py call act north
    python3 world_bridge.py call reset 2
    python3 world_bridge.py call truth

Events are delivered exactly once (the dungeon semantics): the mod
keeps `event` in its state until the next move, so the bridge tracks
the state generation that introduced the current event and only
surfaces it on the first read after that generation.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any, Dict, List, Optional

DEFAULT_WORLD_DIR = Path.home() / "engine-arena" / "luanti" / "worlds" / "arena"


class EngineLink:
    """File-IPC link to the arena mod."""

    def __init__(self, world_dir: Path) -> None:
        self.state_file = world_dir / "bridge_state.json"
        self.action_file = world_dir / "bridge_action.json"
        self._lock = threading.Lock()
        self._seq = 0
        self._event_seen_gen = -1
        st = self.read_state()
        if st:
            self._seq = int(st.get("action_seq", 0))

    def read_state(self) -> Optional[Dict[str, Any]]:
        try:
            raw = self.state_file.read_text()
            return json.loads(raw)
        except (OSError, json.JSONDecodeError):
            return None

    def _write_action(self, payload: Dict[str, Any]) -> int:
        with self._lock:
            self._seq += 1
            payload = dict(payload, seq=self._seq)
            tmp = self.action_file.with_suffix(".json.tmp")
            tmp.write_text(json.dumps(payload))
            os.replace(tmp, self.action_file)
            return self._seq

    def command(self, payload: Dict[str, Any],
                timeout: float = 30.0) -> Dict[str, Any]:
        """Send a command; wait until the mod has consumed it and is
        no longer busy. Returns the resulting state snapshot."""
        seq = self._write_action(payload)
        deadline = time.time() + timeout
        saw_busy = False
        while time.time() < deadline:
            st = self.read_state()
            if st and int(st.get("action_seq", 0)) >= seq:
                if st.get("busy"):
                    saw_busy = True
                else:
                    return st
            time.sleep(0.05)
        raise TimeoutError(f"engine did not settle after {payload} "
                           f"(seq {seq}, saw_busy={saw_busy})")

    # -- framework-shaped views over a state snapshot ----------------
    def observation(self, st: Dict[str, Any]) -> Dict[str, Any]:
        contents = st.get("contents") or []
        if isinstance(contents, dict):  # Lua empty-table artefact
            contents = []
        # Same artefact, sharper edge: a closed door's exit entry is
        # an empty Lua table, which write_json renders as null — the
        # framework's contract wants {"through": None} there. The
        # bridge normalises engine JSON into the Observation shape.
        exits = {}
        for direction, entry in (st.get("exits") or {}).items():
            if isinstance(entry, dict):
                exits[direction] = {"through": entry.get("through")}
            else:
                exits[direction] = {"through": None}
        event = st.get("event")
        # The dedup key carries the engine's boot id: state_seq restarts
        # from zero on every engine boot, and the bridge outlives boots.
        gen = (str(st.get("boot_id", "")), int(st.get("state_seq", 0)))
        with self._lock:
            if event and gen != self._event_seen_gen:
                self._event_seen_gen = gen
            elif event:
                event = None
        return {
            "place": st.get("signature", "open ground"),
            "exits": exits,
            "contents": list(contents),
            "holding": list(st.get("holding") or []),
            "trust": 1.0,
            "event": event,
        }


def make_handler(link: EngineLink):
    class Handler(BaseHTTPRequestHandler):
        protocol_version = "HTTP/1.1"

        def log_message(self, *args):  # keep the desk box quiet
            pass

        def _send(self, code: int, obj: Any) -> None:
            body = json.dumps(obj).encode()
            self.send_response(code)
            self.send_header("Content-Type", "application/json")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        def _body(self) -> Dict[str, Any]:
            n = int(self.headers.get("Content-Length") or 0)
            if not n:
                return {}
            try:
                return json.loads(self.rfile.read(n) or b"{}")
            except json.JSONDecodeError:
                return {}

        def _state_or_503(self) -> Optional[Dict[str, Any]]:
            st = link.read_state()
            if st is None:
                self._send(503, {"error": "engine state unavailable"})
            return st

        def do_GET(self) -> None:
            if self.path == "/health":
                st = link.read_state()
                age = None
                if link.state_file.exists():
                    age = round(time.time()
                                - link.state_file.stat().st_mtime, 2)
                self._send(200, {"ok": st is not None,
                                 "state_age_s": age,
                                 "busy": bool(st and st.get("busy"))})
            elif self.path == "/observe":
                st = self._state_or_503()
                if st:
                    self._send(200, link.observation(st))
            elif self.path == "/actions":
                st = self._state_or_503()
                if st:
                    self._send(200, sorted((st.get("exits") or {}).keys()))
            elif self.path == "/truth":
                st = self._state_or_503()
                if st:
                    self._send(200, {
                        "region": st.get("truth_region"),
                        "pos": st.get("pos"),
                        "holding": st.get("holding"),
                        "day": st.get("day"),
                    })
            else:
                self._send(404, {"error": "no such route"})

        def do_POST(self) -> None:
            try:
                if self.path == "/act":
                    action = str(self._body().get("action", ""))
                    st = link.command({"type": "move", "action": action})
                    self._send(200, link.observation(st))
                elif self.path == "/reset":
                    day = int(self._body().get("day", 1))
                    st = link.command({"type": "reset", "day": day})
                    self._send(200, link.observation(st))
                else:
                    self._send(404, {"error": "no such route"})
            except TimeoutError as exc:
                self._send(504, {"error": str(exc)})

    return Handler


def serve(world_dir: Path, port: int) -> None:
    link = EngineLink(world_dir)
    server = ThreadingHTTPServer(("127.0.0.1", port), make_handler(link))
    print(f"world_bridge serving on 127.0.0.1:{port} "
          f"(world dir {world_dir})", flush=True)
    server.serve_forever()


# ---------------------------------------------------------------- client
class WorldClient:
    """The framework-facing client. Deliberately has NO truth method:
    scoring uses a separate ScorerClient, mirroring agent_view."""

    def __init__(self, base: str = "http://127.0.0.1:8797") -> None:
        self.base = base

    def _req(self, method: str, path: str,
             payload: Optional[Dict[str, Any]] = None) -> Any:
        import urllib.request
        data = json.dumps(payload).encode() if payload is not None else None
        req = urllib.request.Request(
            self.base + path, data=data, method=method,
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=40) as resp:
            return json.loads(resp.read() or b"null")

    def observe(self) -> Dict[str, Any]:
        return self._req("GET", "/observe")

    def actions(self) -> List[str]:
        return self._req("GET", "/actions")

    def step(self, action: str) -> Dict[str, Any]:
        return self._req("POST", "/act", {"action": action})

    def reset(self, day: int = 1) -> Dict[str, Any]:
        return self._req("POST", "/reset", {"day": day})


class ScorerClient:
    """SCORING ONLY. Kept apart from WorldClient on purpose."""

    def __init__(self, base: str = "http://127.0.0.1:8797") -> None:
        self.base = base

    def truth(self) -> Dict[str, Any]:
        import urllib.request
        with urllib.request.urlopen(self.base + "/truth",
                                    timeout=10) as resp:
            return json.loads(resp.read())


def cli(argv: List[str]) -> int:
    ap = argparse.ArgumentParser(prog="world_bridge")
    ap.add_argument("--world-dir", type=Path, default=DEFAULT_WORLD_DIR)
    ap.add_argument("--port", type=int, default=8797)
    ap.add_argument("--base", default="http://127.0.0.1:8797")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("serve")
    call = sub.add_parser("call")
    call.add_argument("name", choices=["observe", "actions", "act",
                                       "reset", "truth", "health"])
    call.add_argument("input", nargs="?", default="")
    args = ap.parse_args(argv)

    if args.cmd == "serve":
        serve(args.world_dir, args.port)
        return 0
    client = WorldClient(args.base)
    if args.name == "observe":
        out = client.observe()
    elif args.name == "actions":
        out = client.actions()
    elif args.name == "act":
        out = client.step(args.input)
    elif args.name == "reset":
        out = client.reset(int(args.input or 1))
    elif args.name == "truth":
        out = ScorerClient(args.base).truth()
    else:
        out = client._req("GET", "/health")
    print(json.dumps(out, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    sys.exit(cli(sys.argv[1:]))
