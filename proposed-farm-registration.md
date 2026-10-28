# Proposed farm registration — DO NOT MERGE BLIND

For the referee to merge into the Orin farm (`~/model-farm/` on the
Orin) once the GPU lane's farm edits settle. Nothing in the farm was
touched by the engine lane. The bridge is already live on the Orin at
127.0.0.1:8797 and startable via `~/engine-arena/run_field.sh`.

**The one honest cost, stated up front:** every existing farm member
is spawn-per-call (`python3 farm.py call <name> '<json>'`). A `world`
cannot be — a place has to *stay standing* between calls, or there is
no chart to build across calls. So this member kind is **resident**:
the Luanti server + bridge are daemons (~61 MB RSS combined, measured),
and the farm entry is a thin CLI adapter over the bridge's HTTP. That
is the new kind's defining difference, and it is why the kind is named
`world` rather than pretending to be another model.

## farm.json entry (append to `members`)

```json
{
  "name": "arena",
  "kind": "world",
  "status": "local",
  "path": "/home/casey/engine-arena",
  "notes": "Luanti 5.6.1 dedicated server + world_bridge (127.0.0.1:8797). A standing harbour arena — quay, warehouse, chapel, market, boathouse, lighthouse — that players are called INTO: observe() returns a perceptual digest (place signature, exits with archway previews, contents, holding), act(direction) walks the avatar in the real engine, reset(day) starts a new day. Truth (region, position) is scorer-side only at GET /truth. Resident, unlike the farm's spawn-per-call members: ~61 MB RSS for engine+bridge. Start/stop: ~/engine-arena/run_field.sh. Bridge CLI mirrors farm.py: python3 ~/engine-arena/bridge/world_bridge.py call observe|act <dir>|reset <day>|truth."
}
```

## FARM.md paragraph (append under a new `## Worlds` heading)

> ### `arena` — a place, not a model (kind: world)
>
> The farm's first `world` member: a Luanti dedicated server hosting a
> small authored harbour (six named places, a locked gate, a brass
> key, the treasure in the lighthouse), bridged at 127.0.0.1:8797 in
> the framework's World shape — `observe()` / `actions()` / `step()` /
> `reset(day)`, with `truth()` scorer-side only. Unlike every other
> member it is *resident* (a world must persist between calls to be a
> world): engine + bridge idle at ~61 MB RSS and are managed by
> `~/engine-arena/run_field.sh start|stop|status`, not by farm.py.
> First league result: the liquid framework's explorer charted all six
> places and reached the treasure on day 1 in 15 steps, then spent
> days 2–3 trapped by a three-way perceptual merge (warehouse, quay
> and boathouse share one signature) — see ENGINE-ON-ORIN.md in the
> programme's records.

## farm.py handler sketch (for the member's `call` surface)

No farm.py change is strictly needed — the bridge CLI already speaks
the farm's call idiom. If the referee wants `farm.py call arena`
parity, the handler is a five-line shell-out:

```python
# in farm.py's call dispatch, for kind == "world":
#   observe -> GET  /observe        act -> POST /act {"action": input}
#   reset   -> POST /reset {"day": int(input or 1)}
# or simply: subprocess to
#   python3 ~/engine-arena/bridge/world_bridge.py call <verb> <input>
```
