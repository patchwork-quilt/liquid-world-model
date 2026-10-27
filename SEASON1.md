# ESP32 Chess Box — Season 1

SuperInstance · 2026-10-26 · Oracle venue (enforceable-native sim, F = 20,
10:00 standard clock, per FORMAT.md v1). The three Season 0 lineages
continued: each builder studied the **total** Season 0 corpus (all nine
games, standings, receipts, the Underfill finding), then wrote a v2 crew
aimed at its parent and the field, under a season brief to deliberately
**fill the box** — Season 1 is the trial of Casey's Phase 2 prediction,
**Pruning**. Crews froze at delivery; every game below was run by the
season runner (`season1_run.py`, referee python-chess) and is recorded in
full — `games/<tag>/{match.pgn, receipts.json}`; the season aggregate is
`receipts.json` beside this file. Twelve official games, 1,013 plies,
**zero desyncs, zero illegal moves, zero flag falls, zero gate failures,
zero draws** — every game ended in checkmate.

## Process — how this season was made (kept in the body, per doctrine)

1. **Builders.** Three LLM builder efforts ran in parallel, one per
   lineage, each inheriting its parent's source and doctrine and each
   required to deliver a STUDY.md beside its crew: corpus lessons
   game-by-game, design rationale, and a **fill ledger** — everything
   added with its byte cost, everything left out with its reason,
   everything pruned with its reason. Those study notes are receipts
   and ship with the molts (`builds/<crew>/STUDY.md`).
2. **Freeze and transfer.** Crews froze at delivery. Sources were
   transferred to the Oracle with md5 verification (byte-identical)
   and built on the venue with each builder's declared command —
   local x86_64 builds were study benches only; nothing local is a
   record.
3. **Referee gates, applied before any official game.** The full
   Season 0 relay-legality suite (castling legal/through-check,
   en-passant legal/pinned, promotions Q/N/missing-suffix) was run
   against all three v2 builds on the Oracle: **ALL PASS ×3**. One
   scratch validation pairing (hoardbox2 vs pawnbox) was played to
   prove the runner end-to-end; it produced the season's one real
   scare, investigated in *Failures and incidents* below. Scratch
   games were then deleted from the venue (Season 0's hygiene rule):
   the season corpus is exactly the twelve games below.
4. **Fixture.** Round-robin among the v2 crews (2 games per pairing,
   colours swapped) mirroring Season 0, three control games (v2 White
   vs pawnbox, mirroring Season 0), and three **lineage duels** — each
   v2 against its own frozen v1 parent, parent as White. Run at ≤2
   games concurrent, nice'd, on the shared box.

## Standings (round-robin, v2 crews)

| Crew | W | D | L | Points | vs pawnbox (control) |
|---|---|---|---|---|---|
| **hoardbox2** (A — Materialist) | 3 | 0 | 1 | **3 / 4** | won by mate, 16 moves |
| **tickbox2** (C — Accountant) | 2 | 0 | 2 | **2 / 4** | won by mate, 31 moves |
| **sliver2** (B — Minimalist) | 1 | 0 | 3 | **1 / 4** | won by mate, 17 moves |

The Season 0 order holds — but compressed: 3.5 / 2.5 / **0** became
3 / 2 / **1**, and where Season 0's field produced mates at moves
14–26, Season 1's round-robin games ran 25–74 moves. The whole field
got harder to kill; the tail came up most.

## Lineage duels — the headline metric (v1 parent White vs v2)

| Duel | Result | Reading |
|---|---|---|
| hoardbox vs **hoardbox2** | **1–0 parent**, mate move 46 | The champion's line holds: v2's cargo did not beat the original on its first asking. Both spent ~350–364 sim-s; this was a chess loss, not a collapse. |
| sliver vs **sliver2** | **0–1 v2**, mate move 28 | The Minimalist's child wins as Black. The parent spent 3.7 sim-s all game (its Season 0 signature); the child spent 261.5 and mated it. |
| tickbox vs **tickbox2** | **0–1 v2**, mate move 69 | The season's longest war: both sides charged ~538 of 600 sim-s. The Accountant's child outlasted the parent at the parent's own game — the clock — and converted. |

**Lineage delta: two of three children beat their parents; the
champion's did not.** Cross-season control gauge (same opponent, same
colour as Season 0): hoardbox's mate of pawnbox quickened 21 → 16
moves; tickbox's lengthened 15 → 31 (a datum, plainly: a longer kill
of the weakest opponent, against round-robin and duel results that
both improved); sliver's control flipped from *lost in 51* to *won
in 17* — the single largest lineage swing of the season.

## The crews — what each one carried, and what it cost

- **hoardbox2 (A)** — parent eval kept; **opening book added** (344
  position-keyed entries, 5,504 B compiled, built only from the corpus
  + 24 authored lines; 59 corpus proposals dropped in conflicts —
  authored lines govern); **TT doubled** 8,192 → 16,384 entries
  (131 → 262 KB); **SEE added** (a Season 0 refusal, reversed on
  corpus evidence); endgame knowledge added (KBN-K corner drive,
  KPK square rule, wrong-bishop draw rule); **repetition contempt
  −45 cp** fitted as the direct rr-ac2 fix. Source 38,160 B
  (+ generated book header 20,991 B) · binary 72,568 B · peak
  anonymous RAM **436 KB (83.8% of cap)** · declared manifest 7,244 B.
- **tickbox2 (C)** — the conversion fix, three mechanisms: repetition
  contempt −70 cp (root-relative), a **progress clock** (≥16 plies
  without pawn move or capture raises criticality ×1.35 and bonuses
  root pawn moves), and a book anti-drift guard; **opening book**
  (12 lines, 444 B manifest, from the corpus + authored — its
  rr-ac2 attacking line is booked to move 20, exactly where the
  parent's drift began); **pawn-structure eval** (a Season 0
  refusal, now carried); TT doubled to 16,384 entries (256 KB BSS);
  the parent's 3.0 host-s reserve discipline untouched. Source
  29,551 B · binary 72,960 B · peak anonymous **436 KB (83.8%)** ·
  declared manifest 444 B.
- **sliver2 (B)** — doctrine held under explicit pressure to fill:
  **manifest 0 B** (book refused again, re-argued against the
  Season 0 evidence in its ledger). What it bought instead, per
  byte: iterative deepening under a self-managed wall-clock budget
  (22 host-s lifetime, 8 host-s reserve — its parent spent 15 sim-s
  in *four games*; the child spent 1,880 sim-s in six), move
  ordering (TT-move, MVV-LVA, killers), repetition awareness, a
  deliberately **half-size TT** (4,096 entries, 64 KiB — half its
  rivals'), quiescence that sees quiet promotions, 1-ply check
  extension. Effective depth: fixed 3 → 7 in the opening, 5–6 in
  the middlegame. Source 14,906 B · binary 71,984 B · peak anonymous
  **232 KB (44.6%)** · Zobrist increment verified against full
  recompute over 103,717 random plies, 0 mismatches.

## The fill census (FORMAT §7 receipts, Season 0 → Season 1)

| Measure | Season 0 | Season 1 | Cap |
|---|---|---|---|
| Mean crew binary | 72,101 B (1.72%) | 72,504 B (1.73%) | 4,194,304 B |
| Carried manifest — books/tables | **0 B** (all crews) | **5,504 / 444 / 0 B** (A/C/B) | — |
| Declared manifest incl. eval tables | — | 7,244 / 444 / 0 B | — |
| Mean crew peak anonymous RAM | 244 KB (46.9%) | **368 KB (70.8%)** | 520 KB |
| Largest crew peak anonymous RAM | 308 KB (59.2%) | **436 KB (83.8%)** | 520 KB |
| Cap violations in official play | 0 | 0 | — |
| Documented prunes / cap-forced cuts | 0 | **8** (register in receipts.json) | — |

## The Pruning verdict — Phase 2 on trial

**The prediction's mechanism is confirmed; its location was one axis
over.** Casey predicted: builders try to fill the box, and the craft
becomes what to leave out. That behaviour arrived in full — two of
three crews carried books for the first time, all three grew their
tables, and the season's ledgers record **eight deliberate cuts**,
two of them forced by the cap's arithmetic itself:

- hoardbox2's first TT design (24,576 entries, 393,216 B) **measured
  560 KiB peak anonymous on the builder's own bench — over the
  520 KiB cap** — and was cut to 16,384 entries before the crew ever
  froze. The prune is the builder's first ledger entry, with the
  lesson attached: stack/heap overhead above BSS counts.
- tickbox2 killed two TT designs on projection (512 KB outright;
  a packed 384 KB design projecting ~576 KB measured) and refused a
  wider book on evidence: *"fill ≠ bulk — 9 games honestly support
  12 lines."*
- sliver2's one added-then-pruned item (CPU-time budgeting, replaced
  by wall-clock after contention showed a ~23% gap) and its renewed,
  argued book refusal are the same craft in minimalist dress.

But the **flash** dimension — the cargo hold in the original image —
is still 98.3% empty, and the receipts say why. Honest cargo from a
nine-game corpus saturates at hundreds of entries; authored lines
are bounded by builder effort (24 and 12 lines); the format forbids
fetched data, so megabyte-scale cargo could only come from build-time
self-generation (computed endgame tables, self-play-grown books) —
and no builder spent its budget there, because at this strength
frontier a byte of transposition table in RAM is still worth more
than a byte of carried data in flash. The fill went where the value
is: **the pressure, the negotiation, and every forced cut happened
on the RAM axis** (crew peaks: 46.9% → 70.8% mean, the two knowledge
crews at 83.8%), at **build time**, not at the gate — official play
saw zero violations and zero forced prunes, because the pruning had
already been done at the workbench. Phase 2 is real; it is a
workbench phase before it is a gate phase, and in this hull its
scarce currency is RAM, not flash.

**Falsifiable expectations filed for Season 2** (Craft's signature,
if the arc holds): (1) at least one crew carries a manifest ≥ 42 KB
(1% of flash) — real cargo, most plausibly self-generated; (2) crew
peak RAM sits in the 85–95% band with strength still rising and no
breach; (3) the Minimalist's strength-per-byte lead narrows as the
knowledge crews learn its economy — or widens, and doctrine beats
cargo outright.

## Game-by-game (termination notes)

| Game | Result | How it closed | Charged (sim-s, W/B) |
|---|---|---|---|
| rr2-ab1 (hoardbox2 W) | 1–0 | mate, move 74 — longest RR game | 462.3 / 433.5 |
| rr2-ab2 (sliver2 W) | 0–1 | mate by hoardbox2, move 51 | 403.7 / 407.9 |
| rr2-ac1 (hoardbox2 W) | 1–0 | mate, move 40 | 286.9 / 449.1 |
| rr2-ac2 (tickbox2 W) | 1–0 | mate, move 62 — **the champion beaten** | 529.1 / 441.3 |
| rr2-bc1 (sliver2 W) | 0–1 | mate by tickbox2, move 51 | 407.2 / 496.2 |
| rr2-bc2 (tickbox2 W) | 0–1 | mate by sliver2, move 25 — its first RR win | 310.4 / 220.5 |
| ctrl2-hoardbox | 1–0 | mate by hoardbox2, move 16 | 86.9 / 8.3 |
| ctrl2-tickbox | 1–0 | mate by tickbox2, move 31 | 339.0 / 8.7 |
| ctrl2-sliver | 1–0 | mate by sliver2, move 17 | 153.8 / 5.7 |
| lin-hoardbox (v1 W) | 1–0 | mate by hoardbox (S0), move 46 | 363.9 / 345.7 |
| lin-sliver (v1 W) | 0–1 | mate by sliver2, move 28 | 3.7 / 261.5 |
| lin-tickbox (v1 W) | 0–1 | mate by tickbox2, move 69 | 537.9 / 537.7 |

## The most interesting game — rr2-ac2, tickbox2 (W) vs hoardbox2 (B), 1–0

Season 0's defining failure was this fixture's mirror: tickbox
attacked the champion, was offered a repetition, and shuffled to a
draw having spent the season's largest clock. Season 1's return
fixture is the indictment answered in the same pairing, one
generation on: tickbox2 — carrying contempt, a progress clock, and
its parent's attacking line booked to the exact move where the drift
began — beat the champion outright, by mate, in 62 moves, spending
529.1 sim-s (the season's largest winning spend) and this time
converting every second of it. Whatever else Season 1 measured, the
night-study loop demonstrably works: a named failure, studied from a
total corpus, produced a mechanism, and the mechanism changed the
result against the same opponent.

## Failures and incidents — unlaundered

- **The 2,464 KB reading (measurement incident, hoardbox2).** The
  first scratch validation game on the Oracle recorded hoardbox2 at
  **2,464 KB peak anonymous — a RAM gate FAIL** — against a builder
  bench figure of 428 KiB. Investigated before any official game:
  identical pairing re-run under the runner → 432 KB; a full replay
  of the same PGN sampled every 20 ms → peak 432 KB, stack flat at
  132 KB, heap zero (the engine performs no dynamic allocation; its
  TT is a static array); two further repetitions → 428 / 428 KB;
  all twelve official games → 420–436 KB. Seventeen subsequent
  measurements, none above 448 KB. Ruled an unreproduced one-off,
  recorded here rather than buried; the crew was cleared on the
  balance of measurements. The standing caveat cuts both ways: had
  it recurred even once, the crew would have been sent back.
- **Both local dress rehearsals reversed on the venue.** hoardbox2
  mated its parent on the builder's bench (48 moves) and lost the
  official duel; tickbox2 lost to its parent locally (mate, move
  29) and won the official duel. n = 1 each way, with time-managed
  search differing across benches and box load — the season's rule,
  now twice-bought: local rehearsals are study evidence, never
  records; only runner games on the venue count.
- **sliver lane /tmp collision.** Builder B's early harness shared
  `/tmp` with another lane and a foreign output briefly entered its
  logs; the builder caught it, discarded the contaminated runs, and
  re-ran everything from a private harness — only re-runs are cited
  in its STUDY.md. No official artefact was touched: season games
  ran under the season runner only.
- **Builder-phase catches (the gates earning their keep).**
  tickbox2's book harness caught three real defects pre-freeze (two
  prefix-collision dead lines, one illegal authored move); its first
  contempt draft had a negamax sign inversion that *rewarded*
  repetition — caught by its own conversion test, fixed, and
  ledgered. hoardbox2's generator/engine key agreement was proven
  by 446/446 corpus plies relayed `ok` before the season.
- **The standing caveat (FORMAT §12):** every time figure here is
  host wall time × F = 20 — box-time is a modelled currency, and
  these are box-records, honestly labelled, not silicon records.

## What the season teaches

Knowledge > time craft > minimalism still orders the podium, but
Season 1's margins tell the real story: the champion's heir lost
twice (once to its improved rival, once to its own parent), the
Accountant converted the exact failure its parent was indicted for,
and the Minimalist — carrying literally nothing — climbed from 0/4
and a lost control to a winning control, a round-robin win, and a
duel won as Black, on 14,906 bytes of source and 44.6% of the RAM
cap. The format's headline metric now has its second point on the
curve: improvement is real, attributable, and differently priced
per doctrine — hoardbox2 bought its step with 7,244 B of manifest
and 83.8% of RAM; sliver2 bought a larger step with 0 B of manifest
and time it already owned. And the box? Still 98.3% empty in flash,
now honestly negotiated in RAM. Phase 2 arrived at the workbench.
Season 2's builders inherit a 21-game corpus, two dethroned parents,
one defended crown, and a filed set of Craft expectations to be
judged against.

## Artefacts

- Crew sources (the molts) + study notes + book generators:
  `builds/hoardbox2/`, `builds/tickbox2/`, `builds/sliver2/`.
- Games: `games/<tag>/{match.pgn, receipts.json}` (full per-ply
  charge tables in each receipts.json).
- Season aggregate: `receipts.json` (this dir) — standings, census,
  prune register, incident log.
- Runner: `season1_run.py`; fixture driver: `run_fixture.sh`;
  relay probe: `replay_probe.py` (this dir; venue copies on the
  Oracle under `~/esp32-chess-box/season1/`).
