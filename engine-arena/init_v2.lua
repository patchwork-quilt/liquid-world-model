-- arena: a standing harbour field for liquid-world-model players.
-- SuperInstance — engine-side mod for the Luanti dedicated server.
--
-- The mod owns everything engine-side: the procedural arena build, the
-- walker entity, BFS pathing, the region graph, the locked gate and its
-- key, and the perceptual signature the agent will perceive as "place".
-- It talks to the bridge (world_bridge.py) by file IPC in the world
-- directory: bridge_state.json out, bridge_action.json in, both atomic
-- (tmp + rename). File IPC because this build never delivers
-- fetch_async callbacks (receipted in ENGINE-ON-ORIN.md); the poll
-- interval is ~0.15 s, far below the timescale of a region step.

local WORLD = minetest.get_worldpath()
local STATE_FILE = WORLD .. "/bridge_state.json"
local ACTION_FILE = WORLD .. "/bridge_action.json"

-- ---------------------------------------------------------------- arena map
-- Coordinates: x east, z south (north = -z). Ground surface at y=0,
-- the walker stands at y=1. Rectangles are inclusive cell ranges.

local REGIONS = {
  quay       = {x0=16, x1=52, z0=15, z1=27},
  warehouse  = {x0=4,  x1=20, z0=3,  z1=14},
  chapel     = {x0=21, x1=34, z0=3,  z1=14},
  market     = {x0=38, x1=52, z0=3,  z1=14},
  boathouse  = {x0=2,  x1=15, z0=16, z1=26},
  lighthouse = {x0=53, x1=62, z0=3,  z1=14},
}

local function region_at(x, z)
  for name, r in pairs(REGIONS) do
    if x >= r.x0 and x <= r.x1 and z >= r.z0 and z <= r.z1 then
      return name
    end
  end
  return nil
end

-- A door joins two regions through a shared border. `gap` lists the
-- wall cells left open on each side; `in_a`/`in_b` are the standpoint
-- cells just inside each region. `archway` = the far side's perceived
-- signature is visible from here (open doorway); the locked gate is
-- never an archway.
local DOORS = {
  {id="D1", a="warehouse", b="quay", dir_a="south", dir_b="north",
   gap={{17,14}}, in_a={17,13}, in_b={17,16}, archway=true},
  {id="D2", a="warehouse", b="chapel", dir_a="east", dir_b="west",
   gap={{20,8},{21,8}}, in_a={19,8}, in_b={22,8}, archway=false},
  {id="D3", a="market", b="quay", dir_a="south", dir_b="northeast",
   gap={{45,14}}, in_a={45,13}, in_b={45,16}, archway=true},
  {id="D4", a="boathouse", b="quay", dir_a="east", dir_b="west",
   gap={{15,21}}, in_a={14,21}, in_b={16,21}, archway=true},
  {id="D5", a="market", b="lighthouse", dir_a="east", dir_b="west",
   gap={{52,8},{53,8}}, in_a={51,8}, in_b={54,8}, archway=false,
   locked="brass key"},
}

-- exits[region] = { direction = {to=region, door=door, stand={x,z}} }
local EXITS = {}
for _, d in ipairs(DOORS) do
  EXITS[d.a] = EXITS[d.a] or {}
  EXITS[d.b] = EXITS[d.b] or {}
  EXITS[d.a][d.dir_a] = {to=d.b, door=d, stand={d.in_b[1], d.in_b[2]}}
  EXITS[d.b][d.dir_b] = {to=d.a, door=d, stand={d.in_a[1], d.in_a[2]}}
end

local BASE_CONTENTS = {
  warehouse = {"brass key"},
  boathouse = {"oars"},
  chapel = {"hymn books"},
  lighthouse = {"treasure"},
  quay = {},
}
local function region_contents(region, st)
  if region == "market" then
    return (st.day % 2 == 1) and {"fish crates"} or {"apple crates"}
  end
  if region == "warehouse" and st.key_taken then return {} end
  return BASE_CONTENTS[region] or {}
end

-- ---------------------------------------------------------------- the build
local function N(x, y, z, name)
  minetest.set_node({x=x, y=y, z=z}, {name=name})
end

local function build_arena()
  -- platform: stone ground y=0 over x 0..62, z 0..27; water south
  -- (z 28..35) and east (x 63..66); quay ground is stonebrick.
  -- The y=1/y=2 air fill is load-bearing, not tidiness: headless,
  -- nothing runs mapgen, so cells the build never touches read back
  -- as "ignore", not "air" (VoxelManip-emerged dummy blocks). The
  -- arena must author its own air or the walker sees walls of void.
  for x = 0, 66 do
    for z = 0, 35 do
      local water = (z >= 28) or (x >= 63)
      if water then
        N(x, -1, z, "default:stone")
        N(x, 0, z, "default:water_source")
      else
        N(x, 0, z, "default:stone")
      end
      N(x, 1, z, "air")
      N(x, 2, z, "air")
    end
  end
  local q = REGIONS.quay
  for x = q.x0, q.x1 do for z = q.z0, q.z1 do
    N(x, 0, z, "default:stonebrick") end end

  local function floor(rect, name)
    for x = rect.x0, rect.x1 do for z = rect.z0, rect.z1 do
      N(x, 0, z, name) end end
  end
  local function walls(rect, name, gaps)
    local gapset = {}
    for _, g in ipairs(gaps or {}) do gapset[g[1] .. "," .. g[2]] = true end
    for x = rect.x0, rect.x1 do
      for _, z in ipairs({rect.z0, rect.z1}) do
        if not gapset[x .. "," .. z] then
          N(x, 1, z, name); N(x, 2, z, name)
        end
      end
    end
    for z = rect.z0, rect.z1 do
      for _, x in ipairs({rect.x0, rect.x1}) do
        if not gapset[x .. "," .. z] then
          N(x, 1, z, name); N(x, 2, z, name)
        end
      end
    end
  end
  local function gaps_for(region)
    local out = {}
    for _, d in ipairs(DOORS) do
      if d.a == region or d.b == region then
        for _, g in ipairs(d.gap) do
          local r = REGIONS[region]
          if g[1] >= r.x0 and g[1] <= r.x1 and g[2] >= r.z0
             and g[2] <= r.z1 then
            out[#out + 1] = g
          end
        end
      end
    end
    return out
  end

  -- warehouse: timber walls, wood floor, shelves + a chest (the key's home)
  floor(REGIONS.warehouse, "default:wood")
  walls(REGIONS.warehouse, "default:wood", gaps_for("warehouse"))
  for x = 6, 10 do N(x, 1, 4, "default:bookshelf") end
  N(18, 1, 5, "default:chest")
  N(6, 1, 12, "default:chest")

  -- chapel: stonebrick walls, glass windows, a gold bell on a post
  floor(REGIONS.chapel, "default:stone")
  walls(REGIONS.chapel, "default:stonebrick", gaps_for("chapel"))
  for _, gx in ipairs({24, 28, 32}) do
    N(gx, 2, 3, "default:glass"); N(gx, 2, 14, "default:glass")
  end
  N(27, 1, 6, "default:stonebrick"); N(27, 2, 6, "default:stonebrick")
  N(27, 3, 6, "default:goldblock")

  -- market: stone ground, fence perimeter, stalls (fence + wool awnings)
  walls(REGIONS.market, "default:fence_wood", gaps_for("market"))
  for _, sx in ipairs({41, 47}) do
    for dz = 0, 2 do N(sx, 1, 6 + dz, "default:fence_wood") end
    for dx = 0, 2 do for dz = 0, 2 do
      N(sx + dx, 2, 6 + dz, "wool:white") end end
    N(sx + 1, 1, 10, "default:chest")
  end

  -- boathouse: timber walls, wood floor, log piles + a chest
  floor(REGIONS.boathouse, "default:wood")
  walls(REGIONS.boathouse, "default:wood", gaps_for("boathouse"))
  for i = 0, 3 do N(5 + i, 1, 19, "default:tree") end
  for i = 0, 2 do N(5 + i, 1, 23, "default:tree") end
  N(12, 1, 18, "default:chest")

  -- lighthouse yard: stone walls; the tower — red/white wool rings
  walls(REGIONS.lighthouse, "default:stone", gaps_for("lighthouse"))
  for y = 1, 6 do
    local ring = (y % 2 == 1) and "wool:white" or "wool:red"
    for dx = 0, 2 do for dz = 0, 2 do
      if dx == 1 and dz == 1 and y < 6 then
        -- hollow core except the top
      else
        N(57 + dx, y, 5 + dz, ring)
      end
    end end
  end
  N(58, 7, 6, "default:torch")
  N(60, 1, 11, "default:chest")

  -- quay: stone wall segments sealing the north edge between buildings
  for x = 35, 37 do N(x, 1, 14, "default:stone"); N(x, 2, 14, "default:stone") end
  -- quay fences along the water (south) with posts, and a crate pile
  for x = q.x0, q.x1, 4 do N(x, 1, 27, "default:fence_wood") end
  N(30, 1, 25, "default:chest"); N(31, 1, 25, "default:chest")
  N(30, 1, 24, "default:chest")
  -- seal the lane north of the boathouse so paths stay in regions
  for x = 2, 15 do N(x, 1, 15, "default:fence_wood") end
end

-- ---------------------------------------------------------------- perception
-- The signature uses ONLY standpoint-local sensed features. No region
-- name, no coordinates.
--
-- Round 1 (v1) was a single presence set: node kinds in a radius-6
-- window (ground + two wall layers), kinds kept at count >= 3, capped
-- at the four most-present. Receipt (ENGINE-ON-ORIN): warehouse, quay
-- and boathouse all read brick·stone·timber — a presence set with a
-- frequency cap keeps exactly what the three places SHARE (their
-- structural materials) and discards exactly what they don't (their
-- furnishings, present in single digits, or — the warehouse's
-- shelves — outside the window from both its doors).
--
-- Round 2 (v2, ARENA-REPLAY) keeps the v1 computation verbatim as the
-- base term and adds two standpoint-local sensed terms:
--   ground   — the kind of the floor cell directly under the
--              standpoint (y=0). Maximally local; cannot alias across
--              a wall. It is what separates the quay's stonebrick
--              from the timber floors behind the doors either side.
--   landmark — the dominant FLOOR-STANDING furnishing kind (y=1
--              only: shelves, logs, chests sit on floors; windows,
--              bells and awnings are architecture and already ride
--              in the base term) within a wider radius-10 horizon,
--              requiring count >= 2, ties alphabetical. The horizon
--              is wider because a landmark is precisely the
--              furnishing you can pick out across the room: the
--              warehouse's shelves stand 7–9 cells from its doors.
-- Format: "<ground>|<base>[+<landmark>]".

local KIND = {
  ["default:stone"] = "stone", ["default:stonebrick"] = "brick",
  ["default:wood"] = "timber", ["default:tree"] = "logs",
  ["default:bookshelf"] = "shelves", ["default:chest"] = "chest",
  ["default:glass"] = "glass", ["default:goldblock"] = "gold",
  ["default:torch"] = "torch", ["default:water_source"] = "water",
  ["default:fence_wood"] = "timber", ["wool:white"] = "wool",
  ["wool:red"] = "wool",
}

local LANDMARK_KIND = {
  shelves = true, logs = true, chest = true, glass = true,
  gold = true, torch = true, wool = true,
}

local function base_signature_at(cx, cz)
  local counts = {}
  for dx = -6, 6 do
    for dz = -6, 6 do
      for _, y in ipairs({0, 1, 2}) do
        local node = minetest.get_node({x = cx + dx, y = y, z = cz + dz})
        local kind = node and KIND[node.name] or nil
        if kind then counts[kind] = (counts[kind] or 0) + 1 end
      end
    end
  end
  local kinds = {}
  for kind, n in pairs(counts) do
    if n >= 3 then kinds[#kinds + 1] = kind end
  end
  table.sort(kinds)
  if #kinds == 0 then return "open ground" end
  if #kinds > 4 then
    -- keep the four most-present kinds, alphabetical for stability
    table.sort(kinds, function(a, b)
      if counts[a] ~= counts[b] then return counts[a] > counts[b] end
      return a < b
    end)
    local top = {}
    for i = 1, 4 do top[i] = kinds[i] end
    table.sort(top)
    kinds = top
  end
  return table.concat(kinds, "·")
end

local function signature_at(cx, cz)
  -- ground: the floor cell under the standpoint itself
  local gnode = minetest.get_node({x = cx, y = 0, z = cz})
  local ground = (gnode and KIND[gnode.name]) or "open ground"
  -- landmark: dominant floor-standing furnishing kind (y=1) in a
  -- radius-10 horizon; count >= 2 required, ties alphabetical. The
  -- best_n floor of 1 plus the strict > makes the winner independent
  -- of pairs() iteration order.
  local counts = {}
  for dx = -10, 10 do
    for dz = -10, 10 do
      local node = minetest.get_node({x = cx + dx, y = 1, z = cz + dz})
      local kind = node and KIND[node.name] or nil
      if kind and LANDMARK_KIND[kind] then
        counts[kind] = (counts[kind] or 0) + 1
      end
    end
  end
  local best, best_n = nil, 1
  for kind, n in pairs(counts) do
    if n > best_n or (n == best_n and best and kind < best) then
      best, best_n = kind, n
    end
  end
  local sig = ground .. "|" .. base_signature_at(cx, cz)
  if best then sig = sig .. "+" .. best end
  return sig
end

-- ---------------------------------------------------------------- state
local BOOT_ID = tostring(minetest.get_us_time())
local storage = minetest.get_mod_storage()
local st = {
  day = 1, cell = {24, 24}, holding = {}, key_taken = false,
  busy = false, event = nil, action_seq = 0, state_seq = 0,
  path = nil, path_i = 0, arrive = nil,
}
local walker = nil

local function current_region()
  return region_at(st.cell[1], st.cell[2])
end

local function exits_obs(region)
  local out = {}
  for dir, e in pairs(EXITS[region] or {}) do
    local through = nil
    if e.door.archway then
      through = signature_at(e.stand[1], e.stand[2])
    end
    out[dir] = {through = through}
  end
  return out
end

local function snapshot()
  local region = current_region()
  return {
    boot_id = BOOT_ID,
    state_seq = st.state_seq,
    action_seq = st.action_seq,
    pos = {x = st.cell[1], z = st.cell[2]},
    truth_region = region,
    signature = signature_at(st.cell[1], st.cell[2]),
    exits = region and exits_obs(region) or {},
    contents = region and region_contents(region, st) or {},
    holding = st.holding,
    busy = st.busy,
    event = st.event,
    day = st.day,
  }
end

local function write_state()
  st.state_seq = st.state_seq + 1
  local tmp = STATE_FILE .. ".tmp"
  local f = io.open(tmp, "w")
  if not f then return end
  f:write(minetest.write_json(snapshot()))
  f:close()
  if os.rename then os.rename(tmp, STATE_FILE) end
end

-- ---------------------------------------------------------------- movement
local function walkable(x, z)
  if x < 0 or x > 66 or z < 0 or z > 35 then return false end
  local feet = minetest.get_node({x = x, y = 1, z = z}).name
  if feet ~= "air" then return false end
  local ground = minetest.get_node({x = x, y = 0, z = z}).name
  return ground ~= "default:water_source" and ground ~= "air"
end

local function door_blocked(door)
  return door.locked and not st.key_taken
end

local function bfs(sx, sz, tx, tz, door)
  -- BFS over walkable cells; the target door's gap cells count as
  -- walkable only when the door is not locked.
  local function ok(x, z)
    if walkable(x, z) then return true end
    if door then
      for _, g in ipairs(door.gap) do
        if g[1] == x and g[2] == z then return not door_blocked(door) end
      end
    end
    return false
  end
  local prev = {}
  local queue = {{sx, sz}}
  prev[sx .. "," .. sz] = false
  local head = 1
  while head <= #queue do
    local cur = queue[head]; head = head + 1
    if cur[1] == tx and cur[2] == tz then
      local path = {}
      local node = cur
      while node do
        table.insert(path, 1, node)
        node = prev[node[1] .. "," .. node[2]]
      end
      return path
    end
    for _, d in ipairs({{1,0},{-1,0},{0,1},{0,-1}}) do
      local nx, nz = cur[1] + d[1], cur[2] + d[2]
      local key = nx .. "," .. nz
      if prev[key] == nil and ok(nx, nz) then
        prev[key] = cur
        queue[#queue + 1] = {nx, nz}
      end
    end
  end
  return nil
end

local function place_walker()
  if walker and walker:get_pos() then
    walker:set_pos({x = st.cell[1] + 0.5, y = 1.0, z = st.cell[2] + 0.5})
  end
end

local function finish_move()
  st.busy = false
  st.path = nil
  local region = current_region()
  if st.arrive then st.event = st.arrive; st.arrive = nil end
  if region == "warehouse" and not st.key_taken then
    st.key_taken = true
    st.holding = {"brass key"}
    st.event = "You take the brass key."
  end
  write_state()
end

local function do_move(dir)
  local region = current_region()
  local e = region and (EXITS[region] or {})[dir]
  st.event = nil
  if not e then
    st.event = "There is no way " .. dir .. " from here."
    write_state()
    return
  end
  if door_blocked(e.door) then
    st.event = "The gate is locked."
    write_state()
    return
  end
  local path = bfs(st.cell[1], st.cell[2], e.stand[1], e.stand[2], e.door)
  if not path then
    st.event = "The way " .. dir .. " is impassable."
    -- evidence at the failure point: what does the map read as, here?
    local function nm(x, y, z)
      local n = minetest.get_node({x = x, y = y, z = z})
      return n and n.name or "nil"
    end
    minetest.log("action", "ARENA impassable " .. dir
      .. " from " .. st.cell[1] .. "," .. st.cell[2]
      .. " north-feet=" .. nm(st.cell[1], 1, st.cell[2] - 1)
      .. " north-ground=" .. nm(st.cell[1], 0, st.cell[2] - 1)
      .. " target-feet=" .. nm(e.stand[1], 1, e.stand[2])
      .. " target-ground=" .. nm(e.stand[1], 0, e.stand[2]))
    write_state()
    return
  end
  st.busy = true
  st.path = path
  st.path_i = 2  -- path[1] is the current cell
  if e.door.locked and st.key_taken then
    st.arrive = "The brass key turns; the gate swings open."
  end
  write_state()
end

local function do_reset(day)
  st.day = day or 1
  st.cell = {24, 24}
  st.holding = {}
  st.key_taken = false
  st.busy = false
  st.path = nil
  st.event = nil
  st.arrive = nil
  place_walker()
  write_state()
end

-- ---------------------------------------------------------------- entity
minetest.register_entity("arena:walker", {
  initial_properties = {
    visual = "cube",
    textures = {"default:wood", "default:wood", "default:wood",
                "default:wood", "default:wood", "default:wood"},
    physical = false, collide_with_objects = false, pointable = false,
  },
  on_activate = function(self)
    walker = self.object
    place_walker()
  end,
})

-- ---------------------------------------------------------------- main loop
local poll = 0
minetest.register_globalstep(function(dtime)
  -- advance an in-progress move: up to 2 cells per step
  if st.busy and st.path then
    for _ = 1, 2 do
      local nxt = st.path[st.path_i]
      if not nxt then break end
      st.cell = {nxt[1], nxt[2]}
      st.path_i = st.path_i + 1
    end
    place_walker()
    if st.path_i > #st.path then finish_move() else write_state() end
  end
  -- poll the action file
  poll = poll + dtime
  if poll < 0.15 then return end
  poll = 0
  local f = io.open(ACTION_FILE, "r")
  if not f then return end
  local raw = f:read("*a"); f:close()
  if not raw or raw == "" then return end
  local req = minetest.parse_json(raw)
  if not req or not req.seq or req.seq <= st.action_seq then return end
  st.action_seq = req.seq
  if req.type == "reset" then
    do_reset(req.day)
  elseif req.type == "move" and not st.busy then
    do_move(req.action)
  end
end)

-- Boot runs on the FIRST globalstep, not in on_mods_loaded: on this
-- build the map is not readable during the loading phase (get_node
-- returns nil there), and emerge_area callbacks are never delivered
-- with no clients connected. The globalstep phase has a live map.
local booted = false
minetest.register_globalstep(function()
  if booted then return end
  booted = true
  -- No players will ever connect: keep the arena's mapblocks resident,
  -- or get_node reads "ignore" and the walker unloads.
  local fl_ok, fl_fail = 0, 0
  for bx = 0, 4 do
    for bz = 0, 2 do
      -- persistent (transient=false): written to force_loaded.txt,
      -- so the log and the file both prove the forceloads landed.
      if minetest.forceload_block({x = bx * 16, y = 0, z = bz * 16},
                                  false) then
        fl_ok = fl_ok + 1
      else
        fl_fail = fl_fail + 1
      end
    end
  end
  minetest.log("action", "ARENA forceloads ok=" .. fl_ok
    .. " fail=" .. fl_fail)
  -- Emerge synchronously BEFORE building: set_node into a block that
  -- has not been emerged is silently dropped on this build (receipt:
  -- first build kept only the spawn block's cells). VoxelManip's
  -- read_from_map is the synchronous emerge; it returned nil during
  -- the loading phase, but the map is live by the first globalstep.
  local vm = minetest.get_voxel_manip()
  if vm then
    vm:read_from_map({x = 0, y = -2, z = 0}, {x = 66, y = 10, z = 35})
    minetest.log("action", "ARENA emerged via VoxelManip")
  else
    minetest.log("action", "ARENA WARNING: no VoxelManip at boot")
  end
  if storage:get_int("built_v4") == 0 then
    build_arena()
    storage:set_int("built_v4", 1)
  end
  -- boot self-check: report two known cells so the log proves the map
  local function nodename(x, y, z)
    local n = minetest.get_node({x = x, y = y, z = z})
    return n and n.name or "nil"
  end
  minetest.log("action", "ARENA check quay-floor=" .. nodename(24, 0, 24)
    .. " bell=" .. nodename(27, 3, 6)
    .. " water=" .. nodename(24, 0, 30)
    .. " gap-air=" .. nodename(17, 1, 14)
    .. " wh-wall=" .. nodename(18, 1, 14)
    .. " market-floor=" .. nodename(45, 0, 16))
  if not (walker and walker:get_pos()) then
    walker = minetest.add_entity(
      {x = st.cell[1] + 0.5, y = 1.0, z = st.cell[2] + 0.5},
      "arena:walker")
  end
  write_state()
  minetest.log("action", "ARENA field ready")
end)
