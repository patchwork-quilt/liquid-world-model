# VJEPA-PROBE — does the pair of views know what happened?

SuperInstance — liquid-world-model, Thor experiment 2. Code and data
in `~/lwm-thor/vjepa_probe/` on the Thor. World seed 7 (as
THOR-TEST); corpus seed 11.

THOR-TEST charted *places*: an I-JEPA embedding per view, places
learned as prototypes, System 2 upgrading them at night. Places are
half a world model. The other half is *transitions* — what changes
when I act. This probe asks whether the representations the fleet
already serves carry transition signal: given (view_before, action,
view_after), can a deliberately simple readout recover (a) what
kind of transition it was and (b) where a move landed — and does
the *pair* know anything the after-view alone does not?

## PROCESS — written as the work happened

**2026-10-26 16:52 AKDT — the rack's live state, as found.**
`GET /health` → `{"ok": true, "device": "cuda", "loaded":
{"ijepa": true, "vjepa2": false, "judge": true}}` — the same
posture as at THOR-TEST time. But `GET /cards` lists
`vjepa2-vitl-fpc64-256` with a live endpoint (`POST /embed/video`,
1024-dim; the server samples 64 frames uniformly, crops 256×256,
means over spatiotemporal tokens) and *two historically measured
calls at ~6.6 s*. The rack's README says models lazy-load on first
call. So "not loaded" is a posture, not a verdict: the decision
point is one real call, made below.

**2026-10-26 16:52 — world mechanics audit; a class the world
doesn't have.** `visual_world.py` on the Thor is md5-identical to
the local copy, and it has **no lock and no key**: conservatory →
vault is a plain exit, and a step into a non-exit direction just
returns "There is no doorway." The locked door in the programme's
memory belongs to the *text* dungeon, not this visual world. The
brief's third class — *blocked-by-door* — therefore cannot be
sampled from the world as shipped. Two honest options: drop the
class, or add the lock harness-side. Dropping it would silently
shrink the question, and blocked-vs-bump is the crux comparison (a
failed move where the before-view *contains a door* vs one where
it doesn't). Decision: corpus walks run under a thin scorer-side
wrapper that refuses exactly one passage — conservatory →east→
vault, "the vault door is locked." Rooms, geometry, renderer,
seed discipline untouched; the refusal is a corpus label, recorded
per transition. Everything else in the corpus is the world as
shipped. (The wrapper also means vault is never a *walk-in*
destination; walks may be placed in the vault by the harness
between walks — scorer-side placement, stated here — and exit
west normally.)

**2026-10-26 16:53 — environment.** Thor system python: numpy
1.26.4, **no sklearn** → the readouts are hand-rolled
(nearest-centroid; multinomial logistic regression in numpy).
ffmpeg and cv2 4.8 are present for clip assembly. Readout
simplicity is by design anyway: the question is whether the
signal is *in* the representations, not whether a big model can
be trained on top of them.

**2026-10-26 16:54 — DECISION POINT: native route.** One real
call: a minimal clip of the world's own renders (32 frames of the
atrium view, then 32 frames of the gallery view after a real
`step("east")`, 448×448 mp4 @ 8 fps; the server's uniform
64-frame sample then sees a clean cut at the midpoint). Answer in
**6.92 s**, a 1024-dim embedding, and `/health` flipped to
`vjepa2: true`. **V-JEPA 2 serves; the native route is taken.**
The I-JEPA pair-feature fallback is not needed as the primary
route — I-JEPA features are still computed for every view,
because the baselines (above all *view_after alone*) are defined
on them and because the diff/concat pair-features make an honest
second contestant.

**Clip construction, stated once:** every transition clip is
`[before ×32, after ×32]` — a hard cut at frame 32, no fabricated
intermediate frames. A crossfade would invent states the world
never contained. A cut is not natural video, and V-JEPA was
trained on natural video; that distribution gap is part of what
the probe measures, not a defect to be hidden.

## Method (as designed before the corpus existed)

- **Corpus.** Scripted seeded walks under the lock wrapper.
  Per step the walk policy mixes: an exit direction (→ *move*),
  a non-exit direction (→ *same / bump*), a wait — no action
  issued, a fresh observation of the same room (→ *same / wait*),
  and, in the conservatory, attempts on the vault door
  (→ *blocked*), plus dedicated door sessions placed in the
  conservatory. Labels are scorer-side truth: class,
  from-room, to-room, action, subtype. Every observation render
  is stored once (PNG); a step's after-view is the next step's
  before-view.
- **Features.** Per transition: the V-JEPA 2 embedding of the
  pair clip (1024); I-JEPA embeddings of both views, used as
  *concat* (2560), *diff* after−before (1280), *after-only*
  (1280), *before-only* (1280). Plus a one-feature reference:
  cos(before, after). Readouts run with and without the action
  appended as a one-hot (the model that issued the action owns
  its efference copy; both numbers are reported).
- **Readouts.** Nearest-centroid (cosine) and multinomial
  logistic regression (numpy, standardised features, fixed
  hyper-parameters) — frozen features, no representation
  training. Split is **by walk** (70/30, seeded): a step's
  after-view is the next step's before-view, so a per-transition
  split would leak near-duplicates across the line.
- **Tasks.** (a) Transition class, 3-way: *same / move /
  blocked*. (b) Destination room, on the move subset only.
- **Baselines that must be beaten, printed alongside:** uniform
  chance; majority class; and *view_after alone* — for (b) that
  is literally the chart's own THOR-TEST perception
  (nearest-prototype on the after-view). The pair earns its keep
  only where after ≈ before: the *same* and *blocked* classes.

**2026-10-26 16:55 — corpus, as generated.** 276 transitions,
324 unique views, 48 walks (40 wandering, starts rotated through
all 7 rooms; 8 dedicated conservatory door sessions). Classes:
*same* 104 (bump 64, wait 40) · *move* 99 · *blocked* 73.
Destinations on moves: gallery 32, atrium 18, library 17,
observatory 15, cellar 11, conservatory 6 — six destination
classes; vault is never a walk-in destination under the lock, as
designed. Balance note: *blocked* is deliberately
over-represented versus natural wandering (32 of its 73 come from
the door sessions) because it is rare in free walks and it is the
crux class. An exec-service restart interrupted the first
extraction launch mid-flight; a state check on the Thor showed
nothing had run, and the launch was redone cleanly — no partial
state anywhere.

**2026-10-26 16:58 — I-JEPA extraction: a cost surprise.** 324/324
views embedded in 152 s ≈ **0.47 s/call — ~5× the 94 ms/call
THOR-TEST measured** on the same endpoint. Suspect, not proven:
V-JEPA 2 is now resident on the same GPU (it was not, during
THOR-TEST). The cost is accepted; the number is recorded because
anyone budgeting a transition corpus on this rack should budget
with both models resident.

**2026-10-26 16:59 — V-JEPA extraction launched.** 276 pair clips,
sequential, resumable partial saves every 5. At the test call's
6.9 s/clip this is ~30 min of rack time; the readout code
(hand-rolled centroid + logistic regression, walk-level split)
was written and staged while it runs.

**2026-10-26 17:33 — extraction complete.** V-JEPA: 276/276 pair
clips in 2,060 s (~7.5 s/clip steady, slower during warm-up).
Total rack budget for the probe: ~37 min (324 I-JEPA views +
276 V-JEPA clips + the test call). Nobody else's queue was
touched; the rack was only ever called, never reconfigured.

**2026-10-26 17:36 — readouts run; two surprises worth the
record.** First, the strongest cheap baseline was not
*view_after alone* — it was a **single number**: cos(before,
after) from I-JEPA separates *move* from the rest almost by
itself (move 0.922 ± 0.032; same 0.998 ± 0.002; blocked
0.9992 ± 0.0006). But that same number is *blind* exactly where
the probe cares: same and blocked sit on top of each other
(0.998 vs 0.9992, ranges overlapping) — as they must, since both
end in the room they started in. Second surprise, in the other
direction: on *destination*, V-JEPA's pair embedding under a
centroid readout (0.733) is a **worse place-reader than a plain
I-JEPA still (1.000)** — the video features blur precisely what
the stills nail. And a process honesty note on the examples
below: the anecdote this report went looking for — one blocked
case where the pair wins and after-only loses — **does not exist
under the centroid readout**, because blocked was easy for every
action-aware baseline (one door, one room, one action: place +
action identifies it). The pair's win is real but aggregate, in
*same*-class recall under the linear readout. Reported as such;
the verbatim examples are from that readout.

## RESULTS

Split by walk: train 193 transitions, **test 83** (same 36,
move 30, blocked 17). Accuracies ±95% CI on the headline rows.

### Task (a) — transition class (same / move / blocked)

Baselines: uniform chance **0.333** · train-majority **0.361**.

| features | centroid | logreg | logreg recall (same/move/blocked) |
|---|---|---|---|
| **VJ-pair + act** | 0.723 | **0.976 ± 0.033** | **0.94 / 1.00 / 1.00** |
| VJ-pair | 0.723 | 0.867 ± 0.073 | 0.81 / 1.00 / 0.76 |
| IJ-concat + act | 0.590 | 0.819 ± 0.083 | 0.64 / 0.93 / 1.00 |
| IJ-diff + act | 0.687 | 0.759 ± 0.092 | 0.64 / 0.80 / 0.94 |
| COS-1feat + act | 0.747 | 0.855 ± 0.076 | 0.75 / 0.90 / 1.00 |
| AFTER-only + act | 0.530 | 0.711 ± 0.098 | 0.61 / 0.67 / 1.00 |
| AFTER-only | 0.530 | 0.590 ± 0.106 | 0.56 / 0.40 / 1.00 |
| BEFORE-only + act | 0.518 | 0.747 ± 0.094 | 0.56 / 0.83 / 1.00 |

Confusion, logreg (rows = true: same, move, blocked):
VJ-pair+act makes **2 errors in 83** — `[[34,0,2],[0,30,0],[0,0,17]]`.
AFTER-only+act makes 24 — `[[22,14,0],[10,20,0],[0,0,17]]` — and
its errors are the predicted disease: 14 *same* misread as *move*
("I must have arrived here") and 10 *move* misread as *same* —
from the after-view alone, staying and arriving are the same
picture, because they are.

### Task (b) — destination room, moves only (test n = 30)

Baselines: chance 0.167 · majority 0.400.

| features | centroid | logreg |
|---|---|---|
| AFTER-only (the chart's own method) | **1.000** | **1.000** |
| IJ-concat + act | 0.933 | 1.000 |
| VJ-pair + act | 0.733 | 1.000 |

Destination is **saturated by the after-view**: rooms are
visually distinct, the chart already reads them at ceiling, and
the pair adds nothing — under a centroid it subtracts. (The
0.50 recalls inside VJ's 0.733 are the library/observatory twins,
the same pair THOR-TEST's stills separate cleanly.)

### Verbatim examples (logreg readouts, held-out test walks)

**The pair wins** — tid 46, walk 7: atrium, action *south*,
truth **same** (bump; the world answered "There is no doorway
south from here"). VJ-pair+act: **same** ✓. AFTER-only+act:
**move** ✗ — standing in the atrium, it concluded it had just
arrived there.

**The pair is wrong** — tid 59, walk 9: conservatory, action
*wait* (no action issued), truth **same**. VJ-pair+act:
**blocked** ✗ (AFTER-only+act: same ✓). In the one room with a
locked door, a no-op pair reads as the door event — the pair
model has over-learned what stillness in the conservatory
usually means in this corpus. Both examples are the corpus
telling the truth about itself: the door dominates its room.

## VERDICT

**Yes — there is transition signal in these representations,
strong enough to build on, and it lives exactly where the
after-view is blind.** A frozen V-JEPA pair embedding plus the
action plus a *linear* readout recovers what happened at 0.976
against 0.711 for the strongest after-only readout, and the
margin is earned in the *same* class (recall 0.94 vs 0.61) —
distinguishing "I stayed" from "I arrived," which no function of
the after-view can do in principle. Two disciplines on the
claim: *blocked* itself was cheap for every action-aware
readout (one door, one room — the pair was not needed there and
this report does not pretend otherwise), and the same features
under a nearest-centroid readout only reach 0.723 — the signal
is in the representation but not in its coarse cluster
geometry; a *fitted* readout (precisely what a night phase
fits) is what reads it.

**What this means for the liquid model.** THOR-TEST's System 2
learned *place* prototypes from the day's replay. This probe
says the same night machinery has a second subject available in
the same corpus shape — (frozen pair embedding, action, scorer
label) → a transition readout. The natural form: per
(place, action), an expected outcome class and an expected
after-prototype. That is the half of a world model that turns
the chart from a map into a *simulator the agent can consult
before it acts* — and its failures are the chart's surprises,
pre-registered: a door the model expects to refuse is no longer
a surprise when it does. Destination prediction should *not* be
part of it in this world; the chart's place recognition already
owns that at ceiling.

Costs, for whoever budgets the night: pair embeddings are the
expensive ingredient — ~7.5 s per transition on this rack versus
0.1–0.5 s per view. The cheap route exists and is respectable:
I-JEPA pair features (concat) reach 0.819, the one-number
cosine 0.855. A plausible night discipline is I-JEPA pairs
nightly, V-JEPA pairs for the transitions the cheap readout
found doubtful — doubt-priced recall, one level down.

**Limits.** One world, seven rooms, one locked door; test
n = 83 with the headline CI ±0.033; the walk-level split stops
direct leakage but the same rooms recur across walks by design —
this measures signal in the representations, not generalisation
to unseen worlds. The pair input is a hard cut between two
stills, not natural motion; V-JEPA's margin survives that, but
what it reads may be "cut-to-same-scene vs cut-to-new-scene plus
door geometry" rather than dynamics in any rich sense. The
transition classes are coarse (three). All of which bounds, and
does not overturn, the headline: the pair knows what happened;
the portrait alone does not.

## Files

`vjepa_probe/` on the Thor: `gen_corpus.py` · `corpus.json` ·
`views/` (324 PNGs) · `extract_features.py` · `ijepa.npy` ·
`vjepa.npy` · `readout.py` · `results.json` ·
`vjepa_extract.log`. This report: `~/lwm-thor/VJEPA-PROBE.md`.

