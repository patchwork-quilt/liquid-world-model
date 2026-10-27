# FOLLOW-UP — the forced observatory visit (live-proving the twins)

SuperInstance — liquid-world-model, Thor experiment follow-up.
Seed 7 throughout. Code: `detour_policy.py` + `run_followup.py`
in `~/lwm-thor/` on the Thor; raw record: `results-followup.json`.

## Headline

**The twin separation is live-proven — with two qualifications,
both measured, both named in advance by THOR-TEST's wart list.**

On day 3, after the goal route completed, the script walked the
agent into observatory for the first time since the night-1
upgrade. The live view — a fresh, jittered render the rack had
never embedded (cache miss; a genuine out-of-sample perception) —
matched the System-2-seeded observatory prototypes at cosine
**0.99897**, clearly clear of the purified library prototype at
**0.99032**. The corpus claim survived contact with the world:
S2's prototypes, not the library's, own the observatory view.

The qualifications:

1. **It answered to the duplicate's name.** The winning
   similarity was an exact tie between place-6 (night 1's seed)
   and place-7 (night 2's duplicate) — identical vectors, margin
   **0.0** — and the matcher's ordering handed the sighting to
   place-7. So the *observatory prototype pair* is live-proven;
   place-6 by name remains unperceived, and which of the pair a
   visit lands on is tie-break luck, not preference.
2. **It was recognised but distrusted.** Margin 0.0 is below the
   senses' doubt threshold, so the observation arrived at trust
   **0.3** and the chart logged a *distrusted* entry — the exact
   behaviour THOR-TEST's wart 1 predicted for a future visit
   ("two identical prototypes would make any future observatory
   visit a margin-0, low-trust match"). Because it was a first
   sight, the chart still sketched the place (confidence 0.6,
   exits and contents written): recognition without full belief,
   which is arguably the correct epistemic posture toward a
   room your senses refuse to vouch for.

## Baseline-match verdict

**Match.** The original three days were re-run from the code
as-is (`run_experiment.py`, seed 7): the fresh `results.json`
is **deep-equal to the original on every non-volatile field** —
all day metrics, both night records, config, and even the
footprint's 18 embed calls / 0 cache hits. (Volatile fields
differ as expected: wall times, latency means, and the rack's
cumulative counter, which advanced 5444 → 5462, exactly this
run's 18 calls.) The follow-up run then re-executed the same
flow internally and asserted equality again — days 1–2, both
nights, and day-3 phase A all match the baseline inside the
run that produced the detour receipts below. The detour stands
on the original floor, twice checked.

## The one change (script layer only)

`DetourScriptPolicy` subclasses the frozen `ScriptPolicy`. It
is behaviourally identical until *armed* — and arming is
unreachable inside `run_day`, which breaks out the moment the
treasure is observed, before `decide()` is ever asked to act on
it. Perception (`perception.py`), System 2 (`system2.py`), the
world, and the framework (`lwm/`) are byte-untouched (md5s
recorded before the run).

**Trigger.** Day 3: `run_day` returns `goal_reached=True` (3
steps, as baseline). The harness takes one arming observation of
the goal place (detour step 0 below); the policy arms on its
treasure contents — the goal route is complete, by the agent's
own senses. The harness then drives the policy through the same
observe → decide → step → record-transition calls `run_day`
itself makes, in the same relative order, because the
framework's day loop ends at the goal by design and the detour
lives after it.

**The excursion** is a fixed programme of four written moves,
each gated on the doorway actually being perceived, aborting
with a stated reason otherwise:

| move | from → to (true) | why |
|------|------------------|-----|
| west | vault → conservatory | leave the goal |
| south | conservatory → library | stand in the twin place |
| east | library → **observatory** | the forced visit |
| west | observatory → library | back out |

Written moves, not chart routing, for a measured reason: at the
end of day 3 the chart contains **no believed route out of the
vault** — place-5's west exit and place-4's south exit were
never traversed, so the believed transit graph flows one-way
into the goal. There was nothing to route over; a script is a
written route, so this one is written.

## Receipts — every observation of the detour

Similarities are the live sighting's cosine against the day-3
prototype set (harness-computed from the recorded embedding).

| n | move | true room | perceived | top sims | margin | trust | chart entries |
|---|------|-----------|-----------|----------|--------|-------|---------------|
| 0 | *(arming glance, no move)* | vault | place-5 | p5 0.99949 · p1 0.94974 | 0.0498 | 1.0 | none |
| 1 | west | conservatory | place-4 | p4 0.99984 · p3 0.96337 | 0.0365 | 1.0 | none |
| 2 | south | library | place-2 | p2 0.99945 · p7/p6 0.99169 | 0.0078 | **0.3** | distrusted |
| 3 | east | **observatory** | **place-7** | p7 0.99897 = p6 0.99897 · p2 0.99032 | **0.0** | **0.3** | distrusted |
| 4 | west | library | place-2 | p2 0.99934 · p7/p6 0.99116 | 0.0082 | **0.3** | distrusted |

Notes on the receipts:

- **Step 3 is the experiment.** The observatory view matched the
  S2-seeded prototypes (0.99897) and not the library prototype
  (0.99032) — an 0.0087 gap, small in absolute terms because
  I-JEPA's space here is anisotropic, but the same ordering the
  corpus predicted, on a view nobody tuned against.
- **The doubt tax is symmetric.** Steps 2 and 4 are *library*
  arrivals, correctly perceived as place-2 at 0.9994 — yet also
  distrusted (margins 0.0078 / 0.0082), because the observatory
  prototypes sit 0.9917 behind them. Near-twinship now taxes
  trust on both twins' doorsteps. (Baseline day 3's single
  low-trust observation is the same mechanism on the route's
  library arrival.) Full day 3: **4 of 9 sightings low-trust**,
  vs 1 of 4 on the baseline day.
- **Surprises generated by the visit: 0.** The only chart
  entries are the three *distrusted* records — which are not
  surprises. Nothing the chart believed was contradicted: its
  beliefs about the doors the detour used were empty
  (destinations unknown), so there was nothing to be wrong
  about. The visit informed; it did not refute.

## What the visit wrote into the chart

- **Chart places 5 → 6.** The visited place (wearing id place-7)
  is now *observed*: 1 observation, day 3, confidence 0.6
  (the first-sight sketch value, reached via the distrusted
  path). Wart 2 from THOR-TEST — "the chart never gains
  observatory as an observed place" — is closed.
- **Beliefs written from the visit:** contents `[]` (formed);
  exits **south** (destination still unknown — never taken) and
  **west**, whose destination the return step then fixed to
  place-2. Symmetrically, place-2's **east** exit belief gained
  its destination: `to: place-7` (was unknown).
- **The uncharted set shrank 5 → 3**: (place-2, east),
  (place-4, south) and (place-5, west) were resolved by being
  walked; one new entry appeared, (place-7, south), never tried.
  place-3's two never-tried exits remain.
- **Side effect, stated plainly:** the detour taught the chart
  the way back. The believed transit graph went from a one-way
  flow into the vault to a graph with return edges (place-5
  west→place-4, place-4 south→place-2, place-2 east→place-7,
  place-7 west→place-2). Future days could route home. That is
  the script's doing, not S2's, and it is reported as
  choreography, not learning.

## Night 3 — System 2 meets a visited twin (computed, not applied)

The original experiment ended before night 3; here the upgrade
was computed on the full corpus (23 sightings, incl. the visit)
and recorded, not applied — there is no day 4.

- **No new prototype seeded** (`added: {}`). With a live
  observatory sighting in the corpus, the room is *covered* by
  the place that perceived it (place-7: dominant room
  observatory, purity 1.0, 1 sighting), so the wart's growth
  mechanism — seeding a fresh duplicate every night — stops.
- **The duplicate itself is not removed.** The post-upgrade
  list still carries place-6 and place-7, both labelled
  observatory. S2 has no retirement move: place-6, still
  without a single sighting, is carried through untouched.
  place-7's prototype would be re-derived from its one live
  sighting (purified, clean 1/1). Corpus accuracy 1.0 → 1.0,
  tau held at 0.95. (Under those night-3 prototypes the live
  sighting assigns to place-7 at similarity 1.0 — trivially,
  since the prototype would be derived from that very sighting;
  in-sample, stated as such.)
- place-2's record stays honest: 9 sightings, 7 clean, purity
  0.778, the 2 day-1 observatory contaminations still counted —
  history is not rewritten by the visit.

A projection, labelled as one: were night 3 applied, place-7's
prototype (from the live view) and place-6's (the day-1 mean)
would no longer be identical, so a day-4 visit might clear the
doubt margin and arrive trusted. The receipts suggest it; only
a day 4 would prove it.

## The price of certainty

Day 3, baseline vs with detour:

| | baseline | with detour | delta |
|---|----------|-------------|-------|
| steps | 3 | 7 | **+4** |
| observations | 4 | 9 | +5 (4 moves + 1 arming glance) |
| rack embed calls (whole run) | 18 | 23 | +5 |
| surprises | 0 | 0 | 0 |
| recognition accuracy | 1.00 | 1.00 (9 sightings) | — |
| rooms truly visited | 4 | 5 (adds observatory) | +1 |
| chart places observed | 5 | 6 | +1 |
| day ends in | vault | library | goal reached first, at step 3 |

Four steps and five embeddings bought: one out-of-sample
recognition, one charted room with its exits, the resolution of
three uncharted exits, and a return path in the graph. That is
the format's own currency, spent at the recorded rates.

## Honest limits

- **n = 1.** One live visit, one jitter draw. The ordering
  (observatory prototypes > library prototype) matches the
  corpus and the pre-flight probe, but a single draw does not
  bound the failure rate; repeated forced visits across days
  would.
- **The tie-break is luck.** place-7 over place-6 came from the
  matcher's ordering over two identical vectors. On another
  implementation the same visit could wear place-6's name with
  identical meaning. Any future claim should be about the
  prototype *pair* until the duplicate is retired.
- **Trust stayed low by construction.** The distrust is not
  evidence against the separation — it is the duplicate's tax,
  and it falls on library arrivals too. Separating *cleanly*
  (trusted recognition) remains unproven and now has a named
  blocker: two identical prototypes.
- The day-3 route's own receipts did not change: phase A is the
  baseline day, asserted field-by-field inside the run.

## Files

`detour_policy.py` (the one change) · `run_followup.py` (the
harness) · `results-followup.json` (full record, incl. baseline
assertions and chart before/after) · `inspect_chart.py`
(chart dump used in design) · baseline archive
`results-original.json`, re-run log `run-repro.log`.
