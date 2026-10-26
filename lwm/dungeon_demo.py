"""The demo: three days in an uncharted dungeon.

    python3 -m lwm.dungeon_demo --days 3 --seed 7

Each day the world resets (entrance, key restored, treasure restored)
and the model wakes with only its chart and its essence. The per-day
printout is the curve: steps to goal, rooms charted, uncharted exits
remaining, surprises, recall spent. The maps written to ``demo-out/``
are drawn from the MODEL's chart — its beliefs, right or wrong,
fog and all — never from engine truth. The scorer's one use of
``truth()`` is to confirm, from outside, where the agent ended up.

After the days, the demo exercises routed recall on a day-1 event:
the same question asked of the essence (distilled, cheap) and of the
ledger (the full testified record, expensive), answers and costs
printed side by side.
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
from xml.sax.saxutils import escape

from .dungeon import DELTAS, DungeonWorld
from .engine import scorer_truth
from .model import LiquidModel
from .tiers import recall


def _chart_positions(chart) -> Dict[str, Tuple[int, int]]:
    """Lay the chart out from its own edges: start at the first
    charted room, walk believed/traversed exits by their directions.
    Pure chart data — the renderer never consults the engine."""
    graph = chart.traversed_graph()
    starts = [pid for pid, p in chart.places.items() if p.observed]
    if not starts:
        return {}
    start = "entrance" if "entrance" in chart.places else sorted(starts)[0]
    pos: Dict[str, Tuple[int, int]] = {start: (0, 0)}
    queue = [start]
    while queue:
        node = queue.pop(0)
        x, y = pos[node]
        neighbours: Dict[str, str] = dict(graph.get(node, {}))
        for direction, belief in chart.known_exits(node).items():
            if belief.get("to"):
                neighbours.setdefault(direction, belief["to"])
        for direction, nxt in neighbours.items():
            if nxt not in pos and direction in DELTAS:
                dx, dy = DELTAS[direction]
                pos[nxt] = (x + dx, y + dy)
                queue.append(nxt)
    # Anything the chart knows but cannot place goes in a side column.
    rest = sorted(pid for pid in chart.places if pid not in pos)
    if rest:
        maxx = max((x for x, _ in pos.values()), default=0)
        for i, pid in enumerate(rest):
            pos[pid] = (maxx + 2, i - len(rest) // 2)
    return pos


def render_chart_svg(chart, day: int) -> str:
    """The Zelda map, drawn by the model: solid for charted rooms,
    faded and marked for fogged ones, outlined for rooms only
    believed in, dashed stubs for exits never taken."""
    pos = _chart_positions(chart)
    if not pos:
        return "<svg xmlns='http://www.w3.org/2000/svg'></svg>"
    SX, SY, W, H, M = 170, 118, 132, 62, 46
    xs = [x for x, _ in pos.values()]
    ys = [y for _, y in pos.values()]
    width = (max(xs) - min(xs) + 1) * SX + 2 * M
    height = (max(ys) - min(ys) + 1) * SY + 2 * M + 26

    def cx(pid: str) -> float:
        return M + (pos[pid][0] - min(xs)) * SX + W / 2

    def cy(pid: str) -> float:
        return M + (pos[pid][1] - min(ys)) * SY + H / 2

    out: List[str] = []
    out.append(f"<svg xmlns='http://www.w3.org/2000/svg' "
               f"viewBox='0 0 {width} {height}' width='{width}' "
               f"height='{height}' font-family='monospace'>")
    out.append(f"<text x='{M}' y='26' font-size='17' font-weight='bold'>"
               f"Day {day} — the chart as the model believes it</text>")
    graph = chart.traversed_graph()
    # traversed ways, solid
    for a, dirs in graph.items():
        for _d, b in dirs.items():
            if a in pos and b in pos:
                out.append(f"<line x1='{cx(a):.0f}' y1='{cy(a):.0f}' "
                           f"x2='{cx(b):.0f}' y2='{cy(b):.0f}' "
                           f"stroke='#666' stroke-width='2'/>")
    # uncharted exits, dashed stubs
    for u in chart.uncharted():
        pid, direction = u["place"], u["direction"]
        if pid in pos and direction in DELTAS:
            dx, dy = DELTAS[direction]
            x2 = cx(pid) + dx * (W / 2 + 16)
            y2 = cy(pid) + dy * (H / 2 + 16)
            out.append(f"<line x1='{cx(pid):.0f}' y1='{cy(pid):.0f}' "
                       f"x2='{x2:.0f}' y2='{y2:.0f}' stroke='#999' "
                       f"stroke-width='2' stroke-dasharray='4 4'/>")
            out.append(f"<text x='{x2:.0f}' y='{y2:.0f}' font-size='13' "
                       f"fill='#999' text-anchor='middle'>?</text>")
    for pid in sorted(pos):
        place = chart.places[pid]
        x, y = cx(pid) - W / 2, cy(pid) - H / 2
        fogged = chart.is_fogged(pid, day)
        if not place.observed:
            fill, stroke, dash, opacity = "#ffffff", "#888", " stroke-dasharray='6 4'", "1"
            tag = "believed, unvisited"
        elif fogged:
            fill, stroke, dash, opacity = "#d8d8d8", "#777", "", "0.55"
            tag = "fogged"
        else:
            fill, stroke, dash, opacity = "#fdf6d8", "#444", "", "1"
            tag = ""
        out.append(f"<g opacity='{opacity}'>")
        out.append(f"<rect x='{x:.0f}' y='{y:.0f}' width='{W}' height='{H}' "
                   f"rx='8' fill='{fill}' stroke='{stroke}' "
                   f"stroke-width='2'{dash}/>")
        star = " ★" if "treasure" in place.belief_contents else ""
        out.append(f"<text x='{cx(pid):.0f}' y='{y + 22:.0f}' font-size='14' "
                   f"font-weight='bold' text-anchor='middle'>"
                   f"{escape(pid)}{star}</text>")
        contents = ", ".join(place.belief_contents) or "—"
        if len(contents) > 21:
            contents = contents[:20] + "…"
        out.append(f"<text x='{cx(pid):.0f}' y='{y + 40:.0f}' font-size='10' "
                   f"fill='#555' text-anchor='middle'>{escape(contents)}</text>")
        if tag:
            out.append(f"<text x='{cx(pid):.0f}' y='{y + 55:.0f}' "
                       f"font-size='10' font-style='italic' fill='#777' "
                       f"text-anchor='middle'>{tag}</text>")
        out.append("</g>")
    out.append("</svg>")
    return "\n".join(out)


def run_demo(days: int = 3, seed: int = 7,
             out: Optional[Path] = None, verbose: bool = True) -> Dict[str, Any]:
    world = DungeonWorld()
    model = LiquidModel(world, seed=seed)
    out = Path(out) if out else Path("demo-out")
    out.mkdir(parents=True, exist_ok=True)
    curve: List[Dict[str, Any]] = []

    def say(msg: str) -> None:
        if verbose:
            print(msg)

    for day in range(1, days + 1):
        world.reset(day)  # the world flushes its presence; the chart stays
        model.wake(f"Day {day}: find the treasure in the vault.")
        stats = model.run_day()
        # Evening reflection, while the episode is still hot: reflex tier.
        if model.day_surprises:
            ans, _cost = recall(model, {"kind": "surprise", "day": day,
                                        "index": 0}, "reflex")
            say(f"  evening recall (reflex): {ans}")
        stats["recall_spent"] = model.recall_spent_today
        model.last_stats["recall_spent"] = stats["recall_spent"]
        truth = scorer_truth(world)  # scoring only: where did it end up?
        say(f"Day {day}: steps {stats['steps']} · rooms charted "
            f"{stats['rooms_charted']} (cumulative) · uncharted exits "
            f"{stats['uncharted_exits']} · surprises {stats['surprises']} · "
            f"recall_spent {stats['recall_spent']} · goal "
            f"{'REACHED' if stats['goal_reached'] else 'not reached'} "
            f"(scorer: agent ended in {truth['room']})")
        testimony = model.dream()
        for line in testimony["lines"][1:]:
            say(f"  {line}")
        svg = render_chart_svg(model.chart, day)
        (out / f"chart-day{day}.svg").write_text(svg)
        model.sleep()
        curve.append({k: stats[k] for k in
                      ("day", "steps", "rooms_charted", "uncharted_exits",
                       "surprises", "recall_spent", "goal_reached")})

    # Routed recall, after the days: one day-1 event, two routes.
    archived = model.archive.get(1, {}).get("entries", [])
    has_surprise = any(e.get("surprise") for e in archived)
    query = ({"kind": "surprise", "day": 1, "index": 0} if has_surprise
             else {"kind": "event", "day": 1, "index": 1})
    say("")
    say(f"Recall after the days — query: {query}")
    ans_e, cost_e = recall(model, query, "essence")
    say(f"  essence ({cost_e} units): {ans_e}")
    ans_t, cost_t = recall(model, query, "truth")
    say(f"  truth   ({cost_t} units): {json.dumps(ans_t, default=str)}")

    result = {"seed": seed, "days": curve}
    (out / "curve.json").write_text(json.dumps(result, indent=2))
    return result


def main() -> None:
    ap = argparse.ArgumentParser(prog="lwm.dungeon_demo")
    ap.add_argument("--days", type=int, default=3)
    ap.add_argument("--seed", type=int, default=7)
    ap.add_argument("--out", type=str, default="demo-out")
    args = ap.parse_args()
    run_demo(days=args.days, seed=args.seed, out=Path(args.out))


if __name__ == "__main__":
    main()
