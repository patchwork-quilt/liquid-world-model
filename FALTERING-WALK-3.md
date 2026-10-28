# The Faltering Walk, Third Form — verify intentions that survive sleep

*SuperInstance — experiment report, 2026-10-27. Round 3 of the
prototype from §9 of MEMORY-PATHS.md. Round 1
([FALTERING-WALK.md](https://github.com/patchwork-quilt/liquid-world-model/blob/main/FALTERING-WALK.md))
proved the question list and failed as a truth-finder. Round 2
([FALTERING-WALK-2.md](https://github.com/patchwork-quilt/liquid-world-model/blob/main/FALTERING-WALK-2.md))
proved intentions (the locked door's surprise abolished: 0 blocked
attempts in 24 arm-days) and the staleness floor as a ranking — and
failed its truth leg anyway: bought is not visited. Its verdict
named this experiment in its own words: **verify intentions that
survive sleep** — carried unfulfilled into the next morning's list
with their floor still accruing — **and a serving order for carried
intentions ahead of the day's goal run**, so the commute cannot
starve them. This is that experiment, built exactly as named.*

## Headline

**The third form's final chart is true — and its headline
mechanism never fired.** B4 ends with contents accuracy
**1.000 in all six runs** (B3 0.972, C 0.987), coverage 0.974
against B3's 0.846, and the door still abolished (0 blocked
attempts, ensure-item fulfilled 24/24 mornings). It pays for
the truth exactly as the pre-registration feared: 3 shrine
surprises — one per seed where a rotten belief existed, each
paid on first re-entry and each correcting the chart — against
B3's 1, so **leg 1 fails against B3** (0.0054 vs 0.0017
surprises per recall unit) while beating the strawman sixfold.
And the carry ledger is *empty*: across 24 mornings, zero
verifies were carried, zero deferred, zero re-buys skipped —
with the serving order fixed (cold before goal-route, the
goal's own verify recognised as the goal run), starvation
never happens in this world, so there is nothing to persist.
The receipts convict round 2's diagnosis of one imprecision:
the agenda's disease was its **order**, not its expiry.
Persistence is built, swept nightly, and honestly reported
as untested by a world this small.

## The third form

Round 2's receipts, read forensically, show the starvation has a
precise mechanism — three facts, all in round 2's `results.json`:

1. **The day ends at the goal, and a goal-shaped intention sits
   ahead of the cold ones.** `verify:vault` is issued nearly every
   morning at rank 2. Serving it *is* the goal run: one step from
   the treasury into the vault, and `run_day` ends the day on the
   treasure before any later intention is consulted. In seed 11,
   `verify:shrine` (rank 6) sat behind fetch (2 steps) +
   verify:treasury (4) + verify:vault (1) — the day was over in 7
   steps, three mornings running.
2. **The treasury is a believed cul-de-sac.** Its south and west
   exits were never traversed *in that direction*, so their
   believed destinations are `None` and believed-way routing from
   the treasury can go only north, into the vault. A cold verify
   first attempted from the treasury is unreachable on believed
   ways — several round-2 intentions were dropped there, correctly
   by round 2's rules, permanently by round 2's expiry.
3. **Nothing carries.** An intention issued on day *d* and not
   served by sundown is gone on day *d+1* unless the morning's
   purse buys its question again at full price — and the purse
   buys in rank order, so the cold questions that starve are the
   same ones that must be re-bought to exist at all.

The third form changes exactly the three things those facts name:

- **Persistence.** At each wake, before the morning allocation,
  the policy sweeps yesterday's intentions: a verify whose place
  has been seen at or after its issue day is closed as fulfilled
  (the question was answered, whenever the visit happened); a
  verify still unfulfilled becomes **carried state** — a record on
  the policy that `sleep()` does not flush, the way the chart and
  the essence are not flushed. It is not re-derived: the record
  keeps its original issue day, its source question, and a count
  of nights carried, and the experiment logs the carry event and
  the place's staleness floor that morning, so the accrual is a
  receipt, not a claim. `ensure-item` intentions do **not** carry
  — readiness is re-derived every morning, exactly as round 2
  proved it (24/24 mornings); what works is not touched.
- **The purse does not buy twice.** The morning allocator (new
  mode `walk4`, scoring = round 2's v2, floor term unchanged)
  skips any non-uncharted question whose place already has a
  carried verify pending: that question was paid for when it was
  issued, and its intention is already on the day's list. The
  purse descends to questions it would otherwise have cut. This
  is persistence made consequential in the allocator, and it is
  the one place round 3's buying receipts may differ from
  round 2's — every skip is logged in `results.json`.
- **Priority.** The day's serving order is: (1) `ensure-item`,
  unchanged; (2) **carried verifies**, cold before goal-route;
  (3) **fresh verifies**, cold before goal-route; (4) probes for
  bought uncharted questions; (5) the shipped policy. Two
  definitions do the work. A verify is *goal-route* if its place
  lies on the believed start→goal path that morning (the treasury
  is; the vault is the goal itself). And a verify **for the goal
  place is never served as an intention at all** — serving it is
  indistinguishable from the goal run, so it is deferred to the
  shipped policy's own goal-seeking, which is where the goal run
  lives in every arm. Within a class, older before newer, then
  issue order. A verify that is unreachable *from here* is no
  longer dropped: it is **deferred** — still pending, retried as
  the day moves, and carried again at sundown if still unserved.
  Unreachable-from-the-treasury stops being a death sentence for
  a question that is reachable from the entrance.

The shipped `ExplorerPolicy`, `Chart`, and day cycle are
unmodified; the change is a new allocator mode in `lwm/tiers.py`
and one new policy class in `lwm/policy.py`, on top of rounds 1+2.

## Setting and falsifier — stated before running

Identical setting to round 2: the framework's own dungeon,
**5 days**, fog on, seeds **3, 7, 11, 19, 23, 42** (the paired set
of both previous rounds), morning purse **24 units** on days 2–5
at round 1's prices, evening reflex recall on surprise days for
all arms. Three arms:

- **C** — round 1's strawman: nearest-uncharted morning
  allocation, probes only. Must reproduce round 2's C.
- **B3** — round 2's second form, unchanged code path
  (`walk3` + `IntentionPolicy`). **Must reproduce round 2's B3
  numbers; any drift is a bug to find, not a result.**
- **B4** — the third form: `walk4` + `CarriedIntentionPolicy`.

Chart truth graded scorer-side at the end of day 5, as before.

**Falsifier for this regime.** All three clauses are stated in
advance; a clause that ties fails.

1. **Leg 1 (quiet):** B4's surprises per recall unit, days 2–5,
   strictly lower than B3's *and* C's (round-2 values: B3
   0.0017, C 0.0354 — subject to the B3 reproduction gate).
2. **Leg 2 (truth):** B4's mean final contents accuracy strictly
   higher than B3's *and* C's (round-2 values: B3 0.972,
   C 0.9872).
3. **Coverage & service clause** (new, because form 3's whole
   claim is that verification actually happens): B4's mean
   coverage strictly above B3's 0.846 **and** at least 0.95;
   **and** at least 80% of the non-goal verify intentions carried
   into a morning are fulfilled by the end of that day, counted
   from the intention receipts.

Absolute surprises, steps, and spend are reported whatever
happens. The known tension is recorded in advance, because both
previous rounds taught it from opposite sides: a surprise is
paid when a rotten belief is finally *met*, so an arm that
actually serves the shrine questions will pay shrine surprises
that round 2's arm avoided by blindness. Leg 1 and leg 2 may
therefore split. If they do, that is the result, published as
two results — as round 2's was.

## Process — written as the work happened

- **Design read (before any code).** The brief's three items map
  onto the three forensic facts above: persistence answers fact
  3 (and fact 2, via deferral replacing the drop), the accruing
  floor is round 2's term untouched, and priority answers fact
  1 — with the sharpening the receipts forced: "ahead of the
  goal run" must mean ahead of *every* goal-shaped service,
  including `verify:vault`, or the priority clause is empty.
  Treating the goal place's verify as the goal run itself (and
  therefore as the shipped policy's business, served last by
  construction) is a design decision taken here, on paper,
  before the run — not a tuning found after it.
- **Where carried state lives, and why that is honest.**
  `LiquidModel.sleep()` flushes the episode and nothing else:
  the chart persists, the essence persists, and the policy object
  persists (the model holds it across days; round 2's
  `IntentionPolicy` already kept an intention log across the
  whole run). Carried verifies live on the policy as agenda
  state, next to that log. No model code changes; the patch
  stays in `tiers.py` + `policy.py`, as in both prior rounds.
- **What was deliberately not changed.** The floor term
  (`_staleness_floor`, v2 scoring) is byte-identical. The
  ensure-item derivation, trigger, and service are round 2's,
  untouched — B4 calls the same `_derive_intentions` and serves
  readiness first, as before. The allocator's strict-order purse
  rule (stop at the first unaffordable question) is kept; the
  carried-skip *continues* past a carried question rather than
  breaking, because a skip is not an unaffordable buy.
- **Deferral vs drop, decided on paper.** Round 2 dropped a
  verify when believed-way routing failed from the current
  place. Under persistence that rule destroys exactly the state
  form 3 exists to keep (fact 2: the treasury cul-de-sac is a
  property of *where the agent stands*, not of the question).
  B4 therefore defers: pending, retried from each new place,
  carried at sundown. The one drop that remains is round 2's
  ensure-item drop (at home empty-handed / readiness
  unreachable) — readiness is not carried, so its expiry rules
  are round 2's own.
- **Smoke test (seeds 7, 11, before the full run) — and the bug
  it caught.** Seed 11 behaved exactly as designed (shrine
  served fresh on day 3 under cold-before-hot, surprise paid,
  belief corrected). Seed 7 day 5 **oscillated hall↔chapel for
  the entire 200-step directed budget**: the goal-route
  classification was being computed from the agent's *current*
  place at every decision, and it is position-dependent — from
  the hall the believed goal path runs through the gallery,
  from the chapel the shortest believed path runs through the
  crypt — so `verify:gallery` counted as cold exactly where
  `verify:study` was being served from, and vice versa, and
  each pre-empted the other across one edge, forever. A
  position-dependent priority is not a priority. **Fix, made
  before the full run and recorded here:** the classification
  is computed once per morning, from the wake place over
  believed geography, and held fixed all day — the morning's
  route is a property of the morning's chart, like the
  question list's rank order was in both prior rounds. After
  the fix seed 7's day 5 is a 12-step day. The falsifier above
  was stated before the smoke and is unchanged by the fix.
- **Regression gate (before the run).** Framework suite on the
  patched copy: see the closing process entries — and arms C /
  B3 in the harness must reproduce round 2's `results.json`
  exactly (all 5 days, every run, chart truth included). The
  harness checks this itself and records it in `results.json`
  (`regression_vs_round2`); a B3 drift would void the
  comparison, not become part of it.

## Results

**Regression gate: 12/12.** Arms C and B3 reproduce round 2's
`results.json` exactly — every run, all five days (steps,
surprises, recall), final chart truth included. The B3 column
below is round 2's second form by measurement, and the
comparison is clean.

| metric (6 runs/arm) | C nearest-uncharted | B3 second form | B4 third form |
|---|---|---|---|
| surprises days 2–5, total | 8 | 1 | 3 |
| recall units days 2–5, total | 226 | 577 | 551 |
| **leg 1: surprises / recall unit** | 0.0354 | **0.0017** | 0.0054 |
| total steps, mean | 160.8 | 53.7 | 80.3 |
| coverage (of 13 rooms) | 1.000 | 0.846 | **0.974** |
| exit-destination accuracy | 1.000 | 1.000 | 1.000 |
| exit recall | 1.000 | 1.000 | 1.000 |
| **leg 2: contents accuracy** | 0.987 | 0.972 | **1.000** |

### Where every surprise actually came from (audited)

Days 2–5 surprise census, all runs. **Door: zero, in both
intention arms** — B4's blocked door attempts counted from the
chart's own edge log are 0 in all six seeds (C: 69), and
`ensure-item:brass key` was issued and fulfilled on **24 of 24
B4 mornings**, round 2's proven half carried through untouched.
**Shrine (`contents`): B4 pays exactly 3** — seeds 7, 11, and
42, each on **day 3**, each on the first re-entry after day 1,
each *correcting* the belief (all three runs end believing
"cold ashes"). B3 paid 1 (seed 42, day 5 — the one shrine
service it ever managed); C paid 2 shrine plus its 6 door bumps.
Nothing else, anywhere. B4's three surprises are not failures
of the agenda; they are the sound of the agenda being served —
the rotten belief met, paid for, and fixed, in every seed where
a rotten belief existed.

### The shrine, seed by seed (the leg-2 audit)

- **Seeds 7, 11, 42** (shrine charted day 1, contents rotten
  from day 2): `verify:shrine` is bought and **served the same
  morning** — day 3 in all three — under cold-before-goal-route
  priority. Surprise paid, belief corrected, contents 1.000.
  Round 2's seed-11 three-morning starvation does not recur;
  neither does seed 7's purse-cut near-miss (the shrine question
  is bought on day 3, when its floor is still small, because
  the serving order no longer needs it to out-rank the route).
- **Seeds 3, 19** (shrine never charted on day 1): the shrine
  is first charted on **day 4**, already holding cold ashes —
  a first sight, no surprise, the belief correct from birth.
  The step arithmetic (seed 3 day 4: 26 steps, 15 intention,
  0 probe; seed 19 day 4: 18, 11, 0) leaves only the shipped
  policy's own edge-probing to have done it, during agenda
  gaps at the chapel — the loitering dividend round 2 priced
  as pure waste, here doing quiet work because the agenda no
  longer ends the day at the vault before the gaps can open.
- **Seed 23:** the shrine is **never charted** — B4's one
  coverage debt (0.846; every other run is 1.000). The reason
  is structural and unchanged since round 2: the chapel's
  north exit is a non-archway whose destination was never
  seen, so the shrine is not even a believed-adjacent node on
  the chart — *no walk question can name it*, and in this seed
  the agenda always had a believed onward route from the
  chapel, so the shipped policy's edge-probing never fired
  there either. The walk family still cannot ask about a
  place that does not exist in its model of the world.

### The carry ledger — empty, and that is a result

The third form's headline mechanism was exercised every
morning and **never once fired**. Across 24 B4 mornings:
carried verifies **0**, allocator carried-skips **0**,
deferrals **0**. Every non-goal verify issued was fulfilled
the day it was issued (100 fulfilled day-issues); the only
intentions ever open at sundown were the 24 `verify:vault`
records — the goal run's own shadow — and the night sweep
closed 18 of them as *fulfilled-overnight* (the vault had
been reached that day; the remaining 6 are day 5's, open at
the horizon). Fix the serving order — cold before goal-route,
the goal's verify deferred to the shipped policy — and in
this world **starvation never happens, so there is nothing
to carry**. Persistence is implemented, swept daily, and
*untested by this world*: no receipt in this study
distinguishes a carried verify from a re-derived one, because
no verify ever needed carrying. That is stated plainly
because the alternative — claiming the carry works because
the code ran — is exactly the claim these rounds exist to
refuse. What the receipts *do* show is which half of form 3
carried the weight: **priority, not persistence**. Round 2's
failure was diagnosed as an agenda that expires; in the
event, it was an agenda that was *ordered* wrong — the cold
questions starved behind the goal run, not behind the night.

## Verdict

**Leg 1 fails against B3 and passes against C. Leg 2 passes
outright. Clause 3 passes on coverage and is vacuous on
service. The pre-registered falsifier therefore fires — and,
as in round 2, the receipts show it is not one result but
several, with different signs.**

- **Leg 1 (quiet): FALSIFIED vs B3** (0.0054 vs 0.0017), as
  the pre-registration itself predicted it might be. B3's
  number is the price of blindness — one shrine surprise,
  paid late, in the one seed its queue happened to reach —
  and B4 pays 3 because it looks in all three. Against the
  strawman B4 is six times quieter per unit (0.0054 vs
  0.0354) with none of the strawman's door bumps. The metric
  still rewards keeping your eyes shut; B4 declines to.
- **Leg 2 (truth): PASSES, completely.** Contents accuracy
  **1.000 in all six runs** — the first arm in three rounds to
  end with a chart that is simply true on every axis the
  scorer grades (contents 1.000, coverage 0.974, exits
  saturated). The second form's "quieter, not truer" is
  answered: the third form is truer, and the price was 2
  extra surprises and ~27 extra steps a run against the
  commute (80.3 mean vs 53.7 — still half the strawman's
  160.8).
- **Clause 3: coverage PASSES** (0.974 ≥ 0.95, above B3's
  0.846; the one debt is seed 23's unnameable shrine).
  **Service is VACUOUS, and the clause fails as stated:**
  the ≥80% rate has a denominator of zero, because nothing
  was ever carried. A clause whose precondition the fix
  abolished cannot be claimed as met.

**What the three rounds together prove.** Round 1: the walk
asks the right questions. Round 2: questions handed to the
policy as intentions change route-level behaviour (the door),
and a staleness floor fixes the list's blind spot as a
ranking. Round 3: **service is an ordering problem before it
is a memory problem** — serve the cold questions ahead of the
goal run, let the goal's own question be the goal run, and
the agenda completes every morning in a world this size;
persistence across sleep, the mechanism round 2's verdict
reached for, turns out to be the spare part, not the missing
one. It remains on the policy, swept nightly, ready for a
world big enough that a day cannot hold its agenda — in
such a world the carry stops being vacuous, and the honest
next experiment is that world, not another clause in this
one. Until then: keep the intentions, keep the floor, keep
the serving order — and the claim for the third form is the
narrow, receipted one: **in this dungeon, it is the first
form whose final chart is true.**

## Process — closing entries

- **Composition check.** Verified, not asserted: a pristine
  repo tree + `faltering-walk.patch` + `faltering-walk-2.patch`
  reproduces round 2's framework `lwm/` byte-for-byte; adding
  `faltering-walk-3.patch` yields an `lwm/` byte-identical to
  this study's framework copy, and the suite passes on the
  composed tree (**TEST SUMMARY: 10/10 PASS**, and 10/10 on
  the study copy itself). The three diffs compose; none of
  them touches the shipped `ExplorerPolicy`, `Chart`, or day
  cycle.
- **Artefacts of the rig, recorded not hidden.** Six
  `verify:vault` records stand open at the horizon (day 5's,
  one per seed): the day ends on the treasure before the
  fulfilment check can run, and there is no day 6 wake to
  close them — the same logging artefact round 2 recorded,
  unchanged. The allocator's carried-skip and the policy's
  deferral path are exercised by no receipt in this run (see
  the carry ledger above); both are code that ran only their
  guard conditions, and the report says so rather than
  letting their presence imply their use.

## Files

- `faltering-walk-3.patch` — the round-3 framework change,
  diffed *against the round-2 patched tree* so it composes on
  top of `faltering-walk.patch` + `faltering-walk-2.patch`:
  the `walk4` allocator mode (carried-skip) in `lwm/tiers.py`;
  `CarriedIntentionPolicy` in `lwm/policy.py`. Shipped
  `ExplorerPolicy`, `Chart`, and the day cycle unmodified in
  all three rounds.
- `experiment3.py` — the three-arm harness (paired seeds,
  5 days, scorer-side chart-truth grading, the C/B3
  reproduction gate against round 2's results).
- `results.json` — every run, every day, every question list
  with carried-in and carried-skipped receipts, every
  intention and its fate, door-attempt logs, shrine tracking,
  aggregates, the falsifier block, and the 12/12 regression
  record.
- `framework/` — the patched working copy the numbers came
  from (suite: TEST SUMMARY 10/10 PASS there).
