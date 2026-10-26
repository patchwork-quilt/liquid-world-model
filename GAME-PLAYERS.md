# SCOUT 2 — existing algorithmic players as agentic scripting systems

SuperInstance · 2026-10-26 · preparation/inventory lane (nothing installed, nothing built;
no game repo modified). Follow-on to SCOUT.md (substrates). Casey's thesis, tested here:
the fleet does not need to write autoplay from scratch — decades-old algorithmic players
already ARE proven System-1 scripts. The agentic move is to **wrap** them: an agent layer
that scripts, supervises, charts, and night-upgrades around a player that already plays.

**Checked this pass (first-hand):** Oracle apt catalogue (angband, crawl, stockfish,
libretro cores; bizhawk/libtas absent); the crawl/qw repo and README end-to-end; the
facebookresearch/nle repo (archived status, README); the maciej-sypetkowski/autoascend
repo and README; upstream Angband release notes for 4.2.5/4.2.6 (rephial.org) and the
project's GPL-2.0 listing; qw morgue/crash files on crawl.dcss.io (the bot's own plan
trace in its message stream; seeded server runs); Jericho's walkthrough issue and
DeepWiki source map (get_walkthrough / get_state / set_state); BizHawk's MIT licence
text and TASVideos Lua function list; libTAS docs (`.ltm` format, Lua, headless mode);
RetroArch's network-command changelog/forum trail; KataGo licence + analysis-engine
command surface. **Known, marked as such where used:** facts carried from SCOUT 1's
fleet record or standard project knowledge not re-verified this pass.

**Seam grades used below** — what an outside agent layer actually gets:
**clean API** (structured state out / control in, in-process or protocol) ·
**pty/config** (drive it like a user; steer by generated config files) ·
**in-process only** (the seam exists, but on the far side of a compile) ·
**sealed** (launch it, watch the screen, read the tombstone).

---

## Inventory

| Player | Plays | Home | Licence | Seam (state out / control in / pause / goal-steer) | Turn structure | Alive? | Wrap cost |
|---|---|---|---|---|---|---|---|
| **qw** | DCSS | github.com/crawl/qw | DCSS umbrella (GPLv2+); no separate LICENSE at repo root *(root listing checked)* | pty/config — **plus a goal language** (see §3) | Turn-based | Maintained by the DCSS devteam; unarchived *(checked)* | An afternoon–2 days |
| **AutoAscend** | NetHack 3.6.6 | github.com/maciej-sypetkowski/autoascend | **MIT** *(checked)* | **Clean API** via NLE gym (glyphs/blstats/message out, actions in, seeded, parallel batch) | Turn-based | Frozen at its 2021 win; unarchived *(checked)* | 1–2 days (dependency archaeology) |
| **NLE (+ heiner/nle, MiniHack)** | NetHack 3.6.6 | github.com/facebookresearch/nle → **new home github.com/heiner/nle** | NetHack licence family (repo licence field: NOASSERTION) *(checked)* | Clean API — the seam itself, player not included | Turn-based, agent *is* the clock | **Upstream archived** *(checked)*; README redirects to the author's fork | The platform, not a player |
| **Angband Borg** | Angband | In-tree: angband/angband `src/borg/` | GPL-2.0 *(checked)* | **In-process only / sealed** to outsiders (see §1) | Turn-based | **Actively maintained** — resurrected 4.2.5 (2023), "many corrections and improvements" in **4.2.6, Dec 2025** *(checked)* | A week, and C thereafter |
| **BotHack** | NetHack 3.4.3 | Historical (2015) | — | tty bot; code availability not verified this pass | Turn-based | Dead — won via a pudding-farming exploit the devs then removed *(checked, two sources)* | Museum piece |
| **Walkthrough-as-script** | Any parser IF | IF Archive + the game's literature | Per-game (Curses: freeware) | stdin/stdout pipe — the script *is* the player | Parser turn-based | Eternal — text files don't rot | **An afternoon; zero build** |
| **Jericho** | ~57 supported IF titles | github.com/Microsoft/jericho | MIT *(known)* | **Clean API++** — savestates, object tree, valid-action generation, `get_walkthrough()` | Parser turn-based | Research-era, stable *(known)* | Days (needs game files) |
| **BizHawk** | Console classics | github.com/TASEmulators/BizHawk | **MIT** frontend; bundled cores vary *(checked)* | Clean API *inside* Lua/C# (memory R/W, joypad, savestates, event hooks) — but a GUI app, not a service | Real-time → **frame-stepped** (see §4) | Actively developed *(checked)* | A week + per-game memory maps |
| **libTAS** | Native Linux games/programs (+emulators it hosts) | github.com/clementgallet/libTAS | GPLv3 *(known)* | Lua + socket UI process; `-n` headless, `.ltm` movies are the receipt | Real-time → **frame-stepped** | Maintained *(checked docs)* | A week |
| **RetroArch network commands** | libretro cores | RetroArch (cores in Oracle apt — *checked*) | GPLv3 *(known)* | UDP text protocol: `READ/WRITE_CORE_MEMORY`, pause, savestate *(memory commands checked)* | Real-time → pausable/steppable | Maintained | Days — the thinnest TAS seam |
| **Stockfish 17** | Chess | apt `stockfish` (Oracle, *checked*) | GPLv3 *(known)* | **UCI** — the protocol ideal (§5) | Request/response | Actively developed | An afternoon as a gauge |
| **KataGo 1.18.x** | Go | github.com/lightvector/KataGo (not in apt — *checked*) | **MIT** *(checked)* | GTP + **JSON analysis engine** (batched position→verdict) | Request/response | Actively developed *(checked)* | An afternoon as a gauge |

---

## 1. The Angband Borg — the famous one is sealed

**What it is.** The automatic player that has shipped inside Angband's own source tree
for three decades, in on/off waves. Removed in the 4.0 restructure, **resurrected by
Adam Goodman for 4.2.5 (Aug 2023)**, and — the part that matters — **still being
actively fixed**: the 4.2.6 release notes (15 Dec 2025, checked on rephial.org) lead
with "many corrections and improvements to the borg automatic player", and the prior
release's changelog credits fixes for borg crashes, stalls needing manual intervention,
and lava-jumping. A downstream dev diary (Sep 2026) describes `src/borg/` as ~70k lines
across 117 files, building warning-free against current headers. This is not abandonware;
it is a maintained subsystem of a living game. Oracle apt carries angband
**1:4.2.5+dfsg1** (checked) — the first Borg-bearing release. **Not verified:** whether
Debian's prebuilt binary enables the Borg; apt metadata doesn't say. The safe route is
a source build, which for a 1.1 MB C game is cheap insurance.

**How it perceives and acts.** In-process, screen-shaped: the Borg "virtually looks at
the display and presses keys just as if it were a real person" (project's own words) —
it scans the game's terminal panel into its own grid mirror and injects keystrokes into
the game's input queue. It keeps remembered maps of levels it has visited *(known)* —
a primitive liquid chart, compiled in, thirty years early. Start/stop is a keystroke
pair (Ctrl-Z, then `z`; any key halts it).

**Wrappability verdict: sealed, honestly.** There is no external API, no state socket,
no goal input. An agent layer gets exactly four levers: launch/kill the process, send
the toggle keystrokes over a pty, read the same screen a human would, and read the
character dump at death. Goal-steering is character creation plus the Borg's compile-
time-era option set — its goal is fixed (descend, gear, kill Morgoth). Night-upgrading
its *brain* means writing C inside the game tree. **Conversion cost: a week** to make
it a supervised citizen (pty harness, screen parser, stall detection, restart policy)
— and what you get for the week is a *benchmark*, not a platform: a Borg league table
(best depth/score per class over N seeds) is a measuring stick other players can be
priced against. Wrap it **last**, as the control group.

## 2. NetHack — a champion bot, an archived platform, a live frontier

**AutoAscend** (checked, repo + README): the symbolic bot that won the NeurIPS 2021
NetHack Challenge "by a considerable margin" — a priority list of hard-coded strategy
modules (combat, exploration, inventory, a Sokoban solver) composed in Python
(`strategy.py`; the main composition in `global_logic.py`). **MIT-licensed**, 254
commits, unarchived, untouched since its win — frozen, but frozen *complete*. Three
seams matter:

- **It already runs as a batch instrument.** `simulate` mode runs episodes in parallel
  under Ray, writes results to JSON, and *skips seeds already simulated* — resumable,
  receipted batch play out of the box.
- **It already accepts a supervisor.** `run` mode's visualisation lets a human override
  any action by typing, execute the bot's choice with backspace, or fast-forward 16
  frames — a designed human-on-the-loop seam an agent can sit in.
- **Its brain is legible and replaceable.** Strategies are Python classes with entry
  conditions, composable functionally (`repeat`, `until`, `preempt`). Goal-steering =
  editing the composition; night-upgrade = patching one module and re-running the fixed
  seed set. No retraining, no weights — the upgrade diff is readable text.

**The catch is the floor it stands on.** AutoAscend drives NetHack through **NLE**, and
facebookresearch/nle is **archived** (checked: "Public archive"). The README itself
redirects: *"Please find NLE at its new home at github.com/heiner/nle"* — the original
author's fork is the live line (pointer checked; the fork's own activity not separately
audited). AutoAscend additionally patches its NLE copy for seeding and wants Docker +
Ray + an X11 socket for visualisation. **Conversion cost: 1–2 days**, almost all of it
dependency archaeology, none of it design. **MiniHack** (FAIR's NLE-based sandbox of
small custom environments, cited in NLE's own paper list — checked) rides the same
fork question.

**The wider field, honestly priced.** BotHack (2015) ascended 3.4.3 by pudding-farming —
an exploit the developers removed in 3.6; it is a museum piece, not a base. And the
frontier has moved since 2021: a community leaderboard (Dunno Lab's NetHackers board,
crawled ~two weeks before this scout — single secondary source, its own protocol) records
an RL agent beating AutoAscend's progression score for the first time in Sep 2026 and a
one-off LLM-agent ascension on 3.6.7 via a self-built harness, while noting **zero
ascensions on 3.6.6**, the NLE standard. Read: AutoAscend is no longer the ceiling —
but it remains the best *runnable, wrappable* System 1 anyone has published. The LLM
result points the same direction as Casey's thesis from the other side: the winning
move was a harness around a player, again.

## 3. DCSS / qw — the bot that already speaks in goals ⭐

**What it is** (checked, repo + README end-to-end): qw, by elliptic, "the first bot to
win DCSS with no human assistance", **now developed and maintained by the DCSS devteam**
— the game's own maintainers keep their bot able to "play and win the current version."
Pure Lua, running *inside* the game's own clua interface: it reads real game state
(not pixels), plans hierarchically, and issues commands. It plays most species/
backgrounds, has won 3-rune and 15-rune games; the older literature credits ~15% winrate
on its best combo (checked, 2021 workshop paper). Morgue files on the public servers
show it playing production games through 2023 (checked) — and dying informatively.

**Why it grades above its seam class.** Nominally qw is pty/config grade. In practice
it exposes the one thing no other candidate has: **a declarative goal language an agent
can write.** qw.rc's `GOALS` table holds named plans as comma-separated goal strings —
`"D:1-11, Lair, D:12-15, Orc, …, Vaults:5, Shopping, Zot:1-4, Orb"` — with a vocabulary
of branch targets, level ranges, `Rune:<branch>`, `God:<god>` conversions, `Shopping`,
`Win`, and two gifts to supervisors: **`Save`** (reach the goal, save, exit, hand over a
save + persist file — a designed pause-and-transfer point) and **`Quit`**. Combo-cycling
lists accept per-combo god sets and `!plan` suffixes. Around that: **Tab starts and
stops qw at runtime** (pause/resume as a keystroke), `AUTO_START`, `DELAYED`/`DELAY_TIME`
pacing, a shipped **expect script (`qw.exp`) that runs qw for many games in a row**, and
— checked in a real morgue file — **qw narrates its plan into the message stream**
(`1748 ||| PLANNING D:1-11`, `Stepping randomly (disturbance)`) where any pty reader can
follow its reasoning turn by turn. Receipts are DCSS's own: morgue + xlogfile, and the
server builds run it **seeded with deterministic pregen** (checked in its crash dumps:
`Seed: …, deterministic pregen: 1`).

**The wrapper an agent builds** therefore writes rc files (goals, combo, god list) per
run, launches console crawl (`-lua-max-memory 128 -no-throttle`) under a pty, tails the
plan trace, intervenes by Tab or by killing at a `Save` boundary, and files the morgue
as the receipt. Night-upgrade = rewriting the goal list and the shopping list from the
day's morgues — text in, text out, no Lua surgery required for the first several rungs.
**Conversion cost: an afternoon to first supervised games; ~2 days to a tidy league
runner.** One honest risk: qw tracks crawl master, and Oracle's apt crawl is 0.34.1
(SCOUT 1, checked) — if master-qw and 0.34.1 disagree, the fix is a source build of
crawl (the bot's README assumes "a local build of crawl" anyway). Also on record: a
2021 research wrapper (dcss-ai-wrapper) offered gym-style vector+symbolic state for
DCSS — paper-era, presumed stale against current crawl; qw's own seam is better.

## 4. TAS tooling — not players, but clock converters

TAS systems don't contain a player; they contain something arguably more valuable to
this fleet: **total control of time.** A console game is real-time, but inside BizHawk
or libTAS it becomes frame-stepped, pausable, rewindable, savestate-addressable — i.e.
*turn-based at frame granularity*, with the movie file as a frozen, replayable,
frame-exact receipt. That converts the entire console-classic shelf from "reflex
substrate the farm can't serve" into "digestion substrate". ROMs are out of scope; the
clean content routes are homebrew/open games and the emulators' own test ROMs.

- **BizHawk** (checked): frontend **MIT** (bundled cores under their own licences —
  the README is explicit that not everything in a release is MIT). Its Lua/C# API is
  the richest scripting seam in this whole inventory: `memory` read/write across
  domains, joypad set per frame, savestate save/load, and event hooks —
  `onframeend`, `onmemoryread/write/execute`, `oninputpoll`, `onsavestate` (TASVideos
  function list, checked). A Lua script inside BizHawk is a full agent harness with
  perfect perception. Costs: it's a desktop app, not a service (no headless-first
  story); not in Oracle apt (checked); and **every game needs its memory map charted**
  before state means anything — though note that charting an unknown memory map by
  watching what changes *is* a liquid-chart-shaped job. **Week + per-game work.**
- **libTAS** (checked docs): the Linux-native counterpart — two processes (UI +
  hooked game) over a Unix socket, Lua scripting with memory access, RAM search/watch,
  deterministic timer, full savestates, and a CLI built for automation: `-r`/`-w`
  movie record/playback, `-l script.lua`, **`-n` non-interactive headless mode**. Its
  `.ltm` movie format stores the game's executable hash in the header — receipts with
  provenance, again. It TASes *native* Linux programs (SDL games, PICO-8, hosted
  emulators like MAME/PCem), which makes it the natural wrapper for the open-source
  native shelf rather than dumped consoles. x86/x86-64 only — Oracle yes, the ARM
  boxes no (checked: supported archs). **Week.**
- **RetroArch network control** (checked): the thinnest seam of the three — plain-text
  UDP commands into a running RetroArch, including `READ_CORE_MEMORY` /
  `WRITE_CORE_MEMORY` (added to the network interface; command list in `command.h`),
  alongside pause/savestate/version commands *(memory commands checked; the rest
  known)*. No Lua host, no GUI automation — just a socket an agent can hold. libretro
  cores are already in Oracle's apt (checked). For "read score/lives from RAM, press
  nothing yet" gauge-style experiments, this is days, not a week.

## 5. Engine-gauges — the same wrap, player demoted to judge (short)

Chess and Go solved the wrapper contract decades ago, and it's the design ideal the
farm's `call()` should imitate. **UCI** (Stockfish — **v17 in Oracle apt, checked**):
a stateless text protocol — `uci` → `uciok`, `isready` → `readyok`,
`position fen …` in, `go depth N`, and out comes `info depth … score cp … pv …` +
`bestmove`. No screen, no state leakage, bounded work per query, the engine's *opinion
is the product*. **KataGo** (MIT, checked; current stable 1.18.x, checked) goes one
 better for a farm: besides GTP it ships a **JSON analysis engine** —
 `./katago analysis`, one JSON query per line on stdin (position, rules, visits),
 batched verdicts (winrate, score lead, policy, ownership) on stdout, purpose-built
 "for a backend Go service" (README, checked). That is a farm gauge's exact shape:
 position in → judgement out, priced per call, swappable by strength (depth/visits =
 the dial). Neither is in the way of the game lanes; either is **an afternoon** to
 register as a farm member, and chess/Go then become the cheapest sealed-performance
 arenas with a superhuman referee already installed. The lesson to steal for every
 wrapper above: *demand a `readyok` — a protocol moment where the wrapped thing states,
 in text, that it is loaded, honest, and waiting.*

## 6. IF — the walkthrough is already a script; Jericho makes it searchable

**Walkthrough-as-script** is the zero-build baseline and it is exactly as strong as it
sounds: a published walkthrough for a parser game is a literal command list, and
dfrotz takes commands on stdin — SCOUT 1 already drove Curses through a plain pipe.
`cat walkthrough.txt | dfrotz curses.z5` *is* an autoplay system with a human-written
System 1, available this afternoon, for every IF title with a published solution. Two
honest caveats: walkthroughs in the wild carry comments, alternatives, and
"if that failed, try…" branches that need cleaning into a pure command stream; and
game RNG can desync a fixed script — which is precisely the gap the research stack
closes.

**Jericho** (Microsoft, checked via its paper, issue tracker, and source map) is the
wrappable form: a Python gym-like environment over the same Z-machine games, with the
three seams a script lacks — **`get_state()`/`set_state()`** (savestate = branch
points), **world-object introspection + change detection**, and
**`get_walkthrough()`**: the cleaned solution shipped *as data*, replayable and
forkable. It also seeds the game's RNG for replicability (checked). Its issue #43
tracks walkthrough coverage across ~57 titles (checked) — most PASS end-to-end; a few
are honestly short (Curses: "Done but score 450/550" in that 2020-era report — the
script gets you most of the game, which for a baseline is the point). Jericho supplies
code and walkthroughs, not game files; the rights-clean lane stays freeware (Curses)
and self-owned titles. **Conversion cost: an afternoon for the dfrotz baseline; days
to stand Jericho up** — and at the end of those days, the IF lane gains the move no
other substrate here has: *replay the master's script to a savestate, then let the
student try something else from exactly there.*

---

## Ranked: wrap first

1. **qw (DCSS)** — the only player that already exposes a goal language. An agent
   steers it tonight by *writing its rc file*; Tab is pause/resume; its plan trace and
   morgue are the receipts; turn-based digestion is native; the game's own devteam
   maintains it. **First experiment:** agent-as-manager — the farm's slow LLM writes
   qw's `GOALS`/combo for each of 10 seeds from a one-line brief, qw plays headless on
   the Oracle, score = morgue receipts vs the stock `Normal` goal over the same seeds.
2. **AutoAscend (NetHack)** — the cleanest programmatic seam (gym state in/out,
   seeded, parallel batch mode with JSON receipts and seed-skip resume; MIT) and a
   brain made of composable Python strategies — System 2 can literally rewrite a
   strategy module at night and A/B it by seed. Costs 1–2 days of NLE-fork archaeology
   first. **First experiment:** the night-upgrade loop — frozen AutoAscend as System 1,
   one strategy patch per night, score = median score/depth over a fixed seed set vs
   the untouched baseline.
3. **Walkthrough-as-script → Jericho (IF)** — zero-build baseline today (pipe a
   walkthrough into dfrotz), graduating to savestate branching: the script becomes a
   *route the student can deviate from and be scored against*. **First experiment:**
   replay the Curses walkthrough by pipe to its known score; then, at one chosen
   point, branch — farm-LLM commands from the walkthrough's own savestate, scored by
   score-delta over the next 50 moves.

**Honourable mentions, deliberately unranked:** Stockfish-as-gauge (an afternoon;
do it whenever a spare one appears — it's the UCI lesson made flesh); the Borg (wrap
last, as the league's control group — a sealed champion is a measuring stick, not a
platform); BizHawk/libTAS (the clock converters — the right second phase, once a
homebrew title's memory map is worth charting).

**Turn-structure summary for the digestion doctrine:** Borg, AutoAscend/NLE, qw, and
IF are natively turn-based — the world waits, the slow model thinks for free. The TAS
trio *manufactures* the same property for real-time games by owning the clock.
Engines never needed it: a gauge is a question, and questions are already turns.
