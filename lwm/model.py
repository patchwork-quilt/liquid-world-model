"""The liquid model: a chart of a world it has not finished learning,
and the day cycle that keeps the chart honest.

SuperInstance — liquid-world-model.

The chart is the model's understanding, built only from what it has
perceived. Its load-bearing properties:

* **Belief with a memory.** Every place holds a *current belief*
  (exits, contents) and an append-only *history* of how that belief
  came to be. A belief is never overwritten silently: every change
  goes through a revision entry that keeps both versions.
* **Doubt, both directions.** The world can contradict the model
  (a door believed passable is locked) — recorded as a *surprise*,
  both versions kept. And the model can doubt its own senses: an
  observation flagged low-trust lowers confidence instead of
  rewriting a held belief (it may still sketch a place never
  charted — a dim first look is better than no look).
* **The uncharted set is first-class.** Exits seen but never taken,
  places believed-adjacent but never entered: enumerable on demand,
  not an absence. The model can list what it knows it hasn't charted.
* **Fog of war.** Charted is not current. A place carries
  ``last_seen_day``; unseen for more than ``FOG_FRESH_DAYS`` days it
  is *fogged* — its belief stands, but its effective confidence
  decays by ``FOG_DECAY`` per fogged day. Re-observing restores both.
* **The day cycle.** ``wake`` begins a day (fresh episode log; the
  chart and the distilled essence persist), ``dream`` turns the day
  into testimony (surprises listed, revisions with reasons, lessons
  in plain lines, essence distilled), ``sleep`` archives the episode
  into the ledger and flushes the day's presence.
"""

from __future__ import annotations

import random
from typing import Any, Dict, List, Optional, Tuple

from .engine import Observation, World, agent_view

# --- fog of war -----------------------------------------------------
# A place last seen FOG_FRESH_DAYS or fewer days ago is current.
# Beyond that it is fogged, and its effective confidence is its
# charted confidence * FOG_DECAY ** (days fogged).
FOG_FRESH_DAYS = 1
FOG_DECAY = 0.9

TRUST_FLOOR = 0.5  # below this, a reading is doubted, not believed


class Place:
    """One perceived place and everything the model believes about it."""

    __slots__ = (
        "id", "observed", "observations", "last_seen_day", "last_seen_step",
        "confidence", "belief_exits", "belief_contents", "history",
    )

    def __init__(self, place_id: str) -> None:
        self.id = place_id
        self.observed = False            # actually been there and perceived it
        self.observations = 0
        self.last_seen_day = -1
        self.last_seen_step = -1
        self.confidence = 0.0            # charted (base) confidence
        self.belief_exits: Dict[str, Dict[str, Any]] = {}
        self.belief_contents: List[str] = []
        self.history: List[Dict[str, Any]] = []  # append-only revision log

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id, "observed": self.observed,
            "observations": self.observations,
            "last_seen_day": self.last_seen_day,
            "confidence": round(self.confidence, 3),
            "belief_exits": self.belief_exits,
            "belief_contents": list(self.belief_contents),
        }


class Chart:
    """The model's whole understanding of the world, as far as it goes."""

    def __init__(self) -> None:
        self.places: Dict[str, Place] = {}
        # (place, direction) -> {"attempts": [ {day, step, outcome, ...} ]}
        self.edges: Dict[Tuple[str, str], Dict[str, Any]] = {}

    # -- internal helpers -------------------------------------------
    def _place(self, place_id: str) -> Place:
        p = self.places.get(place_id)
        if p is None:
            p = Place(place_id)
            self.places[place_id] = p
        return p

    @staticmethod
    def _revise(place: Place, day: int, step: int, aspect: str, key: str,
                old: Any, new: Any, reason: str, surprise: bool) -> Dict[str, Any]:
        entry = {
            "type": "surprise" if surprise else "revision",
            "day": day, "step": step, "place": place.id, "aspect": aspect,
            "key": key, "believed": old, "observed": new,
            "reason": reason, "surprise": surprise,
        }
        place.history.append(entry)  # append-only: both versions kept
        return entry

    # -- perception ---------------------------------------------------
    def observe(self, obs: Observation, day: int, step: int) -> List[Dict[str, Any]]:
        """Fold one observation into the chart. Returns entries made
        (surprises and revisions), in the order they happened."""
        entries: List[Dict[str, Any]] = []
        place = self._place(obs["place"])
        trust = float(obs.get("trust", 1.0))
        first_sight = not place.observed
        place.observed = True
        place.observations += 1
        place.last_seen_day = day
        place.last_seen_step = step

        if trust < TRUST_FLOOR:
            # Doubted senses: confidence drops; a held belief is NOT
            # rewritten. A place never charted may still be sketched.
            place.confidence = max(0.05, (place.confidence or 0.4) - 0.05)
            entries.append({
                "type": "distrusted", "day": day, "step": step,
                "place": place.id, "trust": trust,
                "reason": "senses flagged unreliable; belief not rewritten",
            })
            if not first_sight:
                return entries

        if first_sight:
            place.confidence = max(place.confidence, 0.6)
        else:
            place.confidence = min(0.95, place.confidence + 0.05)

        # --- contents ---
        seen_contents = sorted(obs.get("contents", []))
        if first_sight:
            place.belief_contents = list(seen_contents)
            place.history.append({
                "type": "formed", "day": day, "step": step, "place": place.id,
                "aspect": "contents", "key": "", "believed": None,
                "observed": list(seen_contents),
                "reason": "first sight", "surprise": False,
            })
        elif seen_contents != sorted(place.belief_contents):
            entries.append(self._revise(
                place, day, step, "contents", "",
                list(place.belief_contents), list(seen_contents),
                "contents differ from what I believed was here", True))
            place.belief_contents = list(seen_contents)
            place.confidence = max(0.05, place.confidence - 0.25)

        # --- exits ---
        seen_exits = obs.get("exits", {})
        for direction in sorted(seen_exits):
            through = seen_exits[direction].get("through")
            cur = place.belief_exits.get(direction)
            if cur is None:
                place.belief_exits[direction] = {
                    "to": through, "locked": None, "passable": True,
                    "opens_with": None,
                }
                place.history.append({
                    "type": "formed", "day": day, "step": step,
                    "place": place.id, "aspect": "exit", "key": direction,
                    "believed": None,
                    "observed": {"to": through, "passable": True},
                    "reason": "exit first seen", "surprise": False,
                })
                if through is not None:
                    self._place(through)  # believed-adjacent place
            elif through is not None and cur.get("to") is None:
                entries.append(self._revise(
                    place, day, step, "exit-to", direction,
                    None, through, "destination seen through the opening",
                    False))
                cur["to"] = through
                self._place(through)
            elif through is not None and cur.get("to") != through:
                entries.append(self._revise(
                    place, day, step, "exit-to", direction,
                    cur.get("to"), through,
                    "the opening shows a different place than I believed",
                    True))
                cur["to"] = through
                place.confidence = max(0.05, place.confidence - 0.25)
        # exits that vanished since the belief was formed
        if not first_sight:
            for direction in sorted(set(place.belief_exits) - set(seen_exits)):
                old = place.belief_exits.pop(direction)
                entries.append(self._revise(
                    place, day, step, "exit", direction, old, None,
                    "an exit I believed in is not here now", True))
                place.confidence = max(0.05, place.confidence - 0.25)
        return entries

    def record_transition(self, place_id: str, direction: str,
                          predicted_to: Optional[str], obs_after: Observation,
                          day: int, step: int,
                          holding_before: List[str]) -> List[Dict[str, Any]]:
        """Record what an attempted move actually did. Returns entries."""
        entries: List[Dict[str, Any]] = []
        place = self._place(place_id)
        belief = place.belief_exits.setdefault(
            direction, {"to": None, "locked": None, "passable": True,
                        "opens_with": None})
        event = obs_after.get("event") or ""
        actual = obs_after["place"]
        edge = self.edges.setdefault((place_id, direction), {"attempts": []})

        if actual == place_id and "locked" in event:
            edge["attempts"].append({
                "day": day, "step": step, "outcome": "blocked-locked",
                "holding": list(holding_before), "event": event,
            })
            if belief.get("passable"):
                entries.append(self._revise(
                    place, day, step, "exit-passable", direction,
                    True, False, event, True))
            belief["passable"] = False
            belief["locked"] = True
            place.confidence = max(0.05, place.confidence - 0.2)
        elif actual == place_id:
            edge["attempts"].append({
                "day": day, "step": step, "outcome": "stayed",
                "holding": list(holding_before), "event": event,
            })
        else:
            edge["attempts"].append({
                "day": day, "step": step, "outcome": "traversed",
                "to": actual, "holding": list(holding_before), "event": event,
            })
            self._place(actual)
            if predicted_to is not None and predicted_to != actual:
                entries.append(self._revise(
                    place, day, step, "exit-to", direction,
                    predicted_to, actual,
                    "the way out led somewhere else than I believed", True))
                place.confidence = max(0.05, place.confidence - 0.25)
            if belief.get("locked"):
                # A locked door opening is a resolution, not a surprise:
                # the belief was "locked", never "impassable forever".
                # What it opens WITH is the fact worth charting — the
                # door does not become unconditionally passable.
                opener = next((i for i in holding_before if i in event),
                              None)
                if belief.get("opens_with") != opener:
                    entries.append(self._revise(
                        place, day, step, "exit-opens-with", direction,
                        belief.get("opens_with"), opener,
                        event or "the way opened while I held what it "
                                 "needed", False))
                    belief["opens_with"] = opener
            else:
                belief["passable"] = True
            belief["to"] = actual
        return entries

    # -- queries --------------------------------------------------------
    def known_exits(self, place_id: str) -> Dict[str, Dict[str, Any]]:
        p = self.places.get(place_id)
        return dict(p.belief_exits) if p else {}

    def believed_destination(self, place_id: str, direction: str) -> Optional[str]:
        ex = self.known_exits(place_id).get(direction) or {}
        return ex.get("to")

    def edge_status(self, place_id: str, direction: str) -> Dict[str, Any]:
        edge = self.edges.get((place_id, direction))
        if not edge or not edge["attempts"]:
            return {"tried": False, "traversed": False, "last": None}
        last = edge["attempts"][-1]
        return {
            "tried": True,
            "traversed": any(a["outcome"] == "traversed" for a in edge["attempts"]),
            "last": last,
        }

    def traversed_graph(self) -> Dict[str, Dict[str, str]]:
        graph: Dict[str, Dict[str, str]] = {}
        for (place_id, direction), edge in self.edges.items():
            for a in edge["attempts"]:
                if a["outcome"] == "traversed":
                    graph.setdefault(place_id, {})[direction] = a["to"]
        return graph

    def transit_graph(self, holding: List[str]) -> Dict[str, Dict[str, str]]:
        """Edges the model currently believes it can walk: an edge is
        walkable if its most recent attempt succeeded — or if it last
        blocked under different conditions than the agent is in now
        (it carries something it did not carry then)."""
        graph: Dict[str, Dict[str, str]] = {}
        for (pid, direction), edge in self.edges.items():
            if not edge["attempts"]:
                continue
            last = edge["attempts"][-1]
            dest = None
            for a in reversed(edge["attempts"]):
                if a["outcome"] == "traversed":
                    dest = a["to"]
                    break
            if dest is None:
                continue
            if last["outcome"] == "traversed":
                graph.setdefault(pid, {})[direction] = dest
            elif (last["outcome"] == "blocked-locked" and
                  set(holding) - set(last.get("holding", []))):
                graph.setdefault(pid, {})[direction] = dest
        return graph

    def goal_place(self) -> Optional[str]:
        """A place believed to hold the goal (contents mention treasure)."""
        for pid in sorted(self.places):
            if "treasure" in self.places[pid].belief_contents:
                return pid
        return None

    def rooms_charted(self) -> int:
        return sum(1 for p in self.places.values() if p.observed)

    # -- fog of war -----------------------------------------------------
    def is_fogged(self, place_id: str, day: int) -> bool:
        p = self.places.get(place_id)
        if p is None or not p.observed:
            return False
        return (day - p.last_seen_day) > FOG_FRESH_DAYS

    def effective_confidence(self, place_id: str, day: int) -> float:
        p = self.places.get(place_id)
        if p is None:
            return 0.0
        if not self.is_fogged(place_id, day):
            return p.confidence
        fog_days = (day - p.last_seen_day) - FOG_FRESH_DAYS
        return round(p.confidence * (FOG_DECAY ** fog_days), 4)

    # -- the uncharted set ------------------------------------------------
    def uncharted(self) -> List[Dict[str, Any]]:
        """What the model knows it has not charted. First-class output."""
        out: List[Dict[str, Any]] = []
        for pid in sorted(self.places):
            p = self.places[pid]
            if not p.observed:
                out.append({"place": pid, "direction": None,
                            "believed_to": None, "status": "believed-unvisited"})
                continue
            for direction in sorted(p.belief_exits):
                status = self.edge_status(pid, direction)
                if status["traversed"]:
                    continue
                out.append({
                    "place": pid, "direction": direction,
                    "believed_to": p.belief_exits[direction].get("to"),
                    "status": ("blocked-locked" if status["last"] and
                               status["last"]["outcome"] == "blocked-locked"
                               else "never-tried"),
                })
        return out


class LiquidModel:
    """A chart, a day cycle, and an episode that testifies before it goes."""

    GOAL_CONTENTS = "treasure"

    def __init__(self, world: World, policy: Any = None, seed: int = 0) -> None:
        self.view = agent_view(world)  # agent-side: truth() is unreachable
        from .policy import ExplorerPolicy  # deferred: policy imports chart types only
        self.policy = policy if policy is not None else ExplorerPolicy()
        self.rng = random.Random(seed)
        self.chart = Chart()
        self.day = 0
        self.alignment: Optional[str] = None
        self.episode: List[Dict[str, Any]] = []
        self.archive: Dict[int, Dict[str, Any]] = {}
        self.essence: List[Dict[str, Any]] = []  # distilled notes, persist
        self.day_surprises: List[Dict[str, Any]] = []
        self.recall_spent_today = 0
        self._testimony: Optional[Dict[str, Any]] = None
        self.last_stats: Dict[str, Any] = {}

    # -- day cycle ------------------------------------------------------
    def wake(self, alignment: str) -> None:
        """Begin a day. The chart and the essence persist; the episode
        (the day's presence) starts fresh."""
        self.day += 1
        self.alignment = alignment
        self.episode = [{"type": "wake", "day": self.day, "alignment": alignment}]
        self.day_surprises = []
        self.recall_spent_today = 0
        self._testimony = None

    def spend_recall(self, units: int) -> None:
        """Recall draws from the same purse as action (see tiers.py)."""
        self.recall_spent_today += units

    def run_day(self, max_steps: int = 600) -> Dict[str, Any]:
        """The act loop: perceive, fold into the chart, let the policy
        pick, step, record what the step actually did."""
        if self.day == 0:
            raise RuntimeError("wake() must begin a day before run_day()")
        charted_before = self.chart.rooms_charted()
        obs = self.view.observe()
        steps = 0
        reached = False
        while True:
            for entry in self.chart.observe(obs, self.day, steps):
                self._log(entry)
            if self.GOAL_CONTENTS in obs.get("contents", []):
                reached = True
                break
            if steps >= max_steps:
                break
            action = self.policy.decide(self.chart, obs, self.rng)
            if action is None:
                break
            current = obs["place"]
            predicted = self.chart.believed_destination(current, action)
            holding_before = list(obs.get("holding", []))
            obs = self.view.step(action)
            steps += 1
            for entry in self.chart.record_transition(
                    current, action, predicted, obs, self.day, steps,
                    holding_before):
                self._log(entry)
        self.last_stats = {
            "day": self.day, "steps": steps, "goal_reached": reached,
            "rooms_charted": self.chart.rooms_charted(),
            "rooms_new": self.chart.rooms_charted() - charted_before,
            "uncharted_exits": len([u for u in self.chart.uncharted()
                                     if u["direction"] is not None]),
            "surprises": len(self.day_surprises),
            "recall_spent": self.recall_spent_today,
        }
        return self.last_stats

    def _log(self, entry: Dict[str, Any]) -> None:
        self.episode.append(entry)
        if entry.get("surprise"):
            self.day_surprises.append(entry)

    def dream(self) -> Dict[str, Any]:
        """The day testifies. Surprises listed, revisions given reasons,
        lessons stated in plain lines, essence distilled for the tiers."""
        lines: List[str] = []
        stats = self.last_stats
        lines.append(
            f"Day {self.day}: charted {stats.get('rooms_charted', 0)} places "
            f"({stats.get('rooms_new', 0)} new), {stats.get('surprises', 0)} "
            f"surprise(s), goal "
            f"{'reached' if stats.get('goal_reached') else 'not reached'} "
            f"in {stats.get('steps', 0)} steps.")
        lessons: List[str] = []
        for s in self.day_surprises:
            lines.append(
                f"Surprise: in {s['place']}, I believed {s['aspect']} "
                f"{s.get('key') or ''} was {s['believed']!r}; "
                f"it was {s['observed']!r}. ({s['reason']})")
            lessons.append(self._lesson_from(s))
        for e in self.episode:
            if e.get("type") == "revision" and not e.get("surprise"):
                lines.append(
                    f"Revised: {e['place']} {e['aspect']} {e.get('key') or ''}: "
                    f"{e['believed']!r} -> {e['observed']!r} ({e['reason']}).")
                lessons.append(self._lesson_from(e))
            elif e.get("type") == "distrusted":
                lessons.append(
                    f"Lesson: my senses are unreliable in {e['place']}; "
                    "beliefs there stay soft.")
        lessons = list(dict.fromkeys(lessons))  # a day may repeat itself
        for lesson in lessons:
            lines.append(lesson)
        # Distil essence: one portable line per surprise/revision + summary.
        for s in self.day_surprises:
            self.essence.append({
                "day": self.day, "kind": "surprise",
                "line": (f"day {self.day}: in {s['place']}, the {s['aspect']} "
                         f"I believed ({s['believed']!r}) was wrong; "
                         f"it is {s['observed']!r}."),
            })
        for lesson in lessons:
            self.essence.append({"day": self.day, "kind": "lesson", "line": lesson})
        self.essence.append({"day": self.day, "kind": "summary", "line": lines[0]})
        self._testimony = {
            "day": self.day, "lines": lines, "lessons": lessons,
            "surprises": list(self.day_surprises),
        }
        return self._testimony

    @staticmethod
    def _lesson_from(entry: Dict[str, Any]) -> str:
        aspect, key, place = entry["aspect"], entry.get("key") or "", entry["place"]
        if aspect == "exit-passable" and entry["observed"] is False:
            return (f"Lesson: the {key} way out of {place} is not freely "
                    f"passable — I was stopped there.")
        if aspect == "exit-opens-with":
            return (f"Lesson: the {key} way out of {place} is locked, "
                    f"and opens to the {entry['observed']}.")
        if aspect == "contents":
            return f"Lesson: what sits in {place} can change between visits."
        if aspect == "exit-to":
            return (f"Lesson: the {key} way out of {place} does not lead "
                    f"where I believed it did.")
        if aspect == "exit":
            return f"Lesson: {place} is not shaped the way I believed."
        return f"Lesson: {place} taught me something about {aspect}."

    def sleep(self) -> None:
        """Flush the day's presence into the ledger. The chart and the
        essence — what the day *meant* — persist."""
        if self._testimony is None:
            self.dream()
        self.archive[self.day] = {
            "alignment": self.alignment,
            "entries": list(self.episode),
            "testimony": self._testimony,
            "stats": dict(self.last_stats),
        }
        self.episode = []
        self.day_surprises = []
        self._testimony = None
