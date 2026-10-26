"""The reference environment: an uncharted dungeon.

SuperInstance — liquid-world-model.

A hand-designed grid dungeon of 13 rooms implementing the ``World``
protocol. The agent perceives a room only by being in it: the
observation names the room it stands in, the exits it can see (and,
through open archways, the rooms beyond), and the contents in front
of it. No coordinates are ever given. Features, by design:

* a goal: the vault, holding the treasure;
* one locked door (treasury -> vault) whose brass key sits in the
  library — the agent must learn both facts by walking into them;
* one dark room (the cellar) where the senses report low trust;
* one room whose contents change between days (the shrine: lit
  candles on day 1, cold ashes after) — the world's own small
  surprise, waiting for whoever re-enters on a later day.

``reset(day)`` is harness-side (the demo owns the engine): a new day
puts the agent back at the entrance, the key back in the library,
the treasure back in the vault. Presence is flushed by the world
and the episode by the model; the chart is what persists.
"""

from __future__ import annotations

from typing import Any, Dict, List

from .engine import Observation

# direction -> (dcol, drow), used only for the world's own map and
# for the chart renderer's sketch. Never exposed to the agent.
DELTAS = {
    "north": (0, -1), "south": (0, 1), "east": (1, 0), "west": (-1, 0),
    "up": (-1, -1), "down": (1, 1),
}

# room: description, base contents, exits {direction: (room, archway?)}
ROOMS: Dict[str, Dict[str, Any]] = {
    "entrance": {
        "description": "A torch-lit entrance hall. Cold air from outside.",
        "contents": [],
        "exits": {"north": ("hall", True)},
    },
    "hall": {
        "description": "A long hall with doors on every side.",
        "contents": [],
        "exits": {"south": ("entrance", True), "west": ("library", False),
                  "east": ("gallery", True), "north": ("chapel", False)},
    },
    "library": {
        "description": "Shelves of drowned books. Something glints.",
        "contents": ["brass key"],
        "exits": {"east": ("hall", False), "north": ("study", False)},
    },
    "study": {
        "description": "A desk, a cold hearth, maps under glass.",
        "contents": ["dusty maps"],
        "exits": {"south": ("library", False), "east": ("chapel", False)},
    },
    "chapel": {
        "description": "A small chapel; stairs wind down into dark.",
        "contents": [],
        "exits": {"south": ("hall", False), "west": ("study", False),
                  "north": ("shrine", False), "down": ("cellar", False)},
    },
    "shrine": {
        "description": "A stone shrine, older than the dungeon.",
        "contents": ["lit candles"],  # day 1 only; see reset()
        "exits": {"south": ("chapel", False)},
    },
    "cellar": {
        "description": "A cellar. It is very dark here.",
        "contents": ["wine barrels"],
        "dark": True,
        "exits": {"up": ("chapel", False), "east": ("crypt", False)},
    },
    "crypt": {
        "description": "A crypt of stacked bones and quiet.",
        "contents": ["old bones"],
        "exits": {"west": ("cellar", False), "north": ("treasury", False)},
    },
    "gallery": {
        "description": "A gallery of portraits with scratched-out eyes.",
        "contents": [],
        "exits": {"west": ("hall", True), "north": ("armory", True),
                  "east": ("garden", True)},
    },
    "armory": {
        "description": "Racks of rusted spears.",
        "contents": ["rusted spear"],
        "exits": {"south": ("gallery", True), "north": ("treasury", False)},
    },
    "garden": {
        "description": "A drowned garden under a cracked glass roof.",
        "contents": ["pale flowers"],
        "exits": {"west": ("gallery", True), "east": ("armory", True)},
    },
    "treasury": {
        "description": "An empty treasury. One heavy door leads north.",
        "contents": [],
        "exits": {"south": ("armory", False), "west": ("crypt", False),
                  "north": ("vault", False)},
    },
    "vault": {
        "description": "The vault. Something shines in the dark.",
        "contents": ["treasure"],
        "exits": {"south": ("treasury", False)},
    },
}

LOCKED = {("treasury", "north"): "brass key"}
START = "entrance"


class DungeonWorld:
    """A World. ``truth()`` exists for the scorer only."""

    def __init__(self) -> None:
        self.day = 0
        self.reset(1)

    # -- harness-side --------------------------------------------------
    def reset(self, day: int) -> None:
        self.day = day
        self.room = START
        self.holding: List[str] = []
        self.key_taken = False
        self._event = None

    # -- World protocol --------------------------------------------------
    def observe(self) -> Observation:
        room = ROOMS[self.room]
        exits = {}
        for direction, (dest, archway) in sorted(room["exits"].items()):
            exits[direction] = {"through": dest if archway else None}
        contents = list(room["contents"])
        if self.room == "shrine" and self.day >= 2:
            contents = ["cold ashes"]  # the world's own small surprise
        if self.room == "library" and self.key_taken:
            contents = [c for c in contents if c != "brass key"]
        obs: Observation = {
            "place": self.room,
            "description": room["description"],
            "exits": exits,
            "contents": contents,
            "holding": list(self.holding),
            "trust": 0.3 if room.get("dark") else 1.0,
            "event": self._event,
        }
        self._event = None
        return obs

    def actions(self) -> List[str]:
        return sorted(ROOMS[self.room]["exits"])

    def step(self, action: str) -> Observation:
        room = ROOMS[self.room]
        if action not in room["exits"]:
            self._event = f"There is no way {action} from here."
            return self.observe()
        dest, _archway = room["exits"][action]
        needed = LOCKED.get((self.room, action))
        if needed and needed not in self.holding:
            self._event = f"The {action} door is locked."
            return self.observe()
        origin = self.room
        self.room = dest
        if needed:
            self._event = f"The brass key turns; the {action} door unlocks."
        if dest == "library" and not self.key_taken:
            self.key_taken = True
            self.holding.append("brass key")
            self._event = "You take the brass key."
        if dest != origin and self._event is None:
            self._event = None
        return self.observe()

    # -- scoring only --------------------------------------------------
    def truth(self) -> Dict[str, Any]:
        return {"room": self.room, "day": self.day,
                "holding": list(self.holding), "key_taken": self.key_taken}
