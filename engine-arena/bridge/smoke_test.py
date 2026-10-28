#!/usr/bin/env python3
"""smoke_test: the arena field proves its verbs end to end.

Run ON the Orin against the live bridge (127.0.0.1:8797). Exercises:
reset, a locked attempt without the key (must stay, event names the
lock), the key route (warehouse -> quay -> market -> gate opens with
the brass key -> lighthouse treasure), and times every act so the
round-trip numbers in ENGINE-ON-ORIN.md are this script's output.
"""

import json
import sys
import time

sys.path.insert(0, "/home/casey/engine-arena/bridge")
from world_bridge import ScorerClient, WorldClient  # noqa: E402

w = WorldClient()
s = ScorerClient()
timings = []


def act(direction):
    t0 = time.time()
    obs = w.step(direction)
    timings.append(round(time.time() - t0, 2))
    truth = s.truth()
    print(f"act {direction:9s} -> place={obs['place']!r} "
          f"contents={obs['contents']} holding={obs['holding']} "
          f"event={obs['event']!r} [truth: {truth['region']} "
          f"@ {truth['pos']}] ({timings[-1]}s)")
    return obs, truth


def main():
    print("== reset ==")
    obs = w.reset(1)
    print("start:", obs["place"], "truth:", s.truth())

    print("== locked attempt, no key ==")
    act("northeast")                      # quay -> market
    obs, truth = act("east")              # gate: locked
    assert truth["region"] == "market", "must stay in the market"
    assert obs["event"] and "locked" in obs["event"], obs["event"]

    print("== the key route ==")
    w.reset(1)
    act("north")                          # quay -> warehouse (key)
    obs, truth = act("south")
    act("northeast")                      # -> market
    obs, truth = act("east")              # gate opens with the key
    assert truth["region"] == "lighthouse", truth
    assert "treasure" in obs["contents"], obs
    assert obs["event"] and "brass key" in obs["event"], obs["event"]

    print("== a blocked nonsense verb ==")
    obs = w.step("sideways")
    print("event:", obs["event"])
    assert obs["event"] and "no way" in obs["event"]

    print(f"act round trips (s): {timings}")
    print("SMOKE PASS")
    print(json.dumps({"act_seconds": timings}))


if __name__ == "__main__":
    main()
