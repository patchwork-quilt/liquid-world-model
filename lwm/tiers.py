"""Memory tiers and routed recall.

SuperInstance — liquid-world-model.

The internal engine runs on a budget: retrieval time is spent from
the same purse as action. So remembering is routed, and the route
decides both the price and the fidelity:

* **REFLEX** (``route="reflex"``) — today's hot cache: the live
  episode, still in hand. Instant and summary-grade. It can only
  answer about *today*, and it never opens the archive — by
  construction the reflex branch reads ``model.episode`` and
  nothing else.
* **ESSENCE** (``route="essence"``) — the chart plus the distilled
  notes the dreams left behind. Fast; serves the current believed
  answer, which may be fogged and is always short of the detail.
* **LEDGER / truth** (``route="truth"``) — the archived episode
  logs of slept days: "when I think back on how it actually
  happened." Slow, and the only route that opens the archive and
  returns the full testified record.

``recall(model, query, route)`` returns ``(answer, cost_units)``;
the cost is charged to the model's current day via
``model.spend_recall``.

Query shapes (plain dicts):

* ``{"kind": "surprise", "day": D, "index": i}`` — the i-th surprise
  of day D.
* ``{"kind": "event", "day": D, "index": i}`` — the i-th recorded
  episode entry of day D.
* ``{"kind": "place", "place": name}`` — what is believed about a
  place (served by essence from the chart; reflex cannot know).
"""

from __future__ import annotations

from typing import Any, Dict, List, Tuple

# The purse is denominated in attention units. Ordering is the point:
COST_REFLEX = 1
COST_ESSENCE = 4
COST_TRUTH = 12

ROUTES = ("reflex", "essence", "truth")


def _charge(model: Any, units: int) -> None:
    spend = getattr(model, "spend_recall", None)
    if callable(spend):
        spend(units)


def _find(entries: List[Dict[str, Any]], query: Dict[str, Any]):
    kind = query.get("kind")
    if kind == "surprise":
        pool = [e for e in entries if e.get("surprise")]
    elif kind == "event":
        pool = list(entries)
    else:
        pool = []
    idx = int(query.get("index", 0))
    return pool[idx] if 0 <= idx < len(pool) else None


def _summarise(entry: Dict[str, Any]) -> str:
    """Summary-grade rendering (reflex fidelity)."""
    if entry.get("surprise"):
        return (f"day {entry['day']} step {entry['step']}: surprise in "
                f"{entry['place']} — {entry['aspect']} "
                f"{entry.get('key') or ''} was not what I believed.")
    return (f"day {entry.get('day')} step {entry.get('step')}: "
            f"{entry.get('type')} in {entry.get('place', '?')}.")


def _essence_note(model: Any, day: int, kind: str, index: int):
    notes = [n for n in model.essence
             if n["day"] == day and n["kind"] == kind]
    if 0 <= index < len(notes):
        return notes[index]["line"]
    return None


def recall(model: Any, query: Dict[str, Any], route: str) -> Tuple[Any, int]:
    """Answer ``query`` from the tier ``route`` names.

    Returns ``(answer, cost_units)``. The cost is charged even when
    the tier cannot answer: looking costs what looking costs.
    """
    if route not in ROUTES:
        raise ValueError(f"unknown recall route: {route!r}")
    day = int(query.get("day", model.day))
    kind = query.get("kind")
    index = int(query.get("index", 0))

    if route == "reflex":
        _charge(model, COST_REFLEX)
        # Construction guarantee: this branch reads ONLY the live
        # episode. The archive and the essence are never touched.
        if kind == "place":
            return ("reflex: places live in the chart, not the hot cache.",
                    COST_REFLEX)
        if day != model.day:
            return (f"reflex: day {day} is not today; the hot cache "
                    f"holds only today's episode.", COST_REFLEX)
        entry = _find(model.episode, query)
        if entry is None:
            return ("reflex: nothing in today's episode matches.",
                    COST_REFLEX)
        return (_summarise(entry), COST_REFLEX)

    if route == "essence":
        _charge(model, COST_ESSENCE)
        # Construction guarantee: this branch reads the chart and the
        # distilled essence notes. The archive is never touched.
        if kind == "place":
            chart = model.chart
            pid = query["place"]
            place = chart.places.get(pid)
            if place is None:
                return (f"essence: {pid} is not on my chart.", COST_ESSENCE)
            fog = " (fogged)" if chart.is_fogged(pid, model.day) else ""
            return (f"essence: {pid}{fog} — contents "
                    f"{place.belief_contents!r}, exits "
                    f"{sorted(place.belief_exits)!r}, confidence "
                    f"{chart.effective_confidence(pid, model.day)}.",
                    COST_ESSENCE)
        if kind in ("surprise", "lesson"):
            line = _essence_note(model, day, kind, index)
            if line is not None:
                return (line, COST_ESSENCE)
        line = _essence_note(model, day, "summary", 0)
        if line is not None:
            return (line + " (essence carries the distilled line; "
                    "the full record is in the ledger.)", COST_ESSENCE)
        return (f"essence: nothing distilled about day {day}.", COST_ESSENCE)

    # route == "truth": the only branch that opens the archive.
    _charge(model, COST_TRUTH)
    record = model.archive.get(day)
    if record is None:
        return (f"truth: day {day} has not been slept into the ledger.",
                COST_TRUTH)
    entry = _find(record["entries"], query)
    if entry is None:
        return (f"truth: no matching entry in day {day}'s ledger.",
                COST_TRUTH)
    return (dict(entry), COST_TRUTH)
