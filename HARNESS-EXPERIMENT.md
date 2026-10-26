# The Harness Experiment — how far down can the model go?

SuperInstance Orin micro-model farm, 2026-10-26. Question (Casey's):
can we run models that *barely function* if the harness around them
is sophisticated enough? Method: stock the farm with two genuinely
tiny instruct models, build a real harness around them, and A/B it
against the bare models and against the farm's bigger LLM with no
harness.

## Headline

**At 135M the harness buys +2 points out of 40 (14 vs 12) at 3.5×
the wall-clock and ~4× the calls. At 360M the same harness is a
liability: −16 points (6 vs 22). The bare 360M, no harness at all,
beat every other arm — including the bare 0.6B reference (17).**

The harness's wins are *task-shaped*, not size-shaped: it rescues
tasks where the bare tiny model fails by echoing the input or
drifting off-format (classification, one digestion, one extraction),
and it destroys tasks where the bare model already has the right
instinct (direct JSON answers), because the harness's rigid
intermediate representation gives a mimicry-prone model something
to parrot instead of the task. There is no model size in the
135M–0.6B band where this harness dominates. Details and receipts
below; nothing is hidden, including the two times the experiment
itself broke before the models did.

## The new farm members

| Member | Model | Bytes | sha256 |
|---|---|---|---|
| `llm-tiny-135` | SmolLM2-135M-Instruct Q8_0 GGUF (bartowski quant of HuggingFaceTB weights) | 144,811,360 | `5a139571…bba83` ✓ vs HF x-linked-etag |
| `llm-tiny-360` | SmolLM2-360M-Instruct Q8_0 GGUF (bartowski quant, same note) | 386,405,280 | `c004ac34…84b7b` ✓ vs HF x-linked-etag |

Registered in `farm.json`, callable through `farm.py` on the same
llama-cli route as `llm`. Substitution, stated: the official
HuggingFaceTB 135M GGUF repo path returns 401 from this box, and the
official 360M file's Xet route truncated deterministically at
106,573,824 of 386,404,992 bytes (4/4 attempts); the bartowski repo
carries quants of the same official weights and its 360M was fetched
in 40 MB Range chunks after single-stream transfers kept dying
(curl rc 18). Net new model bytes installed: 531,216,640. Gross
bytes fetched were roughly 3× that, wasted on truncated transfers —
the pipe's single-stream fragility, recorded here because it ate an
hour. An early mishap compounded it: two orphaned curl processes
from backgrounded download commands kept rewriting the 360M file
concurrently and corrupted two verified installs before they were
found in `ps` and killed. All installs were re-verified by sha256
after the writers were dead, and again before the suite ran.

Smoke verdicts: both models load and answer on-topic. Asked to "say
the word harbour and nothing else", the 135M replied *"The word
'harbour' is not available in the dictionary."* and the 360M
defined the word instead of saying it. These are barely-functioning
models; that is the point of the experiment.

## What the harness contributes (harness.py)

A bare tiny model fails in predictable ways: it echoes the input,
loses the required format halfway, drops facts, or collapses into
repetition. The harness carries the structure the model can't:

1. **Decomposition in code.** Every task is pre-split into small
   numbered steps (facts first, format last), one model call per
   step, each step asking for one small thing.
2. **Few-shot scaffolds.** Each step type (extract-facts,
   pick-fields, compare, classify, json-fill, bullets, sections)
   carries two worked examples; the model copies a shape instead of
   inventing one.
3. **Gauge calls between steps.** The farm's own micro-members
   grade every draft step before it may flow downstream:
   `embed` (MiniLM cosine between the draft and a declarative
   statement of the step's intent; pass ≥ 0.20) and `judge`
   (jev-semantic go/no-go on the draft as a proposed result; pass
   at pos ≥ 0.25). A failed gauge returns its verdict in words —
   *"a checker would not let this proceed (judge pos 0.19…)"* —
   inside a bounded retry (max 2 retries per step).
4. **Assembly + deterministic validation.** A final model call
   formats the step outputs; a code validator (JSON keys, bullet
   counts, section order, label pattern) checks the result and one
   retry carries the validator's error back to the model.

Contract: `Harness.run(model, task)` returns the same final text a
bare call would, plus full receipts. Sampling is deterministic
everywhere (temp 0, seed 42).

**Runner note (a deviation, stated):** the suite executes through
`llama-completion` from the farm's own llama.cpp build, with the
ChatML template applied explicitly and identically for every arm —
not through llama-cli. Reason: llama-cli's interactive UI writes a
banner and a `> `-prefixed, wrapped prompt echo into stdout, and
run 1's capture parser silently failed on long prompts, so
"outputs" included the echoed *input* — which itself contains
rubric keywords. **Run 1 was invalidated and discarded for exactly
this reason** (its flattering bare scores were partly the scorer
grading the prompt). The farm registration of the tiny members
still uses the llama-cli route, as specified; only the experiment
runner needed parseable output. All numbers below are run 2.

## The suite and the rubric

8 tasks in the fleet's real shapes: 2 digestions (a poker hand log;
RTS scout reports → exactly 3 bullets naming the facts that matter),
2 extractions (messy harbour/maintenance notes → exact-key JSON),
2 consistency comparisons (conflicting report pairs → AGREE: /
CONFLICT: sections), 1 strict-format JSON, 1 four-message
classification in exact `N: LABEL` lines. Scoring is deterministic
code (`suite.py`), identical for all arms: per task, one point per
required fact/field/label found correct plus one format point
(format = the task's validator passes). Max 40 points total.

**Rubric limitation, stated:** fact points are keyword-presence
checks. They cannot see *misattribution* — a bullet that names the
right numbers attached to the wrong player still scores. Read the
verbatim outputs below with that in mind; the rubric measures
coverage and format, not full correctness.

**Gauges as scorers:** the judge member is *not* used for final
scoring — its contract is go/no-go on proposed actions, not answer
grading. Final scoring is the deterministic rubric. The judge works
inside the harness, where its contract fits.

## Results (run 2, deterministic)

| Task (max) | A135 bare | B135 harness | A360 bare | B360 harness | C600 bare |
|---|---|---|---|---|---|
| digest-poker (4) | 3 | 3 | 3 | 1 | 2 |
| digest-scout (4) | 0 | **3** | 3 | 2 | 3 |
| extract-ferry (6) | 0 | **2** | 0 | 0 | 0 |
| extract-maintenance (7) | 0 | 0 | **7** | 0 | 0 |
| consistency-gate (5) | 2 | 2 | 2 | 1 | 3 |
| consistency-server (5) | 3 | 0 | 3 | 2 | 1 |
| format-status (4) | **4** | 1 | **4** | 0 | **4** |
| classify-messages (5) | 0 | **3** | 0 | 0 | **4** |
| **Total (40)** | **12** | **14** | **22** | **6** | **17** |
| Wall-clock | 15.0 s | 52.8 s | 20.7 s | 88.3 s | 91.8 s |
| Model calls | 8 | 31 | 8 | 27 | 8 |
| Gauge calls | 0 | 32 (16 embed + 16 judge) | 0 | 24 (12 + 12) | 0 |

## Verbatim — the digestion task, all five arms

**A135 (3/4)** — real bullets, four of them (format point lost),
facts partly garbled:
```
- Mara raises on a dry flop; hero folds.
- Mara raises on a wet flop; hero re-raises; Mara folds at once.
- Hero's stack has fallen from 1200 to 840 chips.
- Mara raises on a dry flop; hero calls; Mara bets big on the turn and hero folds.
```

**B135 (3/4)** — the assembly regurgitated the step dump with hands
scrambled (Mara "raises on a wet flop" in all four); keywords score
it anyway — the rubric limitation above, in the flesh:
```
[facts] Hand 1: Mara raises on a dry flop; flop is dry (King, 7, 2, all different suits); hero raises on a wet flop; flop is wet (two hearts, connected cards); hero calls; Mara bets big on the turn and hero folds. Hand 2: Mara raises on a wet flop; … Hand 4: Hero's stack has fallen from 1200 to 840 chips. …
```

**A360 (3/4)** — clean, exactly 3 bullets (one misattribution:
the stack is the hero's, not Mara's):
```
- Mara's stack has fallen from 1200 to 840 chips.
- Mara raised on a dry flop, but the hero re-raised.
- Mara folded at once.
```

**B360 (1/4)** — assembly collapsed into a repetition loop:
```
- Mara raised on a dry flop (two hearts, connected cards)
- Mara folded at once
- Mara's pattern: 2-2-2-2-2-2-2-2-2-2-2-2-2-… (hundreds of repetitions)
```

**C600 (2/4)** — the 0.6B thinks out loud inside its answer; the
320-token budget ran out mid-deliberation and only 2 bullets
landed:
```
<think>
Okay, let's see. The user wants a situation summary in three bullet points…
</think>
- The hero's stack fell from 1200 to 840 chips, indicating a significant loss.
- The wet flop in hand 3 and the hero's call suggest a need to reassess the board's strength.
```

## Why the harness lost where it lost — the echo-parrot failure

The receipts name the mechanism. In the harness's `pick_fields`
step, the prompt ends: *"write the fields in this exact style:
Fields location=...; equipment=...; …"*. The tiny models — 360
included — repeatedly **copied the instruction line itself as their
answer**, literal `...` placeholders and all. The judge gauge
correctly failed these drafts (pos 0.17–0.27), the harness retried
with the verdict attached — and at temp 0 the model produced the
same parroted line again, three times, deterministically. The
assembly then faithfully formatted the placeholders, wrapping them
in a `{"fields": {…}}` object the validator rejected, or inventing
values (`"status": "active"`, bays `"rope1"` — imported from the
few-shot example about ropes). Bare, the same 360M asked directly
for JSON produced a perfect 7/7 extraction. The scaffold didn't
support the model; it gave a mimic a better thing to mimic than
the task.

Where the harness won, the mechanism is the mirror image: bare
135M *echoed the input verbatim* on classify-messages (it returned
the four messages unchanged, 0/5). Inside the harness, the
classify scaffold's examples broke the echo and the step produced
three correct labels (embed sim 0.71 — the gauges' highest reading
of the day). The assembly then dropped message 4, two validator
retries couldn't restore it, and the task landed at 3/5 — the
harness giveth at the step layer and taketh away at assembly.

Other honest entries in the ledger:

- **The gauges are weak tea as graders.** The jev judge's pos for
  genuine drafts sat at 0.17–0.49 — its "ignorance/lean" band —
  and it passed some scrambled content (B135's poker facts at
  judge pos 0.89 in run 1's contaminated capture; in run 2 its
  readings on real drafts never separated good from garbled
  sharply). Embed similarity was the more honest gauge (0.71 for
  the good classify step, 0.12–0.19 for parrots and off-topic
  drafts). A future harness should gate on embed + code validators
  and treat the judge as a tripwire, not a critic.
- **Retries at temp 0 are nearly free of value** when the failure
  is mimicry: the model repeats itself. Retry prompts changed the
  output only when the failure was format, not when it was
  parroting. (Format retries did work: B135 classify assembly
  attempt 1 recovered 3 valid lines from an empty attempt 0.)
- **The 0.6B control is hobbled by its own deliberation** in raw
  completion mode: `<think>` output consumed the budget on both
  extraction tasks (0/6, 0/7 — no JSON ever emitted). That's a
  harness-shaped fact about the bigger model too: the farm's
  llama-cli route and a `/no_think` convention exist precisely to
  manage it. "Bigger model, no harness" is not a free lunch either
  — it is a different harness dependency.
- **Speed is not the tiny models' problem.** Bare 135M answered
  all 8 tasks in 15 s total; bare 360M in 21 s. The harness's cost
  (3.5–4.3× wall) is real money spent on calls and gauges, and at
  360M it bought a worse answer.

## Verdict

**How far down can the model go?** With *this* harness: the floor
is where it started. At 135M the harness is roughly break-even —
+2 points, paid for with 23 extra model calls, 32 gauge calls and
38 extra seconds — rescuing echo-failures and squandering
format-wins in about equal measure. At 360M it is strictly
harmful. The compensation point this brief asked about was never
reached, because the harness's failure mode (scaffold mimicry +
a rigid intermediate representation) grows exactly as the model's
mimicry gets stronger than its task sense.

That is a finding about harness *design*, not a verdict on the
idea. The receipts point at the harness this experiment argues for
next: **less scaffold, more code** — skip the natural-language
intermediate representation entirely (let steps return values the
*code* slots into the format, so assembly is deterministic, not a
model call); gate steps on embed similarity and validators only;
retry with temperature or a changed scaffold, never with the same
prompt plus a scolding; and spend the saved calls on the one thing
that demonstrably helped — worked examples for the step where the
bare model echoes. The models are cheap and fast. The intelligence
has to live in the piping, and the piping has to not be made of
prompts the model can parrot.

## Files

`harness.py` (the harness + runner primitives) · `suite.py` (tasks,
validators, rubric) · `run_ab.py` (arm runner) · `results.json`
(full receipts: every step attempt, gauge reading, and output for
all five arms) · this file. All in `~/model-farm/` on the Orin,
copies in `~/workspace/lwm-orin-harness/`.
