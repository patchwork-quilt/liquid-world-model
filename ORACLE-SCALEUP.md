# ORACLE SCALE-UP — llm-big on the farm + Season 0 replayed at 4×

SuperInstance · Oracle CPU farm (OCI Ampere A1, 4 vCPU Neoverse-N1, 23 GiB RAM) · 2026-10-26

**Headline:** `llm-big` (Qwen2.5-7B Q4_K_M, hashes verified) is registered on the Oracle farm — 3.8 tok/s generation at the polite 2 threads, ~8.9 GiB peak RSS, and the first farm digestion that returns a finished answer instead of a truncated think-trace (27.4 s warm vs the 0.6B's answer-free 14.2 s on the same loaded box). And Season 0's standings **held at 4× the sample**: replay round-robin hoardbox 7.5/8, tickbox 4.5/8, sliver 0/8 — tickbox's fivefold-repetition draw with the champion **replicated exactly** (same colours, same termination), and sliver still never won a game, though it took its first-ever half-point, drawing pawnbox as Black in the controls. One blemish recorded in full: a single RAM-gate FAIL reading against hoardbox in game x4-ab3 (see Job 2).

---

## RESULTS — Job 1: `llm-big`, registered and measured

**Member:** `llm-big` — Qwen2.5-7B-Instruct Q4_K_M GGUF, publisher split (shard 1: 3,993,201,344 B, sha256 `dfce12e3…`; shard 2: 689,872,288 B, sha256 `539cf93f…`; total 4,683,073,632 B), fetched publisher-direct from `Qwen/Qwen2.5-7B-Instruct-GGUF`, **both hashes verified against Qwen's HF LFS records before registration**. Live in `farm.py` (`_call_llm_big`, same contract as `llm`; `-n 256`) and `farm.json`. Default 2 threads (politeness), `FARM_LLM_THREADS` overrides. **Shim caveat:** the :8770 `farm_server.py` was NOT restarted (shared service), so `llm-big` answers via CLI/`call()` only until a sanctioned shim restart. Backups: `farm.py.bak-scaleup-20261026`, `farm.json.bak-scaleup-20261026`. Farm footprint after registration: 5.0 GiB total.

**Measured on CPU (Neoverse-N1, digestion prompt, loaded shared box — see process note 17:02):**

| | `llm` Qwen3-0.6B Q4_K_M | `llm-big` Qwen2.5-7B Q4_K_M |
|---|---|---|
| Generation, 2 threads | 35.4 tok/s *(quiet-box registration)* | **3.8 tok/s** |
| Generation, 4 threads | 58.0 tok/s *(quiet-box)* | 2.6 tok/s *(contended; bandwidth-bound — threads don't buy batch-1 generation)* |
| Prompt, 2 / 4 threads | 114.8 / 221.8 tok/s *(quiet-box)* | 8.8 / 11.6 tok/s |
| Cold call wall (2 thr) | 5.83 s *(quiet-box, 128-tok cap)* | 57.5 s *(first-ever call — includes first-touch page-in of 4.68 GB)* |
| Warm call wall (2 thr, via farm.py) | 14.2 s *(loaded box, same day)* | **27.4 s** |
| Peak RSS | ~1.10 GiB | **~8.9 GiB** (mostly touched mmap weight pages; one call at a time is the polite pattern) |

**The digestion smoke, side by side** (identical input through both members, via `farm.py`): *"Digestion prompt: opponent raised twice on dry boards, then folded to every re-raise; scout caught out of position twice; summarise in exactly two sentences."*

- **`llm-big` (27.4 s):** "The opponent made aggressive raises on dry boards but ultimately folded to every re-raise, while the scout was caught out of position twice, likely indicating poor timing or read errors." — exactly two sentences, facts intact, finished artefact.
- **`llm` (14.2 s, loaded box):** output is entirely its `[Start thinking]` trace — "Okay, let me try to figure out how to approach this. The user provided a digestion prompt and wants a summary in exactly two sentences…" — still mid-deliberation when the -n 128 cap cut it. **The answer does not exist in the output.**

Verdict: llm-big is ~10× slower per generated token and ~2× the loaded wall-clock, and it is the first farm LLM whose digestion call returns a digestion. The 0.6B remains the right member for fast shallow reads; llm-big is the off-turn/night digester the farm doctrine always described, at an honest published price.

---

## RESULTS — Job 2: Season 0 replayed at 4× (18 games)

Same rigging as Season 0 (gates, F=20, 10:00 clock, §6 referee contract), fresh output tree (`season0-replay/`), ≤2 games concurrent at nice 10 on the shared box. 16 games ended in checkmate, 2 in fivefold-repetition draws, **zero flag falls, zero desyncs, zero illegal moves**.

**Round-robin standings — Season 0 (4 games/crew) vs Replay (8 games/crew):**

| Crew | Season 0 | Replay 4× | Pairwise (replay) |
|---|---|---|---|
| hoardbox (Materialist) | 3.5 / 4 | **7.5 / 8** | 4–0 vs sliver · 3.5/4 vs tickbox |
| tickbox (Accountant) | 2.5 / 4 | **4.5 / 8** | 4–0 vs sliver · 0.5/4 vs hoardbox |
| sliver (Minimalist) | 0 / 4 | **0 / 8** | lost every game |

**The order survived variance — and hardened.** Scaled to a per-4-games rate, hoardbox improved slightly (3.5 → 3.75), tickbox eased (2.5 → 2.25), sliver stayed at zero. Combined round-robin across both samples: hoardbox 11/12, tickbox 7/12, sliver 0/12.

**The two questions the bigger sample was bought to answer:**
1. **Does tickbox's draw with the champion replicate? YES — exactly.** x4-ac2 (tickbox White vs hoardbox Black) drew by fivefold repetition, the same colour assignment and the same termination as Season 0's rr-ac2. In the replay tickbox-as-White went draw + loss, tickbox-as-Black 0/2; the draw is a property of the matchup, not a one-off accident.
2. **Does sliver ever take a game off anyone? No win — but its first half-point.** Sliver lost all 8 round-robin games and was mated by pawnbox as White (x4-ctrl-b1, as in Season 0), then **drew pawnbox as Black** (x4-ctrl-b2, fivefold repetition). Across both samples sliver is 0/12 vs crews and 0.5/4 vs the control. The floor is still the floor; it is no longer quite winless-adjacent — it is draw-capable against the baseline when it holds the black pieces.

**Controls (2 per crew vs pawnbox, one per colour):** hoardbox 2–0 (mates both ways; Season 0 had only the White game, also a mate), tickbox 2–0 (same), sliver 0.5/2 (above).

**Per-game terminations:** ab1–ab4 hoardbox mates sliver ×4 · ac1 hoardbox mate · ac2 **draw, fivefold repetition** · ac3 hoardbox mate · ac4 hoardbox mate (as Black) · bc1–bc4 tickbox mates sliver ×4 · ctrl-h1/h2 hoardbox mates pawnbox ×2 · ctrl-c1/c2 tickbox mates pawnbox ×2 · ctrl-b1 pawnbox mates sliver · ctrl-b2 **draw, fivefold repetition**. Full receipts: `receipts.json` + `games/<tag>/`; all 18 PGNs in `pgns/`.

**The one gate incident, unlaundered:** game x4-ab3's receipts record hoardbox peak anonymous RSS at **2,336 KB → RAM gate FAIL**. Every other hoardbox reading across both samples (19 of them) sits at 280–308 KB, and ab3's play was move-for-move ordinary (21 moves, 8.45 host-s — a near-twin of Season 0's rr-ab1 at 300 KB). The runner samples `/proc/<pid>/smaps_rollup` per ply on a busy shared box, and a single-sample pid/measurement artifact is the likely mechanism — labelled a hypothesis, not a finding. What is *not* in doubt: the FAIL stands in ab3's receipts as recorded, because the gate is the gate. Enforced as a forfeit it would flip ab3 to sliver (round-robin: hoardbox 6.5, tickbox 4.5, sliver 1.0) — **the standings order is unchanged either way**, and sliver's only "win" in the books would be a measurement ghost, which is precisely why both readings are published here instead of one being quietly chosen.

---

## PROCESS — documented as it happens (Casey: "the process means more than the product")

**2026-10-26 16:51 AKDT — Lane opened; the model pick, with reasons.**
Job 1 is a bigger digester for the Oracle farm. Pick: **Qwen2.5-7B-Instruct, Q4_K_M GGUF, from Qwen's own HF repo** (`Qwen/Qwen2.5-7B-Instruct-GGUF`). Reasons: (a) the brief names it the safe pick and the box's 23 GiB RAM is exactly what it was waiting for; (b) unlike the 0.6B (whose Qwen repo shipped Q8_0 only, forcing an unsloth mirror), Qwen publishes Q4_K_M for the 7B themselves — publisher-direct sourcing, publisher hash to verify against; (c) ~4.7 GB is a polite guest on an 18 GiB-free stage-and-forward disk; (d) Qwen2.5 instruct tuning is a known quantity in this fleet (the Thor/Orin shelves are Qwen-heavy) and llama.cpp support is bedrock. Qwen3-8B was the alternative; rejected for this registration because its hybrid-thinking default burns the token cap on traces before answers (observed in the farm's own 0.6B member), and digestion callers want the summary, not the soliloquy.

**2026-10-26 16:53 AKDT — Reading the farm before touching it.**
`farm.py`'s `_call_llm` hardcodes the 0.6B path inside the function, so `llm-big` gets its own `_call_llm_big` mirroring the same contract (same llama-cli flags, same return shape), not a refactor of the working member — the 0.6B's behaviour is a measured baseline and stays byte-identical. Registration route is CLI/`farm.json` only: the :8770 shim (`farm_server.py`) holds its dispatch from process start, and the brief forbids restarting it; the shim caveat will be recorded as a known gap, not worked around silently.

**2026-10-26 16:55 AKDT — The publisher ships the 7B split; fetch started.**
HF's blob record for Qwen2.5-7B-Instruct Q4_K_M shows **two shards** (3,993,201,344 B + 689,872,288 B = 4,683,073,632 B total), each with its own publisher LFS sha256. llama.cpp loads split GGUFs natively by pointing at shard 1, so registration stays one member; both hashes get verified — a split file is two chances to be wrong, and the gate applies to each. Fetch launched on the Oracle's pipe into `~/model-farm/models/`, hashes pinned in this lane's notes from the API response *before* the download started (dfce12e3… for shard 1, 539cf93f… for shard 2), so verification compares against the publisher, not against the file's own claims.

**2026-10-26 17:02 AKDT — Measuring on a shared box, and saying so.**
The numbers below were taken with the qw-manager and nethack-chart lanes live on the same 4 vCPUs (load average ~1.8 before I started). That is a deliberate choice, not an accident to apologise for: the farm's members will *always* run on a shared box, so loaded-box figures are the operationally honest ones — but they are not comparable to the 0.6B's quiet-box registration figures without the caveat, and the registry entry carries it in writing. Generation from the 7B is memory-bandwidth-bound (4.68 GB of weights streamed per generated token): threads visibly buy prompt speed (8.8 → 11.6 t/s) and buy nothing for generation (3.8 t/s at 2 threads; the 4-thread run read 2.6 under a contention spike and took 91.8 s wall — recorded, not smoothed). The registered politeness default stays 2 threads.

**2026-10-26 17:05 AKDT — Registration, and the shim line I won't cross.**
`llm-big` is in `farm.py` (new `_call_llm_big`, existing members untouched, `.bak-scaleup-20261026` backups alongside) and in `farm.json` with the measured numbers. The :8770 shim still serves the old four members only — it holds its dispatch from process start, the brief forbids restarting a shared service for a registry change, so `llm-big` is CLI/`call()`-only until a sanctioned restart. Named here and in the registry entry rather than papered over.

**2026-10-26 17:12 AKDT — Fixture ran clean; one reading didn't.**
Relaunched at 01:01 UTC, all 18 games closed by 01:04 UTC — the sim's host-time is short because F=20 makes the *charged* clock the slow one, not the wall. Every game terminated properly (16 mates, 2 repetition draws). The single anomaly is the x4-ab3 RAM reading (2,336 KB vs a 19-reading field of 280–308 KB for the same binary), written up in the Job 2 results rather than explained away here; the likeliest mechanism (per-ply `/proc` sampling on a box running two lanes plus two games) is named as hypothesis. Also worth recording: the two backgrounded ssh deliveries in this lane both arrived *late and out of order* relative to the work they described — the download "completion" landed after I had already re-verified the disk, and the fixture-launch session returned minutes after the games it launched had finished. Anything in this lane that mattered was therefore verified from artefacts on the box, never from session reports. That is now three lanes in one day taught the same lesson by the same harness behaviour; it is in this document so the fourth lane doesn't have to learn it again.

**2026-10-26 17:08 AKDT — Incident: the fixture "completed" in one second, having played nothing.**
First launch reported all 18 games DONE inside a single second. Cause, from the driver log: each game's shell redirect targets `season0-replay/driver-<tag>.log`, a directory only the *runner* creates — the redirect failed before Python ever started, so all 18 "games" were shell errors wearing DONE labels. Nothing was corrupted (no replay directory existed at all), and the false completion was caught by the oldest check there is: chess does not take one second. Fix is one line (`mkdir -p` in the driver before the runs). Recorded because it's the day's second lesson with the same moral as the download: **a completion report is a claim; the artefacts are the record.**

**2026-10-26 17:06 AKDT — Fixture launched.**
18 games (12 round-robin + 6 control) via a driver script that runs ≤2 games at once under `nice -n 10`, each game the unmodified Season 0 rigging (same gates, same F=20, same §6 contract) writing into `season0-replay/`. ETA unknown — tickbox thinks slowly by design — so the lane reports games as they close rather than guessing a finish time.

**2026-10-26 16:57 AKDT — Incident: a "successful" download that wasn't.**
The backgrounded fetch returned exit 0 — and the disk disagreed: shard 1 sat at 3,145,007,104 of 3,993,201,344 bytes with a non-matching hash, and shard 2 didn't exist. The completion report was believed for exactly as long as it took to run `sha256sum`; ground truth was re-established from on-disk sizes and hashes, per fleet doctrine (this exact failure — backgrounded downloads reporting success over partial files — bit the Orin farm seeding earlier today; it is apparently a habit of this harness, not of the pipe). Recovery: resumed shard 1 with `curl -C -`, fetched shard 2 fresh, re-verified. **Both shards now match the publisher's LFS sha256 exactly** (dfce12e3… / 539cf93f…), sizes exact. No registration happened before the gate passed; the gate is the whole point of the gate.

**2026-10-26 16:54 AKDT — Chess replay: don't overwrite history.**
`season_run.py` writes into `~/esp32-chess-box/season0/<tag>/` — Season 0's own receipts live there. The replay gets a copied runner writing to a fresh `season0-replay/` tree with `x4-` tags, so the original season's record is untouched and the two samples stay separable. Fixture arithmetic: 3 pairings × 4 games (colours balanced 2/2) = 12, plus each crew × 2 vs pawnbox (one per colour) = 6 → **18 games**, vs Season 0's 9. Politeness on the shared box: ≤2 games concurrent, `nice -n 10`, because qw-manager and nethack-chart lanes are live neighbours.

