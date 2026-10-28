# An Engine on the Orin — a standing field for the fleet's players

**SuperInstance · 2026-10-27 · the Orin (Jetson Orin Nano Super)**

## Headline

- **Engine chosen: Luanti (Minetest) 5.6.1 dedicated server** — the only
  candidate whose headless server *is* the product: boots to listening
  in ~1 s, idles at ~30 MB RSS, 25 MB on disk, total Lua control over
  generated content. Godot 4.3 headless was the runner-up (faster raw
  round trips — median 47.9 ms TCP — but 104 MB, ~80 MB idle, and an
  editor binary standing in for a server).
- **The field is standing**: a six-place harbour arena (quay, warehouse,
  chapel, market, boathouse, lighthouse; a brass key; one locked gate;
  the treasure in the lighthouse) inside the real engine on the Orin,
  bridged at **127.0.0.1:8797** in the liquid framework's own World
  shape — `observe()` / `actions()` / `step()` / `reset(day)`, truth
  scorer-side only. Start/stop: `~/engine-arena/run_field.sh`.
- **Round trips** (an act is a real walk in the engine, so the number
  carries the walking): 0.21–1.62 s per act in the smoke run; refused
  steps answer in ~0.2 s. The bridge↔engine link is file IPC on a
  ~0.15 s poll — because this Luanti build never delivers its async
  HTTP callbacks with no clients connected (receipted in the process).
- **The framework played in it, unmodified.** LiquidModel +
  ExplorerPolicy, through observe/act alone: **day 1 — all six regions
  visited, treasure reached in 15 steps**, 5 chart places, 23
  surprises. **Days 2–3 — trapped**: warehouse, quay and boathouse
  share one perceptual signature (`brick·stone·timber`), so the chart
  holds them as one place with unioned exits; the explorer ping-ponged
  among them for 120 steps a day at ~330 surprises a day and never
  re-found the route. **Merges: one, three-way. Splits: one (the quay
  reads two signatures from its two standpoints).** The THOR-TEST
  twins problem, at three-way strength, inside a real engine — scored
  from the full step log (`play_results.json`, 255 steps, every step a
  signature/truth pair).
- **Desk impact: ~61 MB RSS for engine + bridge combined**, box RAM
  flat at ~4.9/7.5 GB through play, tegrastats over the run: GR3D mean
  0.9%, peaks 46% (the voxel server is a light, bursty load — honest
  reading: it does not need the GPU, it merely lives on the same box).
  Nothing installed system-wide, no farm files touched, the concurrent
  GPU lane undisturbed.

## The bridge, in one paragraph

The arena mod (Lua, ~490 lines) owns everything engine-side: the
procedural build, a walker entity, BFS pathing over genuinely walkable
cells, the region graph, the locked gate and its key, and the
perceptual signature. The bridge (Python stdlib) owns the API: it
reads the mod's state file, writes action files (atomic renames both
ways), and serves the framework-shaped HTTP. `observe()` returns the
signature as `place` — computed only from standpoint-local sensed
features (material/landmark node-kinds in a radius-6 window) — never a
true region name; `GET /truth` is a separate scorer-only route, and
the play harness's adapter mirrors the framework's own discipline
(the model is wrapped in `agent_view`; truth stays on the harness
handle, as with DungeonWorld).

## PROCESS — as it happened

# Process log — engine on the Orin (written as the work happens)

## Recon (before any install)
- Framework contract (lwm/engine.py): a World owes observe()/actions()/step();
  obs = {place, exits{dir:{through}}, contents, holding, trust, event}.
  The chart (lwm/model.py) keys places by the perceived `place` string and
  learns exits/contents/conditions from transitions; surprises are belief
  contradictions. The reference dungeon hands the agent the true room name
  as `place` — perception there is identity-perfect.
- League scoring precedent (NetHack/THOR): place identity comes from the
  senses; merges = one chart place covering >1 true place; splits = one
  true place scattered over >1 chart place. For the arena, `place` will
  therefore be a *perceptual signature* computed from the surroundings
  digest — not the region's true name (that stays scorer-side).
- Farm idiom (Orin FARM.md/farm.json): members are shelf artefacts called
  via farm.py call(name, input); nothing runs resident; one heavy member
  at a time on this 8 GB desk box; the desktop must stay responsive.
  `world` breaks the "nothing resident" pattern by nature (a server) —
  the registration proposal must say so honestly.
- Box: Ubuntu 24.04 aarch64, 6 cores, 7.5 GB RAM (~3.4 GB available at
  recon), 1.7 TB free disk. minetest-server 5.6.1 in apt (not installed);
  no Godot in apt except godot3 3.5.2 (wrong generation — Godot 4 would
  be a GitHub download).

## Engine evaluation — Luanti boot + the 501 mystery
- Luanti (Minetest 5.6.1, apt debs extracted to ~/engine-arena/root, pure
  user space): the /usr/games binary is a shell wrapper; the real binary
  needed 3 lib debs (luajit, leveldb, spatialindex) extracted alongside,
  and its compiled-in share dir was satisfied by a symlink INSIDE the
  extracted tree (root/usr/lib/share/minetest -> ../../share/games/minetest).
  Boots to "listening on 0.0.0.0:30000" in ~1 s. Idle RSS 30 MB.
  Extracted tree: 25 MB total.
- The HTTP round-trip probe returned 501 for a long, stupid while. Raw
  socket capture finally showed the wire truth: Luanti's fetch sends
  POST with Transfer-Encoding: chunked and Expect: 100-continue. My
  first echo server only implemented do_GET (hence 501), and every
  later "fixed" server silently failed to bind because the first one
  was still alive — three of my kill attempts hit wrong pids (one
  pkill -f matched my own shell and killed it). Lesson receipted:
  instrument the wire before theorising about the stack.
- Bridge consequence: the mod POSTs; the bridge must decode chunked
  bodies itself (~15 lines on BaseHTTPRequestHandler). Topology: the
  mod polls the bridge — POST state digest, receive pending action in
  the same response; the bridge serves observe/act/reset to clients.

## The pick — Luanti, on the numbers
| | Luanti (Minetest 5.6.1 server) | Godot 4.3 headless |
|---|---|---|
| On disk | 25 MB extracted (6.5 MB of debs) | 104 MB binary (49 MB zip) |
| Boot to listening | ~1 s | 0.4 s (Godot wins this one) |
| Idle RSS | ~30 MB | ~80 MB |
| Round trip | HTTP callbacks never delivered on this build (see above); bridge uses file IPC, ~0.15 s poll — measured end-to-end later | TCP median 48 ms (frame-quantised; min 2 ms) |
| Headless form | the dedicated server IS the product | editor binary running a project |
| Content | Lua mods: total voxel control, procedural arena in one file | GDScript scenes — much more code for the same harbour |
| Licence | LGPL-2.1+ | MIT |

Criteria in the brief's order: native headless server (Luanti, decisively),
state API (Godot's plain TCP is simpler; Luanti's mod reads engine truth
directly and the bridge shapes it — the chunked-POST/callback quirks are
bridge-layer problems, solved once), scriptable content (Luanti, by a
mile for a generated arena), licence (both clean), size/boot/RAM (Luanti
except boot). WINNER: Luanti. Godot stays extracted on the box as the
documented runner-up if a physics-first field is ever wanted.

## Bridge design (decided before building)
- Topology: bridge (Python stdlib HTTP, Orin :8797) <-> mod via file IPC
  in the world dir (atomic tmp+rename both ways). The mod polls the
  action file on globalstep; state file is rewritten on every change.
- The mod owns: arena build (procedural, once), the walker entity, BFS
  pathing over walkable cells, region graph, the locked gate + key, and
  the perceptual signature. The bridge owns: the framework-shaped
  observe/actions/act/reset API + a scorer-only /truth.
- Perception discipline: obs["place"] is a signature computed ONLY from
  standpoint-local sensed features (material/landmark kinds in a radius-6
  window + nothing else). True region names never cross to the agent
  side; the scorer maps signature<->region from the run log.
- Arena: 7 harbour regions — quay (start), warehouse (brass key),
  chapel, boathouse, market (contents alternate by day), lighthouse
  (treasure) behind a gate locked with the brass key. One locked edge,
  one key, one goal — the dungeon's teaching shape, rebuilt in voxels.

## Bridge build — the clientless-build discoveries (the expensive chapter)

*(Correction to the chapter above, recorded plainly: the arena as
built has **six** regions, not seven — the chapel counted twice in
the design list. Six meets the brief's ≥6; the count in the results
is six throughout.)*

The HTTP design died on evidence: requests left the mod, 200s came
back, and **fetch_async completion callbacks were never delivered** —
from globalsteps, from timers, with or without bodies. That was the
first of four times this build punished an assumption that a server
with no clients behaves like a server with clients:

1. **Async callbacks are client-tied.** fetch_async and emerge_area
   completions never fire headless. File IPC replaced HTTP on the
   engine link; VoxelManip's synchronous `read_from_map` replaced
   emerge_area.
2. **The loading phase has no map.** In `on_mods_loaded`, `get_node`
   returns nil and `get_voxel_manip()` returns nil. Boot moved to the
   first globalstep, where the map is live.
3. **set_node into an un-emerged block is silently dropped.** The
   first full build kept only the spawn block's cells; every other
   region read back as void. A synchronous VoxelManip emerge of the
   arena volume before building fixed it — proven by a boot
   self-check line in the server log (quay floor, gold bell, water,
   door gap, warehouse wall, market floor — all read back as built).
4. **Untouched cells read "ignore", not "air".** Headless, nothing
   runs mapgen, so VoxelManip-emerged blocks are CONTENT_IGNORE
   dummies: any cell the build didn't explicitly set is a wall of
   void to the walker's BFS — the first smoke runs died on "The way
   northeast is impassable" with real floors underfoot. The arena
   now authors its own air (y=1/y=2 filled before furnishing). An
   arena on a clientless server must build *everything it means*,
   including the empty space.

A fifth lesson was mine, not the engine's: the launcher trusted
`$!` pidfiles that drifted from the real pids, so two "restarts"
kept serving a stale engine while new processes died on the port
bind — a palimpsest of boots that wasted real diagnosis time. The
launcher now kills by process pattern and pgrep-proves exactly one
engine and one bridge after start; the mod also stamps every state
file with a boot id, after the bridge's event-dedup was caught
eating a fresh engine's events (its state sequence restarts at zero
each boot; the bridge outlives boots).

Two bridge-layer normalisations worth naming: Lua's empty table
serialises to JSON `null`, so a closed door's exit arrived as
`null` where the framework's contract wants `{"through": None}` —
the first play attempt crashed the *framework* on it
(`AttributeError` in chart.observe); the bridge now coerces every
engine artefact into the Observation shape. And events are delivered
exactly once, keyed by (boot id, state generation) — the dungeon's
semantics, kept.

## Smoke — the field proves its verbs

`smoke_test.py` against the live bridge, all assertions green:
reset lands on the quay; the locked gate refuses without the key
(avatar stays, event *"The gate is locked."*); the warehouse
auto-hands over the brass key (*"You take the brass key."*); the
gate opens with it (*"The brass key turns; the gate swings open."*);
the lighthouse holds the treasure; a nonsense verb is answered, not
crashed. Act round trips: [1.57, 0.21, 0.96, 0.26, 1.62, 0.81] s —
the spread is walking distance, as it should be in a real engine.

## Play — one of ours, in a real engine

The framework copied to the Orin (stdlib-only, as designed); the
harness adapter mirrors the dungeon leagues' discipline — the model
sees the world through `agent_view`, truth rides the harness handle
for scoring only. Three days, 120-step cap, chart persisting across
days, world reset per day:

| day | steps | goal | places charted | surprises |
|---|---|---|---|---|
| 1 | 15 | **reached** | 5 | 23 |
| 2 | 120 (cap) | — | 5 | 330 |
| 3 | 120 (cap) | — | 5 | 322 |

Day 1's truth sequence is a clean sweep — market, quay, boathouse,
warehouse, chapel, warehouse, quay, boathouse, quay, warehouse, quay,
market, lighthouse — every region, the key fetched en route, done in
15 steps. Days 2–3 are the same three signatures read 120 times:
warehouse→quay→warehouse→quay→boathouse→quay…, because those three
regions are *one place* to the chart. This is not an engine defect
and not a harness artefact (the per-step truth log shows real
crossings); it is the chart's identity assumption meeting honest
perceptual aliasing — radius-6 kind-counts genuinely cannot tell a
timber-floored warehouse from a timber-floored boathouse from the
quay standpoint between them. The named next experiment is a sharper
signature (landmark-weighted kinds, or contents folded in), run as a
new league season in this same field — the field is what makes that
experiment cheap now: change the signature function, replay the same
three days, compare merges.

GPU receipt (tegrastats, 92 samples across the run): GR3D mean
0.9%, peaks of 46% and 38% in bursts; RAM flat at 4,934/7,485 MB.
The engine wakes the GPU for map work but does not live on it —
reported as measured, not as hoped.

## What stands, and what is deliberately left open

- **Standing**: engine + arena + bridge on the Orin, one command
  (`~/engine-arena/run_field.sh start|stop|status`), ~61 MB RSS
  combined, state on disk in `~/engine-arena/luanti/worlds/arena/`.
- **Proposed, not merged**: the farm registration for member `arena`,
  kind `world` — in `proposed-farm-registration.md`, with the honest
  cost stated (a world member is resident; the farm's pattern is
  spawn-per-call). The referee merges it when the GPU lane's farm
  edits settle; farm.json and FARM.md were not touched.
- **Open, named**: the sharper-signature replay (above); a second
  player kind (a farm LLM called into the world through the same
  bridge — the bridge is player-agnostic by construction); Godot
  remains on the box as the documented runner-up.

## Files

- `src/arena_mod/init.lua` — the arena mod (build, walker, BFS,
  regions, gate, signature, file IPC), as deployed.
- `src/bridge/world_bridge.py` — the bridge + farm-idiom CLI +
  `WorldClient`/`ScorerClient`.
- `src/bridge/smoke_test.py` — the field's self-test (SMOKE PASS).
- `src/bridge/run_field.sh` — the standing field's launcher.
- `src/play/play_in_arena.py` — the league harness.
- `play_results.json` — the full play evidence (255 steps).
- `results.json` — the comparison + smoke + play numbers.
- `proposed-farm-registration.md` — the unmerged farm block.
- On the Orin: everything lives under `~/engine-arena/` (extracted
  Luanti tree in `root/`, world in `luanti/worlds/arena/`, bridge in
  `bridge/`, play in `play/`; Godot runner-up in `godot/`).
