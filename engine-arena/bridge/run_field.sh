#!/bin/bash
# The standing field: Luanti arena server + world bridge.
# Usage: run_field.sh start | stop | status
#
# stop kills by process PATTERN, not pidfile: an early version of
# this script trusted $! pidfiles that drifted from the real pids,
# and two "restarts" silently kept serving a stale engine. Pattern
# kill + a pgrep count check makes a restart provable.
ROOT=$HOME/engine-arena
export LD_LIBRARY_PATH=$ROOT/root/usr/lib/aarch64-linux-gnu
SRV_PAT="minetestserver --world $ROOT/luanti/worlds/arena"
BRG_PAT="world_bridge.py serve"

case "$1" in
  stop)
    pkill -f "$SRV_PAT" 2>/dev/null
    pkill -f "$BRG_PAT" 2>/dev/null
    sleep 1
    echo "field down (servers: $(pgrep -cf "$SRV_PAT" || echo 0), bridges: $(pgrep -cf "$BRG_PAT" || echo 0))"
    ;;
  start)
    $0 stop >/dev/null
    nohup $ROOT/root/usr/lib/minetest/minetestserver \
      --world $ROOT/luanti/worlds/arena \
      --config $ROOT/luanti/arena.conf \
      --logfile $ROOT/luanti/arena-server.log &>/dev/null &
    nohup python3 $ROOT/bridge/world_bridge.py serve &>/dev/null &
    for i in $(seq 1 30); do
      sleep 1
      if curl -s -m 2 http://127.0.0.1:8797/health | grep -q '"ok": true'; then
        echo "field up: 1 engine (pid $(pgrep -f "$SRV_PAT" | head -1)), 1 bridge (pid $(pgrep -f "$BRG_PAT" | head -1))"
        exit 0
      fi
    done
    echo "field did not come up; see $ROOT/luanti/arena-server.log"; exit 1
    ;;
  status)
    echo "servers: $(pgrep -cf "$SRV_PAT" || echo 0), bridges: $(pgrep -cf "$BRG_PAT" || echo 0)"
    curl -s -m 2 http://127.0.0.1:8797/health || echo "bridge unreachable"
    echo
    ;;
  *) echo "usage: run_field.sh start|stop|status";;
esac
