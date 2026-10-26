# liquid-world-model (`lwm`) — SuperInstance

**A game-engine-agnostic framework for liquid world models: an agent
that charts a world it has not finished learning — like a hero in a
dungeon it hasn't found the map for, learning room by room — doubts
its senses and its own beliefs, testifies each night before it
forgets, and remembers through priced tiers.** For builders of
agents that must act in worlds they only partially perceive: the
world model is not the engine (the engine is fixed and never in
doubt); the internal model is a different kind of thing — dynamic,
willing to be wrong, and actively probing for where it breaks.

Python 3, standard library only, no dependencies.

## Run it (all commands executed, not illustrative)

```bash
python3 -m lwm.dungeon_demo --days 3 --seed 7
```

Real output from that run (seed 7, the reference dungeon):

```
Day 1: steps 21 · rooms charted 13 (cumulative) · uncharted exits 9 · surprises 0 · recall_spent 0 · goal REACHED
Day 2: steps 27 · rooms charted 13 (cumulative) · uncharted exits 1 · surprises 1 · recall_spent 1 · goal REACHED
Day 3: steps 33 · rooms charted 13 (cumulative) · uncharted exits 1 · surprises 0 · recall_spent 0 · goal REACHED
```

and, asked afterwards about a day-1 event by two different routes:

```
essence (4 units):  Day 1: charted 13 places (13 new), 0 surprise(s), goal reached in 21 steps. (essence carries the distilled line; the full record is in the ledger.)
truth   (12 units): {"type": "distrusted", "day": 1, "step": 5, "place": "cellar", "trust": 0.3, "reason": "senses flagged unreliable; belief not rewritten"}
```

(Day 1 produced no surprise — the agent found the brass key before it
ever tried the locked door — so the recall comparison runs on the
day's first testified event. Day 2's surprise, when the door was
tried empty-handed, is in `demo-out/`'s testimony and chart.)

The demo writes `demo-out/chart-day{1,2,3}.svg` — the map drawing
itself from the *model's chart*, beliefs and fog included — and
`demo-out/curve.json`. Tests: `python3 tests/run_tests.py`
(TEST SUMMARY: 10/10 PASS).

**What the curve honestly shows** (seed 7): coverage and knowledge
improved — uncharted exits 9 → 1, and the locked door was a surprise
exactly once (day 2), never again. Steps did **not** fall
(21 → 27 → 33): day 1's speed was luck, not knowledge — a lucky
route past the key — and on later days the deliberately dumb policy
pays for beelining to a door it cannot open, then fetching the key.
The chart learned; the policy didn't. That separation is the point
of the framework, and the numbers are left as they fell.

## The model

### The contract (`lwm/engine.py`)

Any engine or simulator implements three methods: `observe()`
(partial observation — what the senses deliver *now*, never full
state), `actions()`, `step(action)`. An engine may expose
`truth()` for **scoring only**; the agent never receives it —
`agent_view()` wraps the world so agent-side code gets exactly the
three protocol methods and nothing else. Enforcement is structural,
not conventional.

### The chart (`lwm/model.py`)

Places keyed by perceived identity, each holding a current belief
(exits, contents), observation counts, and an **append-only belief
history**: every change is a revision entry keeping both versions,
so a belief is never overwritten silently. **Doubt runs both
directions** — the world contradicting the model is recorded as a
*surprise*; the model doubting its senses (an observation flagged
low-trust) lowers confidence instead of rewriting a held belief,
though a dim first look may still sketch a place never charted. A
locked door, once opened, is charted as *locked, and opens to the
brass key* — conditionality is a charted fact, not a mood. The
**uncharted set** — exits seen but never taken, places
believed-adjacent but never entered — is enumerable output, not an
absence: the model can list what it knows it hasn't charted.

### Fog of war

Charted is not current. Each place carries `last_seen_day`; unseen
for more than `FOG_FRESH_DAYS = 1` day it is **fogged**: the belief
stands, but effective confidence decays by a factor of
`FOG_DECAY = 0.9` per fogged day
(`effective = charted × 0.9 ** fogged_days`). Re-observing a place
restores it to current and its confidence to the charted value.
The day maps draw fogged rooms faded and marked.

### The day cycle

`wake(alignment)` begins a day — the episode (the day's presence)
starts fresh; chart and essence persist. The act loop perceives,
folds observations into the chart, and records what each step
actually did. `dream()` makes the day testify: surprises listed,
revisions with reasons, lessons in plain lines, essence distilled.
`sleep()` archives the episode into the ledger and flushes it. The
world side resets too (the harness's job): entrance again, key
restored — presence flushed by both, essence kept by the model.

### Memory tiers and routed recall (`lwm/tiers.py`)

Retrieval is spent from the same purse as action. `recall(model,
query, route)` returns `(answer, cost_units)`:

| route | tier | cost | serves | fidelity |
|---|---|---|---|---|
| `reflex` | today's live episode | **1** | today only; never opens the archive (by construction) | summary |
| `essence` | chart + distilled notes | **4** | the current believed answer; may be fogged | distilled line |
| `truth` | the slept days' episode logs | **12** | the full testified record of an event | exact |

Only `truth` opens the archive. Essence answers what the model
*believes now*; truth answers what *actually happened* — and the
price difference is the point.

### The policy (`lwm/policy.py`)

Deliberately dumb, and labelled so: prefer an actionable uncharted
exit (edge-probing — the model hunts its own ignorance), else the
shortest charted path to the goal-belief, else walk toward the
nearest uncharted edge. Seeded and deterministic. Improvement in
the demo is therefore attributable to the chart, not the explorer.

## Honest limits

- **The liquid model here is chart + cycle machinery.** JEPA-class
  perception and learned nightly adapters are *named provider
  slots*: the seams are the observation's trust flag (where a
  perception provider would grade the senses) and the dream's
  distillation (where an adapter would be trained). Nothing in
  this slice learns weights. **One slot now has a receipt:**
  [THOR-TEST.md](THOR-TEST.md) ran the trust seam against a real
  I-JEPA on the Thor — the chart keyed places by embedding
  similarity, confused two near-twin rooms, and a night upgrade
  (prototypes re-derived from the day's labelled replay)
  measurably repaired recognition while the player script never
  changed. Numbers, caveats, and warts are in the report;
  `results.json` is its raw record.
- The policy is intentionally minimal — it reacts to a locked door
  after meeting it rather than planning for the key (see the curve:
  that cost is visible, and it is the policy's, not the chart's).
- One toy environment (a 13-room dungeon) and one goal type
  (contents named `treasure`). The contract is the product; the
  dungeon is its proof, not its scope.
- Perceived identity is taken as given by the observation; two
  places that perceive identically would be merged by the chart —
  aliasing is a known open edge, not handled here.

## Layout

- `lwm/engine.py` — the World contract and the truth-hiding view
- `lwm/model.py` — Place, Chart (belief, doubt, uncharted, fog), LiquidModel (day cycle)
- `lwm/tiers.py` — memory tiers, routed recall, the purse
- `lwm/policy.py` — the deliberately dumb explorer
- `lwm/dungeon.py` — the reference environment
- `lwm/dungeon_demo.py` — the demo + the chart-map renderer
- `tests/` — invariants for all of the above (`run_tests.py`)
- `docs/` — the project page, with the seed-7 day maps
