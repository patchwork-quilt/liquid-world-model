# qw Arm 5 — Nemotron, think-off: the report gets filed, and it is the prompt's own example

**Headline: pulling the lever RESIDENTS named works completely — and what it reveals underneath is the most deferential manager the bench has ever measured. With Ollama's API-level `think: false`, nemotron-3.5-lightning goes from 0/10 valid (arm 4: no artefact at any budget) to 10/10 valid, every call finishing cleanly (`stop`, 60–88 tokens — the answer itself, not the 512-token budget). But the unblocked channel delivers the prompt's worked example nearly whole: example GOALS verbatim in 9/10 configs, distinct answers collapsed to 3 of 10, stock combo and stock gods in 8/10. Its single deviation — the first valid combo change since arm 1, `GrHu` on the zealot pair — changed both its games, and lost both (91 vs 98; 37 vs 216). The nonemission was a costume. Underneath it was the deferent, plus one deviation aimed at the wrong line of the form.**

Setting: the identical bench to rounds 1–4 (`manager-bench.py`, the continual script filed with RESIDENTS.md), one variable changed against arm 4. Manager: **nemotron-3.5-lightning:latest** on the Thor's Ollama (:11434), temperature 0, `num_predict` 512, same 10 seeds (101–110), same 5 frozen briefs, same prompt byte-for-byte, same mechanical validator, same Oracle game rig (DCSS 0.32.1, stock qw @ 8698adc). The single change: the /api/chat payload carries `"think": false` — Ollama's API-level thinking switch. Worth stating precisely because the frozen prompt already ends with the literal string ` /no_think` in *every* arm: arm 4 ignored the prompt-level hint and deliberated forever; arm 5 tests the switch, not the hint. Control receipts are round 1's, reused after the determinism spot-check reproduced exactly for the **fourth consecutive round** (seed 101: 49 / XL 3 / 1,156 turns / iguana — MATCH).

---

## PROCESS — how this was actually done, in the order it happened

*Casey's doctrine (2026-10-26): "Document well as you go. The process means more than the product." This section folds in the running log (PROCESS-LOG.md beside this file), dead ends and failures at the same care as the successes.*

**1. History first.** RESIDENTS.md (arms 3–4), its process log, and its results read in full; the bench script read end to end before anything was touched. Arm 4's failure, carried forward exactly: content channel empty on 10/10 calls, `finish_reason: length` on 10/10, `eval_count` exactly 512 on 10/10; a disclosed 4,096-token probe still empty (64.4 s, 13,757 chars of unterminated thinking); a diagnostic showing the thinking is a numbered restatement of the assignment, still on step 1 at budget's end. RESIDENTS named Ollama's think toggle as the untried lever and deliberately did not pull it — each reconfiguration is a new arm. This is that arm.

**2. Endpoint inventory.** Thor Ollama 0.40.9; `/api/tags` lists `nemotron-3.5-lightning:latest` (nemotron_h_moe, 32.9B Q4_K_M, capabilities include "thinking") — arm 4's receipted id. The bench's md5 (`c27305e2…`) was identical on the VM, the Thor and the Oracle before work began.

**3. Transport smoke (one call, disclosed, not an arm sample).** "Reply with exactly: OK", temp 0, num_predict 512, `think: false`: content `'OK'`, thinking channel empty (0 chars), `done_reason: stop`, `eval_count` **2** — against arm 4's smoke with thinking on, which also answered 'OK' but at `eval_count` 99. The lever does what Ollama documents. One cost, receipted rather than smoothed: the smoke's wall was 74.4 s for a 2-token reply, because the 25 GB model had been unloaded after idle (Ollama's keep-alive expiry) and the call paid the cold load.

**4. The bench extension — minimal, transport-only, proven.** The filed bench had no way to send the think flag, so it was extended — in a copy (`~/workspace/qw-arm5/manager-bench.py`), never in place; the filed bench is untouched everywhere it lives. The whole change (~40 diff lines, all outside the vendored segment): `call_ollama` gains a `think=None` parameter — when not None it is sent as the top-level `think` field of /api/chat and recorded in the receipt's endpoint_meta; when None, no field is sent and the payload is exactly arms 3–4's. `call_openai` accepts the parameter for symmetry and ignores it (that API has no such switch). `ask_manager_http` passes it through. `gen` gains `--think true|false`, parsed to a bool, recorded in arm.json (`"think": false` is in arm 5's). Rig integrity was then re-proven, not assumed: the vendored segment (vocabularies + PROMPT + validator) is still 5,616 bytes and byte-identical to the filed bench's; the rounds 3–4 differential script, pointed at the extended bench on the Oracle, reports **PROMPT byte-identical (1,469 chars), validate() 27/27 identical verdicts** (all 20 historical raw outputs + 7 synthetic chat-shaped variants), **selftest 10/10** — VERIFY OK, and selftest 10/10 again on the Thor copy. Extended bench md5 `5907d4b975a262b8485a1745b0bbd109`, identical bytes on VM, Thor and Oracle.

**5. Generation (Thor, sequential, one call per brief, no retries).** Ten calls, and the story inverted arm 4's on the first one: VALID, `finish_reason: stop`, `eval_count` 88 — a complete three-line config, the deliberation simply absent. All ten followed: 10/10 valid, eval counts 60–88 (the answer's own length), generation proper 0.79–1.11 s per call by the endpoint's own `eval_duration`. The shape was visible by seed 103 and never changed: the prompt's worked-example GOALS returned verbatim, stock combo, stock god trio — until the B5-zealot pair, which changed the combo to `GrHu` on both seeds while keeping the stock gods. Manager-phase wall total 281.3 s is receipted but must be read with its caveat (§Caveats): per-call walls ranged 1.74 s to 87.18 s for near-identical outputs on a Thor shared with concurrent lanes that night; the generation-only figure is ~1.04 s/brief, ~10.4 s for the arm.

**6. Play (Oracle).** Artefacts travelled Thor → local → Oracle with the files verified at each hop; play ran detached in a new bench root (`~/qw-arm5` on the Oracle), so the spot-check ran fresh for this root and MATCHed (see Setting). The launching SSH session hung on the detached child's output pipe — the fleet's known pattern — and was torn down from this side; the Oracle pipeline was verified alive by process listing and its growing log, and finished unattended. Game wall total 701.2 s (seed 106's marathon: 576.4 s), in line with arms 3–4 (~710 s).

**7. Referee pass.** The census was computed from the results file with RESIDENTS' ruler (census.py beside this file), not read off the gen output. The two games that differ from control are exactly the two `GrHu` configs, and the morgues prove the deviation was really played: arm seed 110 *"Began as a Gargoyle Hunter"* (796 turns) against control 110 *"Began as a Gargoyle Berserker"* (2,212 turns). The other eight games match control on all six receipted fields (score, XL, turns, killer, gold, kills).

**8. Call accounting.** Thor generation calls by this lane: 11, all sequential (1 disclosed smoke + 10 arm briefs). No Thor service was restarted, reconfigured, or loaded/unloaded by this lane.

---

## Results — per-seed, arm 5

Control is round 1's column, reused under the spot-check. ✓ = valid config · (=) = game identical to control on all receipted fields.

| Seed | Brief | Control | A5 Nemotron think-off |
|---|---|---|---|
| 101 | B1-survival | 49 | 49 ✓ (=) |
| 102 | B1-survival | 462 | 462 ✓ (=) |
| 103 | B2-rune-rush | 2 | 2 ✓ (=) |
| 104 | B2-rune-rush | 348 | 348 ✓ (=) |
| 105 | B3-orb-sprint | 64 | 64 ✓ (=) |
| 106 | B3-orb-sprint | 49 | 49 ✓ (=) |
| 107 | B4-methodical | 158 | 158 ✓ (=) |
| 108 | B4-methodical | 1,405 | 1,405 ✓ (=) |
| 109 | B5-zealot | 98 | 91 ✓ — `GrHu`: changed, **lost** |
| 110 | B5-zealot | 216 | 37 ✓ — `GrHu`: changed, **lost** |

**Arm 5's pairwise record: 0 wins, 2 losses, 8 ties** — the mirror of arm 3's 0-0-10. Arm 3 never lost a game because it never changed one; arm 5 changed two, and lost both.

The configs themselves, in full — there are only three distinct answers:

- **×7** (101, 103–108): `COMBO: GrBe.handaxe` / `GODS: Trog, Okawaru, Makhleb` / `GOALS: D:1-11, Lair, D:12-15, Orc, Rune:Shoals, Rune:Snake, Vaults:1-4, Depths, Vaults:5, Shopping, Zot:1-4, Win` — the stock combo, the stock gods, and the prompt's worked example, character-for-character.
- **×1** (102): the same, with GOALS shortened to `D:1-11, Lair, D:12-15, Orc, Shopping, Zot:1-4, Win` — the example with its two `Rune:` dives and the Depths return edited out.
- **×2** (109, 110): `COMBO: GrHu` / stock gods / the example GOALS verbatim.

## The five-point posture curve

| | A1: Qwen3-0.6B (farm, temp 0.7) | A2: Qwen2.5-7B (farm, temp 0.7) | A3: Qwen3-Coder-30B (Thor, temp 0) | A4: nemotron-3.5-lightning, think on (Thor, temp 0) | A5: nemotron-3.5-lightning, think OFF (Thor, temp 0) |
|---|---|---|---|---|---|
| **Configs valid** | 3/10 | 10/10 | 8/10 | **0/10 — no output** | **10/10** |
| Validator errors | 13 (7 configs) | 0 | 4 tokens (2 configs) | n/a (empty channel ×10) | 0 |
| Distinct answers (of 10) | 10 *(derived)* | 7 | 7 | 0 | **3** |
| STOCK keyword used | 2 lines *(derived)* | 0/30 | 0/30 | — | 0/30 |
| Worked example verbatim | 1/10 *(derived)* | 4/10 | 4/10 | — | **9/10** |
| Combo deviations, valid configs | **3/3** | 0/10 | 0/8 | — | 2/10 |
| Median managed score | 128 | 81 | 128 (= control) | 128 (control's, by construction) | **77.5** |
| Mean managed score | 434.8 | 239.1 | 285.1 (= control) | 285.1 (ditto) | 266.5 |
| Manager cost per brief | 9.3 s | 93.2 s | **1.57 s** | 8.56 s — for an empty string | 28.1 s wall (contended — see caveat); **~1.04 s generation** |
| Manager phase, total | 93.0 s | 932.5 s | **15.7 s** | 85.6 s | 281.3 s wall; ~10.4 s generation |
| Pairwise vs control | — (2 of its 3 valid won their seeds) | 0W-1L-9T | 0W-0L-10T | 0W-0L-10T (by construction) | **0W-2L-8T** |

## What arm 5 answers

The arm was bought to answer one question: *with deliberation off, does the resident manage — file a valid, deviating report — or does the nonemission just change costume?* The receipts answer it in two cleanly separated halves.

**1. The nonemission was configuration, not character.** A single API field separates arm 4 from arm 5, and every marker flips: content empty ×10 → a complete config ×10; `finish_reason: length` ×10 → `stop` ×10; `eval_count` pinned at the 512 budget ×10 → 60–88, the answer's own length, ×10; the smoke's 99 tokens-for-"OK" → 2. Arm 4's verdict stands, but its scope is now exact: it was a verdict on *nemotron-3.5-lightning as served by Ollama with thinking at its default*, full stop. Any future use of this resident as a form-filler, judge or manager in this fleet goes through `think: false` — that is now a measured fact about the deployment, not a preference.

**2. Underneath the block sits the bench's purest deferent.** Diversity did not recover with emission; it collapsed further. Three distinct answers in ten (arms 2–3 managed seven; even arm 1, spelling half its configs wrong, produced ten). The worked example — which arms 2 and 3 already pasted at 4/10, always in the B4+B5 block — is pasted at **9/10**, in every brief, including B1-survival, whose entire text argues against the example's orb-route haste. The briefs, which differ, made almost no difference: B1, B2, B3 and B4 all received the identical artefact. Temperature 0 explains same-brief pairs matching; it does not explain four different briefs converging on one answer — that is the model's posture, measured at its most legible: given a form with an example filled in, the safest completion is the example.

**3. Its one deviation is real, and it is mis-aimed.** The B5-zealot brief asks for one thing specifically: *choose one of the strongest gods for the combo and structure the route around worship.* Arm 5's response kept the stock god trio untouched — and changed the **combo**, the one line the brief didn't ask about, to `GrHu`, on both seeds. It is the first valid combo deviation since arm 1's three, and the first evidence in five arms that this model will move anything. Both moved games lost (109: 91 vs 98, dead to an iguana at turn 2,450 with no god — the Hunter never converted; 110: 37 vs 216, dead to a gnoll at turn 796). Small numbers, stated at their strength: two games are two games. But the direction is the bench's recurring lesson from the other side — arm 1's boldness won because its deviations were *combo-and-route* changes in the direction of its briefs; arm 5's lone deviation answers a question nobody asked, and qw paid for it twice. Median 77.5 against control's 128 is entirely these two games: arm 5 is the first arm to finish *below* the control it photocopied eight times.

**4. The failure taxonomy closes a loop.** RESIDENTS left four species: orthographic (0.6B), deferential (7B), semantic-compositional (Coder-30B), deliberative-nonemission (Nemotron). Arm 5 shows the fourth species was a *mask* over the second: switch off the deliberation and the same model files the deferent's paperwork — more faithfully than the 7B ever did. The taxonomy's lesson generalises past this bench: for hybrid-thinking residents, *emission failure and posture are separate measurements*, and an arm that scores 0/10 may be hiding any posture at all. You cannot know what a manager is until it files.

## Caveats, kept with the results

- **Manager wall times are contention-inflated and are not quoted as the model's speed.** The Thor was shared with concurrent lanes during this build round; per-call walls for near-identical outputs ranged 1.74–87.18 s, while the endpoint's own generation time (`eval_duration`) was 1.03–1.11 s on all ten calls. The table carries both numbers; the honest per-brief cost of this arm is ~1.05 s of generation plus whatever the box's queue that night adds. Arm 4's 8.56 s/brief, measured uncontended, remains the right comparison for the deliberation's cost: thinking-on spent ~7.6 s generating 512 hidden tokens per brief and emitted nothing.
- **Temperature 0 throughout arms 3–5** (rounds 1–2 ran the farm default 0.7): same-brief pairs returning identical configs is partly the thermostat. Cross-brief convergence (four different briefs, one artefact) is not.
- **One call per brief remains a sample, not a distribution**; the field is still weak (nothing past D:5 in any arm) — all management measured here is management of young deaths, now including two slightly younger ones.
- **Arm 5 is a configuration of the same resident, not a new model.** Its receipts record `think: false` in arm.json and in every seed's endpoint_meta, so the arm can be re-run or distinguished from arm 4 forever.

**Bottom line:** RESIDENTS ended by wondering what the Nemotron would be if it ever sat down in the manager's chair. It sits down now — instantly, validly, at a second a brief — and hands qw its own example back, nine times in ten. The deliberation was never the model's judgement; it was a door stuck shut. Behind the door: the same deference the bench has now measured at 0.6B, 7B and 30B-coder, in its purest form yet — and one deviation, on the one brief that asked for a god, spent on the combo instead, at a cost of two games. Five arms in, the finding has a new clause: *first make the manager emit; then discover, as here, that emission was the easy part.*

## Continual — the bench after arm 5

The think extension is now part of the bench's working copy (`~/workspace/qw-arm5/manager-bench.py`, md5 `5907d4b9…`, mirrored on the Thor and Oracle under `~/qw-arm5/`):

```
python3 manager-bench.py gen --base-url http://localhost:11434 \
    --model nemotron-3.5-lightning:latest --dialect ollama \
    --arm arm5-nemotron-thinkoff --out DIR --think false
```

Any future hybrid-thinking resident gets its think-off arm by adding `--think false`; its think-on arm is the same command without the flag. The filed bench (liquid-world-model-build, md5 `c27305e2…`) is unchanged — folding the extension into the filed copy is the referee's call, with the differential script (`verify_arm5.py`, beside the working copy) as the gate.

## Artefacts & reproduction

- Local (`~/workspace/qw-arm5/`): `ARM5.md` (this), `arm5-results.json` (play results + generation receipts + census + bench-extension record + disclosed smoke + rounds 1–4 summaries), `manager-bench.py` (extended bench), `verify_arm5.py`, `census.py`, `PROCESS-LOG.md`, `thor-originals/arms/arm5-nemotron-thinkoff/` (arm.json + all 10 manager artefacts as generated on the Thor), `results-arm5-from-oracle.json` (the play results as written on the Oracle).
- On the Oracle, `~/qw-arm5/`: the extended bench, `verify_arm5.py`, `arms/`, `runs/arm5-nemotron-thinkoff-<seed>/` (rc, logs, morgue, saves), `results-arm5-nemotron-thinkoff.json`, `spotcheck.json` (MATCH, fourth consecutive round), `play.log`. Rounds 1–4 trees untouched.
- On the Thor, `~/qw-arm5/`: the extended bench + `arms/` (generation originals). No Thor service was restarted, reconfigured, or loaded/unloaded by this lane; 11 sequential generation calls in total.
- Reproduce one game: the same drive.py invocation as RESIDENTS documents, with the run's rc under `~/qw-arm5/runs/`. Same rc + same seed → same game; four rounds of spot-checks and fifty identical-game receipts are standing on it.
