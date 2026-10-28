# TRANSITIONS, CONSULTED — the day side believes the night's table

SuperInstance — liquid-world-model, Thor experiment 4 (build
round, lane 1). Code in `~/lwm-thor/` on the Thor
(`consulted.py`, `run_consulted.py` — new files; every original
untouched). Raw record: `transitions-consulted-results.json`
(both arms' full per-day receipts).

TRANSITIONS left the table in an odd seat: a proven physics
that nothing consulted. Fitted nightly on the day's episodes,
it predicted held-out outcomes at **1.000 (48/48)** and beat
the chart's own implicit predictions **9–0** on the chart's own
ground — and total surprises sat unmoved at 3/day in both arms,
because the table was *scored, not consulted*: nothing in the
policy or the chart ever read it. The report named the obvious
next step itself — "wiring the table into the chart's belief
revision — a trusted outcome record outweighing a distrusted
fold." This round does exactly that wiring, and nothing else.

The design, the thresholds, and the predictions below were
all written **before the run**. The results section is at the
end, filled in after.

## PROCESS — the design audit (before any code)

**2026-10-27 — one mechanism, two harms, so two loci.** The
harm TRANSITIONS measured decomposes into two injuries from a
single mechanism. `Chart.record_transition` forms a belief
entry for *any* attempted direction (`setdefault`, passable
by default) — a phantom exit for every wall the agent bumps.
What happens next depends on trust. At trusted places the
next fold pops the phantom and charges one surprise ("an exit
I believed in is not here now"): that is the **bump tax**,
3/day on stable days (conservatory north and west, gallery
east), minted and paid *inside a single audit excursion* —
the bump forms the phantom, the fold immediately after pops
it. At the twin places the sightings arrive distrusted, a
distrusted fold never rewrites beliefs, so the phantom is
never popped: no tax — instead the chart *believes a wall is
a doorway forever*, and its implicit predictions err there
daily (place-2 west; place-6 north, east — the whole of the
9–0 disagreement record). Any consultation that lives at only
one moment can reach at most one of the two harms: a morning
revision arrives too late for a tax minted and paid within
one excursion; a record-time rule cannot remove a phantom
minted on a pre-table day. So the rule lives at **two loci**,
each with its own named job and its own receipt channel —
morning alignment for standing beliefs, record time for
belief formation.

**2026-10-27 — loci examined and set aside.** *Decision
time* (the policy consulting the table before it acts) was
examined first and rejected on the code, not on taste: the
route is a script over *traversed edges* (`transit_graph`
reads edge attempts, not believed exits), and the audit
excursion is choreography gated on the *raw observation* —
neither reads the beliefs the table would veto, along any
cell where they differ. And suppressing the audit's bumps
at decision time would starve the night fit of the very
`same`/`blocked` evidence the table is fitted on — the
consultation eating its own evidence stream. *Fold time*
(letting the table arbitrate distrusted folds) was examined
and not built: arbitrating a fold is belief-formation from
perception, a different mechanism; the outcome record is the
stronger claimant and needs no per-fold arbitration to win —
it revises at the morning and prevents at the mint.

**2026-10-27 — the tie cell, and the threshold it forces.**
The night-3 table (60 episodes, 19 cells) is not the clean
instrument a threshold designer would wish for. The three
trusted tax cells are unanimous (`same`, n=3 each). But the
twin cells are structurally poor: (place-6, north) and
(place-6, east) have **n=2** (the observatory wing is visited
once a day, late), and (place-2, west) is **genuinely mixed —
3 `move`, 3 `same`** at night 3, its expected class set by
the fit's recency tie-break. The mixture is not noise; it is
the twin disease at the episode level: one perceived name
covers two rooms, and west is a wall in one and a doorway in
the other, so the cell's record holds both. The road not
taken — qualifying on n≥3 *and* unanimity — is therefore not
a stricter version of this rule; it is a different rule that
would cover the three tax cells and exempt every twin cell
(the n=2 pair by count, the tie by unanimity), leaving chart
implicit accuracy exactly where it stands. It was considered
and rejected for that reason, stated here in advance so the
choice is accountable: **a cell qualifies when it carries
n ≥ 2 recorded outcomes and is not flagged contested** by the
night fit's escalation tier (no cell is contested in this
world; the flag is honoured anyway). The consultation then
trusts the table *as fitted* — the fit's own majority verdict,
recency breaking ties, is the expected class — rather than
re-judging the fit at the chart's door. The n≥2 floor still
excludes the table's two singletons (place-3 west, place-6
south, both n=1 `move` cells the chart already agrees with).
Every override's receipt carries the cell's counts, so the
(place-2, west) override will show its 3/3 tie in the open,
and the ON-day scoring channels will judge it daily: if the
recency verdict is wrong for the days' actual episodes, the
implicit-accuracy channel will say so.

**2026-10-27 — the rule.** A qualified cell's expected class
governs the chart's belief about that way:

- *Morning alignment* (at wake on days 4–6, before the
  route, using the table fitted the previous night — the
  same held-out discipline as the scoring): expected `same`
  → the believed exit is **removed**, in the chart's own
  append-only idiom (the fold's vanish move, funded by
  outcomes instead of by a trusted sighting the twins never
  receive); expected `blocked` → a passable belief is marked
  impassable/locked; expected `move` → a belief held
  impassable is restored. Where the chart holds no belief
  for a qualified cell, the table does nothing — it governs
  the passability of believed exits; it does not author
  geography.
- *Record time*: when an attempt a qualified cell expects
  to end `same` does end `same`, and the belief entry for
  that way was minted by this very attempt, the minted
  entry is removed in the same call and a
  `consulted-suppression` receipt rides in the entry stream.
  The edge attempt stays logged — the evidence is kept;
  what the chart may not do is form a belief the night
  already knows is a wall.

Consultation never touches a traversal or a locked outcome
(the chart's own machinery owns them, and a changed world
announces itself there first), never creates an exit, and
never fires on an unqualified or contested cell.

**2026-10-27 — accounting, stated before anyone can argue
with it.** Morning revisions are chart *revisions*
(`surprise: False`), not surprises: the world did not
contradict the model this morning; the model's own night
record corrected it — the same accounting by which System
2's nightly prototype upgrades are not day surprises. Each
carries `source: transition-table` and the cell's counts, so
a reader who disputes the accounting can re-price them from
the receipts (3 extra "surprises" on day 4, 0 thereafter, is
the alternative total, computable from the filed entries).
Suppressions are their own entry type and their own channel,
never folded into the surprise decomposition.

**2026-10-27 — the invariance floor.** The consulted run
re-runs the whole six days on a forked harness whose only
differences are the consulted chart and the morning hook.
Days 1–3 (no table exists) must reproduce TRANSITIONS' days
1–3 exactly, and the runner asserts it in-flight: route and
audit steps, the full surprise decomposition, recognition
accuracy, episode counts, chart implicit accuracy, the
*complete day-log entries*, and the night-3 fitted table
(19 cells) — against the filed `transitions-results.json`.
If the floor fails, the round stops; it does not tune.

## Pre-registered predictions (days 4–6, vs the control arm)

Control = TRANSITIONS' own days 4–6: total surprises 3/day
(0 route / 3 bump tax / 0 audit other), chart implicit
accuracy 0.8125, pre-registered surprises 0, route 3 steps +
audit 13 steps, goal reached, table accuracy 1.000.

| channel | control | predicted, consulted |
|---|---|---|
| total framework surprises / day | 3 | **0** (0 / 0 / 0) |
| chart implicit accuracy (ON-day episodes) | 0.8125 | **1.000** |
| pre-registered surprises / day | 0 | 0 (unchanged) |
| table held-out accuracy | 1.000 | 1.000 (unchanged) |
| steps (route + audit), goal | 3 + 13, reached | identical |
| morning revisions | — | day 4: **3** (place-2 west, place-6 north, place-6 east); days 5–6: **0** |
| record-time suppressions | — | **6 / day** (every audit bump direction is a qualified `same` cell) |

**Falsifier.** The wiring fails if, on any ON day: (a) total
framework surprises do not fall below the control's 3; or
(b) chart implicit accuracy does not rise above 0.8125; or
(c) a surprise appears in a channel that was zero in control
(route, audit-other) — a new surprise class. The channels
are separable by construction, so a partial landing (tax
fixed, twins not; or the reverse) indicts one locus by name
and is reported as such, not averaged away.

## Results — the falsifier does not fire; every prediction lands

**Verdict: consultation works, completely, on the ground it
was pre-registered on.** On all three ON days the consulted
arm ran **0 total framework surprises** against the control's
3 (decomposition 0 route / 0 bump tax / 0 audit other — the
tax is not reduced, it is *not minted*), and chart implicit
accuracy on the same episodes rose from **0.8125 to 1.000**.
All nine of the control arm's ON-day implicit errors — the
(place-2, west), (place-6, north), (place-6, east) episodes,
predicted `move`, outcome `same`, three a day — flip to
correct, and no new error appears anywhere else. No surprise
appeared in any channel that was zero in control: **no new
surprise class**. The pre-registered channel reads 0 and the
table's held-out accuracy 1.000, exactly as in the control —
consultation consumed the table's knowledge without
distorting the measurement of it.

| day | arm | steps | surprises (route / tax / other) | implicit acc | morning revisions | suppressions |
|---|---|---|---|---|---|---|
| 4 | control | 3+13 | 3 (0 / 3 / 0) | 0.8125 | — | — |
| 4 | **consulted** | 3+13 | **0 (0 / 0 / 0)** | **1.000** | **3** | **6** |
| 5 | control | 3+13 | 3 (0 / 3 / 0) | 0.8125 | — | — |
| 5 | **consulted** | 3+13 | **0 (0 / 0 / 0)** | **1.000** | **0** | **6** |
| 6 | control | 3+13 | 3 (0 / 3 / 0) | 0.8125 | — | — |
| 6 | **consulted** | 3+13 | **0 (0 / 0 / 0)** | **1.000** | **0** | **6** |

Every row of the pre-registered prediction table landed as
stated, including the consultation's own receipts: day 4's
morning made exactly the three twin revisions — (place-2,
west) on its 3/3-tied record (n=6, counts {move 3, same 3},
the tie carried in the entry for any reader to re-judge),
(place-6, north) and (place-6, east) on 2/2 each — and days
5–6 mornings made none, because record-time suppression had
kept the mint closed overnight: exactly six suppressions a
day, one per audit bump (conservatory north and west,
library west, observatory north and east, gallery east),
each receipted with its cell's counts. Steps, goal, episode
counts and class mix are identical to control on every day;
the goal was reached every day in both arms.

**The invariance floor held, and then some.** Days 1–3
asserted equal to the filed baseline in-flight — metrics
and the complete day-log entries — and the night-3 table
came out identical (19 cells). More than the floor
required: the night-4 and night-5 tables are also identical
across arms, cell for cell. Consultation changed what the
chart *believes* without changing what the agent *does* or
what the night *learns* — the behaviour stream the evidence
is drawn from is untouched, which is why the comparison is
clean: the only differing entries in the consulted arm's
day logs are the consultation's own, tagged and counted.

**What this does and does not prove.** In this world, the
standing chart is now *exactly as accurate as the table it
used to lose to*: the 9–0 separation of TRANSITIONS is
closed, not by the chart learning better perception (its
senses are as doubted as ever at the twins) but by the
chart being forbidden to hold beliefs its own outcome
record refutes, and forbidden to mint new ones the record
already refutes. The chart's blindness at doubted places
was never a perception failure; it was a bookkeeping rule —
beliefs may only be revised by trusted sightings — and the
outcome record is the second claimant that rule was
missing. Stated limits, unchanged from the last round and
not dissolved by this one: the world never changed during
the run, so the consultation has never had to *retract*
(a changed wall would surface first as a traversal or a
pre-registered surprise, and the night fit would re-judge
the cell — the channel for it exists and, as before, reads
zero because nothing moved); the table was still never
asked about a novel cell; and the escalation tier still
never fired (0 escalations, 0 V-JEPA seconds, in-sample
margins saturated as before). The (place-2, west) override
also deserves its honest footnote: it rests on the fit's
recency tie-break over a cell whose record is genuinely
split, and it was right on all three ON days because the
days' actual (place-2, west) episodes are the library's
bump, not the observatory's doorway — in a programme that
visited the observatory *as* place-2 more often, the same
rule would have to earn its keep the other way, and the
implicit channel is where it would be caught.

**Costs.** The consulted run: **32.9 s wall**, 119 rack
embedding calls (identical count to the control run — the
episodes reuse the day's perception embeddings, and the
consultation itself is bookkeeping over the fitted table,
no new inference), 0 s of V-JEPA, peak RSS 122 MB.

## PROCESS — the run, as it happened

**2026-10-27 — built as copies, pre-registered, then run
once.** `consulted.py` (a `Chart` subclass — morning
`consult()` plus a `record_transition` override; the
framework file is untouched) and `run_consulted.py` (a
faithful fork of the original runner, differing only in the
chart class, the morning hook, a consultation channel in
the day metrics, the in-flight invariance assertions, and
the output filenames, so the original's results are not
overwritten). The design audit, threshold reasoning, rule,
accounting, predictions and falsifier were written into
this document before the run executed. The run then
completed in a single pass: invariance asserted on days
1–3 and at the night-3 fit; consultation live from the
day-4 morning; no aborts, no anomalies, no harness
amendments, no re-runs — unlike TRANSITIONS, the receipts
(the full day entries behind every count, including the
consultation's own entries) were in the results file from
the first pass, because the fork inherited the amended
harness. One deviation from the design text to record: the
design said each suppression receipt would ride "in the
entry stream"; in the code it also carries an explicit
`"surprise": False` field where the base chart's entries
rely on the key's absence — cosmetic, and it changes no
count (the driver's test is `e.get("surprise")` either
way), but the record is the record.

## Verdicts

- **The table, consulted: the wiring works.** Total
  surprises 3/day → **0/day**; chart implicit accuracy
  0.8125 → **1.000**; pre-registered surprises 0; no new
  surprise class. The falsifier, stated in advance, does
  not fire on any leg, on any day.
- **Both loci earned their place.** The morning revision
  cleared the standing twin phantoms once (3 revisions, all
  on day 4); record-time suppression kept the mint closed
  thereafter (6/day, and days 5–6 needed no morning
  revisions at all). Either locus alone would have failed
  one leg of the falsifier — the morning cannot reach a tax
  minted inside an excursion, and record time cannot remove
  a phantom minted before the table existed.
- **The chart now believes its own history.** The deeper
  receipt is the identical fit tables: belief revision by
  outcome record changed nothing about behaviour or
  evidence, only about what the model holds true — the
  chart's map and the model's physics are, in this world,
  finally the same document.
