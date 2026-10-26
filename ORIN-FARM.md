# ORIN-FARM — filed copy

The live registry is on the Orin at `~/model-farm/` (`farm.json` + `farm.py` + this document). This copy is the public, timestamped record of the farm as seeded on 2026-10-26; the machine-readable registry as filed is `orin-farm-registry.json` alongside it.

# The Orin Micro-Model Farm

SuperInstance — a shelf of small models on the Jetson Orin Nano Super (8 GB), each
under one billion parameters, each a different *kind*, each callable on demand.
Nothing here runs resident. A system calls the member it needs for the job in
front of it, gets the answer, and the member goes back on the shelf.

- Call layer: `~/model-farm/farm.py` — uniform `call(name, input)` from Python,
  or `python3 ~/model-farm/farm.py <member> <input>` from the shell.
- Registry: `~/model-farm/farm.json` (this document is the human copy).
- Every member below passed one real call on this box on 2026-10-26. Receipts
  are in the registry and summarised at the bottom.

## Roster

| Member | Kind | Model | Params | On disk | Load + one call (this box) |
|---|---|---|---|---|---|
| `llm` | Slow reasoning / digestion | Qwen3-0.6B Q4_K_M GGUF | ~0.6B | 397 MB | 29.7 s cold call; 4.7 tok/s generation, ~1.1 GB RSS |
| `embed` | Text embedding | all-MiniLM-L6-v2 INT8 ONNX | 22.7M | 23 MB | 0.34 s cold; ~0.01 s/sentence warm |
| `judge` | Go/no-go action judge | jev-semantic intuition student | 6.8M (exact) | 27 MB | 0.21 s load, ~0.05 s/call |
| `whisper` | Speech-to-text | whisper.cpp tiny.en | 39M | 78 MB | 1.5 s for an 11 s clip |
| `depth-small` | Monocular depth | Depth Anything V2 ViT-S | 24.8M | 99 MB | 8.9 s wall; 1.2 s inference @1080p |
| `depth-large` | Monocular depth (heavy) | Depth Anything V2 ViT-L | 335M | 1.34 GB | 27.5 s wall; 3.2 s inference @1080p |
| `pose` | Pose estimation | MoveNet Lightning ONNX | ~3M | 9.4 MB | 0.48 s |
| `face` | Face detection | YuNet ONNX | ~0.1M | 0.23 MB | 0.6 s |
| `matte` | Foreground matting | U2Net ONNX | ~44M | 176 MB | 0.5 s load, 1.1 s @320×320 |

Also on the shelf, present but not members: BRIA RMBG (1.0 GB, same kind as
`matte`, uncalled spare) and whisper base.en (callable through the same
whisper-cli binary with a model swap).

## Calling doctrine — per-purpose, swapped in and out

The farm exists because no system needs all of these at once. Call the kind the
moment needs:

- **Reflexes stay tiny and instant.** `judge`, `embed`, `face`, `pose`, `matte`
  all load in under a second and answer in well under one. Treat them as
  always-available senses and reflexes — call them inline, mid-loop.
- **Perception scales to the question.** `depth-small` is the default depth
  sense (1.2 s of GPU). Reach for `depth-large` only when the small model's
  answer is actually load-bearing; it costs ~27 s of swap-in on this box.
- **Slow reasoning is a turn-structure resource.** `llm` generates at 4.7 tok/s
  on CPU — useless mid-action, exactly right where the game gives it time:
  switch it on at the start of a turn, or during the opponent's turn, and let
  it *digest* — read the event log, name the pattern, draft the plan — while
  nothing is waiting on it. Its 30-second cold call is the price of a thought,
  paid out of the other side's clock. (It is a hybrid-thinking model: it
  reasons out loud before answering. Append `/no_think` to the prompt when you
  want the answer without the deliberation.)
- **One heavy member at a time.** This is the desk box: 8 GB shared with a
  desktop and survey work. `llm` (~1.1 GB RSS) or `depth-large` (fp16
  construction + mmap loading, the low-peak pattern from `~/orin-depth/`) at a
  time; the light members can overlap freely.

## Inventories (taken before acquiring anything)

**Thor shelf, artefacts under 1B params:** jev-semantic judge ONNX (6.8M,
copied), Qwen3-0.6B GGUF in `~/models/tiny-smoke/` (copied), whisper tiny/base
(already resident on the Orin), I-JEPA ViT-H (632M but 2.4 GB fp32 — judged too
heavy for this box), CLIP ViT-H vision tower (632M, text tower separate —
couldn't form a coherent zero-shot pair), clip_l text encoder (in the ComfyUI
tree). Everything else on the Thor (LFM2.5-8B, Qwen-Image stack, Nemotron) is
over 1B or parked mid-serve.

**Orin, pre-existing:** Depth Anything V2 ViT-L + its venv
(torch 2.11 + onnxruntime), whisper.cpp CUDA build with tiny.en and base.en,
MoveNet Lightning, YuNet, rembg nets (u2net, bria-rmbg). System python3.12
carries torch 2.14 + onnxruntime 1.31. No llama.cpp and no transformers library
in either environment — the GGUF route was chosen for the LLM because a native
llama.cpp build is a one-time ~10 min compile and then dependency-free forever.

## Deliberately not stocked

A tiny image classifier / zero-shot tagger: the shelf offered no artefact that
forms a working <1B pair (see inventory). Recorded as a gap, not papered over.

## Receipts (one real call per member, 2026-10-26)

- `llm` — digestion prompt (opponent's raising/folding pattern + a scout caught
  out twice, answer in two sentences): opened its reasoning trace correctly on
  the facts ("The opponent's actions: raising twice on dry boards, then folding
  to every re-raise…") — 92 tok/s prompt eval, 4.7 tok/s generation.
- `embed` — sim("The harbour ferry leaves the dock at dawn.",
  "A boat departs the pier early in the morning.") = **0.669**;
  sim(same, "Quarterly tax filings are due next week.") = **−0.005**.
- `judge` — contract go/no-go pair, family assembly: "Delete the production
  database…" → pos 0.353; "Post a short status summary…" → pos 0.487. The
  destructive action scores *less* proceed-worthy than the routine one.
  ⚠️ The Thor serving assembly omits the §4 prefix and reads near-inverted on
  this pair (0.297 vs 0.259) — the skew documented in the Thor's
  INPUT-CONTRACT §5. The farm uses the family assembly on purpose.
- `whisper` — resident jfk.wav → "And so my fellow Americans ask not what your
  country can do for you, ask what you can do for your country." (exact, 1.5 s).
- `depth-small` / `depth-large` — same 1920×1080 overhead photo: plausible
  relative-depth fields (ViT-S mean 2.74; ViT-L mean 132.8 — different raw
  scales, both relative, neither is metres).
- `pose` — 17 COCO keypoints returned for the test photo in 0.48 s.
- `face` — 0 faces, max score 0.106 at threshold 0.9 on a faceless overhead
  harbour photo: a true negative, no false positives. Positive-face validation
  not performed (no sample used).
- `matte` — saliency mask over the test photo: mean 0.194, range 0–0.996.

## Bytes

- New downloads: **122,902,465 B** (depth-small 99.2 MB, embedder 23.0 MB,
  tokenizer 0.7 MB), each verified against its publisher sha256. Fetched
  directly on the Orin (house pipe; total well under the 1.5 GB target).
- Copied over the LAN from the Thor: **424,575,206 B** (Qwen3 GGUF + judge
  payload; judge hashes match the SuperInstance/intuition manifest).
- Build inputs: cmake via apt and a llama.cpp source clone (tree now 369 MB
  including build artefacts) for the native Orin llama-cli.

## Blockers and traps found (unlaundered)

- **Thor-built llama.cpp binaries SIGILL on the Orin** (Thor's ggml-cpu is
  compiled for a newer ARM ISA than the Orin's Cortex-A78AE). Copied, crashed
  (exit 132), deleted; replaced by a native build on the Orin.
- **llama-cli hangs after generating** in interactive mode when stdin stays
  open; the farm always calls it with `-st` (single-turn) and stdin closed.
  An early smoke was also OOM-killed (rc 137) while the llama build was still
  running — memory contention, not a model fault; it passes cleanly since.
- **HF's API returns 401 unauthenticated** from both the Orin and the staging
  VM; model files themselves resolve fine, and authoritative hashes were taken
  from the resolve endpoint's `x-linked-etag`.
- **Depth Anything fp16**: the model's `infer_image` feeds fp32 into fp16
  weights and throws; the farm's helper follows the resident recipe —
  `forward(image.half())` — for both depth members.
- **The `thor-lan` SSH alias is broken from the Orin** (`thor.local` doesn't
  resolve there); LAN copies used `caseydigennaro@192.168.0.78` directly.
- **YuNet's ONNX outputs** are grouped by type across strides (cls_8/16/32,
  obj_…, bbox_…, kps_…), not interleaved per stride; farm.py's decoder indexes
  them accordingly.
