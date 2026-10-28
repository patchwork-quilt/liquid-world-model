#!/usr/bin/env python3
"""play_in_arena: the liquid framework plays in the real engine.

Run ON the Orin. The framework's LiquidModel + ExplorerPolicy chart
the Luanti arena through the bridge's observe/act alone; truth is
read scorer-side only, exactly as in the dungeon leagues: the
adapter below is the harness's world handle (like DungeonWorld, it
carries a truth() the model's agent_view structurally hides), and
every step is logged as (signature, truth region) pairs so merges
and splits are counted from receipts, not impressions.

Also captures tegrastats during play as the GPU receipt.

Outputs ~/engine-arena/play/play_results.json.
"""

import json
import subprocess
import sys
import time
from pathlib import Path

sys.path.insert(0, "/home/casey/engine-arena/play")    # the lwm package
sys.path.insert(0, "/home/casey/engine-arena/bridge")  # world_bridge

from lwm.model import LiquidModel          # noqa: E402
from world_bridge import ScorerClient, WorldClient  # noqa: E402

OUT = Path("/home/casey/engine-arena/play/play_results.json")
TEGRA_LOG = Path("/home/casey/engine-arena/play/tegrastats.log")
DAYS = 3
MAX_STEPS = 120


class ArenaWorld:
    """The harness's handle on the field. Agent-side methods use the
    WorldClient only; truth() is scorer-side and never reaches the
    model (LiquidModel wraps this in agent_view)."""

    def __init__(self) -> None:
        self._client = WorldClient()
        self._scorer = ScorerClient()
        self.step_log = []

    # agent-side (the World's contract)
    def observe(self):
        return self._client.observe()

    def actions(self):
        return self._client.actions()

    def step(self, action):
        obs = self._client.step(action)
        truth = self._scorer.truth()
        self.step_log.append({
            "signature": obs["place"],
            "region": truth["region"],
            "pos": truth["pos"],
            "event": obs.get("event"),
        })
        return obs

    # harness-side
    def reset(self, day):
        obs = self._client.reset(day)
        truth = self._scorer.truth()
        self.step_log.append({
            "signature": obs["place"],
            "region": truth["region"],
            "pos": truth["pos"],
            "event": "reset",
        })
        return obs

    def truth(self):
        return self._scorer.truth()


def main() -> None:
    tegra = subprocess.Popen(
        ["sudo", "-n", "tegrastats", "--interval", "1000"],
        stdout=open(TEGRA_LOG, "w"), stderr=subprocess.DEVNULL)
    t0 = time.time()
    try:
        world = ArenaWorld()
        model = LiquidModel(world, seed=7)
        day_stats = []
        for day in range(1, DAYS + 1):
            world.reset(day)
            model.wake("attend")
            stats = model.run_day(max_steps=MAX_STEPS)
            model.dream()
            model.sleep()
            day_stats.append(stats)
            print(f"day {day}: {stats}", flush=True)
    finally:
        tegra.terminate()
        try:
            tegra.wait(timeout=5)
        except subprocess.TimeoutExpired:
            tegra.kill()
    wall = round(time.time() - t0, 1)

    # -- score the chart against the arena's truth -------------------
    sig_to_regions = {}
    region_to_sigs = {}
    for entry in world.step_log:
        sig_to_regions.setdefault(entry["signature"], set()).add(
            entry["region"])
        region_to_sigs.setdefault(entry["region"], set()).add(
            entry["signature"])
    merges = {s: sorted(r) for s, r in sig_to_regions.items()
              if len(r) > 1}
    splits = {r: sorted(s) for r, s in region_to_sigs.items()
              if len(s) > 1}
    chart = model.chart
    results = {
        "days": day_stats,
        "wall_s": wall,
        "total_steps": sum(d["steps"] for d in day_stats),
        "goal_days": sum(1 for d in day_stats if d["goal_reached"]),
        "places_charted": chart.rooms_charted(),
        "true_regions": sorted(region_to_sigs.keys()),
        "true_region_count": len(region_to_sigs),
        "signatures_seen": len(sig_to_regions),
        "merges": merges,
        "splits": splits,
        "total_surprises": sum(d["surprises"] for d in day_stats),
        "step_log": world.step_log,
        "chart_places": sorted(chart.places.keys()),
    }
    OUT.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    print(json.dumps({k: v for k, v in results.items()
                      if k != "step_log"}, indent=2, ensure_ascii=False))
    print(f"wrote {OUT}")


if __name__ == "__main__":
    main()
