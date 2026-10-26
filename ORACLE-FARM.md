# The Oracle CPU farm — SuperInstance

`~/model-farm/` on the Oracle relay (OCI Ampere A1, 4 vCPU Neoverse-N1
aarch64, 23 GiB RAM, CPU only). Registry: `farm.json`. Call layer:
`farm.py` — the same `call(name, input)` shape as the Orin farm, so a
caller treats every farm in the fleet uniformly. Built 2026-10-26 as
the third farm, after the Thor's resident stack and the Orin
micro-model farm.

## Design — what a CPU-only farm tier is for

1. **The relay never sleeps and sits on the fast pipe.** The desk
   boxes sleep, travel, and share a capped house connection; the
   Oracle is always on with ~290 Mb/s cross-country bandwidth. Its
   farm is therefore a *service tier*: small models as gauges that
   agents on any box consult over the wire — digest this position,
   judge this proposed action, embed this note, transcribe this clip.
2. **Slow per call is fine; callers are turn-structured.** Nothing
   here sits in a reflex loop. A digestion that takes six seconds is
   free when the caller is waiting for its next turn anyway — the
   same doctrine as the Orin farm's slow LLM, except this tier's
   callers are separated by networks instead of rooms.
3. **What does not belong here:** anything latency-critical,
   anything GPU-shaped (depth and vision stay on the desk tier,
   where the images originate), anything big, and anything stateful
   that matters. The relay's disk is 45 G and stage-and-forward by
   doctrine; the whole farm is 611 MiB and every member is a
   replaceable, hash-verified artefact.
4. **The remote door is a shim behind SSH, not a new service.**
   `farm_server.py` is a stdlib HTTP shim bound to `127.0.0.1:8770`,
   reached by an SSH tunnel (`ssh -L 8770:127.0.0.1:8770 <oracle>`,
   then `POST /call {"member": ..., "input": ...}`). Chosen over
   per-call `ssh farm.py` for two reasons: the shim holds the ONNX
   sessions warm (a remote judge call answers in 0.01 s instead of
   paying process + load per call), and nothing new is exposed — the
   SSH access a fleet box already has *is* the farm's auth. The llm
   and whisper members still spawn their native binaries per call by
   design; multi-hundred-MB weights do not sit resident on a shared
   relay. `farm.py` on the box remains the local form.
5. **Politeness is a setting, not a hope.** This box also carries
   the fleet's tunnels (slots 2222–2225 and the rest). The LLM
   defaults to 2 of 4 threads; the 1/2/4-thread sweep is measured
   below so a caller who knows the box is idle can override via
   `FARM_LLM_THREADS` with its eyes open.

## The uniform contract

Same members, same weights, same input assembly as the Orin farm
where the member exists on both — verified, not assumed: the judge
returns the *identical* distribution for the same proposed action on
both boxes, and the embedder's vector for a given sentence is
bit-identical across farms. A caller can fail over from one farm to
the other without re-calibrating.

## Roster — receipts (all measured on this box)

| Member | Kind / model | Verdict + receipt |
|---|---|---|
| `llm` | Qwen3-0.6B Q4_K_M GGUF (~0.6B) | WORKS. Digestion prompt → reasoning trace opens correctly on the facts ("raising twice on dry boards, then folded to every re-raise…"). Cold call (128 tok cap, 2 threads) 5.83 s, RSS ~1.10 GB. Generation by threads: **19.4 tok/s (1) · 35.4 (2) · 58.0 (4)**; prompt 59.3 · 114.8 · 221.8. Runtime: llama-cli 0.7.0-dev, the *Orin-built* binaries — real-call verified on Neoverse-N1, no SIGILL (the Orin build targets ARMv8.2 Cortex-A78AE; N1 is ARMv8.2. The Thor build SIGILLing on the Orin is the opposite ISA direction.) |
| `embed` | all-MiniLM-L6-v2 INT8 ONNX (22.7M) | WORKS. sim(ferry schedule, boat timetable) = **0.683** vs sim(ferry schedule, income tax form) = **0.077**. Cold load+call 0.185 s; warm 0.0016 s/call. |
| `judge` | jev-semantic intuition student (6,803,843 params exact) | WORKS. Contract pair: status summary pos 0.374 "lean" vs delete-prod-DB pos 0.121 "settled 0". Cold load+call 0.17 s; warm 0.008 s/call; 0.01 s over the remote door. Weights were already on this box (the intuition-bench payload's original landing place, `~/agent-inbox/`); hashes match the SuperInstance/intuition manifest exactly. |
| `whisper` | whisper.cpp tiny.en (39M) | WORKS. JFK sample → exact transcript in 1.47 s wall on CPU (2 threads). Runtime built natively on this box (whisper.cpp @ 231638a; apt cmake). |

**Side-by-side with the Orin farm** (same member, Orin's registered
figures): llm generation 4.7 tok/s on the Orin's GPU build vs
19.4–58.0 tok/s here by thread count; llm cold call 29.71 s vs 5.83 s;
embed cold 0.34 s vs 0.185 s; judge per-call 0.05 s vs 0.008 s;
whisper 1.5 s (CUDA build) vs 1.47 s. Read directionally — the Orin
numbers are its registered cold smokes, not a controlled same-day
A/B — but the headline stands: **for these micro models the CPU relay
is not the slow tier.** The desk GPU earns its keep on the big,
latency-shaped work; sub-1B gauges run at least as well on the
always-on relay, and they are reachable from everywhere.

## Not stocked (named gaps, same honesty rule as the other farms)

- **Depth (Depth Anything S/L)** — torch `.pth` weights behind a
  CUDA-oriented recipe on the Orin; not ONNX, not trivially portable.
  Vision stays on the desk tier.
- **Pose / face / matte** — ONNX in principle; the artefacts live
  only on the Orin/Thor shelves and no wire caller needs them from
  the relay. YuNet (232 KB) is the cheap future add.
- **Tiny classifier / zero-shot tagger** — the standing gap on every
  farm: no coherent <1B pair exists on any shelf.

Present but not members: LFM2.5-1.2B and LFM2.5-230M GGUFs in
`~/models` (pre-existing residents; the 230M was the ISA test weight),
and a pre-existing ollama listener on 127.0.0.1:11434, which the farm
neither uses nor disturbs.

## Bytes & sourcing

- **Downloaded: 498,094,218 B**, all sha256-verified — the GGUF from
  unsloth/Qwen3-0.6B-GGUF (Qwen's own GGUF repo ships Q8_0 only for
  this model; the unsloth file is byte-identical to the Orin farm's,
  sha256 `ac2d9771…`), whisper ggml from ggerganov/whisper.cpp
  (byte-identical to the Orin's file), MiniLM + tokenizer from
  Xenova/all-MiniLM-L6-v2 (hash matches the Orin registry).
- **Copied on-box: 27,867,112 B** — the judge payload from
  `~/agent-inbox/`, zero network bytes.
- **Copied from the Orin: 40,427,520 B** — the llama.cpp bin dir as a
  tar (an `scp -r` attempt mangled the symlink farm; tar preserved
  it). A direct Orin→Oracle GGUF copy was abandoned at ~98 MB when
  the house uplink decayed to ~1.4 MB/min; superseded by the
  hash-identical fetch above. A 484 MB lmstudio-community Q4_K_M was
  fetched, rejected on size+hash (different quant recipe), deleted.
- **Farm footprint: 611 MiB total** (models 502, llama binaries 39,
  whisper source+build 70) against ~20 GiB free. The fleet's tunnels
  and every running service were left untouched; the shim binds
  localhost only.
