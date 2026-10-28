# TRANSITIONS — the night phase learns what happens when I act

SuperInstance — liquid-world-model, Thor experiment 3 (maturity
round A). Code in `~/lwm-thor/` on the Thor (`transitions.py`,
`run_transitions.py`, `audit_policy.py`, `locked_world.py`,
`system2_r.py`, `run_retirement.py`); raw record:
`transitions-results.json`.

THOR-TEST's System 2 learned *places*. The V-JEPA probe proved
the representations also carry *transitions*: a frozen pair
embedding plus a fitted readout recovers what happened at 0.976,
and the probe's own verdict named the form the standing machinery
should take — per (place, action), an expected outcome class and
an expected after-prototype, with the pair readouts as the night
phase's instruments, doubt-priced (I-JEPA pairs nightly, V-JEPA
pairs only where the cheap readout is uncertain). This round
builds that machinery and runs it for six days. The follow-up's
wart — the duplicate observatory prototype S2 could not retire —
gets its retirement move in the same round, tested by re-running
the follow-up's forced-detour protocol against its published
receipts.

## PROCESS — written as the work happened

**2026-10-27 — design audit before any code (the two facts that
shaped everything).** (1) The frozen policies only ever attempt
*perceived doorways* (`ExplorerPolicy.decide` chooses among the
chart's known exits; a blocked exit stops being actionable under
unchanged conditions). So episodes harvested from free days are
almost all *move* — a transition table fitted on them would be a
diary that says "doors open." The probe got its class balance
from scripted walks that deliberately bump and wait; the day
loop needs the same honesty in the follow-up's own idiom: a
**written audit excursion** after the goal is reached (the
detour pattern — choreography, labelled, separately priced),
which at each place on a written return route attempts one
non-exit direction (a *same* episode), and at the gallery
attempts the locked cellar door (a *blocked* episode). (2) A
pre-registered expectation cannot run the probe's pair readout
*before* the act — the after-view does not exist yet. So the
standing form is the one the probe's verdict prescribed: the
table stores, per (perceived place, action), an **empirical
expectation** — majority outcome class and mean after-embedding
from the night's scorer-labelled episodes. The readouts move to
the night, where they belong: an I-JEPA-pair logistic readout is
fitted on the accumulated episodes each fit-night, each cell's
mean readout margin is computed, and cells under the stated
threshold are escalated to V-JEPA pair embeddings (the expensive
feature, ~7.5 s/episode) whose probe-trained readout verdict is
recorded as a second opinion. The table keeps the empirical
expectation regardless — scorer-labelled evidence outranks a
readout — but a cell the expensive readout contradicts is
flagged *contested* in the table, in the open.

**2026-10-27 — the lock cannot sit on the goal door.** The
probe's wrapper locked conservatory→east→vault. In the day loop
that door *is* the goal route (THOR-TEST day 2: atrium → library
→ conservatory → vault) — locking it makes the vault unreachable
and the six days meaningless. The lock therefore moves to the
one branch whose loss leaves both the goal route and the twin
wing intact: **gallery→south→cellar** ("The cellar door is
locked."), a thin subclass of the shipped world, present on all
six days, stated here rather than discovered later. Consequence,
also stated: this run's days are **not** THOR-TEST's days — the
cellar is never entered, day-1 exploration differs, and the
control for the transitions question is this run's own days 1–3
(transitions machinery logging, no table fitted), not the
published THOR-TEST metrics. THOR-TEST's floor is still asserted
where it legitimately applies: the retirement re-run (below)
uses the shipped world and asserts deep-equality against the
published baseline, as the follow-up did.

**2026-10-27 — the bump tax, found in the framework before it
could contaminate the counts.** `Chart.record_transition`
forms a belief entry for any attempted direction
(`belief_exits.setdefault(...)`), even a wall the agent merely
tried. At the place's next observation that phantom exit
"vanishes" and the chart charges exactly one surprise
("an exit I believed in is not here now", confidence −0.25).
So every audit bump costs one mechanical chart surprise at the
immediately following fold — framework bookkeeping, identical
on control and treatment days, *not* a world contradiction and
*not* a pre-registered surprise. Surprises in this report are
therefore always decomposed: route surprises, audit bump-tax
surprises, audit other surprises. The pre-registered channel
predicts the bumps correctly as *same* while the chart pays its
tax — prediction outrunning belief bookkeeping is itself one of
the round's findings, recorded with its receipts below.

**2026-10-27 — thresholds, stated before the run.** Readout
uncertainty: a cell escalates to V-JEPA when its mean I-JEPA
readout margin (top minus second predicted probability, on its
own episodes, in-sample — the instrument is doubt-pricing, not
validation) is **< 0.50**, capped at **24 episodes per night**,
lowest margin first. After-prototype check: an ON-day episode
whose after-view cosine to the cell's expected after-prototype
is **< 0.992** counts as a pre-registered surprise even if the
class matched — 0.992 sits between THOR-TEST's published
within-room floor (≥ 0.994) and the twin cross-similarity
(0.991), so the check is blind to jitter and sensitive to
arriving in the wrong twin. Class comparison uses the
*perceived* outcome (what the agent could know); the table's
accuracy is additionally scored against scorer truth on the
same episodes.

**2026-10-27 — workstream 2 ran first (it is the fast one), and
the retirement rule fired exactly where the wart said it
would.** The re-run stands on THOR-TEST's floor: days 1–3 and
both nights assert deep-equal to the published baseline modulo
the retirement fields alone. Night 1: no duplicate exists, the
rule is a no-op. Night 2: S2 seeds place-7 as it always did —
and the new step retires it the same night, into place-6, with
the testimony in the change record (duplicate label
'observatory'; zero clean assigned sightings; seed evidence 2
sightings; incumbent kept on the tie). Day 3 therefore carries
exactly one observatory prototype into the forced visit. Full
receipts in the workstream-2 section below.

## Workstream 2 — the wart, retired

**The rule** (`system2_r.py`, the original `system2.upgrade`
forked with one step added between seeding and the tau search;
the original file is untouched): after purification and
seeding, group prototypes by S2 label. In a group of ≥ 2, the
winner is the prototype with the most *clean assigned
sightings* (perceived as it, truly the label); ties break to
the incumbent, lowest id. Any other member with **zero** clean
assigned sightings — in force, never once perceived — is
retired into the winner: its id leaves the prototype set and
the labels; the winner's vector is kept as-is; the merge is
testified in the night change record. The rule's stated
boundary: a duplicate whose members have *both* been perceived
is a split, not this disease, and the rule does not touch it.
The follow-up's suggested alternative — prevention, counting
labelled-but-unvisited prototypes as covered so the duplicate
is never seeded — was deliberately not implemented: it would
leave the retirement move itself unproven, and it cannot clean
a duplicate that arises any other way.

**The re-run** (`run_retirement.py`): the follow-up's protocol
exactly — shipped world, seed 7, DetourScriptPolicy, day-3
forced visit, night 3 computed-not-applied — with System 2
swapped for the fork. Assertions against THOR-TEST's published
`results.json`, all **true**: day 1, day 2, day 3 phase A
deep-equal; night 1 and night 2 change records deep-equal
modulo the retirement fields alone (i.e. purification, seeding,
and tau are bit-for-bit the original's work; only the new step
differs).

**Before / after, against the follow-up's published receipts:**

| | follow-up (before) | this run (after) |
|---|---|---|
| observatory prototypes in force, day 3 | place-6 **and** place-7 | **place-6 only** |
| forced visit perceived as | place-7 (tie-break luck) | **place-6** |
| visit top sims | p7 0.99897 **=** p6 0.99897 · p2 0.99032 | p6 0.99897 · p2 0.99032 |
| visit margin | **0.0** | **0.00865** |
| visit trust | 0.3 | 0.3 (see below) |
| place-7 in the day-3 chart | yes (as the visited place) | **nowhere** |
| night-3 prototypes (computed) | place-1…place-7, observatory ×2 | place-1…place-6, observatory ×1 (place-6) |
| night-3 change | added {} · duplicate carried | added {} · retired {} — nothing to retire |
| detour price | +4 steps, +5 observations, 0 surprises | +4 steps, 0 surprises — unchanged |

The visit's winning similarity is the identical number,
0.99897 — the same jittered view (the day-3 render sequence is
the baseline's, draw for draw), now answered by one prototype
instead of a tied pair. The margin is no longer zero; it is
exactly the twin gap the corpus always said was there
(0.99897 − 0.99032).

**What did not change, honestly:** the visit still arrives at
trust **0.3**. The doubt threshold is a margin of 0.03, and the
honest twin gap is 0.00865 — with the duplicate gone, the
distrust that remains is twinship's own tax, the same one the
follow-up measured falling on *library* arrivals (margins
0.0078 / 0.0082, also distrusted). Retirement removed the
artificial doubt (an exact tie with a copy of itself); it did
not — and should not — remove the real doubt between two
different rooms that genuinely look alike. Under night 3's
computed prototypes the live sighting assigns to place-6 at
1.0 (in-sample, stated as the follow-up stated it: the
prototype is re-derived from that very sighting). Night 3 also
closes the wart's growth mechanism for good in this lineage:
with place-6 perceived, observatory is covered by a visited
place, and there is no second observatory prototype left to
carry.

**Verdict on the wart: retired.** The duplicate is gone before
it can tax a visit, the merge is testified in the night log
with its evidence counts, the day-3 chart holds exactly one
observatory place, and every baseline receipt the follow-up
stood on still asserts equal — the fix cost the original
experiment nothing it had measured.

## Workstream 1 — the transition table, six days

**What was built** (`transitions.py`, `run_transitions.py`).
Every step of every day logs an episode — (place, action,
view_before, view_after) with the embeddings the day's
perception already computed, the perceived outcome class, and
the scorer's true class kept in separate fields. On fit nights
(3, 4, 5) S2 builds the table: per (place, action), the
empirical expected class (majority of the cell's episodes),
the expected after-prototype (mean of after-embeddings), and
two instruments from the probe — an I-JEPA pair readout fitted
on all episodes so far (its per-cell margins price doubt), and
the probe's own V-JEPA readout refitted on the probe's corpus
as the escalation judge. Cells whose mean I-JEPA margin falls
below 0.50 escalate up to 24 of their episodes to V-JEPA pair
embeddings; a cell whose escalated episodes mostly disagree
with its empirical class is flagged **contested** in the night
record. On ON days (4–6), before each action the day's table
entry — if the cell exists — is registered; after the action it
is scored: class mismatch, or an after-view cosine to the
expected prototype below 0.992, is a **pre-registered
surprise**, counted in its own channel. The chart and policy
are untouched; the table predicts alongside them. As a
baseline, every episode of all six days is also scored against
what the *chart itself* implicitly predicts (believed passable
exit → move; believed impassable → blocked; no believed exit →
same).

**The six days** (locked-cellar world, seed 7; the audit
excursion ran in full every day — 13 written steps, never an
abort; the wart never formed here: nightly visits kept
observatory covered by a perceived place, night 2 seeded
nothing):

| day | mode | steps (route+audit) | surprises (route / bump tax / audit other) | recognition acc | episodes | chart-implicit acc |
|---|---|---|---|---|---|---|
| 1 | control | 9+13 | 16 (6 / 9 / 1) | 0.79 | 22 | 0.955 |
| 2 | control | 9+13 | 4 (1 / 3 / 0) | 1.00 | 22 | 1.000 |
| 3 | control | 3+13 | 3 (0 / 3 / 0) | 1.00 | 16 | 0.812 |
| 4 | **ON** | 3+13 | 3 (0 / 3 / 0) | 1.00 | 16 | 0.812 |
| 5 | **ON** | 3+13 | 3 (0 / 3 / 0) | 1.00 | 16 | 0.812 |
| 6 | **ON** | 3+13 | 3 (0 / 3 / 0) | 1.00 | 16 | 0.812 |

Day 1's sixteen surprises are the young chart's weather, now
with the audit's anatomy visible: six vanish-revisions at the
merged twin place on the route, nine more vanish-revisions in
the audit window (the twins still trusted on day 1, so every
re-arrival popped the other twin's exits), and one
exit-passable surprise — the locked cellar door announcing
itself at step 21. From day 2 the pattern freezes: the only
framework surprises left are the audit's bump tax, 3 a day.

**The table.** Night 3 fitted **19 cells** from 60 episodes
(12 expected *move*, 6 *same*, 1 *blocked* — the gallery's
south cell, the locked door, its count growing 3 → 4 → 5 over
the fit nights). No cell ever changed its expected class on
nights 4 or 5; the table converged on its first night and two
further nights of evidence only deepened its counts. Held-out
performance — each ON day scored against the table fitted the
night before, episodes the fit had never seen:

- **Coverage 48/48 episodes** (16/16 every ON day — the closed
  daily programme revisits the same cells; the table was never
  asked about a novel (place, action), and that limit is
  stated, not hidden).
- **Accuracy 1.000** — against the perceived outcome *and*
  against scorer truth, all three ON days.
- **Pre-registered surprises: 0.** The after-prototype check
  never came close to firing either: minimum after-view cosine
  across the 48 episodes was **0.9962** against the 0.992
  threshold (means 0.9991–0.9992). The twins never actually
  swapped under the agent — recognition held at 1.00 from day 2
  — so the prototype check verified arrivals but was never
  exercised as a discriminator. Stated as such.

**Where the table separates from the chart — the result of the
round.** The chart's own implicit predictions score **0.812**
on the same ON-day episodes, and the disagreement is perfectly
one-sided: **9 episodes where table and chart disagree, the
table right in all 9, the chart right in none.** The three
errors repeat identically every day from day 3 on:
(place-2, west), (place-6, north), (place-6, east) — the chart
believes these are passable exits; the agent bumps into the
wall daily; the chart never learns. The receipts name the
mechanism. Those are the twin places, and twin sightings arrive
**distrusted** (trust 0.3 < the framework's 0.5 floor — the
twins' honest margin), and a distrusted fold *does not rewrite
beliefs*: the day logs show 7 distrusted folds a day on the
stable days (10 on day 2), every one at place-2 or place-6. The phantom exits were written by the
bump records themselves; no trusted observation ever arrives
to pop them. So the chart is structurally blind exactly where
its senses are doubted — while the table, fitted on *outcomes*
(recorded regardless of trust), knows those three actions end
at the same view. A diary cannot out-predict the chart on the
chart's own ground; this one did, 9–0, on pre-registered
predictions. By the brief's own test, that is a physics of this
world, not a diary of it.

**The honest negatives, kept.** (1) *Total surprises did not
fall.* Control days 2–3 ran 4 and 3; ON days ran 3, 3, 3 — the
same bump tax, untouched. The table in this round is scored,
not consulted: nothing in the policy or the chart reads it, so
its knowledge prevents nothing yet. The pre-registered channel
exists and reads zero because the predictions were right, not
because the world got less surprising. Wiring the table into
the chart's belief revision — a trusted outcome record
outweighing a distrusted fold — is the obvious next step and
was out of this round's scope. (2) *The escalation tier never
fired.* The I-JEPA readout's in-sample accuracy was 1.000 on
every fit night and the *least* certain cell's mean margin was
0.985 — against the stated 0.50 threshold, no cell ever came
within sight of doubt: **0 escalations, 0 V-JEPA seconds, 0
contested cells**, all three nights. The probe's discipline is
implemented and priced, but in a seven-room deterministic world
the cheap readout finds every outcome legible in-sample and the
expensive tier is never bought. The instrument's known
softness, stated at design time and now confirmed: in-sample
margins measure legibility, and legibility saturates; a
held-out margin (fit on earlier days, priced on the newest)
is the sharper doubt instrument for a world that can actually
doubt. The probe-corpus refit of the V-JEPA readout scored
1.000 in-sample on its own corpus — a sanity receipt only; the
probe's published numbers were held-out, which is why they
were below 1. (3) *The world never changed.* Six days, one
static house: the table was never wrong, so its fallibility —
how fast a pre-registered surprise would surface a changed
lock, a moved wall — is unmeasured. The channel is built and
reads zero; what it reads on the day the world moves is the
next experiment, not this one's claim.

**Costs.** The whole six days: **26.5 s wall**, 119 rack
embedding calls at ~105 ms (the episodes reuse the day's
perception embeddings; the only new inference the design could
have bought was escalations, and there were none), peak RSS
123 MB. The probe spent ~37 minutes of rack time learning that
pair features carry transitions; the standing machinery that
result bought runs a full day-night cycle in about four
seconds. The run was executed twice end-to-end (see process);
both runs' day metrics are identical.

## PROCESS — the run, as it happened

**2026-10-27 — workstream 2 first (minutes), then the six
days.** The retirement re-run's receipts are above. The
transitions run then completed in a single pass: audit full
every day, table fitted nights 3–5, no aborts, no anomalies in
the harness. Two findings arrived that were not in the design
notes: the escalation tier's silence (analysed above — the
world is too legible in-sample for the doubt instrument to
spend anything), and the bump tax's stable value of 3, not the
6 the design arithmetic suggested.

**2026-10-27 — a receipts gap, found and closed by re-running.**
The first run's results file carried the surprise *counts* but
not the day-log entries behind them — counts without receipts,
exactly what this programme's referee discipline rejects. The
harness was amended to archive each day's full entry list and
the run repeated; the second run's day metrics are identical
to the first's on every compared field, and
`transitions-results.json` is the second run's file (the
first run's is kept on the Thor as
`transitions-results-run1.json`). The entries are what let the
bump tax be decomposed honestly: on stable days the three
taxed bumps are the conservatory's two and the gallery's east;
the twins' three bumps pay nothing — not because their walls
are believed in, but because distrusted folds never pop the
phantom beliefs the bumps create. That same freeze, found in
the entries, is the mechanism behind the chart's three
permanent implicit errors. One mechanism, three receipts: the
tax table, the distrusted-fold counts, and the 9–0
disagreement record.

**2026-10-27 — deviations from the design notes, all told.**
The lock's placement (gallery→cellar) and the own-control
definition were pre-registered deviations from THOR-TEST's
published control, stated before the run in the process log
above. In the run itself: the audit bumped six directions a
day, not five as the early design text said (the programme as
coded is the record: conservatory N+W, library W, observatory
N+E, gallery E). The day-2 route ran 9 steps, not 3 — the
frozen policy explored once more before its route settled —
and produced the run's only route surprise after day 1 (an
exit-to revision at the gallery). Nothing else deviated.

## Verdicts

- **The table: a physics, locally.** Held-out across days at
  **1.000** on 48/48 covered episodes, and 9–0 against the
  chart's own implicit predictions on pre-registered ground.
  Its limits are named: never tested on a novel cell, never
  tested against a changed world, and not yet consulted by
  anything that acts.
- **Pre-registered surprises: 0; total surprises: unmoved**
  (3/day on both sides of the switch — the residue is the
  audit's own bump tax, a measurement cost, not world
  surprise). The channel is built, priced, and honest; the
  reduction it exists to produce awaits the wiring that lets
  predictions revise beliefs.
- **The escalation tier: implemented, unexercised.** Doubt,
  priced by in-sample I-JEPA margins, never occurred in this
  world; V-JEPA spend for the round: **0 seconds**.
- **The wart: retired** (workstream 2) — one observatory place
  in force, the visit resolving to place-6 at 0.99897 with a
  real margin of 0.00865 where the tie gave 0.0, the merge
  testified in the night log, and every baseline receipt still
  asserting equal.
