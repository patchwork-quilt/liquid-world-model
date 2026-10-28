# ORIN GPU, LIT — the farm's `llm` gets its GPU

**Headline: full GPU offload takes `llm` from 37 to ~71 tok/s generation (1.9× today's CPU, 15× the figure in the registry), prompt eval from ~180 to ~1,118 tok/s (6.2×), and the farm call from a registered 29.7 s to 3.59 s end-to-end through farm.py. The registered call is now the CUDA build at `-ngl 99`. Partial offload is a trap on this box — 14 of 28 layers generated at 12.5 tok/s, three times *slower* than pure CPU — and the registry's 2026-10-26 CPU numbers did not reproduce (see Process, item 2).**

SuperInstance · Jetson Orin Nano Super (8 GB unified) · 2026-10-27

## Results

All runs: the farm's exact flags (`-t 6 -c 2048 -n 128 --temp 0.7 --no-warmup -st`), the farm's registered digestion prompt verbatim, rates as printed by llama-cli itself, wall by process timer.

| Form | Gen tok/s | Prompt tok/s | Wall (128 tok) | GPU seen |
|---|---|---|---|---|
| Registered 2026-10-26 (CPU build, `-ngl 0`) | 4.7 | 92.1 | 29.71 s cold | n/a — binary had no GPU backend |
| CPU `-ngl 0`, re-measured today, cold (drop_caches) | 36.6 | 180.3 | 5.93 s | GR3D 0% |
| CPU `-ngl 0`, re-measured today, warm | 37.3 | 167.8 | 5.82 s | GR3D 0% |
| GPU partial `-ngl 14` (14/28 layers) | **12.5** | 350.3 | 12.22 s | GR3D max 46% |
| GPU full `-ngl 99`, first run | **70.8** | 1,118.3 | 3.58 s | GR3D max 91% |
| GPU full `-ngl 99`, warm | **72.7** | 1,231.0 | 3.32 s | GR3D max 92% |

- **Device receipt:** `llama-cli --list-devices` → `CUDA0: Orin (7485 MiB, 3176 MiB free)`. During the full-offload run, tegrastats (250 ms interval) recorded `GR3D_FREQ 91%@[1007]` with system RAM at 5,310/7,485 MB — the GPU working, in numbers, not by assumption.
- **Memory:** GPU-form process peak VmRSS 1,225,520 kB (~1.2 GB, `/proc` probe at `-n 1024`) vs the CPU form's registered 1,083,120 kB. tegrastats system RAM across both full-offload runs stayed in 4,907–5,323 MB of 7,485 — roughly 2.2 GB of headroom at the peak sample, on the live desk box.
- **End-to-end proof of the registration:** after the farm edits, `python3 ~/model-farm/farm.py llm "<digestion prompt>"` returned in **wall_s 3.59** with the model's normal think-trace text; `farm.py judge …` answered in 0.4 s, untouched.

## What was registered (the standing docs, updated in place)

- **farm.py** — `_call_llm` only: binary → `src-llama/build-cuda/bin/llama-cli`, `-ngl 0` → `-ngl 99`, with a comment recording the partial-offload trap and the CPU fallback. `_call_llm_file` (the tiny members) and every other member are untouched.
- **farm.json** — `llm.call` rewritten; `llm.measured` replaced with today's (cold wall 3.58 s, gen 70.8, prompt 1,118.3, RSS 1,225,520 kB); a new `llm.gpu_recheck_2026_10_27` object carries the full table, the tegrastats windows, and the note about the unreproduced 2026 figures; the smoke verdict keeps its original text with a dated addendum appended.
- **FARM.md** — roster row updated; the "Slow reasoning" doctrine bullet rewritten (role unchanged, price changed; both measured warnings ride with it); the receipts bullet keeps the 2026-10-26 text and gains a dated "Superseded 2026-10-27" line.
- **On-box additions:** `src-llama/build-cuda/` (the CUDA build tree; the original `build/` is untouched) and `llama-build-cuda.log`. Backups of all three edited files sit beside them as `*.bak-gpu-20261027` — see Process item 5 for their one honest caveat.

## Desk check

This is Casey's front room; the constraint outranked speed throughout. One call at a time, registered context (2048) never raised, compile at `-j 4` of 6 cores. gnome-shell alive at every check including the last; system RAM peaked at 5,323/7,485 MB during GPU runs and sat at 5,214 used / 2,271 available after; **zero OOM events on 2026-10-27** — the newest dmesg OOM lines are ~31 hours old (a llama-cli and a python from the farm-build era, uptime 338,360 s/338,657 s vs ~449,700 s now) and are not this lane's. Nothing from this lane is left running. No edge search was needed: at ~1.2 GB RSS against 3.2 GB free device memory, full offload of a 397 MB model is nowhere near the 8 GB edge — the one deliberate step toward it (partial offload first) is what produced the trap finding instead.

## Process — written as the work happened

1. **The registered binary could not have used the GPU at all.** First check of the day: `farm.json` says `-ngl 0`, and the suspicion was that flipping the flag would suffice. It wouldn't have. `build/CMakeCache.txt` records `GGML_CUDA:BOOL=OFF`, `build/bin/` holds `libggml-cpu.so` and no CUDA backend, and the binary says so itself on every run: *"warning: no usable GPU found, --gpu-layers option will be ignored / one possible reason is that llama.cpp was compiled without GPU support."* The farm's brain wasn't running with the GPU switched off; it was built without one. So the lane became a build, in the farm's own tree: same source, new `build-cuda` dir, `GGML_CUDA=ON`, Release, `llama-cli` target only.
2. **The baseline refused to match the registry.** Re-measured cold (after `drop_caches`) the CPU form ran 5.93 s wall / 36.6 tok/s generation — nowhere near the registered 29.71 s / 4.7 tok/s. This was checked rather than smoothed over: same binary, same flags, same prompt verbatim, two runs (cold 36.6, warm 37.3). The 2026-10-26 figures were taken on farm build day, with the box compiling and swapping members; that is the suspected cause, but suspicion is not a measurement, so the registry and FARM.md now say exactly that — *did not reproduce; cause not established; superseded, not explained.* (One consequence worth naming: against the *registered* number the GPU looks 15× faster; against *today's actual CPU* it is 1.9×. Both are in the table; the honest headline is the 1.9×.)
3. **First configure failed on PATH, not on CUDA.** CMake found no CUDA compiler because `/usr/local/cuda/bin` isn't on the non-interactive shell's PATH; nvcc (CUDA 13.2) was on the box the whole time. Fixed by passing `-DCMAKE_CUDA_COMPILER=/usr/local/cuda/bin/nvcc` explicitly. The build then ran ~25 minutes at `-j 4` — deliberately not `-j 6`: nvcc instances are the RAM-hungry part and this is the desk box (system RAM touched 5.6 GB used mid-build, no swap storm, desktop fine).
4. **Partial offload was tried as the step toward the edge, and it is the day's cleanest negative.** `-ngl 14`: prompt eval doubled (350 tok/s) but generation fell to 12.5 tok/s — on unified memory, split layers pay sync and launch costs per token while gaining nothing in bandwidth, since CPU and GPU drink from the same LPDDR. GR3D averaged 9.8%: the GPU was mostly waiting. Full offload (`-ngl 99`) inverted everything: weights resident, GR3D peaking at 91–92%, generation ~71 tok/s. The rule now written into farm.py's comment and FARM.md: **on this box, full offload or none.**
5. **A shell-quoting accident ate the pre-edit backups; they were reconstructed and the reconstruction is disclosed, not hidden.** The first registration command died at local bash parse time (nested heredoc quoting) — before the remote `cp` backups ever executed — but the *edits* in the follow-up run were applied without re-checking that the backups existed. The `.bak-gpu-20261027` files were therefore rebuilt by exactly reversing the anchor-asserted edits, and verified: the reconstructed `farm.json.bak` parses, and its `llm.measured` equals the pre-edit values field-for-field (29.71 / 4.7 / 92.1 / 1083120) with no recheck object present. The live files were never at risk (every edit asserted a unique anchor before replacing), but the backup chain has this seam in it and the record says so.
6. **Small measurement notes, kept:** this llama.cpp build prints its rates to *stdout* (`[ Prompt: X t/s | Generation: Y t/s ]`) and writes nothing to stderr in the CUDA form — an early grep for the older `llama_perf_context_print` wording found nothing and briefly looked like missing timing data; the rates were in stdout all along. tegrastats on this box has no `--count` flag; it was run under `timeout`/SIGINT windows instead. A backgrounded SSH wrapper and two long `sleep` check-ins died at the tunnel layer during the build wait (exit 255, no output) — the build itself, being `nohup` on the box, never noticed; progress was always read from `llama-build-cuda.log` on the box, never from the tunnel's health.

## Files

- This report + `results.json` (full machine-readable tables, tegrastats excerpts, desk-check record) — programme workspace `~/workspace/orin-gpu/`.
- On the Orin: `~/model-farm/farm.py`, `farm.json`, `FARM.md` (edited, registered form live), `*.bak-gpu-20261027` (pre-edit state), `~/model-farm/src-llama/build-cuda/` + `~/model-farm/llama-build-cuda.log` (the CUDA build and its log).
