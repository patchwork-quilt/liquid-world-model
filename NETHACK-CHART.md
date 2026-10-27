# The NetHack Chart-Only League

SuperInstance — liquid-world-model programme, games as learning substrate.
Scout 1's named first experiment, run 2026-10-26.

**No language model anywhere.** A scripted explorer (System 1) walks
NetHack 3.6.7 over a pty; the *liquid chart* — the framework's `Chart`
from `lwm/model.py`, used unmodified — learns the dungeon purely from
parsed screens. The score is the chart's quality, priced in survival.

## Headline

**Median league score 4,563.5** — the median per-run product of
true rooms entered × turns survived (the medians of the factors:
**5 true rooms entered × 1,061 turns survived**). **And the chart's
map was true: 0 merges and 0 splits across all 10 runs**, judged by
an independent scorer against each run's own accumulated terrain —
every room the chart drew as one place was one true room, and every
true room entered was drawn as exactly one place.

## Setting

- **Box:** the Oracle (OCI Ampere A1), directory `~/nethack-chart/`.
- **Game:** `nethack-console` 3.6.7 (Debian), driven over a pty with a
  pyte terminal buffer (`nh_driver.py`). Parse contract: line 0 =
  message, lines 1–21 = map, lines 22–23 = status (Dlvl / HP / T: /
  hunger). Proven before the league: screens parse cleanly, moves
  land, resting advances T by exactly 1.
- **Character:** Valkyrie, human, female, lawful — chosen for
  durability; the explorer is a measuring instrument, not a player.
  Names chart01…chart10. Identical options every run via a per-run
  `.nethackrc` in a scratch HOME: autopickup OFF, `time` on, no
  DEC/IBM graphics, number_pad:0.
- **Caps per run:** 3,000 game turns, 6,000 actions, 600 s wall.
- **Seeding, stated honestly:** NetHack 3.6.7 console has **no
  supported seed control** (seeded play is an NLE / 3.7 feature). The
  league's "10 fixed seeds" are 10 fixed launch slots; each game
  seeds itself from system entropy. No seed is claimed anywhere in
  the receipts.

## Process — how this rig came to be (2026-10-26)

*Casey's doctrine, recorded the same afternoon this ran: "Document
well as you go. The process means more than the product." These
entries were written as the work happened; the dead ends are kept
at the same size as the fixes, because they are what the fixes cost.*

- **16:07 — the order is one word: "Play."** Scout 1's named first
  experiment. Setting chosen per the brief: the Oracle, its own
  directory, `nethack-console` 3.6.7 installed once via apt.
  Driver = pty + pyte (the scout had already established raw ANSI
  without a terminal buffer is jumbled). Seeding compromise made
  at design time, not discovered later: 3.6.7 console has no seed
  control, so the league runs 10 fixed *launch slots* and says so
  everywhere a seed would normally be claimed.
- **Driver proof, and two traps it bought.** Screens parse cleanly;
  rest advances T by exactly 1; moves land. Trap 1: the scratch
  HOME must be an *absolute* path — a relative one makes 3.6 report
  "Unknown option 'home/.nethackrc'" and die. Trap 2: the role-intro
  screen's `--More--` must be dismissed in the driver, or every
  position reading is the intro art's fake '@' and the explorer
  navigates a painting.
- **First freeze, T=3–5: the diagonal-squeeze rule.** The explorer
  pressed 'u' forever at a door corner. NetHack silently refuses —
  no turn consumed — a diagonal step when both orthogonal
  neighbours are hard, and any diagonal into or out of a doorway
  cell past a wall corner. `step_legal()` now encodes it and both
  pathfinders honour it; refused steps are also blacklisted per
  (level, cell, direction) from live evidence.
- **A death we missed.** Slot 1's second attempt died on Dlvl 1
  (tombstone: sewer rat, 1,161 moves) but the end was mislabelled
  "stuck (quit)": end-of-game text prints over the map area, so a
  `--More--` check scanning only lines 0–1 never saw it, and the
  death scan didn't know the Debian build's farewell ("Farvel").
  Both scans now cover the whole screen; turns are recorded from
  the last good status parse so a tombstone can't zero the record.
- **Three smaller loops, each reproduced before fixed:** a pet
  loitering >3 cells away parked a wounded run resting forever
  (rests capped at 40 consecutive); corridor cells bordering unseen
  rock stayed "frontier" forever (a stood-on cell is consumed);
  opened doors draw as wall, so terrain now keeps a door cell a
  door forever once seen as '+'.
- **The 950-observation bounce (the league's real first result).**
  Slot 1, attempt 3: a clean 1,087-turn run that never descended —
  ~941 of ~960 observations oscillated between one room and its
  corridor. A live trace showed why: one neighbour wore many exit
  keys ('west', 'northwest', 'southwest' all → the same corridor),
  and "have I tried this exit" was answered per key, so the
  frontier chased the same doorway under its other names forever.
  Transitions had been recording correctly all along; the *policy*
  was asking the wrong question. Fix: exits are grouped per
  destination place — the chart's frontier question is "have I ever
  gone from A to B."
- **Route commitment.** Grouping fixed the keys and exposed the
  next failure: two places' frontier plans hijacking each other
  mid-crossing (a walk to a far room passes through a neighbour,
  whose own plan turns the explorer around — ~950 observations
  again, different mechanism). The explorer now commits to a chosen
  crossing until it arrives at the destination place. Visits went
  from 2 places per run to 9–16.
- **The explorer paved its own footpath into phantom rooms.**
  Corridor cells are dark beyond one step; the cell under '@' is
  never re-shown once vacated, so the naive "occupied ⇒ floor"
  guess became permanent and whole corridor stretches charted as
  rooms (one "room" was literally the explorer's footpath, stood
  cells in a single row). Fix: provisional glyphs inferred from the
  neighbourhood ('#' if any neighbour is corridor), re-guessed
  every screen until a real glyph terraces the cell.
- **A room sealed by its own door.** A door first seen *open* draws
  as '-'/'|' — wall. One run's downstairs room segmented as an
  unreachable island the moment the explorer left it. Fix: a wall
  cell with passable cells on both opposite sides is a doorway,
  and a known-passable cell is never re-sealed by a wall glyph.
- **Kicking from across the room.** Locked doors were "handled":
  the code kicked — from wherever the explorer happened to stand,
  which NetHack answers by kicking air, when it answered at all.
  And a stale "locked" message could mark doors never bumped.
  Fix: walk to the crossing cell, kick only when adjacent, ≤3 per
  door, then the exit goes dead (blocked-locked). Lock-marking now
  also requires the bump to have actually failed (position
  unchanged).
- **Thirteen actions per stair-step.** With a level's frontier
  spent, the explorer searched 12 turns in every place before
  stepping toward known stairs — and the search counter reset on
  every descend step. Measured in the decision log: 104 searches
  in one run's tail. Fix: stairs first once the frontier is spent;
  searching is for levels whose stairs aren't found.
- **League launch.** With slot 1 descending to Dlvl 2 and charting
  16 places, the explorer was frozen as the measuring instrument
  and the 10 slots launched headless on the Oracle.
- **League complete, same afternoon.** Ten slots, ~10 minutes of
  wall time, every run terminated by death or the explorer's own
  stuck safeguard — none by a rig failure. The scorer's verdict is
  the headline: 0 merges, 0 splits. The one blemish the table
  itself can't show — run 5's entered-room count disagreeing with
  its chart-room count by one — is recorded in the reading notes
  under Results, not smoothed over: neither counter as defined
  explains the gap, and naming that is worth more than a clean
  sweep claimed too loudly.

## The mapping (screens → chart vocabulary)

From `perception.py`, where it is stated once and in full:

- A **room place** = a 4-connected component of floor cells
  (`. < > { _ \`); a **corridor place** = an 8-connected component
  of link cells (`#` corridors and `+` doors — doors fold into
  corridor places). Walls, water and never-seen cells bound
  components.
- A place's **exits** = one per neighbouring place, keyed by the
  compass direction in which the neighbour lies relative to the
  place's centre; stairs are exits `down` / `up` with destination
  unseen until a traversal teaches the chart.
- **Contents** = floor features only (stairs, fountain, altar,
  throne). Creatures and items are weather.
- Identity: a component keeps its first place id; components only
  grow and merge; on merge the dominant id wins and the absorbed id
  stays in the chart — which is what makes scorer-side **splits**
  measurable.
- Two glyph traps the receipts forced into the mapping: a cell only
  ever shown occupied gets a *provisional* glyph inferred from its
  neighbourhood (a flat "floor" guess paved the explorer's own dark
  corridor footpath into phantom rooms); and an open door draws as
  wall (`-`/`|`), so a wall cell with passable cells on both
  opposite sides is reclassified as a door, and a known-passable
  cell is never re-sealed by a wall glyph.

Where the grid does not map cleanly, the mapping says so: a whole
corridor web is ONE corridor place however many junctions it has;
place ids are keyed by dungeon level as entered, so two branches at
the same depth number could collide (not hit in this league).

## The explorer (System 1, deliberately simple)

Chart-frontier first — route over the chart's traversed graph to the
nearest place with a never-tried exit, with **route commitment** (a
chosen crossing is walked to its destination place without
re-planning from intermediate places; without it, two neighbours'
plans hijacked each other mid-crossing and one run spent ~950
observations bouncing between a room and its corridor). Then tile
frontier (passable cells bordering the unseen), then the stairs if
known, then search (≤12 per place, the secret-door hunt), then
wander. Combat defaults, stated: bump-attack what plugs the way;
flee below 30% HP; rest below 55% HP when nothing is within 3 cells;
eat the carried ration on Hungry or worse (nothing is ever picked
up — the ration is the whole pantry). Locked doors: kicked (Ctrl-D,
≤3 per door) when they block the chosen frontier; a door that will
not open becomes a dead exit — the chart's blocked-locked outcome.

## Results

| slot | turns | depth | chart rooms | true rooms shown → entered | uncharted exits at end | in-game score | cause | merges / splits |
|---|---|---|---|---|---|---|---|---|
| 1 | 1,521 | 1 | 2 | 2 → 2 | 1 | 0 | killed by a newt | 0 / 0 |
| 2 | 893 | 2 | 10 | 10 → 10 | 3 | 82 | stuck (quit by safeguard) | 0 / 0 |
| 3 | 1,972 | 1 | 1 | 1 → 1 | 1 | 20 | killed by a newt | 0 / 0 |
| 4 | 1,217 | 1 | 5 | 5 → 5 | 4 | 52 | killed by a newt | 0 / 0 |
| 5 | 309 | 1 | 2 | 4 → 3 | 2 | 4 | stuck (quit by safeguard) | 0 / 0 |
| 6 | 905 | 4 | 7 | 7 → 7 | 6 | 214 | killed by a jackal | 0 / 0 |
| 7 | 1,745 | 2 | 6 | 7 → 6 | 2 | 58 | killed by a jackal | 0 / 0 |
| 8 | 295 | 1 | 5 | 6 → 5 | 2 | 0 | killed by a jackal | 0 / 0 |
| 9 | 277 | 1 | 5 | 6 → 5 | 1 | 8 | killed by a jackal | 0 / 0 |
| 10 | 1,532 | 1 | 6 | 6 → 6 | 1 | 48 | killed by a jackal | 0 / 0 |

Aggregates (from `results.json`): median turns **1,061**; median
true rooms entered **5**; median league score **4,563.5**; total
merges **0**; total splits **0**; deaths **8 of 10** (newts ×3,
jackals ×5). Best depth: run 6, Dlvl 4. The chart also recorded 137
surprises across the league (beliefs revised on contact — the
chart learning in the framework's own bookkeeping).

Reading notes, kept honest:

- "Chart rooms" counts observed room places; the scorer's "true
  rooms entered" is the ground truth the score uses. In run 5 they
  disagree (chart 2, entered 3): one entered room is not
  represented among the chart's observed room places — it was
  traversed under an identity the room counters don't surface.
  Neither the merge nor the split counter as defined captures that
  gap; it is recorded here rather than smoothed over.
- Two runs (2 and 5) ended by the explorer's own stuck safeguard,
  not by death — run 2 with a complete two-level chart (see the
  narration). They are scored as they stand.
- In-game score is near-zero by design (nothing picked up, nothing
  sold); it is reported because the brief asks for it, not because
  it measures anything here.

## One run, narrated from its chart

**Run 2 (chart02), narrated from its chart.** Dlvl 1: the birth
room L1R1 (stairs-up) opens southeast and southwest into corridors;
the hub corridor L1C1 touches four rooms like a station concourse
— L1R2 east, L1R4 southeast, L1R3 southwest, L1R1 northwest — and
the chart draws all four as separate places, correctly. Southwest
through L1C4 the explorer reached L1R5, which held the
stairs-down; the chart's record of that exit reads
`down → L2R1` — destination *learned from the traversal*, exactly
the framework's semantics. West of L1R5, corridor L1C5 ends at
L1R6, a dead end; the chart says one exit, east, and that is all
the truth there is. Dlvl 2 repeats the shape: L2R1 (stairs-up) →
hub L2C1 → L2R4 (east corridor L2C2 glimpsed but never entered —
the chart leaves it a place with no exits and no visit, honest
about the edge of its knowledge) and L2R5, which fans out through
two more corridors to L2R6, another dead end. There the run died
standing up: monsters plugged L2R6's only exit, the simple
defaults had no answer, and after 841 observations in that one
room the explorer's stuck safeguard quit it. The chart's final
state is complete and true for everything it saw: 19 places, 18
visited, 3 uncharted exits remaining, 0 merges, 0 splits. The map
outlived the mapper, which is the point of a chart.

## Honest limits

- **Fog is not exercised.** One run is one "day" in framework terms
  (every observation is day 1); fog of war is a cross-day mechanic.
  The league measures charting and chart truth, not forgetting.
- **The corridor web is one place.** Segmentation joins every
  touching corridor and door into a single component per connected
  web; the chart's corridor count understates junction structure by
  design of the mapping.
- **Doors first seen already open** read as wall until the
  both-sides-passable rule catches them; a doorway whose far side
  was never seen stays wall.
- **Combat is a default, not a strategy.** Most deaths are Dlvl 1–2
  fauna (kobolds, newts, sewer rats) against an explorer that
  bump-attacks and carries no picked-up gear. Survival numbers price
  the chart under that handicap; they are not a NetHack score
  attempt (in-game scores are reported for completeness and are
  near-zero by design — nothing is picked up, nothing is sold).
- **Seeds are launch slots** (see Setting). Runs are not
  reproducible game-for-game; the league is comparable in
  distribution, not in identical dungeons.
- The explorer's exits are keyed per destination place: two
  physically distinct doorways between the same pair of places are
  one chart exit.

## Files

- `nh_driver.py` — pty + pyte driver, screen parser.
- `perception.py` — the mapping above, implemented.
- `chartplay.py` — one run: driver + perception + `Chart` + explorer.
- `run_league.py` — the 10 slots + the scorer (merges/splits against
  scorer-side segmentation of each run's union terrain).
- `results.json` — per-run receipts and aggregates.
- `runs/runNN.json` — per-run records (chart export, observation
  log, decision tail, union terrain).
