# The Faltering Walk — a question-generating recall over the liquid chart

*SuperInstance — experiment report, 2026-10-26. Prototype of §9 of
[MEMORY-PATHS.md](https://github.com/patchwork-quilt/liquid-world-model/blob/main/MEMORY-PATHS.md):
does probing guided by a question-ranked walk over the chart find a
truer world, cheaper, than the shipped dumb policy — and than the
study's named strawman, "probe nearest uncharted exit"?*

## Headline

**The falsifier's letter goes to the walk; the claim goes to the
strawman.** On the pre-registered metric — days-2–3 surprises per
recall unit — the Faltering Walk (B) beats nearest-uncharted (C),
0.0204 vs 0.0449, and on absolute surprises, 6 vs 8. But the
mechanism audit underneath shows B's edge is two shrine surprises
it avoided by never re-entering the shrine — leaving its chart
*wrong* there — while the dominant surprise (the locked door, 6 of
6 runs in every arm) is a policy failure no recall purchase can
touch. Chart truth is not better under B (contents accuracy 0.962,
worst of the three; everything else saturates at 1.000 in a world
this small) and steps are not cheaper (B 87.0 mean vs C 80.0, A
91.2). What *is* proven: the ranking. The walk's top question was
the genuinely live issue in all 6 seeds on both mornings — the
locked-door place on day 2, its conflict, bought at truth price,
#1 on day 3. The Faltering Walk is a good agenda and, in this
dungeon, a decoration as a truth-finder — and the receipts below
show both halves of that sentence.

## Process — written as the work happened

- **Design read.** §9 asks for: PPR over the chart graph (edges =
  believed exits weighted by charted confidence × fog factor ×
  conditional satisfaction); output a ranked *question list* scored
  activation × disagreement (path conflicts, prototype ties, fog /
  low effective confidence, uncharted exits on hot routes); the
  1/4/12 purse spent strictly in that order; fog questions buy a
  re-observation, contradiction questions buy a truth-tier recall of
  the exact testified event, uncharted questions become probes.
- **Operationalisation decisions (mine, documented because §9 is a
  sketch, not a spec).** (1) The shipped dungeon is one fixed world;
  the *seed* drives only the policy RNG — so the protocol is paired
  seeds × 3 days, identical seed set per arm. (2) The shipped policy
  spends no recall in-day, so the purse is spent as a **morning
  allocation at wake** (days 2–3; day 1 starts from an empty chart):
  each bought question costs its tier price — conflict → truth
  recall (12) of the exact archived surprise; fog / ambiguity /
  uncharted → essence recall (4) of the place — and queues one
  physical probe, executed in-day by a wrapper around the untouched
  `ExplorerPolicy` (route to the place, observe; for an uncharted
  question, traverse the exit). Daily purse budget: 24 units for
  both probing arms; spending stops at the first unaffordable
  question (strict order). (3) The dungeon chart has no prototypes,
  so §9's disagreement term (b) "prototype margin-tie" is
  operationalised as **destination ambiguity**: believed exits whose
  destination was never seen (`to: None` — closed doors), plus
  believed-unvisited places. The twin/margin-tie case exists only in
  the Thor world; this build is the dungeon version §9 names first.
  (4) HyDE (§9 step 4): implemented in seed form — when no goal place
  is charted, the walk's second seed is the place whose id/contents
  tokens best match a hypothetical goal description ("treasure
  vault"). In this protocol day 1 normally charts the vault, so the
  HyDE seed is expected to be idle; it is code, documented, and
  logged when used. (5) Arm C's "nearest" = BFS distance over the
  believed graph from the wake place (entrance) to the exit's place,
  ties broken by place then direction. (6) Every arm, including A,
  pays the demo's evening reflex recall (1 unit) on days with
  surprises — parity with the shipped demo, charged to all arms.
- **Where the change lives.** Framework copy only (the repo itself
  is untouched; the change ships as `faltering-walk.patch`):
  `lwm/tiers.py` gains the walk graph, PPR, disagreement scoring,
  the ranked question list, and the morning allocator;
  `lwm/policy.py` gains one wrapper class, `ProbePolicy`. The
  shipped `ExplorerPolicy`, `Chart`, and day cycle are not modified
  — S1 machinery byte-identical, per the THOR-TEST attribution
  discipline.
- **First run of the walk (sanity, seed 7).** Day-2 morning ranked
  treasury first (a "tie" — its three doorways' destinations were
  never seen from inside) and vault second: the walk's top questions
  were the goal route's own unknowns, which is what §9 predicted
  activation × disagreement would surface. Both probing arms spent
  exactly their 24-unit purse; arm C's list was the same exits in
  distance order.
- **The full run (6 seeds × 3 arms × 3 days).** Fast and clean; one
  wrinkle worth recording: arm C's recall spend *varies* (25–41 per
  run) while B's is constant (49). Not a rigging bug — C's only
  question kind is uncharted exits, and by day 3 they nearly run
  out (most C day-3 mornings bought exactly one question). The
  strawman's purse goes unspent because its curiosity has one
  word. B always finds six questions worth buying.
- **Mechanism audit (the part that matters).** The aggregate said
  B had fewer surprises; before believing it I traced every
  day-2/3 surprise in every run. All 18 runs, all three arms, eat
  exactly one treasury locked-door surprise on day 2 — probing did
  not touch the dominant surprise. The *entire* B-vs-rest delta is
  two shrine-contents surprises (A: 2, C: 2, B: 0) — and B avoided
  them not by resolving the shrine question but by never re-entering
  the shrine in any run, leaving its chart *wrong* there ("lit
  candles" on day 3). The audit changed the verdict; see below.
- **Why the shrine starved.** Disagreement includes staleness only
  through effective confidence and the fog term, both multiplied by
  activation — and the shrine is a dead end off the goal route, so
  its activation is near zero no matter how stale it gets. The walk
  is route-centric by construction; contents rot on cold routes is
  invisible to it. A real design finding, not a tuning miss.

## Method, in one paragraph

At each wake on days 2–3, arms B and C receive a 24-unit purse.
**B** builds the walk graph from the chart (believed exits weighted
by effective confidence × conditional satisfaction), runs
Personalized PageRank seeded at the entrance (0.6) and the believed
goal place (0.4; a HyDE seed substitutes when no goal is charted —
it never fired in this protocol, day 1 always charted the vault),
scores every place activation × disagreement, and buys questions in
rank order: conflict → truth recall of the exact testified event
(12); tie/fog/uncharted → essence recall of the place (4); each
bought question queues one probe (visit the place; for an uncharted
question, traverse the exit), executed in-day by `ProbePolicy`
routing over believed ways, capped at 200 directed steps, before
the untouched shipped policy resumes. **C** buys uncharted exits
nearest-first (BFS over the believed graph), same prices, same
probe machinery. **A** is the shipped demo behaviour. All arms pay
the demo's 1-unit evening reflex recall on surprise days. Chart
truth is graded scorer-side against the dungeon's real map at the
end of day 3. Seeds 3, 7, 11, 19, 23, 42 — paired across arms.

## Results

| metric (6 runs/arm) | A dumb | B Faltering Walk | C nearest-uncharted |
|---|---|---|---|
| surprises/day, mean (d1 · d2 · d3) | 0 · 1.0 · 0.33 | 0 · 1.0 · 0.0 | 0 · 0.67 · 0.67 |
| surprises days 2–3, total | 8 | **6** | 8 |
| recall units spent, total | 8 | 294 | 178 |
| — by tier (reflex/essence/truth) | 8/0/0 | 6/216/72 | 6/172/0 |
| **falsifier metric: d2–3 surprises / recall unit** | (n/a — spends ~nothing) | **0.0204** | 0.0449 |
| steps/day, mean (d1 · d2 · d3) | 20.8 · 30.3 · 40.0 | 20.8 · 27.7 · 38.5 | 20.8 · 27.7 · 31.5 |
| total steps, mean (range) | 91.2 (66–127) | 87.0 (68–129) | **80.0 (68–89)** |
| chart coverage (of 13 rooms) | 1.000 | 1.000 | 1.000 |
| exit-destination accuracy | 1.000 | 1.000 | 1.000 |
| exit recall | 1.000 | 1.000 | 1.000 |
| **contents accuracy** | 0.987 | **0.962** | 0.987 |

Arm A's day curve on seed 7 reproduces the shipped README exactly
(21/27/33 steps, 0/1/0 surprises) — the harness changed nothing for
the control. The framework suite on the patched copy:
**TEST SUMMARY: 10/10 PASS.**

### The walk's questions, verbatim (receipts)

Seed 7, day 2 — top 3 of 13: `treasury / tie / 0.3968`
(activation 0.153, disagreement 2.6: two unseen destinations +
an untraversed exit + ignorance 0.4); `vault / tie / 0.2197`;
`armory / uncharted / 0.0744`. Bought, in order: treasury, vault,
armory, gallery, library, hall — 6 questions, 24 essence units.

Seed 7, day 3 — top 3: `treasury / conflict / 0.1849` (the day-2
locked-door surprise, now in history); `vault / tie / 0.1413`;
`chapel / fog / 0.0545`. Bought: treasury (truth recall, 12 — the
exact testified day-2 event), vault, chapel, garden — 24 units.

In all 6 seeds: the day-2 top-3 includes the treasury (the
locked-door place) and the day-3 **#1 question is the treasury
conflict**, bought with the truth tier every time. On §9's
question-quality test — does the top of the list name the known
live issues — the walk passes 6/6 on both days. The ranking is
not the problem.

### Where every surprise actually came from (audited)

Days 2–3 surprise census, all runs: treasury `exit-passable`
(locked door tried empty-handed, day 2): **6 per arm**. Shrine
`contents` (lit candles → cold ashes, discovered day 3): A 2,
C 2, **B 0**. Nothing else, anywhere. The locked-door surprise is
a *policy* failure (beelining to the goal without the key), not a
recall failure — no morning purchase available to any arm
prevents it, because on day-2 morning the chart still believes
the door passable (day 1 opened it, key in hand). And B's two
missing shrine surprises are not resolutions: B's probes never
targeted the shrine in any run (it ranks low — dead end, cold
route), so B's final chart still believes "lit candles" in the
seeds where A and C paid a surprise to learn better. That is
exactly why B's contents accuracy is the worst of the three.

## Verdict

**On the falsifier's letter: B wins.** Question-ranked probing
beats nearest-uncharted on next-day surprises per recall unit
(0.0204 vs 0.0449), and on absolute days-2–3 surprises (6 vs 8).
The pre-registered falsifier does not fire.

**On the study's actual claim — a *truer* world, *cheaper* — the
result is a negative, and it should be published as one.** Chart
truth under B is not better: coverage and exit beliefs saturate at
1.000 for every arm (the 13-room dungeon in 3 days is too small
to separate graph beliefs), and on the one axis that separates —
contents — B is *worst* (0.962 vs 0.987), because its surprise
advantage is ignorance preserved, not ignorance resolved: it
never looked at the one place that changed. Steps are not
cheaper either: B (87.0 mean) sits between A (91.2) and C (80.0),
with the worst single day in the study (seed 23, day 3: 85 steps
of probe routing). A surprise avoided by not looking is not a
surprise understood; a metric that counts only surprises will
reward any policy that keeps its eyes shut, and B's ranked eyes
happened to be aimed at the route, not the rot.

**What the prototype did prove:** the question list itself. A
PPR walk with activation × disagreement puts the genuinely live
issue at the top of the morning, every morning, in every seed —
the locked door before it is tried again, the contradiction
bought at truth price the day after it happens. As an *agenda*
the Faltering Walk works exactly as §9 hoped. What does not work
— in this world, at this size — is cashing the agenda out as
re-observation probes and expecting truth to follow: the world
is too static, its one change sits where activation can't see
it, and its dominant surprise belongs to the policy layer, not
the memory layer. The honest next experiment is a bigger, less
saturating world (the Thor visual world, where contents-equivalents
— recognition — genuinely rot), a disagreement term that prices
staleness *unconditionally* (activation-independent floor for
fogged places), and questions routed to the policy as intentions,
not just to the feet as probes. Until then: keep PPR recall as an
agenda for the morning alignment; do not claim it finds a truer
world cheaper. The walk asks good questions. This dungeon was
too small to pay for the answers.

## Files

- `faltering-walk.patch` — the whole framework change (+403 lines,
  additions only): the walk, PPR, disagreement scoring, question
  list, and morning allocator in `lwm/tiers.py`; `ProbePolicy` in
  `lwm/policy.py`. Shipped `ExplorerPolicy`, `Chart`, and the day
  cycle unmodified.
- `experiment.py` — the three-arm harness (paired seeds, scorer-side
  chart-truth grading).
- `results.json` — every run, every day, every question list,
  aggregates, and the falsifier block.
- `framework/` — the patched working copy the numbers came from
  (suite: TEST SUMMARY 10/10 PASS there).
