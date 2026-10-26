# THOR-TEST — a liquid world model with real perception (I-JEPA on the Thor)

SuperInstance — liquid-world-model. Code, `results.json`, and this
report live in `~/lwm-thor/` on the Thor. Seed 7 throughout.

## Rack verification (before anything ran)

- `GET /health` → `{"ok": true, "device": "cuda", "loaded":
  {"ijepa": true, "vjepa2": false, "judge": true}}`.
- `GET /cards` → I-JEPA card present: `ijepa-vith14`,
  `POST /embed/image`, 1280-dim; measured cost at run time
  "87.9 ms mean over 5444 calls".
- Fetch log: both weight files `model.safetensors: OK` (sha256)
  and `FETCH8-DONE` — the gap recorded on 2026-10-23 is closed;
  the endpoint serves.
- One real embed call on a synthetic test PNG returned a 1280-dim
  embedding (~0.1 s end-to-end). In the experiment the rack's own
  per-call latency averaged **94.4 ms** over 18 calls.
- V-JEPA 2 was **not** used (not loaded; not needed). I-JEPA alone
  is the slice, as briefed. The rack was not restarted or
  reconfigured — it is a shared service and was only ever a client
  relationship away.

## Headline

**Yes — System 2's night upgrades measurably improved System 1's
autoplay.** Recognition accuracy 0.80 → 1.00, place merges 1 → 0,
framework surprises 6 → 0, steps-to-goal 9 → 3, held on day 3.
The improvement is attributable to the model, not the script:
S1's machinery (chart + ScriptPolicy) was byte-identical across
all three days; only the perception prototypes and threshold
changed, at night, from the labelled replay corpus.

Read the attribution notes below before quoting the step count —
part of the 9 → 3 is the chart persisting (the framework's
essence), which is S1 remembering, not S2 upgrading. The cleanly
S2-attributable gains are the recognition accuracy and the
resolved twin merge.

## The setup

- **World** (`visual_world.py`): 7 rooms on a grid — a loop
  (atrium, gallery, observatory, library) with branches (cellar,
  conservatory, vault). The observation is a rendered image only:
  a 448×448 contact sheet of the room's four walls (patterned
  surfaces, furniture, pillars, motif; doorways as dark openings).
  Library and observatory are deliberate near-twins (same
  blue-grey panels, same diamond motif). Ground truth stays
  scorer-side (`truth()`, `visit_log`); the render carries no
  text and no identity cue beyond visible decor. Per-observation
  viewpoint jitter (roll ±3 px, brightness ±5%) keeps the same
  room from being pixel-identical twice.
- **Perception** (`perception.py`): each image → I-JEPA embedding
  via the rack → nearest-prototype cosine match against the
  chart's place prototypes. Exits are doorways *detected* in the
  image quadrants (destinations never visible: `through` is
  always None). A gold-mass detector reports the vault's
  treasure. **Trust is the match margin**: near-ties report 0.3
  (below the framework's trust floor — the chart softens instead
  of rewriting); first sights 0.8; clear matches 1.0.
- **tau calibration (pre-flight probe, stated openly):** I-JEPA
  embeddings of synthetic scenes are anisotropic — flat-colour
  rooms measured cross-room cosine 0.955–0.996 (everything one
  place). After the renderer gained surface patterns and
  furniture: within-room ≥ 0.994, most cross-room ≤ 0.967, the
  twin pair at 0.991. tau0 = 0.97 sits in that gap: a naive
  default that gets most rooms right and the twins wrong.
- **System 1** (`script_policy.py`): the framework's
  ExplorerPolicy plus one discipline — once the chart supports a
  believed route to the goal place, follow the script; when
  perception breaks it, resume exploring. Frozen across days.
- **System 2** (`system2.py`): at night the scorer reveals the
  cumulative (embedding, true room) corpus — studying the replay.
  S2 (a) re-derives each place's prototype from its *clean*
  sightings only (dominant room; contamination counted and
  excluded), (b) seeds a prototype for any true room no place
  claims, (c) re-chooses tau by grid search (0.40–0.95) for
  corpus assignment accuracy. The change is recorded in full.

## Results

| day | tau | steps | surprises | goal | recog. acc. | merges | splits | rooms visited | chart places |
|-----|-----|-------|-----------|------|-------------|--------|--------|---------------|--------------|
| 1   | 0.97 | 9  | 6 | yes | 0.80 | 1 | 0 | 6/7 | 5 |
| 2   | 0.95 | 3  | 0 | yes | 1.00 | 0 | 0 | 4/7 | 5 |
| 3   | 0.95 | 3  | 0 | yes | 1.00 | 0 | 0 | 4/7 | 5 |

**Day 1.** Exploration formed 5 places for 6 rooms: `place-2`
absorbed the twins — library ×3, observatory ×2 (purity 0.60).
The framework felt the confusion from inside: 6 surprises, as the
merged place's exit beliefs kept contradicting what the agent
found (the twins have different exits). The vault was still
reached in 9 steps — a confused model is not a paralysed one.

**Night 1** (corpus 10). place-2 purified to library (3 clean
sightings; 2 observatory sightings named as contamination and
excluded); `place-6` seeded for observatory from its corpus mean;
tau 0.97 → 0.95. Corpus assignment accuracy 0.80 → 1.00 — and
note the direction: accuracy rose while the gate *loosened*,
because the prototypes did the separating.

**Day 2.** The script ran the charted route (atrium → library →
conservatory → vault): 3 steps, 0 surprises, every perception
correct. One observation on the route reported low trust
(margin doubt) — the doubt mechanism engaging even on a clean
day; the chart softened and nothing broke.

**Night 2** (corpus 14). tau held at 0.95, corpus accuracy
1.00 → 1.00, prototypes re-purified. One wart, below.

**Day 3.** Identical receipts to day 2. The gains held.

## Attribution, stated carefully

- **Steps 9 → 3 is not purely S2.** Day 2 starts with day 1's
  chart (essence persists — that is the framework working as
  designed) and S1's script priority exploits it. Any honest
  day-over-day comparison in this framework has that term in it.
- **Recognition accuracy 0.80 → 1.00 and merges 1 → 0 are S2's.**
  The only thing that changed between day 1 and day 2 on the
  perception side is the night upgrade.
- **The twin separation is corpus-proven, not live-proven.**
  After night 1 the model's route never re-entered observatory,
  so no live observation ever tested place-6. The corpus says the
  upgraded prototypes assign all 14 sightings correctly; the
  world was not asked again. A route forced through observatory
  on day 3 is the obvious follow-up experiment.
- **Corpus accuracy is in-sample.** S2 tunes on the corpus it is
  scored on. The live day metrics are the out-of-sample evidence,
  and they agree — on the rooms the route visited.
- **Within-room perception was easy.** Jitter is small
  (same-room cosine ≥ 0.994); the difficulty in this world lives
  between rooms (anisotropy + the twins), not within them.

## Warts found (measured, not hidden)

1. **Night 2 added a duplicate observatory prototype
   (`place-7`).** "Covered rooms" is computed from *sightings*;
   place-6, seeded on night 1 but never since perceived, is
   invisible to that computation, so night 2 seeded observatory
   again. No behavioural effect in this run (the route never went
   there), but two identical prototypes would make any future
   observatory visit a margin-0, low-trust match. Fix direction:
   coverage must count labelled-but-unvisited prototypes.
2. **The chart never gains observatory as an observed place**
   (chart places stay 5): a seeded prototype is recognition
   without knowledge — exits and contents for place-6 remain
   uncharted until a visit. That is arguably correct behaviour
   (recognition precedes knowledge), but it means S2's gift is
   only half-spendable until S1 chooses to go and look.

## Footprint

Whole experiment: **2.33 s** wall on the Thor (days of 1.27 /
0.51 / 0.51 s), 18 rack embed calls at ~94 ms mean, harness peak
RSS 53 MB, no model held in the harness process. The rack's GPU
cost is the rack's own, metered per call. The experiment was a
good citizen: it never loaded, restarted, or reconfigured the
shared service.

## Files

`visual_world.py` · `perception.py` · `script_policy.py` ·
`system2.py` · `run_experiment.py` · `probe.py` (the pre-flight
similarity probe) · `smoke.py` · `results.json` · the `lwm`
package (copied from the framework repo, unmodified).
