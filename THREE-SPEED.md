# The Pi Three-Speed Agent — reflexes, decisions, reflection in one harness

**Headline (referee-completed — the lane finished every run and wrote this document, then its final report died in transit; numbers below are the referee's, recomputed from `three-speed-results.json`): the three-speed stack MATCHES the flat scripted explorer and does not beat it (full arm median 4,113 vs baseline 4,563.5, same 5 rooms, fewer turns) — but the layers are individually legible: reflexes alone survive long and go nowhere (1,489 turns, 1 room); the decision tier triples the rooms; and reflection demonstrably steers (run 22: DESCEND chosen 0 times in ~300 decision replies before the directive, 76 times after). The chart never lied under any configuration: 0 merges / 0 splits in 11/11 runs.**

Casey's stack doctrine, built literally: reflexes (fast, cheap,
immediate) → decision-making (mid-speed, weighs options, calls gauges)
→ reflective LLM calls (slow pulse, sets the gates of what means
what). The harness is **pi** (the coding-agent install on the Oracle,
v1.4.0); the field is NetHack 3.6.7 on the Oracle, played through the
chart league's own rig, so every number here is scored by the league's
own scorer against the league's own baseline (the flat scripted
explorer: **median 5 rooms × 1,061 turns = 4,563.5, chart truth
0 merges / 0 splits**, `liquid-world-model/NETHACK-CHART.md`).

## The stack as built

One player process per run. Only the policy is new: `chartplay.Run` is
subclassed and only `decide()` is replaced — perception, the liquid
chart, the plan machinery (frontier / tile-frontier / descend / search
/ wander), the end-of-game flows and the run record are the league's
own code, unmodified. The game process itself stays on the Oracle:
the league's real `NHGame` runs there behind a JSON-lines server, and
a local shim speaks the same interface across one persistent SSH
channel, because that is where the game belongs and where the
TypeSafe credential isn't (see Step 0).

**REFLEX — TypeSafe Jev (hosted, `jev-latest`).** Fires on hunger, on
evidenced hostility (below), or on low HP with no monster near. The
script proposes candidate actions in an order set by the gates in
force; Jev answers each with a go/no-go probability ("Should this
action proceed?"); the first GO (p ≥ 0.5) executes. If Jev vetoes
every candidate, the league's script default executes (counted as
`reflex_all_veto`). Jev never picks a direction; it vets proposals —
models as gauges, code holds the values.

**DECISION — pi, `kimi-coding/kimi-for-coding-highspeed`.** Whenever
a commitment completes, fails, or runs 40 actions, pi picks the next
commitment from a closed menu — FRONTIER / TILE / DESCEND / SEARCH /
WANDER — from a digest of the chart state (places charted, uncharted
exits, current place kind, HP, hunger, the gates in force). The reply
is parsed mechanically (earliest menu word wins); invalid replies
keep the previous state and are counted. The chosen commitment is
then executed step-by-step by the league's plan machinery. When no
commitment can produce a step, the league's own plan order fills the
turn as a *substrate* — counted separately, so the reader can see
exactly how much of each run the model actually drove.

**REFLECTION — pi, `kimi-coding/k3.1-pro`, thinking medium.** Every
~150 turns, on each descent, or when HP first dives under 25%. It
reviews the run so far (including the reflex tier's own trigger/veto
counts) and re-sets the gates, in a fixed five-field format:
`POSTURE` (bold/balanced/cautious), `FLEE_BELOW` (0.10–0.60),
`EAT_AT` (Hungry/Weak/Fainting), `FOCUS` (explore/descend/survive),
`NOTE` (one sentence). The gates are mechanical, not decorative:
FLEE_BELOW and POSTURE re-order the reflex candidate list, EAT_AT
moves the hunger trigger, FOCUS is read by the decision prompt as an
instruction to honour. Every directive is logged verbatim with the
gates it replaced.

**Ablations.** `reflex` mode: reflex tier only, exploration = the
league plan order (the baseline's brain with Jev reflexes bolted on).
`reflexdec`: reflex + decision, gates frozen at default (no
reflection). `full`: all three speeds.

## Step 0 — driving pi, and the TypeSafe surprise

pi was driven the way its own help prescribes for programs:
`pi -p --no-tools --no-session --thinking <level> --model
<provider/id>`, over the fleet's pinned SSH wrapper, with stdin
closed (an open stdin pipe makes pi wait for a piped prompt — found
the hard way). Two traps on record: invoking through a stripped
non-interactive env fails to exec at all (full path works), and the
very first call per model pays a one-off cold cost (94 s / 40 s in the
bench; seconds thereafter).

Inside pi, "TypeSafe" is exactly one model: `classifier:jev-latest`
— **Jev, a classifier**, usable only through pi-ai's `classify()`
library function, invisible to pi's chat surface and model list. And
pi holds **no TypeSafe credential**: `pi auth check --provider
typesafe` → `not_ready / credentials_not_configured`; pi's provider
expects `TYPESAFE_API_KEY`, which exists nowhere on the Oracle. The
fleet's working route to Jev is the connector CLI (`bin/jev.py`),
which attaches the stored `custom.typesafe` credential as a surrogate
value, only to api.typesafe.ai, from this VM. That is the route the
reflex tier uses. Nothing was read, moved, or re-minted: pi's
`auth.json` was never opened by this lane.

**The gauge verdict (measured before any game was played).** Jev has
two fleet servings, and they are not interchangeable:

- The Oracle farm's local `judge` (the jev-semantic training
  assembly, in-process ONNX, median **7.5 ms**) was tested on twelve
  sane proposals and five deliberately reckless ones (attack at 4% HP
  while surrounded; rest with a monster adjacent at critical HP;
  descend at 6% HP…). It answered "settled +" to four of the five
  reckless proposals; eating while already satiated earned its
  highest positive score of the day. As an absolute go/no-go gauge on
  action text, it cannot be trusted to veto anything.
- The hosted Jev (median **0.52 s**/call, max 0.71 s, n=12)
  discriminates like a reflex should: rest-with-a-monster-near 0.14,
  pray-at-8%-HP 0.32, kick-the-door 0.38, attack-at-62% 0.42,
  flee-at-18% 0.70, eat-when-hungry 0.66, rest-when-safe 0.76.

So the reflex tier is the hosted model, and the local judge's failure
is recorded as a finding, not routed around in silence.

## Latency — what each speed costs (measured)

| tier | route | median | notes |
|---|---|---|---|
| Reflex | Jev hosted via `jev.py` | **0.52 s**/eval | max 0.71 s, n=12; identical texts cached per run |
| Reflex (rejected) | farm `judge` local ONNX | 7.5 ms | fast and wrong-side-out; see gauge verdict |
| Decision | pi `kimi-for-coding-highspeed` | **~3.5 s**/call | n=5 warm: 2.5–4.6 s |
| Reflection | pi `k3.1-pro`, thinking medium | **~5.5 s**/call | n=5 warm: 4.0–6.8 s |
| (first choice) | pi MiniMax-M3.1-Flash | ~3.9 s | benched fine, then its key died — see Process |
| (first choice) | pi MiniMax-M3, thinking medium | ~3.6–5.3 s | same outage |

## Process — how this lane actually went (written as it happened)

[carried in full in the working log; the load-bearing incidents:]

1. **Step 0 cleared by reading the launcher.** pi's launcher is a
   shell script that resolves a managed node and the release's
   `.bin/pi`; full-path invocation works where the stripped SSH env
   failed. Print mode + `--no-tools` is the programmatic door.
2. **TypeSafe is a classifier, not a chat model**, and uncredentialed
   inside pi (above). The reflex tier was rebuilt around that fact
   instead of pretending otherwise.
3. **The farm judge failed its audition** (above) — absolute
   readings on action text are near-useless; only the hosted model
   earned the reflex seat.
4. **Records from backgrounded exec sessions vanish.** Both smoke
   runs played fully and printed summaries, yet their JSON records
   exist nowhere on disk; writes from foreground execs and from
   detached `nohup` children persist (verified by probe). All real
   runs were launched detached with log files, per fleet practice.
5. **"Too many hacks running now."** NetHack allows ten concurrent
   game slots (playground lock letters a–j, MAXPLAYERS=10). Stale
   level files from the league's own games (a–g) plus this lane's
   two smoke games (h, i) filled every slot; the batch's first ten
   runs "died" in 0.1 s at startup. An orphaned smoke game was
   killed, the stale slots a–i were removed with sudo (the live
   game's slot j was not touched), and the poisoned zero-turn
   records were deleted before relaunch. The box was 7/10 full
   before this lane started — the leak is a property of killed
   games, not of any one lane.
6. **Run 21, first attempt — two failures for the price of one**
   (record kept as `evidence-run21-pi401-petstorm.json`). (a) Every
   pi call returned **401 invalid api key**: pi's MiniMax credential
   is solely the `MINIMAX_API_KEY` env var on the Oracle (proven by
   `env -u` → "No API key found"), and MiniMax began rejecting that
   key between the latency bench (~03:05, working) and the first run
   (~03:20). Not a wiring fault; replacing keys is the user's move,
   never the lane's. The stack re-tiered **inside pi** to the user's
   OAuth Kimi provider (decision `kimi-for-coding-highspeed`,
   reflection `k3.1-pro`), documented here rather than silently.
   (b) With the decision tier dead, the reflex tier exposed a design
   bug: the combat trigger fired on any creature within 2 cells —
   which in NetHack includes the valkyrie's own **pet**. 764
   triggers, Jev GO 764 times (FLEE 502, FIGHT 262), and the run
   parked itself into the stuck-quit at 326 turns / 1 room. Reflex
   triggers were re-based on evidence of hostility: HP actually
   dropping, HP under the flee gate with company, or adjacent
   company while already hurt; the rest reflex got the league's own
   consecutive cap.
7. **The second batch froze inside the sandbox overlay** (its log
   stopped at 03:37 in every later view; its slots 23/24 spawned real
   Oracle servers three minutes later by the Oracle's clock, then
   orphaned). Two completed full-mode runs exist only in that
   overlay and are counted as lost. **Pivot: the player moved onto
   the Oracle** — durable filesystem, detached logs, the fleet's
   normal pattern for long work. pi calls became local subprocesses;
   the league rig imports natively (which also removed the ~1.4
   s/turn SSH seam); only the Jev reflex crosses over, via the spool
   bridge described in the stack section, at ~1–3 s per uncached
   evaluation. The first Oracle launch failed every run in 10 s on a
   missing `sys.path` entry (the local layout had hidden it); fixed
   and relaunched. Batch #2's orphaned servers/games were killed and
   their two lock slots freed (the live games' slots were identified
   by start-time order and left untouched).
8. **Seeding, stated as before:** NetHack 3.6.7 has no seed control;
   runs are fixed launch slots (21–25 full, 31–33 reflex-only,
   41–43 reflex+decision), each game seeding itself from system
   entropy. Caps per run: 1,500 turns / 4,000 actions / 3,000 s wall.
   In the final architecture the player is Oracle-resident (no SSH
   seam per turn); the wall cap binds only where a tier's latency
   taxes the loop, which the results below itemise.
9. **The re-ask spiral and the quota (slots 21/22, first Oracle
   batch).** The decision tier was asked 440 times in 457 turns:
   a commitment whose plan could not produce a step (FRONTIER
   routing fails often on a young chart) cleared itself and
   re-asked next turn at ~3 s a call — the flat league falls
   through its plans for free; this design paid per fall-through.
   ~850 pi calls across two runs then exhausted the Kimi plan's
   5-hour usage window mid-batch (429s from turn 350 in run 21,
   turn 825 in run 22). Fixes, in the code before batch 2: a
   12-action substrate cooldown after any fizzled commitment, a
   25-action cooldown after any errored/invalid ask, an 80-ask
   per-run cap, and a pi stand-down after 3 consecutive errors.
   Post-fix decision economy: 26–80 calls per run steering
   hundreds of commitment steps.
10. **Batch 2 and the quota gate.** Remaining slots ran under a
    batch that played the reflex arm first (no pi), then probed
    the Kimi window every 10 minutes; the gate opened after 8
    probes (~05:55 UTC) and the pi arms played with live tiers.
11. **The bridge died twice, once by my own hand.** The Jev spool
    bridge (agent-VM side) was reaped by a sandbox service restart
    during slot 42; worse, the hand-written test request I filed
    to verify the restart had the wrong schema (no `text` field),
    and the bridge raised KeyError on it at the head of every poll
    — no answer was filed while it sat in the spool, through the
    rest of slot 42 and all of slot 43. Both runs are therefore
    decision-live / reflex-dead, and their records say so
    themselves (reflex_errors 60/60 and 62/62). Fixes: poison file
    deleted; bridge patched to quarantine a malformed request
    instead of dying on it; the reflex client gained the circuit
    breaker from item 9's family (3 consecutive timeouts → the
    tier stands down instead of taxing every later turn 45 s).
    Health checks now read filed answers, never process lists.
12. **The flee loop (slots 24/25).** 527 and 504 FLEE choices,
    ~99% of evaluations cache hits on one recurring digest: flee
    at low HP is right per call, but with no hysteresis a single
    monster owned the body for hundreds of turns until the stuck
    detector quit both games. Slot 24's reflection tier saw it in
    words ("rather than repeatedly contesting reflex…") but its
    gates cannot express "stop fleeing this one." Named fix for
    the next iteration: a per-digest flee budget, after which
    FIGHT/PRAY inherit the turn.

## Results

All 11 canonical runs completed (records in `runs-canonical/`,
analysis in `results.json`). The league scorer is unmodified;
score = rooms × turns. Baseline (the flat scripted explorer of
NETHACK-CHART.md, n=10): **median 1,061 turns × 5 rooms =
4,563.5 pts, chart truth 0 merges / 0 splits.**

| slot | mode | turns | rooms | score | depth | cause | wall s |
|---|---|---|---|---|---|---|---|
| 21 | full | 457 | 9 | 4,113 | 2 | wall-clock cap | 3,009 |
| 22 | full | 974 | 5 | 4,870 | 2 | wall-clock cap | 3,017 |
| 23 | full | 1,331 | 5 | 6,655 | 1 | killed by a jackal | 751 |
| 24 | full | 791 | 2 | 1,582 | 1 | stuck (quit) — flee loop | 623 |
| 25 | full | 756 | 2 | 1,512 | 1 | stuck (quit) — flee loop | 351 |
| 31 | reflex | 1,489 | 1 | 1,489 | 1 | killed by a jackal | 86 |
| 32 | reflex | 1,523 | 1 | 1,523 | 1 | turn cap (alive) | 73 |
| 33 | reflex | 1,327 | 6 | 7,962 | 1 | killed by a jackal | 98 |
| 41 | reflexdec | 112 | 2 | 224 | 1 | stuck (quit) | 108 |
| 42 | reflexdec † | 762 | 11 | 8,382 | 2 | wall-clock cap | 3,104 |
| 43 | reflexdec † | 769 | 3 | 2,307 | 1 | wall-clock cap | 3,006 |

† slots 42/43: reflex tier dark (bridge outage, Process §11);
decision tier live throughout.

**Arm medians — full (n=5): 791 turns / 5 rooms / 4,113 pts.
Reflex (n=3): 1,489 / 1 / 1,523. Reflex+decision (n=3): 762 / 3 /
2,307. Chart truth: 0 merges / 0 splits in 11/11 runs** — the
liquid chart never lied under any tier configuration.

**Per-tier latency (measured).** Reflex, hosted Jev direct:
median 0.52 s (bench); in-game via the spool bridge ~4–5 s
uncached, ~0 s on the in-process cache (which served ~99% of the
flee-loop evals and most repeated digests). The local farm judge
answers in 7.5 ms but failed the pre-play safety bench (it
approved resting beside a monster at critical HP) and was never
wired in. Decision (pi, kimi-for-coding-highspeed): bench ~3.5 s,
in-game median 2.7–3.2 s per call. Reflection (pi, k3.1-pro):
7.7–17.9 s per call, median ≈14 s, every ~150 turns.

**Reflection directives — verbatim, with effects.** Every full run
carries its directives in its record (`tiers.reflection[].raw`).
Two receipts matter most:

- *Run 22, turn 750:* "POSTURE: balanced / FLEE_BELOW: 0.35 /
  EAT_AT: Hungry / FOCUS: descend / NOTE: Finish safe nearby
  exploration, then seek the downstairs; eat promptly and avoid
  prolonged fights while Hungry." The decision tier had chosen
  DESCEND **zero** times in ~300 live replies before this landed;
  from turn 750 it chose DESCEND 76 times in a dense run. The
  slow tier's gate moved the mid tier's menu distribution from
  the moment it was set.
- *Run 23, turns 150→1331:* FLEE_BELOW ratcheted 0.35 → 0.40 →
  posture flipped to cautious with FOCUS: survive at turn 900 as
  hunger bit; the final directive (turn 1331) reads "At 1 HP and
  Fainting, avoid all combat, eat any safe food immediately, and
  retreat toward the upstairs…" — the reflection tier tracked
  the run's deterioration and tightened the gates progressively.
  The valkyrie died to a jackal anyway; gates advise, they do
  not save.

Elsewhere directives were variations on "chart the exits,
disengage early" with FOCUS explore throughout — honest
boilerplate, no measurable distribution shift beyond run 22's.

## What each speed buys

**The honest headline: the three-speed stack MATCHES the flat
scripted explorer's median (5 rooms; 4,113 vs 4,563.5 pts) and
does not beat it.** Per-run variance (layout luck: locked-door
starts, jackal density) is larger than any tier effect at n=5.
What each layer demonstrably bought, in numbers:

- **Decision tier — buys rooms per unit time, when its
  commitments can step.** Commitment-led play produced the two
  best room counts of the day relative to turns survived (run 21:
  9 rooms in 457 turns; run 42: 11 rooms in 762 turns with the
  reflex tier dark), and the fixed ask economy (26–80 calls/run)
  makes that affordable. When commitments fizzle (57–58 fizzles
  in runs 23–25), it buys nothing and the substrate carries the
  game — the single most valuable repair would be commitment
  plans that kick locked doors and complete escapes, not a
  smarter chooser.
- **Reflection tier — buys exactly one proven thing: gates that
  move behaviour.** The run-22 FOCUS receipt (0 → 76 DESCEND
  choices at the directive's turn) is a causal, in-record proof
  that the slow pulse steers the mid tier. It also bought a
  legible, verbatim account of each run's risk posture over time
  (run 23's ratchet). It bought no points: no run's score is
  attributable to a directive, and two runs died under freshly
  tightened gates.
- **Reflex tier (the model) — earned nothing measurable in this
  field.** Across 11 runs Jev's veto never changed a game's
  outcome: it GO'd the script's first candidate in ~99% of live
  triggers, its all-veto fallbacks were rare and inert, and its
  two failure modes (the pre-fix pet storm; the flee loop) were
  the day's most expensive pathologies. The script gates around
  it — damage-evidenced triggers, candidate order, the flee
  threshold the reflection tier sets — did the observable work.
  A veto that never binds is instrumentation, not a tier; the
  bench says the model *can* discriminate (0.14 for
  rest-beside-monster vs 0.76 for rest-when-safe), so the honest
  reading is that live candidate sets rarely contained a choice
  worth vetoing. Wire it where the script must choose between
  two live options, or leave it out.
- **The substrate is the load-bearing layer**, exactly as the
  doctrine predicts (hand steering at the bottom): reflex-only
  play is substrate play, and its 6-room / 7,962-pt run 33 shows
  the floor is high when the layout allows. Every tier above it
  is a gauge consulted at a price; this experiment priced them.

**Limits.** n is small and NetHack's variance is huge; two
reflexdec runs lost their reflex tier to infrastructure, and two
full runs were spent partly under a dying quota — all stated in
their records rather than cleaned up. The Kimi 5-hour window is
a real budget constraint on pi-driven play at this call rate.
Overlay-timeline records from this lane's sandbox incidents
exist and are quarantined (`runs/*.overlay.json`): real games,
unverifiable provenance, excluded from every number above.
