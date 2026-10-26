"""The engine-agnostic contract: what a World owes an agent.

SuperInstance — liquid-world-model.

Any engine or simulator can host a liquid world model by implementing
the ``World`` protocol below. The split that matters:

* ``observe()`` delivers a *partial* observation — what the agent's
  senses report NOW. It is never the full state. Rooms are perceived
  by being in them; the rest of the world is belief.
* ``actions()`` lists the legal action names in the current state.
* ``step(action)`` advances the world and returns the new observation.

An engine MAY also expose ``truth()`` — the ground state — but that
exists for SCORING ONLY: a demo harness or referee may call it to
grade what happened. Agent-side code (the liquid model, the policy)
must never see it. That is enforced by structure, not by honour:
``agent_view()`` wraps a world in an object that exposes exactly
``observe`` / ``actions`` / ``step`` and nothing else. There is no
attribute path from the view back to the wrapped world's ``truth``.

Observation shape (a plain dict, JSON-friendly):

    {
      "place":    <perceived identity of the current place>,
      "exits":    {<direction>: {"through": <perceived place or None>}},
      "contents": [<perceived contents...>],
      "holding":  [<items the agent perceives itself carrying>],
      "trust":    <0.0..1.0 — how much the senses vouch for this reading>,
      "event":    <string or None — what just happened, e.g. a locked door>,
    }

Engines may add fields; the model only relies on these.
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, Protocol, runtime_checkable

Observation = Dict[str, Any]


@runtime_checkable
class World(Protocol):
    """The surface an engine/simulator exposes to an agent."""

    def observe(self) -> Observation:
        """Partial observation of the current state. Never full state."""
        ...

    def actions(self) -> List[str]:
        """Legal action names right now."""
        ...

    def step(self, action: str) -> Observation:
        """Take an action; return the resulting observation."""
        ...


@runtime_checkable
class ScoredWorld(World, Protocol):
    """A World that can also be graded. ``truth`` is for scorers only."""

    def truth(self) -> Dict[str, Any]:
        """Ground state. SCORING ONLY — never shown to the agent."""
        ...


class _AgentView:
    """The only face of a world that agent-side code ever receives.

    Exposes exactly the World protocol surface. ``truth`` (and every
    other engine attribute) is unreachable through this object.
    """

    __slots__ = ("_world",)

    def __init__(self, world: World) -> None:
        self._world = world

    def observe(self) -> Observation:
        return self._world.observe()

    def actions(self) -> List[str]:
        return self._world.actions()

    def step(self, action: str) -> Observation:
        return self._world.step(action)


def agent_view(world: World) -> _AgentView:
    """Wrap ``world`` so agent-side code cannot reach ``truth()``."""
    return _AgentView(world)


def scorer_truth(world: World) -> Optional[Dict[str, Any]]:
    """SCORING ONLY. Harness/referee helper — never pass to a model."""
    fn = getattr(world, "truth", None)
    return fn() if callable(fn) else None
