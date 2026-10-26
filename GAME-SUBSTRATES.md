# SCOUT — game environments as learning substrate for the fleet's model stack

SuperInstance · 2026-10-26 · preparation/inventory lane (nothing built; no game repo modified)
Question (Casey): the fleet has a lot to learn — which of our own programs and the old
games make good, fast places to learn in? Mapped against what the fleet now has:
the liquid-world-model chart (an agent charting an uncharted world room by room),
the model farms (Orin desk tier + Oracle CPU tier, one uniform `call()`), and the
doctrine — sealed performance, score = receipt, slow models digesting on off-turns.

**Checked live by this scout:** both boxes' apt catalogues; Sail and Sink's shipped
file, line by line at the seams; the Projectionist repo's existence; NetHack and
dfrotz actually running on the Oracle (probe log at the end). **Known from fleet
record, not re-verified here:** farm membership/latencies, the Thor JEV rack state.

---

## Inventory

| Game | Runs where | Agent perceives | Agent acts | The score / receipt | Turn structure | Rights |
|---|---|---|---|---|---|---|
| **NetHack 3.6.7** (`nethack-console`) | Oracle + Orin, apt, 1.4 MB | ASCII dungeon grid + message line + status line over a pty — the whole state as cheap text | Single keystrokes (move, search, eat, cast…) | In-game score; death/victory record with cause, level, turns — a born receipt | **Strictly turn-based** — the world waits forever between moves | GPL (NetHack GPL), apt-packaged |
| **Interactive fiction via dfrotz** (Z-machine) | Oracle + Orin, apt, 124 KB | **Pure prose on stdout** — room descriptions, no screen geometry at all | Typed commands on stdin (`go north`, `examine map`) | In-game score + moves (Curses: points as you solve); transcript is the receipt | **Parser turn-based** — waits indefinitely | Interpreter GPL; story files: freeware via IF Archive (Curses verified, below) |
| **Sail and Sink** (house, Level 1 of Projectionist) | Browser page; deploys from SuperInstance/Projectionist via GitHub Pages | The page **logs its own state as JSONL every second** (boat speed, flooding per compartment, wave height, all render dials) + a rendered text panel | Keyboard/pointer events in the page; dial settings as the learnable actions | The page's own quality formula (below) + the downloadable JSONL training log | **Real-time** physics (rAF loop) — the exception in this table | Ours |
| **DCSS 0.34.1** (`crawl`) | Oracle apt, 4.7 MB — and on this Ubuntu the `crawl` package's deps are **ncurses + Lua, no SDL: it is the console build** | Console screen (pty scrape) + in-game Lua state hooks; morgue/xlog files written by the game | Keystrokes; seeded runs make games reproducible | Score + xlogfile/morgue — the most formal receipt format of any candidate | Turn-based | GPL, apt-packaged |
| **Angband 4.2.5** | Oracle + Orin, apt, 1.1 MB | Console screen (pty scrape) | Keystrokes | Score / character dump on death | Turn-based (energy system; waits for input) | GPL, apt-packaged |
| **Cataclysm: DDA 0.H** (`cataclysm-dda-curses`) | Oracle apt (candidate confirmed, size not checked) | Console screen; JSON world/save data on disk — deep but the least legible per byte | Keystrokes | Survival time / kills; no single canonical score | Turn-based per action, very long games | CC-BY-SA / open source, apt-packaged |
| rogue | **Not in apt on either box** (checked) | — | — | — | — | skipped: no clean packaged route |

Also on the shelf, noted not inspected: GitHub repos **SuperInstance/quilt-arena**
(pushed 2026-10-18) and **SuperInstance/voice-games** (Sitka Skies flight + COLOR
SQUAD RTS + tournament demo) — house game surfaces whose programmatic seams this
scout did not open. Magnus's repos (Scrapcraft / OpenSkyFlight) are context only
and were not touched.

---

## The three that matter

### 1. NetHack — the liquid chart's native habitat

A fresh procedural dungeon every game is precisely "a world it hasn't charted yet,
and hasn't found the map." The chart maps 1:1: rooms/corridors charted, uncharted
exits enumerated, beliefs revised when a corridor isn't where memory said. The
turn structure is the digestion doctrine built into the substrate — between moves
the world holds still, so a slow farm model can think for as long as it wants and
it costs nothing. Death is cheap, frequent, and itemised (score, depth, cause,
turns): sealed runs produce comparable receipts across seeds. State legibility is
the best of the screen games — the map is already text; a driver needs a pty plus
a small terminal buffer (the one real piece of work, and a solved problem in the
field: the upstream NLE/gym ecosystem exists — *known, not installed or verified
on either box; this scout's Oracle pip check for gym/nle/textworld came back
empty*). Every farm member has a job here: the judge as a per-move soundness
gauge, the embedder over message text, the tiny LLM as the off-turn digester
re-reading the run and revising the chart's beliefs at night.

**First experiment:** chart-only league — a scripted explorer walks while the
liquid model charts from pty screens; score = rooms charted × turns survived over
10 fixed seeds, no LLM in the loop. The chart's quality, priced alone.

### 2. Interactive fiction (dfrotz + Curses) — the purest language world

No perception layer at all: the world arrives as prose and the chart *is* text.
dfrotz (the dumb-terminal interpreter inside the apt `frotz` package) is a
programmatic interface by design — commands in on stdin, world out on stdout,
nothing to scrape. This is the cleanest possible test-bed for the fleet's actual
research question — *how far down can the model shrink when the harness carries
it?* — because every failure is a language/reasoning failure, never a vision
failure. Curses (Graham Nelson, freeware; the file this scout fetched from the
IF Archive identifies itself as Z-machine 5, Release 16, serial 951024) opens in
an attic full of family clutter and secrets: a long, scored, solvable world.
Glulxe (apt, 109 KB) extends the same door to modern Glulx titles.

**First experiment:** harness-vs-bare in the attic — the farm's tiny LLM plays
Curses through dfrotz with the liquid chart as its only memory; score = game
points + rooms discovered in 200 moves, bare arm vs harnessed arm.

### 3. Sail and Sink — the house lane (ours, and already instrumented)

Ranked third as substrate for the model stack, first in house relevance — and the
honest split matters. The sailing itself is real-time Canvas physics (83 KB single
HTML file; keyboard/pointer in, `requestAnimationFrame` loop): there is no turn
clock to digest on, and boat-handling is not chart-shaped. **But that's not the
game the arcade study was playing.** The learnable game aboard is the Projectionist
layer: a full dial set (tone/edge mixes, gains, gamma, ramps…) rendered side-by-side
with the scene, and the page scores itself, on itself, in writing — *"Placeholder
reward, not intelligence… 0.40 edge band + 0.35 contrast + 0.25 stability"* — and
emits a structured JSONL training log (dials, fps, wave height, boat speed, cargo,
per-compartment flooding, quality) with a Download button. The receipt was built
in before we knew to ask for one; the earlier study's 35-line always-jitter
learner lifting remembered quality 0.51 → 0.94 is the proof a learner can eat
here. A driver is plain: a headless browser reads the page's own log and presses
keys / sets dials. What it teaches is different in kind from 1–2 — continuous
control and render judgment, not charting — which is a reason to run it in
parallel, not instead.

**First experiment:** dial-learner league, second season — the original jitter
learner vs a farm-gauge-guided learner, both scored on remembered quality over
the page's own JSONL; the log is the receipt.

### Honourable mention — DCSS

Console-build-by-deps on the Oracle, Lua under the hood, seeded runs, and the
xlogfile: the most rigorous receipt discipline of any game here. It loses the
top-3 only on cost-to-first-signal: bigger install, screen-scrape state, and a
much longer game before the receipt means anything. It's the natural *second*
dungeon after NetHack prices the harness.

---

## Live-probe receipts (Oracle, 2026-10-26)

**NetHack 3.6.7, driven over a pty by a Python script** (fixed character via
NETHACKOPTIONS; raw stream, ANSI collapsed — a production driver wants a real
terminal buffer, stated plainly):

```
Unix NetHack Version 3.6.7 - last revision Wed Feb 11 22:36:12 2026.
Hello Probe, welcome to NetHack!  You are a neutral male human Wizard.
(map glyphs in-stream: ------ walls, . floor, @ the wizard, f the kitten)
```
After three eastward moves the game resolved combat on its own clock:
```
The kitten bites the grid bug.
The grid bug is killed!
```

**dfrotz + Curses, plain pipe** (`printf "look\n…" | dfrotz curses.z5`) — no pty,
no scraping; prose straight out:

```
CURSES — An Interactive Diversion, Copyright (c) 1993-1995 by Graham Nelson.
Release 16 / Serial number 951024
Attic
The attics, full of low beams and awkward angles, begin here in a relatively
tidy area which extends north, south and east…
```

**Apt facts (checked both boxes):** nethack-console 3.6.7 (1.4 MB), frotz 2.55
(124 KB, ships dfrotz), glulxe (109 KB), angband 4.2.5 (1.1 MB) — candidates on
*both* Oracle and Orin; `crawl` 0.34.1 on Oracle only in this check (4.7 MB,
console deps); cataclysm-dda-curses 0.H candidate on Oracle; `rogue`: no
candidate on either box.

**Probe hygiene log:** nethack-console, nethack-common, frotz and glulxe were
apt-installed on the Oracle for the probes and then **purged** (binaries verified
gone); the extracted .deb tree, probe scripts and the fetched curses.z5 were
deleted. Nothing else on either box was modified; no game repo was touched.
