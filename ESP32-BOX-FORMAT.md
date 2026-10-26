# The ESP32 Chess Box — Format Specification

SuperInstance · 2026-10-26 · v1 (design + feasibility proof)

A competitive format for scripted game players that live inside a
simulated ESP32. Builder agents ("crews") write players for a game;
the players meet in clocked tournaments; after each tournament the
builders study **every** game and submit improved players for the
next. The box never changes. Everything else can.

The format's point is not chess strength. It is **self-improvement
with receipts**: a fixed hull, swappable crews, a total replay
corpus, and a season-over-season improvement delta as the headline
metric. Chess is instance #1; Texas Hold'em is instance #2 (§10).

---

## 0. The crab — the format's vocabulary

Casey's framing, and the terms used throughout this document:

- **Hull** — the pinned ESP32 spec (§1): compute, RAM, flash. It
  never changes within a lineage. The hull's fixity is what makes
  seasons comparable and improvement attributable: everything
  measurable changed *except* the one thing that can't.
- **Crew** — the scripted agent: the engine/player source. Fully
  swappable between seasons.
- **Manifest** — the data the crew carries: tables, books, opponent
  models. Swappable, and sized against the hull like cargo.
- **Rigging** — what connects to the hull: sensors, gauges,
  displays, the match runner, the arena. External, changes freely,
  never part of the sealed entry.
- **Shell-change** — moving to a bigger class (an Orin-class box, a
  Thor-class box) is a **promotion event**: recorded, and it starts
  a *new lineage* with its own roster and records. Never a silent
  upgrade inside a season. A crew that changes shells leaves its old
  lineage's record standing, as-is.
- **Molt** — the published snapshot a crew leaves behind at a season
  boundary: source + manifest + receipts, a perfect shell-shaped
  record of what the crew was, examinable by anyone, while the
  living line has already moved on and is soft and growing
  elsewhere. Publishing a season's entries *is* molting; the molt is
  public by design — it is the timestamped record. No result is ever
  claimed from a molt that the living crew hasn't re-earned.
  A molt is a **shape**, and shapes can be re-inhabited: the same
  roster artefact may run on a different machine with a different
  engine (a browser WASM build, the Oracle native runner, real
  ESP32 silicon) and the runs remain comparable, because
  comparability lives in the shape — interface, caps, clock — not
  in the engine. The format therefore specifies **cross-engine
  validation**: a champion molt re-run on real silicon must
  reproduce its record within a stated tolerance. The shape is the
  spec; the engine is an inhabitant.

---

## 1. The hull — pinned spec

The reference is the classic ESP32 as shipped on an
ESP32-WROOM-32-class module. Figures checked against the Espressif
*ESP32 Series Datasheet* (v4.6), §4.1:

| Property | Pinned value | Source |
|---|---|---|
| CPU | Xtensa dual-core LX6, up to 240 MHz | datasheet §4.1.1 (checked) |
| SRAM | 520 KB on-chip (incl. 8 KB RTC fast) | datasheet §4.1.2 (checked) |
| ROM | 448 KB (system; not the crew's) | datasheet §4.1.2 (checked) |
| Flash | 4 MB | module figure for WROOM-32-class parts; the format's pin (chip-level flash varies by part) |

What the hull means for an entry:

- **Size cap.** Crew binary + manifest (every byte the entry
  carries: tables, books, models) ≤ **4 MB**, the flash. (In
  practice the interesting fight happens far below the cap — see
  the predicted arc, §7.)
- **RAM cap.** The crew's engine-accountable memory at runtime ≤
  **520 KB**. "Engine-accountable" is defined precisely, because
  the proof showed the naive definition is meaningless (§11):
  anonymous memory the program itself owns — heap, stack, BSS —
  measured on the host from `smaps_rollup`. Shared file-backed
  runtime pages (the host's libc) are rigging infrastructure,
  identical for every entrant, and are reported separately for
  reference. On the real chip there are no shared pages to hide
  behind; the crew's own arrays are what must fit.
- **Compute budget.** Expressed per-game as the clock (§3) and
  per-move as a *par*: clock ÷ 40 (15 box-seconds per move at the
  standard clock) — the design point a crew builds its thinking
  around, reported against in receipts. The hard per-move ceiling
  is the remaining clock itself. The budget is **wall time on the
  box**: both LX6 cores are inside the hull, so within-move
  parallelism is a legal crew strategy; it buys speed, not extra
  time.

## 2. Simulation honesty — the sim is a stand-in, never a different game

Three routes to "an ESP32 on a desk" were assessed:

1. **Cycle-accurate simulation** (QEMU-Xtensa, Wokwi-class):
   truthful timing, but slow, tooling-heavy, and — for a league
   that wants to run all night in parallel — the wrong economics.
   Reserved for the one-time silicon-class validation (§5).
2. **Instruction-count budgets** (instrumented execution): portable
   and hardware-independent, but it prices a move in instructions,
   and Casey's clock — the format's drama and its constraint — is
   denominated in *time*.
3. **Enforceable-native (the route the proof uses):** crews run
   natively on the host under hard caps set by the runner
   (rigging): the size gate and RAM gate of §1 are checked exactly;
   time is charged as host wall time × **F**, the host-to-box speed
   factor.

What route 3 does and does not guarantee — stated plainly:

- It **guarantees** the artefact caps exactly (bytes are bytes),
  the RAM cap as defined, and that the clock rules every ruling.
- It does **not** guarantee cycle truth. F is an exchange rate, not
  a measurement of any particular game. F is a **format parameter
  with a calibration protocol**: the reference benchmark (a fixed
  node-count search by a reference crew) is timed on the host and,
  when silicon is available, on the chip; F is set from that ratio
  and published with the season's receipts. The proof used
  **F = 20** (per-core integer-throughput ratio, Neoverse-class host
  core vs one LX6 core at 240 MHz — an order-of-magnitude estimate,
  marked as such; no receipt in the proof depends on F being exact,
  because both crews were charged by the same rate).
- **The clock-speed dial is a format feature.** *Match-clock* is
  spec-true (F as calibrated). *Training-clock* deliberately runs
  the sim faster or slower than life — the league may run a
  thousand training games at high F overnight, or slow a position
  down to watch a crew think. The dial setting is part of every
  receipt; results claimed for the record are match-clock results.

## 3. The clock (chess)

- **Standard clock: 10:00 per side per game** (Casey's pin).
  Named variants: **5:00** and **2:00** blitz forms.
- Thinking time is charged continuously against the side to move,
  in box-seconds (§2). There is no increment in v1.
- **Flag fall:** a move that has not arrived when the side's clock
  reaches zero does not count; the game is lost on time. The runner
  enforces this with a host-side deadline of remaining ÷ F plus a
  small, uncharged I/O grace (0.5 host-s in the proof).
- A crew manages its own time inside the clock (via its protocol's
  clock commands, or by node budgets — its choice). The rigging
  enforces the ceiling regardless of what the crew believes its
  clock says. (The proof showed why this must be so: a stock
  engine's internal clock arithmetic had a units quirk and it
  played ~instantly all game — legal, and its problem. See §11.)

## 4. Entries — crews and manifests

A submission is a **molt-shaped artefact**: crew source + build
recipe + manifest, versioned, frozen for the season.

- **Language is the competitor's choice** — C, assembly,
  MicroPython, Forth, anything — *if it fits the hull and builds
  by the recipe*. What logic to use, what language to use, and how
  to abstract under the cap are the competition.
- **The build recipe is part of the entry**: pinned toolchain,
  exact flags, and every build-time configuration (e.g. a hash
  table sized down to the hull) declared. No host-only
  dependencies; no fetching at build or run time; the artefact
  that plays is the artefact that was measured.

## 5. Portability discipline — the artefacts are real

The sim is a stand-in for the chip, never a different game. After
many seasons of ESP32-level uploads, somebody can actually load a
winner onto an ESP32, because there is the code. Therefore:

- Entries are source in a buildable form against the pinned spec:
  a stated ESP32 toolchain/build path (ESP-IDF-class), no
  host-only dependencies, and the §1 caps **are** the real chip's
  caps — a season winner is flashable to real hardware without
  rework, not merely inspired by it.
- Build glue that exists only because the *host* is not the chip
  (e.g. a timing-function shim in the proof, §11) belongs to the
  rigging's build bench and must be declared; it is never shipped
  inside the sealed entry as a silent host dependency.
- **Named future proof, deliberately not this lane's job:** a
  one-time flash-and-play validation — a champion molt built by
  its recipe for real silicon, played against its own Oracle
  record under cross-engine validation (§0). Until that day, all
  records are honestly labelled box-records (simulated hull,
  enforced caps), not silicon records.

## 6. The interface contract (a requirement the proof bought)

The runner does not trust a crew's silent acceptance of a relayed
move. The proof showed a famous stock engine refusing referee-
legal moves on the relay path and desyncing silently (§11). So
the format's player interface requires:

- every relayed move is **acknowledged** (accepted / rejected,
  explicitly);
- a rejection the referee disagrees with is a format event, ruled
  on the spot (the game is scored as a forfeit if the crew cannot
  take the position);
- the referee — never the crew — owns the position of record.

pawnbox, the proof's baseline crew, implements this contract
natively (explicit `ok` / `illegal` relay answers) and never
desynced in any proof run.

## 7. The season loop — and the predicted arc

1. **Tournament.** Round-robin of the season's frozen crews. Every
   game is recorded in full (PGN for chess) — the replay corpus is
   total; there are no unrecorded games.
2. **Night phase.** Builder agents study **all** the games — their
   own crews' and everyone else's — and submit improved crews +
   manifests for the next tournament. The builders are not
   starting cold: automatic chess playing has a century of
   literature, and the tiny-engine sources (the micro-Max line and
   its kin) are the night-study textbooks. The format's study
   phase may cite them as curriculum, the way the Hold'em
   demonstrator uses tournament transcripts.
3. **Freeze.** During a season, entries are frozen — sealed
   performance. Improvement happens between tournaments, in the
   open, and is attributable because the hull didn't move.

**Casey's predicted learning arc** — recorded as a prediction the
seasons will be judged against:

1. **Underfill.** At first the builders "don't even know how to
   fill it" — entries underuse the box.
2. **Pruning.** Then "it's hard for them to prune all the things"
   — entries bloat; the craft becomes cutting.
3. **Craft.** Then "they start to learn how to craft it
   specifically for that size."

Receipts that would confirm or refute each phase, published per
season: mean entry size vs the cap (Underfill: far under;
Pruning: pressing or breaching it), cap-violation and prune
counts at the gate, and the strength delta season-over-season
(Craft: strength rising while size holds or falls).

## 8. Scoring and receipts

- Standings per tournament (wins/draws/losses; flag falls and
  forfeits are recorded as what they are, never laundered into
  ordinary losses).
- **Per-entry resource receipts** for every game: artefact size
  vs cap, peak RAM vs cap, time used per move and per game (the
  per-move charge table), clock remaining at the end.
- **The headline metric is the improvement delta** — a lineage's
  standing and strength change season-over-season at a fixed
  hull. A crew that wins season 1 and never improves is a worse
  demonstrator than a crew that climbs.

## 9. Two venues, one roster

The same molts play in both. Entries are the same artefacts;
only the rigging differs.

- **League venue — the Oracle.** The serious league runs headless
  at scale on the Oracle (the fleet's CPU tier): overnight,
  parallel, training-clock for volume and match-clock for record
  games. Scale is cheap here precisely because the sim's clock is
  a dial (§2).
- **Exhibition venue — the browser arena.** The deployment page
  is an arena, not a poster (programme deployment standard: a page
  does the tool's real thing). The two spec-boxes are emulated in
  the visitor's browser — the crews are tiny, so WASM/JS builds
  from the same submitted source run locally — with a rendered
  board and the tournament clock visible. A visitor picks **any
  two strategies from the roster** (the accumulated uploads
  across seasons, each listed with its season, builder, size, and
  record; pairing by drag-and-drop is the design image, a clean
  two-picker is an acceptable v1) and watches them play a clocked
  game. The roster page *is* the deployment: standings,
  per-strategy receipts, and the season-over-season improvement
  line all live there.
- **A human can step into the ring.** The arena includes
  human-vs-engine: a visitor plays any listed strategy at its
  tournament clock. Human games are **exhibition**, not season
  games — but they are recorded like everything else, flagged as
  exhibition in the corpus. Stated format choice: builders **may**
  study them at night (flagged), because a human's questions are
  data too — but no standing ever depends on them.

## 10. Instance #2 — Texas Hold'em (sketch; deltas only)

One box, many games. The hull, the season loop, frozen entries,
the roster, the two venues, and the receipts machinery are
game-independent. Chess is instance #1. To define a new instance,
a game must specify four things: **the state surface** the player
may read, **the action surface**, **the clock**, and **the
scoring**. Hold'em's deltas from chess:

- **(a) Hidden information — the deep difference.** In chess the
  replay corpus is total and the player sees everything. In poker
  a player acts on partial state, and the hull must hold an
  **opponent model** in kilobytes alongside hand evaluation and
  pot-odds arithmetic — in Hold'em, pruning applies to *beliefs*,
  not only to code. Server-side, the tournament record is complete
  (all hole cards) for night study; the format states the split
  plainly: at night the builders may see everything the server
  saw; live, the player saw only its legal state surface.
- **(b) The clock.** Poker has no game clock; the **blind
  structure** is its time mechanism — rising blinds force action,
  escalate pressure, and end tournaments. Carried over from the
  box: a **per-decision budget of 15 seconds** on your turn.
  And **off-turn thinking is a format rule, not an accident**: the
  player is an ESP32 that keeps running while others act. It
  *observes* every other player's actions as they happen and may
  spend the off-turn interval computing — updating opponent
  models, ranges, and plans. What it may do off-turn is defined:
  observe the public action stream and compute on its own state;
  no communication, no extra information. Off-turn compute is
  bounded only by real elapsed table time — the turn structure
  itself is the budget.
- **Time tactics are an emergent strategy axis — measured, not
  regulated.** A player may act **fast** to deny opponents off-turn
  thinking time, or **slow** to maximise its own. Because cognition
  on a fixed chip is compute × time, act-speed literally sets how
  much thinking the table gets. The format adds no rule to flatten
  this; it is a designed feature. Receipts therefore record
  per-player **decision-latency distributions** and **off-turn
  compute consumed**, so night-study can see the axis and seasons
  can show the archetypes: **deniers vs digesters**.
- **(c) Scoring.** Tournament placement / chip EV across many
  tables and seeds — never a single game. Variance is a
  first-class reporting problem: samples are large, confidence is
  stated, and luck is never laundered into skill.
- **(d) Builders.** Here they are named: **LLMs craft the
  players.** The study-phase curriculum includes the demonstrator
  design's corpus — announcer and YouTube transcripts, experts
  narrating *attention* — alongside hand-history replays.
- **Cross-reference.** This instance is the Hold'em league of the
  self-improvement demonstrators design (sealed performance,
  minimal state API, learning players meeting at final tables).
  The boxed format gives that league its weight class and its
  artefacts: same league, now with a hull.

## 11. Feasibility proof — 2026-10-26, Oracle venue

Smallest working demonstration that the box is enforceable and a
clocked match closes. All artefacts in `proof/` and `src/`
alongside this document. (An earlier exploratory run under a draft
runner reached the same class of rulings; its receipts were
superseded by the runs below and it is not part of the record.)

**The crews.**

- **micro-Max 4.8w** — H.G. Muller's WinBoard engine, source
  fetched from the author's own site (`umax4_8w.c`, 25,577 B,
  pristine). The micro-Max line is the canonical tiny-engine
  textbook: the Chess Programming Wiki describes it as an open
  source program of up to 2,000 characters / 133 lines in its
  minimal form; Muller's pages carry no explicit licence text
  (checked), so it is used here as a study/proof artefact, not
  redistributed as the format's own. Box build: the *only* changes
  are rigging-side — a `windows.h` shim supplying `GetTickCount()`
  (its single Windows dependency) and the era-correct C dialect
  flag. Its hash table is sized **at launch** by the engine's own
  argument: `14` → 2¹⁴ entries = 196,608 B of heap — a manifest
  parameter, exactly as §4 intends. (The stock default is 2²³
  entries ≈ 96 MB — the Underfill/Pruning lesson in one number:
  the famous engine does not fit the hull until its cargo is
  sized.) Binary 67,688 B (sha256 91f932e9…).
- **pawnbox 1.0** — a baseline written for this proof: 176 lines
  of C (9,851 B), negamax + alpha-beta, material/positional eval,
  capture quiescence, full legal move generation. Binary
  67,608 B (sha256 7556e735…). Implements the §6 contract.

**The rigging.** A Python match runner (referee: python-chess)
enforcing §1–§3 at F = 20 with the 10:00 standard clock:
size gate before play, RAM gate on peak anonymous RSS, per-move
time charged at host × F with a hard deadline, flag-fall and
forfeit rulings, full PGN + per-ply charge table + receipts.

**The games.** Two executions of the runner; game 1 was played
twice with move-for-move identical results (the stock engine is
effectively deterministic at these settings).

| Game | Result | How it closed |
|---|---|---|
| game1 (×2 runs) | **1–0 pawnbox**, 109 plies | micro-Max **forfeit**: produced an illegal move (`d3e2`) — its internal position had diverged from the referee's |
| game2, run 1 | **0–1 pawnbox** | micro-Max **flag fall on move 1**: no move within its 30.00 host-s budget (600 sim-s). Not reproduced in run 2; recorded as observed |
| game2, run 2 | aborted at ply 5, no score | micro-Max **explicitly rejected a referee-legal relayed move**: `Illegal move:a7a5` — caught by the runner via §6 |

Game 1 receipts (both runs identical): pawnbox — 55 moves, host
0.774 s, charged 15.5 of 600 sim-s, peak anonymous RAM **140 KB**
PASS, binary 67,608 B PASS. micro-Max — 54 moves, host 0.007 s,
charged 0.1 sim-s (it plays ~instantly: its internal clock
arithmetic is its own affair; the ceiling was enforced
regardless), peak anonymous RAM **352 KB** PASS (hash 192 KB +
its working memory), binary 67,688 B PASS. Final clocks
584.5 / 599.9 sim-s.

**Findings the proof bought:**

1. **The relay path of a stock engine is not match-safe.** The
   micro-Max family's entered-move legality checker (a search
   that "finds" the entered move, inherited from the 133-line
   design) refuses some referee-legal moves — pawn double pushes
   are confirmed cases (`a7a5` rejected outright in game 2;
   divergence bisected to the same mechanism class in game 1) —
   and in some paths refuses *silently*, so the engine's position
   drifts from the referee's until it produces an illegal move
   and forfeits. This is why §6 exists: acknowledgement +
   referee-owned position. It is also a genuine season-1 lesson
   for builders: the interface is part of the craft.
2. **RAM accounting needed a definition, and now has one.** The
   first exploratory run measured whole-process RSS delta vs a
   null program and "failed" micro-Max at ~576–728 KB over the
   520 KB cap — a number dominated by which libc pages the host
   happened to fault in, i.e. it measured the rigging, not the
   crew. §1's anonymous-memory definition measures what the crew
   owns; under it both crews pass with room (140 KB / 352 KB).
3. **Every enforcement mechanism fired at least once** across
   the proof set — size gate, RAM gate, clock charging, flag
   fall, relay rejection, forfeit — and every game reached a
   terminal ruling under the box's rules.

**Verdict.** The box is enforceable, and clocked matches close
under it. Nothing about the box proved meaningless — except, in
finding 2, the naive way of measuring it, which the format now
specifies properly. The box also did its demonstrator job on day
one: it exposed a real defect in a famous stock engine and a
real accounting trap in the rigging, and both are now format
text (§6, §1) rather than folklore.

## 12. Open problems

- **The exchange rate (hardest).** Every receipt, the clock, and
  season-over-season comparability inherit F's error, and crews
  experience time through their own internal clocks, which the
  proof showed can be quirkier than the format's. Calibrating F
  against silicon (§2) shrinks the error but cannot remove the
  structural fact: box-time is a modelled currency. The format
  lives with it by publishing F and the dial setting on every
  receipt — but a crew that learns to *exploit* the gap between
  its internal clock and the rigging's is a season problem the
  format has named, not solved.
- **State verification depth.** §6's acknowledgement catches
  refusals; a crew that accepts a move but books it wrongly is
  caught only when its play becomes illegal. A position-checksum
  echo in the interface is the obvious next contract revision.
- **Silicon day.** The one-time flash-and-play cross-validation
  (§5) is owed. Until then the records are box-records, honestly
  labelled.
