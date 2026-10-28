# The Faltering Walk, Second Form — staleness with a floor, questions as intentions

*SuperInstance — experiment report, 2026-10-27. Round 2 of the
prototype from §9 of MEMORY-PATHS.md. Round 1
([FALTERING-WALK.md](https://github.com/patchwork-quilt/liquid-world-model/blob/main/FALTERING-WALK.md))
proved the question list (top question = the genuinely live issue,
6/6 seeds, both mornings) and failed as a truth-finder: its entire
surprise edge was a shrine it never re-entered, because a cold
route's activation is ~0 and activation × disagreement is ~0 no
matter how stale the belief rots. Round 1's verdict named its own
next experiment — a disagreement term that prices staleness
unconditionally, and questions routed to the policy as intentions,
not just to the feet as probes, in a regime where beliefs actually
rot. This is that experiment, built exactly as named.*

## Headline

**Leg 1 passes overwhelmingly; leg 2 fails; the falsifier
fires.** As intentions, the morning's questions abolish round 1's
dominant surprise entirely: B3 records **zero blocked door
attempts and zero door surprises in 24 arm-days** (every other
arm: one bump per run, 48–70 blocked attempts), 1 surprise total
against 8 apiece for B2 and C — 0.0017 surprises per recall unit
against 0.0138 and 0.0354 — in a third of the steps. But on final
chart truth B3 is again worst (contents 0.972 vs 0.987): the
staleness floor verifiably promotes the shrine into the bought
list, and the intention queue then starves it — Fix 2's success
shortened the day to a 7-step commute that ends at the goal
before cold questions are served, while dumber arms correct the
shrine by loitering. The second form finds a quieter world, not
a truer one. Both halves are receipted below.

## The two fixes

**Fix 1 — a staleness floor in the disagreement accounting.**
Round 1's score is `activation × disagreement`, and disagreement's
ignorance term is `1 − effective_confidence`. Effective confidence
already contains the fog rot: `eff = conf × 0.9^(fogged days)`. So
the ignorance term decomposes as `(1 − conf) + (conf − eff)` — what
the model never knew, plus *what it knew and has since lost to
time*. Round 1 multiplied both by route relevance. The second form
splits them:

```
score(p) = activation(p) × disagreement(p)  +  staleness(p)
staleness(p) = max(0, charted_confidence(p) − effective_confidence(p, day))
```

The floor is not a tuned knob: it introduces no constant. It is
the fog component of the model's own ignorance — the framework's
own numbers (`FOG_DECAY`, the charted confidence) — counted once
unconditionally instead of being multiplied by how fashionable the
route is. Defence, in one sentence: the walk may discount what it
never knew by relevance, but confidence it held and let evaporate
is a debt denominated in the same currency as ignorance, and debts
are not discounted by route. A place last seen on day 1 carries a
floor of ~0.06 on day 3, ~0.11 on day 4, ~0.16 on day 5 (at conf
0.6) whether or not the goal route passes anywhere near it — which
is precisely the shrine's situation, and precisely the round-1
failure mode (activation × staleness ≈ 0) removed.

**Fix 2 — questions as intentions.** In round 1 a bought question
became a foot-probe: a blocking pre-phase that walked the agent to
a place before the shipped policy got a turn. But round 1's
dominant surprise was a *policy* failure — beelining to the vault
door empty-handed — and no probe ordering fixes a route-level
behaviour. In the second form the morning's bought questions are
also handed to the day policy as **intentions**: named, expiring
policy modifiers that bias the policy's own choices all day.

- `verify:<place>` — from a bought conflict/fog/tie question. The
  policy treats the place as a subgoal woven into its own day:
  when no stronger intention is acting, it routes there over
  believed ways; arrival (the chart recording the place as seen
  today) fulfils it. This is round 1's probe-visit, demoted from a
  pre-phase to a standing bias — it interleaves with the policy's
  own search instead of pre-empting it.
- `ensure-item:<item>` — derived, not from the question's kind but
  from what the question's place is *gated by*. If a believed exit
  of a questioned place is item-gated — its belief names an
  `opens_with`, or the model's own attempt log testifies the
  passage was an unlocking performed while holding the item — and
  the item's home is on the chart (the place where the model's log
  says it acquired the item), the morning issues a readiness
  intention for that item. It fires only when it matters: when the
  believed goal route from the agent's current place crosses a
  gated edge for that item, or the agent stands at a gated exit —
  and then the policy fetches the item *before* the route proceeds.
  Nothing about this is treasury-shaped: any gated edge on any
  questioned place produces it, for whatever item the chart names.
- Uncharted questions stay foot-probes (round 1's machinery,
  reused): traversing an exit is an act, not a bias, and round 1
  already priced it.

Intentions expire: each is issued for one day, is dropped when
fulfilled, when its target proves unreachable on believed ways, or
when the day's directed-step budget (200, shared with probes —
round 1's cap) is spent. Every firing, fulfilment, and expiry is
logged; the log is a receipt in `results.json`. Routing under an
intention never routes *through* a gated edge whose item the agent
doesn't hold — a door you cannot open is not a way.

## Setting and falsifier — stated before running

The framework's own dungeon, unchanged, but the horizon is **5
days** instead of 3, so fog stops being a rounding term: a place
seen on day 1 is fogged from day 3 and its effective confidence is
×0.9, ×0.81, ×0.729 on days 3, 4, 5. Rounds of re-observation
become necessary; round 1's regime never forced them. Seeds
3, 7, 11, 19, 23, 42 (round 1's set, paired). Four arms:

- **A** — the shipped dumb policy, no morning allocation.
- **C** — round 1's strawman: nearest-uncharted morning allocation.
- **B2** — round 1's Faltering Walk, unchanged (v1 scoring,
  probes only). The ablation: B3 minus both fixes.
- **B3** — the second form: floor scoring + intentions.

Morning purse 24 units on days 2–5, prices as round 1 (conflict →
truth recall 12, else essence 4, strict rank order). All arms pay
the demo's evening reflex recall on surprise days, as round 1.
Chart truth graded scorer-side at the end of day 5.

**Falsifier for this regime.** B3 must beat **both** B2 and C on
both legs, or the second form is decoration too and that gets
published:

1. **Surprises per recall unit, days 2–5** (totals across seeds:
   surprises on days 2–5 ÷ recall units spent on days 2–5) —
   strictly lower for B3 than for B2 and for C.
2. **Final chart truth** — B3's contents accuracy (the shrine
   metric: the axis round 1 lost) strictly higher than B2's and
   C's, with coverage and exit metrics reported alongside.

Absolute surprises, steps, and per-arm spend are reported whatever
happens; a leg that ties fails. Known regime risk, recorded in
advance (round 1's lesson): this world has exactly two surprise
sources after day 1 — the gated door (once per run) and the
shrine's changed contents (once per run) — so both legs turn on a
small number of events per seed, and a 5-day horizon gives even
the strawman time to blunder into the shrine. The falsifier is
kept as stated anyway; if the world is too small to separate the
arms, that is the finding.

## Process — written as the work happened

- **Design read (before any code).** Round 1's three named
  successors map one-to-one onto this brief: staleness floor →
  Fix 1; intentions → Fix 2; the bigger/rotting world → the 5-day
  fogged horizon (the Thor visual world was the alternative named;
  the brief pins the framework's own world, so fog over 5 days is
  the rot available — recorded here so the substitution is a
  decision, not a drift).
- **Probe before building (chart forensics, seed 7, day 1).** Two
  facts the design had to survive, both verified against the
  shipped framework before writing a line: (1) after a clean day 1
  the treasury door's belief is `{passable: True, locked: None,
  opens_with: None}` — `opens_with` is only charted after a
  blocked attempt has marked the door locked and a later keyed
  traversal resolves it, so on day-2 morning *no belief on the
  chart says the door is gated at all*. An ensure-item derivation
  that read beliefs alone would fire first on day 3 — one day
  after the surprise it exists to prevent. (2) No place believes
  it contains the brass key (the library's first observation is
  already post-pickup; its believed contents are `[]`). The key's
  home survives only in the chart's attempt log: the traversed
  attempt `hall → west → library` carries the event *"You take the
  brass key."* Both derivations therefore read the model's own
  testimony — attempt events and holdings, which the framework
  records for every edge — never the engine: an exit is
  item-gated if its belief names an opener, **or** a recorded
  traversal of it was an unlocking performed while holding the
  item (the event names the item and the unlocking); an item's
  home is the destination of the recorded attempt whose event
  reports acquiring it. If either derivation comes up empty, the
  intention is issued unroutable and expires — recorded, not
  papered over.
- **Fix 1's form.** Chosen as above and deliberately *not* swept:
  the floor is the fog summand of the model's own ignorance term,
  moved outside the activation product. Alternatives considered
  and rejected in the log: `activation × (disagreement +
  staleness)` (still zeroed by activation — the failure mode
  itself); a constant floor ε (a tuned knob, and route-blind in
  the wrong way — it would pay equally for places the model never
  knew); `max(activation × disagreement, staleness)` (defensible,
  but discontinuous and it *replaces* route sense with rot sense
  instead of adding the debt to the bill).
- **The readiness hole, found on paper before running.** Tracing
  the belief mechanics forward: if Fix 2 works on day 2, the door
  is never contradicted, so its belief stays `passable: True`
  forever, and the treasury's own question score *decays* as the
  place freshens — a derivation that only scans bought questions
  can lapse on day 3+, and the surprise lands late instead of
  never. The derivation therefore has two sources, both stated
  here in advance: (a) any bought question whose place has a gated
  exit; (b) if the goal place's question is bought, every gated
  edge on the believed start→goal route — buying the goal buys
  its route's readiness. Source (b) is structurally self-
  sustaining in this world: the goal room's own exit is
  permanently uncharted (the day ends on arrival), so the goal
  question is re-bought every morning. Noted so the reader can
  check the receipts for exactly this: the vault question should
  appear in every B3 morning's bought list.
- **Smoke test (seed 7, before the full run).** The mechanism
  fired exactly as designed: day 2, the ensure-item intention
  derived from the treasury question (source (a)) plus the bought
  vault question (source (b)), 2 fetch steps, door traversed
  key-in-hand, **zero surprises on days 2–5**, and the day
  collapsed to 7 steps. Two things spotted in the smoke and
  carried into the audit list: verify:vault ends every day still
  "active" (arrival at the goal ends the day before the next
  fulfilment check — a logging artefact, behaviourally inert),
  and verify intentions for chapel/garden were dropped as
  unreachable *from the treasury* — true of the believed graph
  (the treasury's side exits were never traversed, so their
  destinations are unbelieved and no route exists), the same
  believed-way property that dropped round-1 probes.
- **Regression gate (before the run).** Framework suite on the
  patched copy: **TEST SUMMARY: 10/10 PASS.** Round-1 protocol
  re-run against the new code (arms A/B/C, days 1–3): all 18 runs
  reproduce round 1's results.json **exactly** — steps, surprises,
  and recall per day. The v1 arm in this study (B2) is round 1's
  walk by measurement, not by claim.
- **The full run** (6 seeds × 4 arms × 5 days) followed, then the
  mechanism audit below: every day-2–5 surprise traced, every
  door attempt counted from the chart's own edge log, the
  shrine's last-seen day tracked at every day-end, and every B3
  intention's fate read from its log.

## Results

| metric (6 runs/arm) | A dumb | C nearest-uncharted | B2 walk v1 | B3 second form |
|---|---|---|---|---|
| surprises days 2–5, total | 8 | 8 | 8 | **1** |
| recall units days 2–5, total | 8 | 226 | 580 | 577 |
| **leg 1: surprises / recall unit** | (n/a — spends ~nothing) | 0.0354 | 0.0138 | **0.0017** |
| total steps, mean | 167.2 | 160.8 | 162.2 | **53.7** |
| coverage (of 13 rooms) | 1.000 | 1.000 | 1.000 | 0.846 |
| exit-destination accuracy | 1.000 | 1.000 | 1.000 | 1.000 |
| exit recall | 1.000 | 1.000 | 1.000 | 1.000 |
| **leg 2: contents accuracy** | 0.987 | 0.987 | 0.987 | **0.972** |

B3's single surprise in 24 arm-days is the seed-42 shrine, day 5 —
paid by a verify intention that finally got served, and it
*corrected* the belief (that run ends contents-perfect). Every
other arm's eight surprises split into six door bumps and two
shrine corrections.

### Where every surprise actually came from (audited)

Days 2–5 surprise census, all runs. **Door** (`treasury /
exit-passable / north`): A 6, C 6, B2 6, **B3 0** — one per run
for every non-B3 arm, on day 2 except C's seeds 7/23/42, where
the strawman's probes merely postponed the bump to day 3. **Shrine**
(`contents`): A 2 (seeds 11, 42), C 2, B2 2 (seed 11 day 5,
seed 42 day 4 — the v1 walk's late growth did eventually buy
those), B3 1 (seed 42, day 5). Nothing else, anywhere.

The door attempts underneath, counted from the chart's own edge
log: across the six seeds, blocked attempts total **A 70, C 69,
B2 48, B3 0**. B3's door record is five clean keyed traversals
per run and nothing else. The intention receipts agree:
`ensure-item:brass key` was issued and **fulfilled on 24 of 24
B3 mornings**, at 2 directed fetch steps each — source (a) (the
treasury question) on most mornings, source (b) (the bought goal
question's route scan) whenever the treasury question itself
wasn't the carrier. The readiness hole predicted in the process
log did not open.

### The shrine, seed by seed (the leg-2 audit)

- **Seed 7:** charted day 1, re-entered by *nobody* — all four
  arms end believing "lit candles" (contents 0.9231 across the
  board). In B3's day-5 morning the shrine question scores
  0.1769, of which the staleness floor is 0.1626 (92%; its v1
  product is 0.0143, which ranked it near-last in round 1) —
  and it ranks **7th**, one slot below the 24-unit purse. The
  floor lifted it twelve-fold and the purse still cut it.
- **Seed 11:** B3 *buys* the shrine question on days 3, 4, and 5
  (verify:shrine issued — impossible under v1) — and never serves
  it: the intention sits active with 0 directed steps while the
  day runs fetch (2) + verify:treasury (4) + goal arrival, over
  by step 7. A pays the shrine surprise on day 3 by wandering;
  B2 pays it on day 5; C pays it on day 2. B3 ends wrong.
- **Seed 42:** verify:shrine issued day 5, *served* (3 directed
  steps — that morning's queue happened to reach it), surprise
  paid, belief corrected, contents 1.000. The one run where the
  full Fix-1 chain — floor → bought → intention → visit →
  correction — completes.
- **Seeds 3, 19, 23:** the shrine was never charted on day 1, so
  there is no rotting belief to be wrong about — and B3's commute
  never charts it later either (coverage 0.69–0.77 in those runs).
  Contents accuracy is vacuously 1.000 there; the coverage column
  is where that debt shows.

## Verdict

**Leg 1 passes, decisively. Leg 2 fails. The pre-registered
falsifier therefore fires: on the standard stated in advance, the
second form does not hold — and the receipts show it is not one
result but two, with opposite signs.**

**Fix 2 (intentions) is a complete success, mechanism-verified.**
Round 1's dominant surprise was a policy failure that "no morning
purchase available to any arm" could prevent. As an intention it
is simply gone: 0 blocked attempts and 0 door surprises in 24
arm-days, against 48–70 blocked attempts and a guaranteed bump
for every other arm — and the steps show it wasn't bought with
wandering (B3's mean day after day 1 is a 7-step commute; total
steps 53.7 against ~161–167). A question handed to the policy as
a standing readiness modifier changed route-level behaviour
exactly where a foot-probe couldn't. This half of the second
form should be kept and built on.

**Fix 1 (the staleness floor) works as a ranking and starves as
a servant.** The floor demonstrably does what it was derived to
do — the shrine's score goes from 0.0143 (v1) to 0.1769, 92% of
it floor; the shrine enters B3's bought list in seeds 11 and 42
where v1 never bought it in time. But bought is not visited.
Intentions are served in rank order inside a day that *ends at
the goal*, and Fix 2's own success shortened that day to the
length of the commute: in seed 11 the shrine intention waited
behind fetch + treasury for three straight mornings and the day
ended first, every time. Meanwhile the arms that still blunder
around for 20–90 steps a day end shrine-correct in 5 of 6 seeds
with no machinery at all — twice by paying the contents surprise,
three times by simply arriving first after the change. Round 1's
disease was avoidance by not looking; round 2's is avoidance by
finishing too fast to look. Contents accuracy: B3 0.972, worst
of the four — the same chair the first form sat in, reached by
the opposite road. And B3's coverage regression (0.846 vs 1.000)
is the same fact in another column: an agent whose intentions
make it a perfect commuter stops learning the map, and in a
bigger world that debt compounds.

**What the two rounds together actually prove.** The walk's
question list was never the problem (round 1), the floor fixes
the list's known blind spot (round 2, ranking-verified), and
intentions are the right currency for route-level failures
(round 2, mechanism-verified). What neither form has solved is
*service*: an agenda item that expires at sundown, in a day that
ends when the goal is reached, will systematically starve
exactly the slow, cold questions the floor exists to promote.
The honest third-form candidate is written down by the failure
itself: **verify intentions that survive sleep** — carried
unfulfilled into the next morning's list with their floor still
accruing — and a serving order for carried intentions ahead of
the day's goal run, so the commute cannot starve them. Until
that is built and run: keep the intentions, keep the floor as a
ranking, and do not claim the second form finds a truer world.
It finds a *quieter* one — 1 surprise in 24 arm-days, none of
them at the door — and quiet, this study has now twice had to
learn, is not the same as true.

## Process — closing entries

- **Composition check.** The patch below was verified the way
  round 1's was: applied to a pristine repo tree *on top of*
  `faltering-walk.patch`, the resulting `lwm/` is byte-identical
  to this study's framework copy, and the suite passes there
  (**TEST SUMMARY: 10/10 PASS**). The two diffs compose; neither
  touches the shipped `ExplorerPolicy`, `Chart`, or day cycle —
  S1 machinery byte-identical in both rounds, per the THOR-TEST
  attribution discipline.
- **Artefacts of the rig, recorded not hidden.** verify:vault
  ends every B3 day still "active" (the day ends on arrival,
  before the fulfilment check can run); several verify
  intentions were dropped as unreachable from the treasury, a
  believed-graph cul-de-sac the shipped policy escapes by taking
  untried exits directly — believed-way routing cannot. Both are
  in `results.json` as they happened.

## Files

- `faltering-walk-2.patch` — the round-2 framework change,
  diffed *against the round-1 patched tree* so it composes on
  top of `faltering-walk.patch`: the staleness floor and v2
  scoring, the gating/home derivations from the chart's attempt
  log, and the walk3 allocator in `lwm/tiers.py`;
  `IntentionPolicy` in `lwm/policy.py`. Shipped `ExplorerPolicy`,
  `Chart`, and the day cycle unmodified in both rounds.
- `experiment2.py` — the four-arm harness (paired seeds, 5 days,
  scorer-side chart-truth grading, round-1 regression checks).
- `results.json` — every run, every day, every question list
  with both scores and the floor itemised, every intention and
  its fate, door-attempt logs, shrine tracking, aggregates, the
  falsifier block, and the 18/18 regression record.
- `framework/` — the patched working copy the numbers came from
  (suite: TEST SUMMARY 10/10 PASS there).
