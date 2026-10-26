"""The policy: deliberately dumb, so improvement belongs to the chart.

SuperInstance — liquid-world-model.

A simple legible explorer:

1. If the current place has an *actionable uncharted exit* — never
   successfully traversed, and not known-blocked under the same
   conditions — take one. This is edge-probing: the model hunts its
   own ignorance first. (A door that blocked the agent while
   empty-handed becomes actionable again once it carries something
   new: conditions changed, so the edge is unprobed again.)
2. Else, if a charted path leads to the goal-belief (a place
   believed to hold the treasure), follow its first step.
3. Else, walk the charted graph to the nearest place that still has
   an actionable uncharted exit, first step first.
4. Else, pick a legal exit at seeded random.

All randomness flows from the model's seeded RNG, so a run is fully
deterministic per seed. The policy knows nothing the chart doesn't;
it has no access to the world, to ``truth()``, or to the engine.
"""

from __future__ import annotations

import random
from collections import deque
from typing import Any, Dict, List, Optional

from .engine import Observation


class ExplorerPolicy:
    def decide(self, chart: Any, obs: Observation,
               rng: random.Random) -> Optional[str]:
        place = obs["place"]
        holding = list(obs.get("holding", []))
        exits = chart.known_exits(place)
        if not exits:  # chart hasn't formed this place yet: trust the senses
            exits = {d: {"to": None, "locked": None, "passable": True}
                     for d in obs.get("exits", {})}

        def actionable(direction: str) -> bool:
            status = chart.edge_status(place, direction)
            if status["traversed"]:
                return False
            last = status["last"]
            if last and last["outcome"] == "blocked-locked":
                # Retry only if we now carry something we didn't then.
                return bool(set(holding) - set(last.get("holding", [])))
            return True

        here = [d for d in sorted(exits) if actionable(d)]
        if here:
            return rng.choice(here)

        graph = chart.transit_graph(holding)

        def bfs_to(predicate) -> Optional[str]:
            seen = {place}
            queue = deque([(place, None)])
            while queue:
                node, first = queue.popleft()
                if node != place and predicate(node):
                    return first
                for direction in sorted(graph.get(node, {})):
                    nxt = graph[node][direction]
                    if nxt not in seen:
                        seen.add(nxt)
                        queue.append((nxt, direction if first is None else first))
            return None

        goal = chart.goal_place()
        if goal is not None and goal != place:
            step = bfs_to(lambda n: n == goal)
            if step is not None:
                return step

        def has_actionable(node: str) -> bool:
            node_holding = holding  # conditions travel with the agent
            for d in chart.known_exits(node):
                st = chart.edge_status(node, d)
                if st["traversed"]:
                    continue
                last = st["last"]
                if last and last["outcome"] == "blocked-locked":
                    if not set(node_holding) - set(last.get("holding", [])):
                        continue
                return True
            return False

        step = bfs_to(has_actionable)
        if step is not None:
            return step
        if exits:
            return rng.choice(sorted(exits))
        return None
