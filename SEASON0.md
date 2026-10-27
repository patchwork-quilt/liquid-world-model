# ESP32 Chess Box — Season 0

SuperInstance · 2026-10-26 · Oracle venue (enforceable-native sim, F = 20,
10:00 standard clock, per FORMAT.md v1). Three builder agents each wrote
one crew from a different doctrine; crews were frozen before the first
gate game; every game below was run by the season runner
(`season_run.py`, referee python-chess) and is recorded in full —
`games/<tag>/match.pgn`, `receipts.json`, `runner.log`; the season
aggregate is `receipts.json` beside this file. Nine official games,
446 plies, **zero desyncs, zero illegal moves, zero flag falls, zero
gate failures**.

## Standings (round-robin, 2 games per pairing, colours swapped)

| Crew | W | D | L | Points | vs pawnbox (control) |
|---|---|---|---|---|---|
| **hoardbox** (A — Materialist) | 3 | 1 | 0 | **3.5 / 4** | won by mate, 21 moves |
| **tickbox** (C — Accountant) | 2 | 1 | 1 | **2.5 / 4** | won by mate, 15 moves |
| **sliver** (B — Minimalist) | 0 | 0 | 4 | **0 / 4** | lost by mate, 51 moves |

Every decisive game ended in checkmate; the only draw was fivefold
repetition. pawnbox, the proof baseline, played only the three control
games (one per crew, crew as White) and is not in the standings.

## The crews — doctrine, and how much of the hull each actually used

- **hoardbox (A, "the Materialist")** — *evaluation is king.* Full
  tapered piece-square tables, PeSTO-class values, pawn structure,
  mobility, king safety, bishop pair, outposts; the search serving it
  (iterative-deepening alpha-beta, 8192-entry transposition table,
  null-move pruning, LMR) is deliberately disciplined rather than
  deep. Refused: opening book, tablebases, SEE.
  Source 29,061 B · binary 72,464 B · peak anonymous RAM (official
  games) 308 KB.
- **tickbox (C, "the Accountant")** — *time is the weapon.* Keeps its
  own books with `CLOCK_MONOTONIC`: a 3.0 host-s reserve that can never
  be spent, a decaying per-move allocation scaled by a criticality
  multiplier (starved opening, ×1.6 in check, capped inside the search
  every 1024 nodes), iterative deepening that always holds a legal
  fallback move, and an early-exit rule that banks time. Eval kept
  deliberately thin; its 128 KB transposition table exists for search
  discipline, not knowledge. Refused: book, pawn-structure terms, SEE.
  Source 21,161 B · binary 72,512 B · peak anonymous RAM 292 KB.
- **sliver (B, "the Minimalist")** — *smallest correct engine.*
  64-square board, copy-make (a position is 76 B of payload), negamax
  depth 3 + capture quiescence, 30k-node cap, eval = material + pawn
  advance + centrality. Refused: hash, book, move ordering, killers,
  repetition detection, tapered eval. It also fixed two pawnbox traps
  on principle: all four promotions generated, and relay matching on
  the exact promotion suffix. Source 7,844 B (136 lines) · binary
  71,328 B · peak anonymous RAM 132 KB.
- **pawnbox (control)** — the proof's baseline, unchanged: source
  9,851 B · binary 67,608 B · peak anonymous RAM 144 KB.

### The Underfill measurement (FORMAT §7 receipts)

| Measure | Season 0 | Cap | % of cap |
|---|---|---|---|
| Mean crew binary | 72,101 B | 4,194,304 B | **1.7%** |
| Largest crew binary (tickbox) | 72,512 B | 4,194,304 B | 1.7% |
| Mean peak anonymous RAM | 244 KB | 520 KB | 46.9% |
| Largest peak anonymous RAM (hoardbox) | 308 KB | 520 KB | 59.2% |
| Carried manifest data (books, tablebases) | **0 B** | — | — |
| Cap violations / forced prunes at the gate | **0** | — | — |

Two honest caveats on the numbers: host binaries are libc-startup
dominated (~67–72 KB for every entrant including the baseline), so the
binary row mostly says the *cargo* is empty, not that the code is —
the source row (29 KB / 21 KB / 8 KB) is the truer size of each crew's
ideas. And peak anonymous RAM is a whole-process measure including
host arenas; by design accounting the largest single objects in the
season are the two transposition tables (hoardbox 131 KB, tickbox
128 KB) — memory spent on *search*, not on carried knowledge.

**Arc verdict: Phase 1 — UNDERFILL — confirmed for Season 0.** Casey's
prediction was that the first builders "don't even know how to fill
it", and the receipts say exactly that: flash usage is a rounding
error, nobody carried a single byte of book or tablebase, nobody had
to prune anything to fit, and the only dimension anyone spent into
was RAM — and only halfway, and only on transposition tables. The
box's cargo space is untouched. If the arc holds, Season 1's fight is
the opposite one: entries pressing the caps and builders learning to
cut. That is now a falsifiable expectation with a baseline attached.

## Game-by-game (termination notes)

| Game | Result | How it closed | Charged (sim-s, W/B) |
|---|---|---|---|
| ctrl-hoardbox | 1–0 | mate by hoardbox, move 21 | 156.7 / 6.5 |
| ctrl-tickbox | 1–0 | mate by tickbox, move 15 — fastest kill of the season | 135.8 / 4.5 |
| ctrl-sliver | 0–1 | mate by pawnbox, move 51 — sliver's longest resistance | 5.8 / 9.0 |
| rr-ab1 (hoardbox W) | 1–0 | mate, move 21 | 168.9 / 3.8 |
| rr-ab2 (sliver W) | 0–1 | mate by hoardbox, move 14 | 2.5 / 101.7 |
| rr-ac1 (hoardbox W) | 1–0 | mate, move 25 | 188.0 / 271.5 |
| rr-ac2 (tickbox W) | ½–½ | **fivefold repetition**, move 30 | 354.7 / 251.1 |
| rr-bc1 (sliver W) | 0–1 | mate by tickbox, move 23 | 3.9 / 254.4 |
| rr-bc2 (tickbox W) | 1–0 | mate, move 26 | 310.4 / 4.8 |

Time behaviour, three signatures: **sliver** plays essentially
instantly (15.0 sim-s charged across all four of its round-robin
games; its busiest single game cost 0.8% of its clock) like the stock
micro-Max of the proof; **hoardbox**
spends a steady ~175 sim-s per game from a 24 host-s internal purse;
**tickbox** spends like it means it — 1,191 sim-s across its four
round-robin games, roughly half its clock every game, peaking at
354.7 in the draw — and never came within sight of a flag fall
(worst single move all season: 30.6 sim-s, rr-ac1 ply 30).

## The most interesting game — rr-ac2, tickbox (W) vs hoardbox (B), ½–½

1. tickbox mounted the only sustained attack anyone aimed at the
   champion all season: h4–h5, the g-pawn storm, g5 by move 20.
2. hoardbox answered not with a refutation but with an offer — its
   bishop began shuttling Bd6/Bb4, a repetition the Materialist was
   happy to sign.
3. tickbox's king joined the dance (Kh2/Kg1) instead of finding a
   break; the Accountant's clock craft had bought it time, not a plan.
4. It spent 354.7 sim-seconds — the largest spend of Season 0 — and
   the position at move 30 was the position at move 22.
5. Fivefold repetition: tickbox proved the champion can be held,
   and in the same game proved that time spent is not progress made.

## Failures and incidents — unlaundered

- **In the nine official games: none.** No desync, no illegal move,
  no flag fall, no size or RAM breach, in 446 plies. §6's contract
  (acknowledged relays, referee-owned position) held for every crew
  — including the two relay traps the proof exposed (pawn double
  pushes, promotion suffixes), which all three builders handled.
- **Builder phase:** hoardbox's first build had a real bug — its
  think routine returned a move without applying it internally, so
  it rejected the opponent's first reply. Its own smoke test caught
  it at ply 2; the fix was in before the entry froze and the frozen
  entry never desynced. Recorded because the smoke gates earned
  their keep on day one.
- **sliver's known costs, as designed:** no repetition detection (it
  can neither claim nor deliberately avoid a repetition — the
  referee owns those rulings) and quiet promotions invisible to its
  quiescence. Neither fired as a loss cause this season; its losses
  were chess losses — depth 3 is simply not enough chess at this
  clock. Its correctness record is spotless and its play was the
  weakest: legality is the floor, not the event.
- **tickbox's draw cuts both ways** (see annotation): the season's
  biggest time spend produced no progress for eight moves. The
  Accountant's doctrine is validated on survival (never flagged,
  held the champion) and indicted on conversion.
- **Corpus hygiene:** a pawnbox-vs-pawnbox rigging validation game
  was run before the season to prove the runner, and was deleted
  from the venue — it is not a season game and appears nowhere in
  these receipts. The season corpus is exactly the nine games above.
- **The standing caveat (FORMAT §12):** every time figure here is
  host wall time × F = 20 — box-time is a modelled currency, and
  these are box-records, honestly labelled, not silicon records.

## What the season teaches

At this hull and this clock, the doctrines rank **knowledge > time
craft > minimalism** — but the margins are the lesson, not the order.
hoardbox's knowledge won games *as both colours* and quickly (its
four mates landed between moves 14 and 25); tickbox's discipline never lost it a
game on the clock and bought the season's only half-point off the
champion; sliver showed that a perfectly legal, perfectly honest
engine can still be outclassed by 136 lines of enough. And the
format's headline metric now has its baseline: the box is 98%
empty. Season 1's builders inherit a total corpus of nine games, a
champion whose weakness nobody found (its draw was an offer, not a
wound), and a prediction — Pruning — waiting to be tested.

## Artefacts

- Crew sources (the molts): `builds/hoardbox/hoardbox.c`,
  `builds/sliver/sliver.c`, `builds/tickbox/tickbox.c` — each with
  its design note as its header.
- Games: `games/<tag>/{match.pgn, receipts.json, runner.log}`.
- Season aggregate: `receipts.json` (this dir).
- Runner: `season_run.py` (this dir; Oracle copy at
  `~/esp32-chess-box/season0/`).
