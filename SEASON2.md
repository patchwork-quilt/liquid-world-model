# ESP32 Chess Box — Season 2

*The third season of the box league, played on the Oracle venue on
28 October 2026 (04:51–04:57 UTC, 18 games back to back) under the
unchanged format: classic ESP32 WROOM-32 hull, artefact ≤ 4 MB,
anonymous RAM ≤ 520 KB, per-move wall × F=20, clock 600 sim-s a
side, §6 relay law, 240-ply cap with declared material
adjudication. Runner `season2_run.py` — Season 1's rigging
byte-identical; only the wiring (output tree, PGN header, three v3
engine definitions) is new.*

## Headline

**The Minimalist won the season.** sliver3 — 0 bytes of manifest,
the smallest binary on the venue, barely half the hull's RAM —
took the round robin at 2.5/4 and the season at 5.5/8, beating the
Accountant at both colours and holding the Materialist to a
fivefold draw as Black. The Materialist's heir, carrying 399 KB of
verified cargo and the season's only in-band RAM peak, finished
third in the round robin (1.5/4) — beaten home and away by the
Accountant it was built to answer for. And for the first time, **no
heir beat its parent**: all three lineage duels finished level
(two draws; two splits). Season 1's heirs went 2–1 against their
parents; Season 2's went 0–0–3. The parents hold.

| Crew | Round robin | Control (pawnbox ×2) | Lineage (parent ×2) | **Total** |
|---|---|---|---|---|
| **sliver3** (B — Minimalist) | **2.5** | 2 | 1 | **5.5 / 8** |
| tickbox3 (C — Accountant) | 2 | 2 | 1 | 5 / 8 |
| hoardbox3 (A — Materialist) | 1.5 | 2 | 1 | 4.5 / 8 |

The round robin is a perfect non-transitive triangle — the first
in the league's three seasons: hoardbox3 beat sliver3 (1.5–0.5),
tickbox3 beat hoardbox3 (2–0), sliver3 beat tickbox3 (2–0). There
is no strongest v3 crew; there are three matchups.

**18 games, 1,752 plies, 15 checkmates, zero desyncs, zero illegal
moves, zero flag falls.** One gate event, on the control's receipt,
published in the open at §6.

---

## 1. The round robin

| Game | Result | End | Plies |
|---|---|---|---|
| rr3-ab1 hoardbox3–sliver3 | 1-0 | checkmate | 135 |
| rr3-ab2 sliver3–hoardbox3 | ½-½ | fivefold repetition | 116 |
| rr3-ac1 hoardbox3–tickbox3 | 0-1 | checkmate | 62 |
| rr3-ac2 tickbox3–hoardbox3 | 1-0 | checkmate | 113 |
| rr3-bc1 tickbox3–sliver3 | 0-1 | checkmate | 152 |
| rr3-bc2 sliver3–tickbox3 | 1-0 | checkmate | 143 |

**The Accountant's question, answered.** Season 2's brief for
tickbox3 was conversion against the Materialist — *can it ever beat
it, not just hold it?* It beat it twice, once per colour, both by
checkmate (§5 prints the Black win's companion game). The S1
pattern (draw as Black in S0's fivefold shape, win as White) is
broken upward. What beat the Materialist was not the new book line
or the new SEE: it was the S1 conversion machinery, plus an
allocator that no longer banks time in a bleeding position —
rr3-ac1's spend tells the story in one row: hoardbox3 spent 227
sim-s, tickbox3 358. In S1's rr2-ac1 the same fixture read 449
against 287 the other way, and the Accountant was mated. The
defensive-criticality rule (dig in at ≤ −60 cp) has exactly one
job, and its receipt is that inversion.

**The Materialist's consolation is real but narrow:** it is the
only crew that beat the champion (rr3-ab1), and the only crew
sliver3 could not beat. Its losses were both to the one opponent
whose entire doctrine is converting small edges against it.

**sliver3's two wins over tickbox3 were the season's longest
fights** (152 and 143 plies) — the Minimalist outlasted the
Accountant in the ending phase both times, the phase its two new
eval terms (king shelter, passed pawns) were bought for. No single
game is attributed to a single term; the shape is the receipt.

## 2. The controls — the v3 generation sweeps pawnbox 6-0

| Game | Result | Plies |
|---|---|---|
| ctrl3-hoardbox-w / -b | 1-0 / 0-1 | 37 / 34 |
| ctrl3-tickbox-w / -b | 1-0 / 0-1 | 77 / 50 |
| ctrl3-sliver-w / -b | 1-0 / 0-1 | 39 / 34 |

Every v3 crew beat the fixed control at both colours — a first
(Season 1's crews went 2–1 in single-colour controls, sliver2
losing as White; Season 0's went 3–0 but only as White).
hoardbox3's kills (37 and 34 plies) are the season's fastest;
sliver3's 2-0 buries its S1 control loss outright. tickbox3's White
kill (77 plies) remains its slowest fixture — longer than its S1
31-move win — while its Black kill shortened to 50. The control
fixture's verdict on the generation: the floor rose everywhere.

## 3. Lineage — the parents hold (the headline metric)

| Duel | White game | Black game | Verdict |
|---|---|---|---|
| hoardbox3 vs hoardbox2 | ½-½ fivefold, 126 plies | ½-½ ply-cap 240, material level | **level** |
| tickbox3 vs tickbox2 | 0-1 (parent wins as Black), 136 | 0-1 (heir wins as Black), 132 | **level** |
| sliver3 vs sliver2 | 1-0 heir, 55 | 1-0 parent, 71 | **level** |

Three duels, three different shapes of parity:

- **Materialist:** the S1 regression is closed. In Season 1 the
  champion's heir FELL in this duel (hoardbox beat hoardbox2).
  hoardbox3 did not fall: two draws, the second a 240-ply cap game
  in which both sides spent 498 of their 600 sim-s and the
  adjudication found the material level. Parity, not revenge —
  scored as such.
- **Accountant:** Black won both games — the same colour anomaly
  the local dress rehearsal produced (there, too, the duel split
  with Black winning twice). Two independent samples of the same
  weird shape is the beginning of a pattern worth naming: in this
  pairing, the second player's book-and-contempt machinery is
  worth more than the move.
- **Minimalist:** White won both games, symmetrically — the heir
  took the White game in 55 plies (its parent needed 71 to return
  the favour). Depth's children, decided by the move and nothing
  else.

## 4. The crews and the fill census

| Crew | Source | Venue binary | Manifest | Peak anon RAM (range over 8 games) |
|---|---|---|---|---|
| hoardbox3 | 43,224 B | 465,976 B (11.1% of cap) | **399,056 B** | 456–472 KB (**87.7–90.8%**) |
| tickbox3 | 35,230 B | 73,152 B (1.7%) | 482 B | 412–428 KB (79.2–82.3%) |
| sliver3 | 18,519 B | 71,984 B (1.7%) | **0 B (refused)** | 284–296 KB (54.6–56.9%) |

Mean venue binary 203,704 B = 4.9% of the flash cap (Season 0:
1.7%; the census keeps climbing, and for the first time it climbs
on *data with a proof attached* — see below). Mean peak RAM 399
KB = 77% of the hull.

**What each heir carried, and what it bought:**

- **hoardbox3 (Materialist).** The diagnosis that built it is the
  season's cleanest piece of work (PROCESS §7.1): the S1 heir's
  regression was *book pollution* — an unfiltered corpus booked
  pawnbox's losing …a5 defence, and both S1 losses as Black ran
  through it. v3's book is result-filtered (losers' moves are
  walked, never booked; 365 entries) with two authored Nc3
  defences; at both Nc3 keys the venue artefact answers **d7d5**.
  Plus the league's first tablebase: an exact **KPK table,
  393,216 states, solved by retrograde and verified against the
  Bellman equations over every legal state** by its generator
  (222,558 wins / 108,794 draws; regenerated byte-identical on the
  venue). Plus a pawn-structure hash (32 KB) whose eval-equivalence
  was proven over 57,078 positions before it shipped. This is the
  craft crew — and it finished third in the round robin. Both
  things are in the record; §8 reads them together.
- **tickbox3 (Accountant).** The S1 STUDY's own two queued fixes
  (the 3.Nf3 book line; SEE, bought exact and spent narrowly) plus
  defensive criticality. Note the book line's season honestly: it
  covers the S1-named 3.Nf3-*after-d4* order; rr3-bc2's sliver3
  played 2.Nf3 *before* d4 — a different order, still unbooked,
  answered by search (…d4) in a game decided 140 plies later by a
  promotion race. The line did its named job; it was not the
  season's lever. The lever was the allocator's new rule and the
  old conversion machinery.
- **sliver3 (Minimalist).** Two eval terms totalling a dozen lines
  (king shelter +9; passed pawns 6+6×adv), a doubled TT, a
  recalibrated purse — and a book **refused on corpus evidence**
  (in 21 games its decisive errors live at moves 20+, where no book
  byte reaches; the refusal's re-trial condition is on record in
  its STUDY). It won the season. See §8 for what that does and
  does not prove.

## 5. Most interesting game — rr3-ac2

The authored deviation, played on the venue against the very crew
whose published line it answers. tickbox3 (White) opens from its
book; hoardbox3 replies from its new authored Nc3 defence,
verbatim through the deviation **6…Nxe5** (where Season 0's
defence shuffled 6…Bd6 into a fivefold draw):

```
1. Nc3 Nc6 2. Nf3 d5 3. d4 Bf5 4. Be3 Nf6 5. a4 e6 6. Ne5 Nxe5
7. dxe5 Ne4 8. Nxe4 dxe4 9. Qxd8+ Rxd8 10. Bxa7 b6 11. g4 Bxg4
12. e3 Bb4+ 13. c3 Bf8 14. a5 Bf3 15. Rg1 Rd5 16. a6 Rd8
17. Bb5+ Ke7 18. Bxb6 cxb6 19. a7 f6 20. a8=R Rxa8 21. Rxa8 fxe5
22. Rb8 Kf6 23. h4 g6 24. b4 Bg7 25. Rxb6 Rd8 26. Be2 Rc8
27. Bxf3 exf3 28. Kd2 Ra8 29. Kd3 Ra2 30. Rg3 Rxf2 31. Ke4 Bf8
32. c4 h5 33. c5 Be7 34. c6 Bd6 35. Rb7 g5 36. Rxg5 Rh2
37. Rxh5 Kg6 38. Rbh7 Bf8 39. Rh8 f2 40. Rxf8 Kxh5 41. Kxe5 Rxh4
42. e4 Rh3 43. Rxf2 Rc3 44. Kd6 Rd3+ 45. Kxe6 Rc3 46. b5 Rc4
47. Kd5 Ra4 48. c7 Ra8 49. Rc2 Rc8 50. b6 Rg8 51. b7 Rg5+ 52. e5
Rg8 53. c8=Q Rxc8 54. bxc8=Q Kg5 55. Rf2 Kh4 56. Rg2 Kh5 57. Qh3#
```

An underpromotion (20.a8=R), a two-rook ending, a pawn race in
which both sides queen (53.c8=Q, 54.bxc8=Q), and mate by the
second queen. The book fix did exactly its job — hoardbox3 reached
a real middlegame with no …a5 collapse — and tickbox3 won the
middlegame anyway. The Materialist's opening is repaired; the
Accountant's conversion is, for now, simply better.

*Runner-up:* lin3-hoardbox-b — 240 plies, both clocks at 498/600,
adjudicated level: the season's longest game, and the sound of
the Materialist line at exact parity with itself.

## 6. Incidents and gate events (in the open)

**All artefact gates passed for all three v3 crews before any
game** (venue receipts): size (71,984 / 73,152 / 465,976 B ≤ 4 MB),
relay legality suite ALL PASS ×3, RAM peaks under the runner
(hoardbox3 468 KB in its scratch probe; all in-game peaks at §4).
Scratch validation games were played, receipted, and deleted from
the venue per the established hygiene; the season corpus is
exactly the 18 fixtures.

**One gate event — ctrl3-sliver-b, the control's receipt.**
pawnbox (White) recorded peak anonymous **2,172 KB** (VmHWM
3,100 KB) — a RAM-gate FAIL line on a frozen baseline that has
read 128–144 KB in every other appearance on record, including
its five other Season 2 games (132–144 KB). Named here as a
one-off reading of the same class as Season 0-scaleup's x4-ab3,
and published with its proof, per doctrine: after the fixture, a
fresh pawnbox on the venue replayed the identical 34-ply game
under dense sampling and peaked at **136 KB**, reproducing every
move. sliver3's own gate in that game PASSED (284 KB); the result
(mate in 34) is protocol-clean and stands. The reading is not
explained — the receipts store peaks, not series — and it is not
waived either: it is in the results file, flagged, where the next
season can see it.

No other anomalies: 18/18 games completed, every termination by
checkmate, fivefold repetition, or the declared ply-cap rule.

## 7. PROCESS — how the season was built

*(Written as the work happened, per the standing doctrine: the
process is part of the deliverable.)*

### 7.1 The diagnosis came first, and it was proven three ways

Before any v3 design: the frozen hoardbox2 binary, fed the two
Nc3 keys, answers a7a5 in 0.1 ms (book lookup; its search floor is
40 ms). Its generator has no result filter. The donor game is
ctrl-hoardbox, where that …a5 structure was dismantled by move 8.
Two secondary mechanisms were noted and treated as unproven
(SEE quiescence blindness to checking sacrifices; root-only
contempt) — the design addresses the proven one as the headline
and softens the plausible one cheaply, and says which is which.

### 7.2 The KPK generator failed twice, instructively

Draw propagation by successor-countdown left state 961 (WK a1,
BK c2, P a2) unresolved — closed king-dance cycles reach no seeded
draw. The fix (win attractor + complement-is-draw, sound because a
bare king cannot mate) then produced wrong *distances* on 15,684
states (FIFO order is not distance order): split classification
from a separate relaxation pass (35 sweeps), which itself leaked
promotion-to-draw successors into the min as distance 0 (54
states) before they were excluded. The finished generator
re-checks every legal state against the Bellman equations and
emits nothing unless the check asserts exactly; the venue
regeneration matched byte-for-byte. The table's authority is the
re-check, not the solver.

### 7.3 The pawn hash was designed to be unable to desync

The fashionable build is an incremental key in make/unmake. This
one accumulates its key inside eval's own material loop — no
mutable search state — and shipped only after a same-TU harness
showed eval identical with the cache on and off over 57,078
positions (and the KPK lookup exact over 50,510 sampled
positions). The equivalence proof is the artefact's licence; the
cache is just a cache.

### 7.4 Authored lines are chess, and chess is checked by machine

The first draft of the deviation line ended …Bc4 — illegal (the
e2 pawn never moved; then e3 was occupied by the other bishop;
then the f1 bishop blocked castling). Three illegal drafts, each
caught by the generator's SAN walker, before the line that stands
(g3/Bg2 fianchetto) passed. The book generator asserts its three
acceptance keys (startpos, both Nc3 keys → d5) at build time.

### 7.5 Night-phase discipline

Each v3 design was justified only from the public S0/S1 record.
tickbox3 carries no answer to hoardbox3's new deviation, because
the deviation did not exist in any record tickbox3's builder was
entitled to use — the answer to it was left for the board, and
the board's answer (rr3-ac2) was that conversion machinery sufficed.

### 7.6 Local rehearsals, reported and discounted as precedented

Local parent duels (study rig, python-chess referee): hoardbox
parent 1.5–0.5, sliver parent 1.5–0.5, tickbox split 1–1 (Black
won both). On the venue: all three duels level, the tickbox colour
anomaly repeated exactly, the other two shapes changed entirely.
Both prior seasons taught that local rehearsals reverse on the
venue; Season 2 taught it a third time, in a third pattern.

## 8. The expectations, scored — and the learning arc

**Expectation 1 — manifest ≥ 42 KB from at least one crew: MET,
~9.5×.** hoardbox3 carries 399,056 B (KPK table 393,216 + book
5,840), all of it self-generated and machine-verified. tickbox3
carries 482 B; sliver3 carries 0 B by argued refusal.

**Expectation 2 — crew RAM peaks in the 85–95% band: MET BY ONE
CREW, MISSED BY TWO, for three different reasons.**
hoardbox3: every one of its 8 games peaked between 87.7% and
90.8% — in band, by design (pawn hash bought for exactly this,
with an equivalence proof as its licence). tickbox3: 79.2–82.3% —
a near miss; its S2 purchases were code, not BSS, and its STUDY
declined to pad. sliver3: 54.6–56.9% — missed by doctrine, argued
in advance in its STUDY (fill what a receipt justifies; the TT
doubling was justified, a second doubling was not yet).

**Expectation 3 — the Minimalist's strength-per-byte lead narrows
or widens: IT WIDENED — on the standings.** The lead was supposed
to narrow as knowledge crews learned the Minimalist's economy.
Instead the 0-byte crew won the season outright while the
399 KB crew finished third in the round robin. But the triangle
forbids the simple moral: hoardbox3 still beat sliver3 head-to-
head (1.5–0.5), and sliver3's wins came against the Accountant.
Doctrine beat cargo in the table; cargo beat doctrine in the
pairing. Both halves are the finding.

**The learning arc (Casey's phases: 1 underfill → 2 pruning →
3 craft), read from the receipts, not the hope.** Craft is
unambiguously *present* in Season 2's artefacts in a way it was
not in Season 1's: an authored deviation played verbatim on the
venue, a solved endgame carried as verified cargo, a cache with
an equivalence proof, a book policy changed by a proven diagnosis,
a refusal argued from corpus statistics. That is phase-3 work by
any definition. But the season's *results* were decided by
phase-2 machinery: the Accountant's wins ride its S1 conversion
engine; the Minimalist's title rides S1's depth plus two
twelve-line eval terms; the craft crew's cargo decided no game
outright (no fixture ever reached a pure KPK position — checked
over all 1,752 plies — and the deviation game was lost in the
middlegame). The honest verdict: **Season 2
is where craft arrived and was not yet strength.** The arc's next
test writes itself — whether craft, given a season to compound,
starts deciding games; and whether the parents, now level with
every heir, are the ceiling or the floor.

## 9. Artefacts

- Venue (Oracle `~/esp32-chess-box/season2/`): `src/` (the three
  v3 sources + book headers + kpk.h + generators), `season2_run.py`,
  `run_fixture_s2.sh`, and the 18 game directories (match.pgn,
  receipts.json, runner.log each).
- Study tree (`~/workspace/esp32-s2/`): this report,
  `season2-results.json` (every game: crews, colours, result,
  termination, plies, RAM peaks, manifest bytes, gate receipts),
  `aggregate_s2.py`, `builds/{hoardbox3,tickbox3,sliver3}/`
  (source, generators, STUDY.md each, test harnesses), the local
  study games under `games/`, and the S0+S1 corpora under
  `corpus/`.
- Crew binaries (venue): hoardbox3 465,976 B, tickbox3 73,152 B,
  sliver3 71,984 B — the winner stays flashable in principle, like
  every season's: still the smallest artefact on the venue.

*Season 2 closes with the league's first non-transitive triangle,
its first level lineage round, its first tablebase, and its
champion carrying nothing at all.*
