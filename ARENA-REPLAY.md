# Arena Replay — a sharper signature in the same field

**SuperInstance · 2026-10-27 · the Orin (Jetson Orin Nano Super) · Lane 4 of the build round**

## Headline

- **The merge is dead.** Zero merges in the replay (round 1: one
  three-way). Warehouse, boathouse and quay are pairwise distinct at
  every standpoint the protocol reached — the warehouse by its
  shelves, the boathouse by its logs, the quay from both by the
  ground underfoot.
- **The trap is gone with it.** Goals **3 of 3 days** (round 1: 1 of
  3); steps **13 / 11 / 4** by day against round 1's 15 / 120 / 120 —
  28 steps total against 255; surprises **1 per day, 3 total**,
  against 23 / 330 / 322. Day 3 is a four-step commute: reset,
  warehouse for the key, quay, market, lighthouse. The chart had
  become a map.
- **The split survived in a new costume — twice over.** The quay
  reads three signatures, exactly the predicted too-fine chart of one
  open apron. The **warehouse also split**, which the pre-registration
  said would falsify the hand-derivation — and it does, narrowly:
  the derivation missed one chest sitting exactly on the horizon's
  corner, and a 2–2 tie handed the east-door standpoint to `+chest`
  instead of `+shelves`. Both warehouse signatures are subsets of the
  warehouse (same ground, same base, different suffix); it cost the
  explorer nothing measurable — no extra steps, no extra surprises —
  but it is a split the design did not predict, reported as such
  below.
- **Everything else was held identical**: same arena build (the
  engine's boot self-check read back the round-1 cells), same seed,
  same framework and policy, same 3-day / 120-step protocol, run
  through the bridge alone. Only the signature function changed —
  the diff is the whole intervention (`signature-diff.patch`).
- **Cost**: 21.4 s of play; the field stands at ~57 MB RSS combined
  (engine 37 MB + bridge 20 MB), inside its established class, and
  was left **up and healthy** (receipts at the end).


## The failure being attacked (round 1, filed as ENGINE-ON-ORIN)

The unmodified liquid framework played three days in the standing
Luanti harbour on the Orin. Day 1 was a clean sweep (treasure in 15
steps, 23 surprises). Days 2–3 it never came home: 120 steps (the cap)
each, 330 and 322 surprises, goal unreached. The scorer's receipts
name the cause exactly — one **three-way merge**: warehouse, quay and
boathouse all read as the single signature `brick·stone·timber`, so
the chart held them as one place with unioned exits and the explorer
ping-ponged inside a place that does not exist. One **split** is also
on record: the quay reads two signatures (`brick·stone·timber` at its
door standpoints, `brick·timber·water` at the start cell).

## Why the round-1 signature merges them (read from the mod)

The round-1 signature is a *presence set*: node kinds counted in a
radius-6 window over three heights (floor + two wall layers), kinds
kept at count ≥ 3, and — the decisive line — **capped at the four
most-present kinds**. A presence set with a frequency cap keeps
exactly what the three places *share* (their structural materials:
brick, stone, timber, all abundant in every standpoint window) and
discards exactly what they *don't* share (their furnishings, present
in single digits). The distinguishing facts exist in the world; the
reduction throws them away:

- **warehouse** is furnished with bookshelves (5 cells) and two
  chests — but its door standpoints sit 7–9 cells from the shelves,
  outside the radius-6 window entirely, and its chests fall under
  the count threshold or out of window at both doors.
- **boathouse** is furnished with log piles (7 cells of `default:tree`)
  and a chest — from its only door standpoint just one log cell falls
  inside radius 6, under the threshold.
- **quay** is the open stonebrick apron between them: same window
  contents (the neighbours' timber floors and walls, its own brick
  floor, platform stone) minus everything that would name it.

## The sharpened signature (v2) — the choice, stated before the run

Perception side only. The framework, the ExplorerPolicy, the arena
layout, contents, gate, key and treasure are untouched. The base term
is the round-1 computation, verbatim. Two standpoint-local sensed
terms are added — both computed from nodes the walker could in
principle sense, neither a region name nor a coordinate:

1. **Ground term** — the kind of the floor cell *directly under the
   standpoint* (y = 0). The most local fact a standpoint has; it
   cannot alias across a wall. It is what separates the quay
   (stonebrick underfoot at every standpoint) from the two timber
   floors behind the doors on either side of it — the two quay /
   boathouse door standpoints are two cells apart across the
   door line, and the ground underfoot is the one sensed fact that
   differs categorically between them.
2. **Landmark term** — the dominant *floor-standing furnishing*
   kind within a wider **radius-10** horizon, sampled at **y = 1
   only**, requiring count ≥ 2, ties broken alphabetically.
   Furnishing kinds: shelves, logs, chest, glass, gold, torch, wool.
   The reasoning for the shape of this probe: what a place is
   *furnished with* stands on its floor (bookshelves, log piles,
   chests all sit at y = 1), while structure at height — windows,
   the bell, awnings — is architecture, already carried by the base
   term's all-heights near-field count. The wider horizon exists
   because the warehouse's shelves are 7–9 cells from its doors:
   a landmark is precisely the furnishing you can pick out across
   the room. The count floor of 2 keeps a single glimpsed cell from
   naming a place.

Format: `<ground>|<base>[+<landmark>]` — e.g. the warehouse should
read `timber|brick·stone·timber+shelves`. The string stays an opaque
key to the framework; the archway previews use the same function at
the far standpoint, so a preview and an arrival can never disagree
about what a place is called.

**Hand-derived prediction, all eleven standpoints** (counted from
the mod's build tables; the method was validated against the live
field before the run — the round-1 archway previews at the start
cell matched the hand-derived bases for warehouse (17,13),
boathouse (14,21) and market (45,13) exactly):

| standpoint | region | v2 signature (predicted) |
|---|---|---|
| (17,13) | warehouse | `timber|brick·stone·timber+shelves` (shelves 4 in horizon) |
| (19,8) | warehouse | `timber|brick·stone·timber+shelves` (shelves 2 — same winner) |
| (14,21) | boathouse | `timber|brick·stone·timber+logs` (logs 7) |
| (17,16) | quay | `brick|brick·stone·timber+logs` (logs 3 glimpsed) |
| (16,21) | quay | `brick|brick·stone·timber+logs` (logs 5 — ground term, not the glimpse, keeps it out of the boathouse) |
| (45,16) | quay | `brick|brick·stone·timber+chest` (stall chests 2) |
| (24,24) start | quay | `brick|brick·timber·water+chest` (quay chests 3; base as round 1) |
| (22,8) | chapel | `stone|brick·glass·stone·timber` (no landmark ≥ 2 — unchanged but for the ground prefix) |
| (45,13) | market | `stone|brick·stone·timber·wool+chest` |
| (51,8) | market | `stone|stone·timber·wool+chest` (base loses brick — see latent split, below) |
| (54,8) | lighthouse | `stone|stone·timber·wool+wool` (tower's ground ring) |

Predicted consequences, owned in advance:

- **The merge dies**: warehouse, boathouse and quay are pairwise
  distinct at every standpoint — warehouse/boathouse by landmark
  (shelves vs logs over identical ground and base), quay/either by
  the ground term.
- **The quay split survives in a new costume** — predicted, not
  excused: the quay is one open apron spanning two perceptual
  neighbourhoods (log piles west, market chests east, the start
  cell's own base differing again). It should read 2–3 signatures,
  all subsets of the quay. A split is a too-fine chart, not a false
  one — round 1's day 1 routed fine with one — and no standpoint-
  local signature honestly removes it. If the run shows the quay
  unified, this prediction was wrong and that is a result too.
- **A latent market split exists at (51,8)** (arriving from the
  lighthouse): its radius-6 base never reaches the quay's brick.
  The protocol should never occupy that standpoint — reaching the
  lighthouse ends the day — so it is predicted *unexercised*; the
  step log will prove whether it stayed latent.

## Pre-registered expectations (written before the run)

Against round 1's receipts — days (15 steps, goal, 23 surprises),
(120, no goal, 330), (120, no goal, 322); merges: one three-way;
splits: quay ×2; 5 signatures, 5 chart places, 255 total steps:

1. **Merges: zero.** No signature covers more than one true region.
2. **Goals: 3 of 3 days** (round 1: 1 of 3).
3. **Day 2 and day 3 steps: ≤ 60 each** (round 1: 120, the cap) —
   with the chart now holding the true graph, both days should look
   like commutes, not searches.
4. **Day 2 and day 3 surprises: ≤ 80 each** (round 1: 330 / 322).
   The floor is not zero: contents churn is signature-independent
   (the key leaves the warehouse when taken; the market's crates
   alternate by day parity) and day 1 itself paid 23 with a working
   route. Residual surprises should be contents-class, not
   identity churn.
5. **Splits: the quay only, 2–3 signatures** (see above). Any other
   region splitting — or the market's latent standpoint going live —
   falsifies the hand-derivation and gets reported as such.
6. Day 1 is *not* predicted identical to round 1's: the chart keys
   change, so its learning path may differ in detail; it is
   predicted to reach the goal in ≤ 40 steps.

## Results — scored against the pre-registration

| # | expectation (registered above) | landed | verdict |
|---|---|---|---|
| 1 | merges: **zero** | merges `{}` — no signature covers two regions | **PASS** |
| 2 | goals **3/3** | 3/3 (13, 11, 4 steps) | **PASS** |
| 3 | day 2/3 steps ≤ 60 | 11 / 4 | **PASS** (5× inside the bound) |
| 4 | day 2/3 surprises ≤ 80 | 1 / 1 | **PASS** (two orders under round 1) |
| 5 | splits: quay only, 2–3 sigs | quay ×3 **and warehouse ×2** | **MISS** — see below |
| 6 | day 1 goal in ≤ 40 steps | 13 steps, 1 surprise (round 1: 15 steps, 23 surprises) | **PASS** |

Day 1's surprise count deserves its own line: 23 → 1 was *not*
predicted in magnitude. With the previews and the arrivals computed
by the same sharpened function at the same standpoints, a preview
can no longer promise a place the arrival contradicts; the residual
one surprise per day is contents-class (the key leaving the
warehouse, the market's day-parity crates — both named in advance as
the floor), not identity churn.

**The warehouse split — the miss, with its mechanism.** The east
door standpoint (19,8) read `timber|brick·stone·timber+chest`, not
the predicted `+shelves`. Recounting that window from the receipts:
the boathouse's chest at (12,1,18) sits *exactly* on the horizon's
corner from (19,8) — dx −7, dz +10 — inside the radius-10 probe. The
derivation had written it off as out of range. Chest therefore
totals 2 (that chest + the warehouse's own at (18,1,5)), tying the
shelves' 2 (only x = 9, 10 of the five shelf cells fall in the
window), and the alphabetical tie-break hands the suffix to `chest`.
The same missed cell gives the chapel — whose only standpoint is
the other end of the same doorway — an unpredicted `+chest` suffix
(its base is unique, so no split follows there). One miscounted
boundary cell, two prediction errors, both confined to the landmark
suffix; the ground and base terms — the terms that killed the
merge — matched the derivation at all eleven standpoints. The
named follow-up, if a third round is ever wanted: count the
landmark over the region-side half-horizon, or weight by inverse
distance, so a furnishing glimpsed at the very edge of perception
cannot outvote the room's own shelves at a tie. It is a refinement
of a working sense, not a repair of a broken one: the split it
caused is a too-fine chart in one room, and the run's explorer
walked through it without noticing.

**Also as predicted**: the market's latent standpoint (51,8) was
never occupied — every lighthouse entry in the step log is a
day-ending arrival at (54,8) — so that split stayed latent, proven
by the log rather than asserted.

## PROCESS — as it happens

- **Recon (before any edit).** Read the filed ENGINE-ON-ORIN, the
  mod (535 lines), the bridge and the play harness end-to-end. The
  replay protocol is the harness's own: 3 days, 120-step cap,
  `LiquidModel(seed=7)` + ExplorerPolicy unmodified, chart persisting
  across days, world reset per day, truth scorer-side via `/truth`,
  merges/splits scored from the full per-step signature/truth log.
- **Field check.** `run_field.sh status`: 1 engine, 1 bridge,
  `/health` ok. Deployed mod md5 `25bba644…` — byte-identical to
  the filed `src/` copy. A live `/observe` at the start cell matched
  the round-1 record (quay reading `brick·timber·water`, the merged
  `brick·stone·timber` in both archway previews north and west).
- **Design.** (Above — written before the mod was edited. The two
  candidate one-line fixes were rejected on the arithmetic, not on
  taste: lowering the presence threshold to ≥ 1 leaves the warehouse
  reading plain from both its doors — its shelves are outside the
  radius-6 *window*, not merely under the count — and raising the
  window alone hands the win to the frequency cap, which cuts the
  rare landmark kinds first: at radius 10 the boathouse's window
  fills with water and its 7 log cells lose the top-4 cut. The
  sharpening had to change what the reduction *keeps*, not just
  what the window *sees*.)
- **Pre-run validation, live.** The v2 mod was deployed (md5
  `67999e6b…`, byte-identical to the edited copy; the deployed
  round-1 file backed up on the box as `init.lua.bak-r1`, round 1's
  on-box play results as `play_results_round1.json`) and the field
  restarted clean: one engine, one bridge, boot self-check reading
  back the round-1 arena cells (quay floor, gold bell, water, door
  gap, warehouse wall, market floor — the build is the same build;
  only `signature_at` changed). The first `/observe` from the start
  cell confirmed four predicted signatures before a single play
  step: the start quay `brick|brick·timber·water+chest`, and in the
  archway previews the warehouse `timber|brick·stone·timber+shelves`,
  the boathouse `timber|brick·stone·timber+logs`, the market
  `stone|brick·stone·timber·wool+chest`. The smoke test then passed
  all its verbs under v2 (lock refusal, key, gate, treasure) and
  confirmed a fifth standpoint: the lighthouse
  `stone|stone·timber·wool+wool`.
- **The run.** The harness, unmodified, on the Orin: 3 days in
  21.4 s of wall clock. One launch artefact of my own, owned: the
  first status check read "bridges: 2" — `pgrep -cf` matching my
  own probe shell's command line, the same self-match trap round 1
  receipted. Process-level proof: exactly one bridge (pid 2223134,
  sole listener on :8797) and one engine (pid 2223133).
- **GPU receipt** (tegrastats, harness-captured, 20 samples over
  the short run): GR3D mean 0.0%, peak 0% — the replay was too
  brief and too light to wake it; reported as measured. Box RAM
  5,028/7,485 MB used at the final check, the desktop's own share
  included; the field's combined RSS ≈ 57 MB (engine 37,152 KB,
  bridge 19,864 KB).
- **Field left standing**: `run_field.sh status` — 1 engine,
  1 bridge, `/health` ok, final `/observe` answering from the
  lighthouse at the end of day 3 (treasure in contents, brass key
  in hand). The next player resets it with one call.

## Flag for the referee (registered claims)

The farm registration merged last night describes the arena's
`observe()` as returning "a perceptual digest (place signature,
exits with archway previews, contents, holding)" and quotes round
1's merge as the first league result. Neither claim becomes false:
the digest is still perceptual (no region name or coordinate
crosses), and round 1's result stands as history — this replay is
its second season, not a correction of its record. The one
format-visible change is the signature string itself
(`<ground>|<base>[+<landmark>]`), which every consumer treats as an
opaque key; no registered text quotes a round-1 signature verbatim.
Flagged here per instructions rather than edited.

## Files

- `ARENA-REPLAY.md` — this report.
- `replay-results.json` — the harness's full output: per-day stats,
  merges/splits as scored by the harness, and the complete 31-entry
  per-step signature/truth log.
- `signature-diff.patch` — the whole intervention: round-1
  `init.lua` → v2, perception block only.
- `init_v2.lua` — the deployed mod, byte-identical to the file now
  running on the Orin (md5 `67999e6b…`).
- On the Orin: the field at `~/engine-arena/` (backups
  `init.lua.bak-r1`, `play_results_round1.json` beside the live
  files); the replay's on-box log at `~/engine-arena/play/replay_v2.log`.
