# The qw Manager Experiment — MANAGER.md

**Headline: managed vs stock tied on median score across the 10 seeds (128 vs 128) — because the manager produced a valid configuration for only 3 of its 10 briefs; the other 7 managed runs are verified-identical stock runs. On the 3 seeds the manager actually managed, it won 2 and lost 1 (scores 575 vs 49, 1613 vs 462, 36 vs 216). The channel works end to end; a 0.6B manager is not yet a reliable config-writer.**

Setting: Dungeon Crawl Stone Soup (DCSS) console on the Oracle, played by **qw** — the devteam-maintained Lua bot that plays DCSS from a declarative `GOALS` table in its rc file. The experiment tests the manager pattern from the game-substrate scout (SCOUT2-PLAYERS.md, ranked wrap-first #1): a slow, cheap model writes the plan; the proven bot plays the game. Manager brain: the Oracle CPU farm's `llm` member, Qwen3-0.6B (Q4_K_M GGUF, llama.cpp, 2 threads). All artefacts live in `~/qw-manager/` on the Oracle; the full per-run receipts are in `results.json` beside this file.

---

## PROCESS — how this was actually done, in the order it happened

*Casey's doctrine (2026-10-26): "Document well as you go. The process means more than the product." This section is the process record, kept as a first-class part of the deliverable — dead ends and failures included, at the same care as the successes. Entries follow the session's real sequence; times are Oracle UTC where a receipt carries one.*

**1. Read the scouts, then inventory before building.** Read SCOUT2-PLAYERS.md (qw section) and SCOUT.md first. On the Oracle: no crawl installed; the farm's `llm` member answered a live probe in 8.4 s ("MANAGER-PROBE-OK"). qw was cloned from its GitHub home (github.com/hovercow/qw) — master HEAD `8698adc`, dated **2024-07-15**. That date later turned out to be the single most important fact of the setup: qw has been quiet for 15 months while crawl kept moving.

**2. First route — apt crawl 0.34.1: REJECTED by evidence.** Installed the distro package (candidate 2:0.34.1-1) and ran stock qw under a pty driver. qw crashed instantly: `qw.lua:18145: attempt to index a nil value (global 'arg')`. qw's `turn_memo_args` relies on the Lua 5.1 vararg table `arg`; Debian's crawl 0.34 is built against Lua 5.4, where that table does not exist. A one-line shim (`arg = {...}`) was considered and rejected: it would only reveal the *next* incompatibility, and every patch makes "stock qw" less true — the experiment's whole point is steering the *proven* bot, not a fork of it.

**3. Second route — source build of crawl 0.34.1: same failure, and that was information.** Cloned crawl at tag `0.34.1`, built the console binary (~7 min, all cores). Identical `arg` crash. Two builds, two packagings, same crash → the problem is the Lua *version DCSS itself now embeds*, not Debian. Checked the vendored Lua in the 0.34.1 tree: `LUA_VERSION_MAJOR 5, MINOR 4`, no `LUA_COMPAT_VARARG`. qw cannot run under 0.34 unpatched. Route closed.

**4. Detour — LuaJIT build: ABANDONED after three distinct failures.** DCSS can build against LuaJIT (Lua 5.1 semantics). Failure one: the LuaJIT contrib needs a host `lua` binary to run its dynasm preprocessor — installed lua5.4, build still failed (`loadstring` is 5.1-only). Failure two: with lua5.1 + a shim, dynasm passed but buildvm stopped: *"No support for this architecture (yet)"* / *"No target architecture defined"* — LuaJIT's buildvm does not support this ARM64 host configuration through crawl's contrib wrapper. This was eating the session; the detour was cut here rather than ground through.

**5. Version archaeology — the pairing qw was written for.** Instead of fighting forward, dated the drift. qw's own changelog (0.4-a) says "supports DCSS 0.32-a0". Checked `you.strength` across crawl tags: **0.31.0 and 0.32.0 return two values** (current, max — `LUARET2`); **0.33.0, 0.34.1 and trunk return one** (`LUARET1`). qw's armour valuation does `select(2, you.strength())` — under 0.33+ that is `nil`, and the bot dies comparing nil with a number (this second crash was actually observed when a minimal qw patch was tried against 0.34 — patched qw got past `arg` and died exactly there, confirming the diagnosis by experiment). And crawl 0.32.1's vendored Lua carries `#define LUA_COMPAT_VARARG` — the `arg` table exists. Conclusion: **qw @ 8698adc pairs natively with crawl 0.32.x.** Built crawl **0.32.1** (tag, commit f5deb65) from source. qw runs on it **100% stock — zero patches.** The one-line lesson, worth more than the experiment it enabled: *a bot and its game are a versioned pair; when the game moves and the bot doesn't, adopt the game's older version, don't patch the bot.*

**6. Smoke + determinism proof (Oct 27, ~00:31–00:40 UTC).** Stock qw, seed 101, headless under the pty driver: zero Lua errors, a real game (Gargoyle Berserker, died to an iguana on D:2, score 49, 1,156 turns), clean exit in 9.9 s, morgue written. Then the load-bearing check: an identical re-run reproduced the game **exactly** (same score, XL, turns, killer). Design consequence, stated before the experiment ran: same seed + same rc → identical game, so any difference between arms comes from the rc alone — which is precisely the manager's artefact.

**7. Manager design — fixed before any run.** Brief list frozen in `scripts/briefs.json` (5 briefs × 2 seeds, §Design). The prompt demands exactly three lines — `COMBO:` / `GODS:` / `GOALS:` — from closed vocabularies taken from qw's *source* (`qw.rc`'s combo table, `GOD_LIST`, the `GOALS` grammar in qw.lua), not from memory. Two source-level finds while grounding the vocabulary: (a) qw's per-species combo table in qw.lua is keyed with a literal `{` typo for Draconian — harmless in Lua, noted, not touched (stock means stock); (b) the goals grammar is `Rune:<branch>` — *singular* — which the manager would later get wrong five times. A mechanical validator (allowlists, token grammar, count caps) was unit-tested 10/10 before the run. Invalid → stock fallback, **counted, never silently fixed**. `Save`/`Quit` goals are legal qw but were ruled invalid for this experiment (they end a run administratively, with no morgue — a manager that learns to quit has gamed the metric).

**8. The run (Oct 27, 00:42–01:08 UTC).** Phase 1: all 10 manager calls (93.0 s of LLM wall total). Phase 2: 20 games interleaved by seed, control first. Early games closed in 5–30 s. Seed 106 produced the session's one long game — 16,969 turns, 662.7 s — and its managed twin then *appeared* to hang: output stalled in my checks while the process burned CPU, and for some minutes a genuine nondeterminism in qw looked possible. It was not: managed 106 finished with the identical game (49 / XL 3 / 16,969 turns), faster than its control. The stall was output buffering plus box contention, and the correct move was the boring one — wait for the receipt instead of theorising. Final pair, seed 110, gave the manager its one clean loss (36 vs 216).

**9. Referee pass.** results.json was not taken on trust: the managed-102 morgue header was read directly and matches the recorded receipt field for field (1613, XL 8, 4,461 turns, gnoll sergeant, D:6); the seed-103 fallback pair's two morgue files are **byte-identical** (diff clean) — as are, by score/turns/killer, all 7 fallback pairs including the 17k-turn seed 106. Every game produced a morgue; no game approached either cap (max 16,969 turns vs the 200,000 cap; max 662.7 s vs the 1,800 s wall cap).

---

## Design

- **Arms.** *Control*: qw's stock rc (combo `GrBe.handaxe`, gods Trog/Okawaru/Makhleb, goals `Normal`) — qw's proven default 3-rune plan. *Managed*: same rc machinery with three values replaced by the manager's validated output — starting combo, god preference list, GOALS string. Everything else (the other ~800 rc lines, qw.lua itself) is untouched stock in both arms.
- **Seeds.** 10 fixed seeds, 101–110, DCSS seeded mode (`-seed`). Deterministic per §Process-6.
- **Briefs (fixed before running).**
  - **B1-survival** (101, 102): "Prioritise survival over depth. A long-lived run that dies late and safe beats a fast run that gambles. Avoid optional and dangerous branches, take the safest route to three runes, and value a durable combo and a protective god."
  - **B2-rune-rush** (103, 104): "Rush the first rune. Get to the Lair early, take the first lair-branch rune as soon as the character can fight for it, and do not fully clear optional content on the way. Speed of the first rune is the whole plan."
  - **B3-orb-sprint** (105, 106): "Play for the Orb. Take the shortest sane three-rune route, ignore optional branches entirely, and keep moving down. Every turn spent sightseeing is a turn the dungeon gets stronger."
  - **B4-methodical** (107, 108): "Be methodical. Fully explore each branch in a safe order before moving on, build experience and equipment depth, and only attempt runes with an over-prepared character. No gambles, no shortcuts."
  - **B5-zealot** (109, 110): "Convert early to a powerful god and lean on divine help for hard fights. Choose gods whose active powers carry a run, and shape the route around worship: find an altar fast, then let the god do the heavy lifting."
- **The manager's template.** Exactly three lines: `COMBO:` (one of qw's `species.background.weapon` combos, or STOCK), `GODS:` (1–3 full god names from a 13-god allowlist, or STOCK), `GOALS:` (1–24 comma-separated tokens from qw's real grammar — branch ranges `Branch:N-M`, `Rune:<branch>`, `God:<name>`, and the special goals `Normal, Shopping, Win, Orb, Escape, Hells, Zig`). One worked example in the prompt; `/no_think` set. The farm CLI echoes the prompt into its captured output, so extraction takes the *last* occurrence of each label (visible in the raw artefacts; the parse is recorded per run in `runs/managed-<seed>/manager.json`).
- **Validation.** Mechanical, pre-registered: unknown combo/god/token → the whole config is invalid → stock rc is used and the run is **counted as a fallback** with the validator's reasons kept. No repair, no retry, no second sample: one brief, one call, one verdict — the artefact is the management, repairs would falsify it.
- **Caps, stated and enforced.** Wall cap **1,800 s per game**, enforced by the pty driver (process-group kill; never triggered). Turn cap **200,000 turns**, enforced by post-hoc receipt check with exclusion-from-aggregates as the stated consequence — disclosed plainly: there is no in-game hook that does not touch qw (`ready()` is qw's own, and its state table is chunk-local), so an in-game cap would have meant patching the bot the experiment exists to keep stock. No run exceeded it (max 16,969), so the disclosure is moot for these results.
- **Receipts per run.** Morgue file, score, XL, turns, absdepth (the xlog's own number — the depth at which the run ended, in the Dungeon for all 20 runs), place, god, killer, gold, kills, wall-clock, plus the manager artefact (prompt, raw output, parsed config, validity, validator errors, LLM wall time) for every managed seed.

## Results — per-seed, both arms

| Seed | Brief | Control score | XL | Turns | Depth | Managed score | XL | Turns | Depth | Manager config |
|---|---|---|---|---|---|---|---|---|---|---|
| 101 | B1-survival | 49 | 3 | 1,156 | 2 | **575** | 7 | 3,159 | 3 | VALID |
| 102 | B1-survival | 462 | 7 | 3,968 | 5 | **1,613** | 8 | 4,461 | 6 | VALID |
| 103 | B2-rune-rush | 2 | 1 | 117 | 1 | 2 | 1 | 117 | 1 | fallback |
| 104 | B2-rune-rush | 348 | 6 | 2,801 | 4 | 348 | 6 | 2,801 | 4 | fallback |
| 105 | B3-orb-sprint | 64 | 4 | 1,905 | 3 | 64 | 4 | 1,905 | 3 | fallback |
| 106 | B3-orb-sprint | 49 | 3 | 16,969 | 2 | 49 | 3 | 16,969 | 2 | fallback |
| 107 | B4-methodical | 158 | 5 | 1,661 | 3 | 158 | 5 | 1,661 | 3 | fallback |
| 108 | B4-methodical | 1,405 | 8 | 4,661 | 5 | 1,405 | 8 | 4,661 | 5 | fallback |
| 109 | B5-zealot | 98 | 4 | 2,802 | 4 | 98 | 4 | 2,802 | 4 | fallback |
| 110 | B5-zealot | 216 | 5 | 2,212 | 4 | 36 | 3 | 825 | 2 | VALID |

Fallback rows are identical games by construction (same seed, stock rc) — and verified so, morgues included (§Process-9). They are controls wearing a managed label, and are reported as such everywhere below.

## Aggregates

| | Control (n=10) | Managed (n=10) | Managed, valid only (n=3) vs same-seed control |
|---|---|---|---|
| Median score | 128 | 128 | 575 vs 216 |
| Mean score | 285.1 | 434.8 | 741.3 vs 242.3 |
| Median depth (absdepth) | 3.5 | 3.0 | 3 vs 4 |
| Median turns | 2,506.5 | 2,801.5 | 3,159 vs 2,212 |
| Wins | 0 | 0 | 0 |
| Runes | 0 | 0 | 0 |

Manager production: **3 of 10 configs valid; 7 fallbacks (counted).** Cost per brief: mean **9.3 s** LLM wall on the farm (range 8.5–10.8 s), 93.0 s for the set. Total game wall: control ≈ 796 s, managed ≈ 715 s (seed 106 alone accounts for 1,242 s across both arms).

## One full manager config, verbatim (seed 101, B1-survival, VALID)

What the farm's `llm` emitted (the three config lines, exactly as extracted; full prompt + raw output in `runs/managed-101/manager.json` on the Oracle, copied in `artefacts/manager-101.json`):

```
COMBO: MiFi.waraxe
GODS: Beogh, Cheibriados, Hepliaklqana
GOALS: Normal, Rune:Shoals, Vaults:1-4
```

As written into the run's rc (the surgery that turns the artefact into the game): `combo = MiFi.waraxe`, `GOD_LIST = { "Beogh", "Cheibriados", "Hepliaklqana" }`, `GOALS = {{"Normal", "Rune:Shoals", "Vaults:1-4"}}` — everything else in the rc byte-identical to the control's.

The other two valid configs: seed 102 — `GrHu` / Beogh, Makhleb / `D:1-11, Vaults:1-4, Normal`; seed 110 — `MiFi.waraxe` / Beogh, Hepliaklqana / `D:1-11, Vaults:1-4, Normal`.

## One morgue excerpt, verbatim (managed 102 — the best run of the twenty)

```
 Seeded DCSS version 0.32.1 (console) character file.

Game seed: 102 (custom seed)

1613 qw the Skirmisher (level 8, -5/51 HPs)
             Began as a Gargoyle Hunter on Oct 27, 2026.
             Slain by a gnoll sergeant
             ... wielding a +6 spear of distortion
              (19 damage)
             ... on level 6 of the Dungeon.
             The game lasted 00:00:14 (4461 turns).
```

## Honest verdict

**Did managed qw beat stock qw? On these seeds, as a system: no verdict is available — the arms tie on median score (128 vs 128) because 7 of the 10 "managed" runs never received a manager config at all.** Reporting the managed mean (434.8 vs 285.1) without that sentence would be exactly the kind of number this programme exists not to ship: the entire mean gap is three games.

What the evidence does support, stated at its true strength:

1. **The pattern works mechanically, end to end.** A 0.6B model on a CPU farm wrote declarative configs; a validator gated them; the proven bot played them unattended to real morgues; the fallback path is so clean it doubles as a determinism audit (7/7 identical games, morgues byte-identical where diffed). Nobody patched the bot. The scout's claim — *an agent steers qw today by writing its rc file* — is now a receipt, not a claim.
2. **Where the manager did manage, its leverage was character selection, not strategy.** All three valid configs changed the combo away from stock `GrBe.handaxe` (twice to `MiFi.waraxe`, once to `GrHu`), and the two wins track the combo change: the managed runs lived longer, levelled higher, and scored 3.5–11.7× their controls. The *goals* — the part that is actually strategy — were conservative to the point of timidity: every valid GOALS list still routes through `Normal` or an early-Dungeon descent, and the one distinctive idea (seed 101: take the Shoals rune first) was never tested by play, because the run died on D:3 before any rune branch. The B5-zealot brief's god lists (Beogh first in both valid B1/B5 configs) were never even worshipped — the morgues record no god for any of the three managed runs; each died before qw's altar-driven conversion ever fired. And seed 110 shows the other face: same winning combo family as 101, dead at XL 3 on D:2, 36 points. With n=3, "the manager picks better starting characters than qw's default" is a hypothesis with two supporting receipts and one against — nothing stronger.
3. **The manager's binding constraint is vocabulary precision, not format or reasoning.** All 10 outputs had exactly the three labelled lines in order — the 0.6B model follows the *shape* perfectly. It failed on the *lexicon*: pluralising the grammar's `Rune:` into `Runes:` (5 of 7 failures), inventing tokens (`Shrine`, `Runestone`, `Run:GrHu` — a combo pasted into the goals field), hallucinating a god (`Mgazlal`), and once echoing the prompt's parenthetical *description* of `Normal` as if it were part of the token. These are fixable failures — a tighter prompt (the grammar stated as exact strings, `Rune:` shown mid-list), constrained decoding, or a post-parse suggestion the manager must accept or reject in a second call would each plausibly lift validity well above 3/10 — but every one of those is a *different* manager design, and this experiment's discipline was to measure this one as built.
4. **The field was weak, and that bounds everything.** Stock qw at these seeds scores 2–1,405, never leaves the Dungeon, and takes no runes in 20 games; qw's reputation was earned over full runs on favourable setups, and nothing here contradicts it — but a manager can only be measured against the bot's actual play on the day, and on the day, both arms died young. A rematch on seeds where stock qw reaches the Lair would give the GOALS layer something real to steer.

**Bottom line:** the manager pattern is proven as plumbing and unproven as management. qw accepted a manager's orders through its rc file with zero modification; the 0.6B manager could only write a legal order 30% of the time, and when it did, it managed the *character sheet* better than the *plan*. The next experiment writes itself: same rig, a manager constrained to the exact grammar (or a bigger farm brain), seeds screened for stock qw reaching Lair — and the GOALS list, not the combo, as the only variable.

## Artefacts & reproduction

- On the Oracle, `~/qw-manager/`: `scripts/` (briefs.json, common.py, mkrc.py, drive.py, parse_run.py, run_experiment.py), `runs/<arm>-<seed>/` (rc.txt, manager.json for managed, output.log, driver.log, morgue/, saves/), `results.json`, `results-partial.json` (the in-flight snapshot), `experiment.log`, `qw/` (stock qw @ 8698adc, unmodified), `crawl-032/` (the 0.32.1 build), `crawl-src/` (the rejected 0.34.1 build, kept as evidence), `qw-built/` (the abandoned patch experiment, kept as evidence).
- Local copies in `~/workspace/qw-manager/`: this file, `results.json`, `artefacts/manager-<seed>.json` (all 10 manager artefacts), `morgues/` (the referee-checked morgues: control-101, managed-102, control-103, managed-103).
- Reproduce one game: `python3 scripts/drive.py out.log drv.log 1800 ~/qw-manager/crawl-032/crawl-ref/source/crawl -lua-max-memory 128 -no-throttle -rc <run>/rc.txt -rcdir ~/qw-manager/qw -dir <run> -morgue <run>/morgue -seed <seed>` under any pty. Same rc + same seed → same game.
- Untouched, as ordered: the Oracle's tunnels and the farm service (the farm was called, never reconfigured). Nothing outside `~/qw-manager/` on the Oracle and `~/workspace/qw-manager/` locally.
