# The qw Residents — arms 3 and 4: the Thor's hot models take the manager's chair

**Headline: the posture curve now has four points, and it does not bend the way size suggests. The Thor's Qwen3-Coder-30B (arm 3) manages exactly like the farm's 7B — deferential, example-anchored, every game a stock replay — except sixty times faster (1.6 s vs 93.2 s per brief) and with one new, coder-flavoured error: it composed `Rune:Lair` and `Rune:Orc`, runes for branches that hold none. The Thor's nemotron-3.5-lightning (arm 4) differs in kind, not degree: it never produced a configuration at all. Given a three-line form to fill, it spent its entire generation budget on hidden deliberation — answer channel empty on all 10 briefs at 512 tokens, and still empty at 4,096 (64 s, 13,757 chars of unterminated thinking). The only manager that has ever changed a game for the better remains round 1's illiterate 0.6B.**

Setting: the identical bench to rounds 1–2 (QW-MANAGER.md, QW-REMATCH.md), two arms changed only in the manager. Dungeon Crawl Stone Soup 0.32.1 on the Oracle, stock qw @ 8698adc, same 10 seeds (101–110), same 5 frozen briefs, same prompt byte-for-byte, same mechanical validator, same caps. Arm 3's manager is the Thor's resident **Qwen3-Coder-30B-A3B-Instruct** (llama-server, OpenAI-style API on the Thor's :8001); arm 4's is **nemotron-3.5-lightning:latest** (Ollama native API on the Thor's :11434). Generation ran on the Thor itself (localhost endpoints; the latency receipts are the endpoints' own); games ran on the Oracle. Per Casey's brief for these arms, calls are temperature 0 via each endpoint's native API — rounds 1–2 ran the farm's raw-completion default (temp 0.7); temperature and transport are part of the arm definition and are stated in every receipt. Control receipts are round 1's, reused after the determinism spot-check reproduced exactly for the third consecutive round (seed 101: 49 / XL 3 / 1,156 turns / iguana). Artefacts live in `~/qw-residents/` on the Oracle and Thor; local copies beside this file.

---

## PROCESS — how this was actually done, in the order it happened

*Casey's doctrine (2026-10-26): "Document well as you go. The process means more than the product." This section folds in the running log (PROCESS-LOG.md beside this file), dead ends and failures at the same care as the successes.*

**1. History first, then inventory.** Rounds 1–2 read in full; the rig is round 2's tree on the Oracle (`~/qw-rematch/`), untouched by this lane except as a read source and shared binaries. Thor endpoints probed before anything was built: `:8001/v1/models` serves exactly `Qwen3-Coder-30B-A3B-Instruct`; `:11434/api/tags` lists `nemotron-3.5-lightning:latest` (arm 4's full receipted id) and a `qwen3.5:9b` that is not in this experiment.

**2. The bench became one script — and the script was spliced, not transcribed.** `manager-bench.py` (deliverable, §Continual) vendors the frozen prompt, briefs, vocabularies and validator. Writing it locally, the validator's regex line went through three hand-edits over backslash escaping in tool output — precisely the silent-transcription class this programme keeps receipts to catch. The structural fix: the script was written with a placeholder, and the entire rig segment (5,616 bytes, sha256 `578473217881fffbbfa79a0bcf6d068a6b94c167059579adfda4ba1d6caf8db1`) was spliced byte-identically from `qw-rematch/scripts/manager.py` on the Oracle. Differential verification then ran against the rig itself: PROMPT byte-identical (1,469 chars), BRIEFS identical, and `validate()` verdicts identical on 27/27 inputs — all 20 historical manager raw outputs from rounds 1–2 plus 7 synthetic chat-shaped variants (bulleted, bold labels, fenced, prose-wrapped, quoted example, lowercase, think-then-lines). Selftest 10/10, on both the Oracle and the Thor.

**3. Transport smokes.** One trivial call per dialect before any brief: the coder answered 'OK' in 0.19 s; the Nemotron answered 'OK' in 1.63 s with `eval_count` 99 for a one-word visible reply — it spends tokens on hidden reasoning even on a smoke. Noted at the time; it became arm 4's whole story.

**4. Generation (Thor, sequential, one call per brief, no retries).** Arm 3 completed in 15.7 s of total manager wall: 8/10 valid, and the shape was visible by seed 105 — stock combo everywhere, the worked example returning in the B4/B5 block, and the B2 pair invalid on a *new* error: `Rune:Lair`, `Rune:Orc`. Arm 4 took 85.6 s and produced nothing: all 10 calls returned an **empty content channel**, `finish_reason: length`, `eval_count` exactly 512 (the full budget) — the model spent everything on Ollama's separate thinking channel and never emitted an answer line.

**5. The budget question, decided openly.** One disclosed probe (not an arm sample): seed 101 again at `num_predict` 4096 — 64.4 s, still `length`, content still empty, thinking 13,757 chars and unterminated. Not a near miss. A second diagnostic captured the thinking itself at 512: a numbered meta-deliberation ("1. **Analyze User Input:**") that restates the task, quotes the brief, and lists the COMBO options — at budget's end it is still on step 1. Decision, recorded in the process log before the games ran: no further reconfiguration of arm 4. Ollama's think toggle is the obvious untried lever; pulling it would define a different arm, and re-rolling a manager until it manages is the failure this bench's discipline exists to prevent. A future arm can be exactly that experiment, run through the same script.

**6. Play (Oracle).** Artefacts travelled Thor → local → Oracle with md5s taken; the executed script is md5-identical on all three boxes (`c27305e2…`). Spot-check first (MATCH, third round running), then both arms' games at 2-concurrent, nice 10. Midway the local SSH chain dropped at ~10 minutes — the fleet's known long-chain failure — and for some minutes the arm looked dead; the Oracle-side pipeline had in fact survived detached and finished unattended, verified by process listing and the completed play log. The boring move (check the box, don't restart anything) was again the right one. Game wall: arm 3 710.4 s, arm 4 708.9 s, each including its own seed-106 marathon (572 s / 573 s).

**7. Referee pass.** Results were not taken on trust. Arm 3 seed 105's morgue was diffed against round 1's control-105: exactly three hunks — the calendar date (the games ran past midnight UTC), the real-time duration string, and qw's turn-0 status line echoing the *loaded* goals (`Goals: Normal, Rune:Shoals, Rune:Snake, Shopping, Orb, Win` vs control's `Goals: Normal`). Every event line of the 1,905 turns is identical: the plan was verifiably loaded and announced, and the game still replayed stock — because `Normal` never completed on that seed, so the goals behind it never became standing orders (the mechanism round 2 read out of qw.lua). Seeds 108 and arm 4's 103 diff the same way. All 20 new games were also checked field-for-field against controls (score, XL, turns, killer, gold, kills): arm 3 10/10 identical, arm 4 10/10 identical.

**8. A debt paid to the table.** Round 1 never published a config census. For the four-point table below, round 1's census was derived here from its artefacts with the same ruler as arms 2–4 (distinct raw answers 10, STOCK lines 2, example verbatim 1, valid combo deviations 3/3). It is marked *derived* wherever used.

---

## Results — per-seed, four arms

Control and arms 1–2 are the prior rounds' receipts; arms 3–4 are this run's. "Identical" means score, XL, turns, killer, gold and kills all equal to control, morgue-diffed where stated.

| Seed | Brief | Control | A1 0.6B (farm) | A2 7B (farm) | A3 Coder-30B (Thor) | A4 Nemotron (Thor) |
|---|---|---|---|---|---|---|
| 101 | B1-survival | 49 | **575** ✓ | 49 ✓ (=) | 49 ✓ (=) | fallback (=) |
| 102 | B1-survival | 462 | **1,613** ✓ | **2** ✓ | 462 ✓ (=) | fallback (=) |
| 103 | B2-rune-rush | 2 | 2 fb | 2 ✓ (=) | 2 ✗ fallback (=) | fallback (=) |
| 104 | B2-rune-rush | 348 | 348 fb | 348 ✓ (=) | 348 ✗ fallback (=) | fallback (=) |
| 105 | B3-orb-sprint | 64 | 64 fb | 64 ✓ (=) | 64 ✓ (=) | fallback (=) |
| 106 | B3-orb-sprint | 49 | 49 fb | 49 ✓ (=) | 49 ✓ (=) | fallback (=) |
| 107 | B4-methodical | 158 | 158 fb | 158 ✓ (=) | 158 ✓ (=) | fallback (=) |
| 108 | B4-methodical | 1,405 | 1,405 fb | 1,405 ✓ (=) | 1,405 ✓ (=) | fallback (=) |
| 109 | B5-zealot | 98 | 98 fb | 98 ✓ (=) | 98 ✓ (=) | fallback (=) |
| 110 | B5-zealot | 216 | 36 ✓ | 216 ✓ (=) | 216 ✓ (=) | fallback (=) |

✓ = valid config · ✗ = invalid (fallback, counted) · fb = round 1 fallback · (=) = game identical to control.

**Arm 3's pairwise record: 0 wins, 0 losses, 10 ties** — the first manager arm that never lost a game, because it never changed one. **Arm 4's:** 10 ties by construction (all fallback), verified identical.

## The four-point posture curve

| | A1: Qwen3-0.6B (farm, temp 0.7) | A2: Qwen2.5-7B (farm, temp 0.7) | A3: Qwen3-Coder-30B (Thor, temp 0) | A4: nemotron-3.5-lightning (Thor, temp 0) |
|---|---|---|---|---|
| **Configs valid** | 3/10 | **10/10** | 8/10 | **0/10 — no output** |
| Validator errors | 13 (7 configs) | 0 | 4 tokens (2 configs) | n/a (empty channel ×10) |
| Distinct answers (of 10) | 10 *(derived)* | 7 | 7 | 0 |
| STOCK keyword used | 2 lines *(derived)* | 0/30 | 0/30 | — |
| Worked example verbatim | 1/10 *(derived)* | 4/10 | 4/10 | — |
| Combo deviations, valid configs | **3/3** | 0/10 | 0/8 | — |
| Median managed score | 128 | 81 | 128 (= control) | 128 (control's, by construction) |
| Mean managed score | 434.8 | 239.1 | 285.1 (= control) | 285.1 (ditto) |
| Manager cost per brief | 9.3 s | 93.2 s | **1.57 s** | 8.56 s — for an empty string |
| Manager phase, total | 93.0 s | 932.5 s | **15.7 s** | 85.6 s |

## Arm 3 — the coder manages like a bigger deferent, at 60× the speed

The resemblance to arm 2 is line-for-line uncanny: 7 distinct answers to 5 briefs; same-brief pairs identical in three of five briefs (101=102, 105=106, 107=108); the `STOCK` keyword never used (the defaults spelled longhand in all 30 lines); the prompt's worked example returned verbatim in 4/10 — and in the same place, the entire B4-methodical + B5-zealot block, where the 7B also pasted it; the stock god trio in 8/10 (the B5 deviations are permutations and one substitution — Trog/Makhleb/Qazlal, Trog/Makhleb/Okawaru — inside the example's goals, so the "zealot" brief moved the god list's *order*, not its route). Among valid configs the combo **never changes**: `GrBe.handaxe` 8/8. The B1-survival pair is the purest deference on record in this bench: `COMBO: GrBe.handaxe / GODS: Trog, Okawaru, Makhleb / GOALS: Normal` — qw's own defaults, restated in full, twice.

Two differences from the 7B, both informative:

1. **Its one error is a composer's, not a clerk's.** The B2-rune-rush brief says "Get to the Lair and into a Lair branch as fast as possible and secure a rune early," and the coder reached for the `Rune:` machinery the prompt taught it — and aimed it at the branches the brief named: `Rune:Lair`, `Rune:Orc`. Lair and Orc hold no runes; the grammar's rune-branch list exists precisely because only some branches do. The 0.6B failed *orthographically* (it could not spell `Rune:`); the 7B failed *not at all*; the coder fails *semantically* — it generalises a pattern one step past the domain fact that bounds it. That is a recognisably code-trained failure: the syntax of composition, applied where the semantics don't hold.
2. **It never lost.** Arm 2's lone divergence was its catastrophe (seed 102, `Normal, Escape, Hells`, dead in 88 turns). Arm 3's B1 lists carry no teeth (goals `Normal` alone — stock's own final-and-alone form), so no promotion accident was possible; and its one Normal-first list with real content behind it (B3's `Normal, Rune:Shoals, Rune:Snake, Shopping, Orb, Win`) never fired, because Normal completed in neither B3 run. Ten ties is what perfect deference scores: the control column, photocopied at 1.6 s per brief.

And the speed is real and it matters for the continual-honing purpose: **15.7 s for a full arm's manager phase** — against 93.0 s (0.6B) and 932.5 s (7B) — on a resident model that was already loaded, on our own silicon, at zero marginal cost. If this bench becomes a standing instrument (a new resident arrives, run the arm), arm 3's profile — instant, valid-ish, deferential — is the baseline profile to beat, and the bench's cost per arm is now dominated by the games (~710 s), not the manager.

## Arm 4 — the Nemotron differs in kind: it files no report

Arm 4's receipts are an absence, measured precisely. Ten briefs, ten calls, and:

- content channel **empty** in 10/10; `finish_reason: length` in 10/10; `eval_count` **exactly 512** in 10/10 (the whole budget, every time);
- the disclosed 4096-token probe on seed 101: 64.4 s, still `length`, content still empty, thinking 13,757 chars unterminated;
- the thinking diagnostic: the deliberation is a numbered restatement of the assignment ("1. **Analyze User Input:**", the brief quoted back, the COMBO menu re-listed) — at 512 tokens it has not finished *reading the prompt to itself*.

This is not arm 1's failure (a small model that means something and cannot spell it) and not arms 2–3's (models that spell perfectly and mean little). It is a model for whom a request to *decide* is an occasion to *deliberate*, with no internal rule that deliberation must end. As configured — Ollama native API, temp 0, thinking left as the endpoint defaults it — nemotron-3.5-lightning cannot serve as a qw manager at any budget tried, because the artefact the bench exists to collect is never emitted. Its manager-phase cost (85.6 s of pure hidden reasoning) bought zero configurations; for scale, that is roughly the wall-clock in which the 0.6B wrote all ten of its (three of them valid, two of them winners).

Stated at its true strength: this is a verdict on **the arm as configured**, not on the model's intelligence in the abstract. The untried lever is named — Ollama's think toggle (and hybrid-thinking controls generally) — and deliberately not pulled (§Process-5). If a future arm runs `think: false`, it will be arm 5, with its configuration in its receipts like everyone else's.

## What the four points together say

1. **Diversity collapses as validity rises.** Distinct answers per 10 briefs: 10 → 7 → 7 across the three answering arms, and the collapse is convergence on the same attractor: stock combo, stock gods, the prompt's example. The bench has now measured the same posture at 0.6B-with-errors, 7B, and 30B-coder: the bigger and more capable the model, the more faithfully it hands qw its own defaults back. Round 2's conclusion survives a second, larger, differently-trained witness.
2. **The combo is still the only lever that has ever moved a game — and only the weakest manager pulled it.** All three of arm 1's valid configs changed the combo; two produced the best runs of all four rounds (575, 1,613). Arms 2–4 changed the combo in 0 of 18 valid configs. Nothing in four arms contradicts round 1's hypothesis; everything since has been increasingly polished evidence that capable models won't test it.
3. **Failure has a taxonomy now, one species per arm.** Orthographic (0.6B: `Runes:`), none-but-deference (7B), semantic-compositional (Coder-30B: `Rune:Lair`), and deliberative-nonemission (Nemotron: no artefact at all). A bench that only counted validity would rank them 3 < 10 > 8 > 0 and miss that each number is a different *kind* of wrong.
4. **Residency changes the economics, not the posture.** The Thor's hot models made the manager phase nearly free (15.7 s) — the honest cost of honing a new resident in this system is now the games themselves. That is the continual loop Casey pointed at, and §Continual leaves it as one command.

Caveats, kept with the results: arms 3–4 ran temperature 0 where rounds 1–2 ran the farm default 0.7 (Casey's specification for these arms; determinism at temp 0 is also why same-brief pairs returned identical configs in both new arms — the narrowness is partly the thermostat, and is reported, not hidden). One call per brief remains a sample, not a distribution. The field is still weak — no wins, no runes, nothing past D:6 in any arm — so all management measured here is management of young deaths. And arm 4's verdict is configuration-bound, as stated twice above.

**Bottom line:** put the Thor's residents in the manager's chair and the chair doesn't change: the coder is the 7B's deference with a GPU's manners — flawless paperwork at 1.6 s a brief, one inventive grammar error, and not a single game altered — while the Nemotron never sits down at all, thinking about the assignment in another room, indefinitely. Four arms in, the bench's finding has hardened: on this evidence, management is not a capability these models lack the size for; it is a posture they are trained out of — and the one arm that had it couldn't spell.

## Continual — the bench as one command

`manager-bench.py` (beside this file; md5 `c27305e2db545ba28cfe3119cce88743`, identical bytes on the VM, the Oracle and the Thor) is the whole bench:

```
python3 manager-bench.py selftest                      # validator, 10/10 anywhere
python3 manager-bench.py gen  --base-url <endpoint> --model <id> \
    --dialect openai|ollama --arm <name> --out <dir>   # 10 briefs -> artefacts
python3 manager-bench.py play --arm <name> --root <dir>  # Oracle: spot-check + games
```

`gen` runs wherever the endpoint is reachable (here: on the Thor, at localhost); `play` runs on the Oracle against the shared rig. A future resident model is honed by exactly one `gen` + one `play`, and its arm lands in the same results shape as arms 1–4. The frozen parts (prompt, briefs, validator) are vendored *byte-identically* from the rig — spliced, not retyped (sha256 in §Process-2) — so an arm run next season is the same bench, not a descendant of it.

## Artefacts & reproduction

- Local, beside this file (`~/workspace/qw-residents/`): `manager-bench.py` (the bench), `RESIDENTS.md` (this), `PROCESS-LOG.md`, `results.json` (both arms' full receipts + round 1 controls + arms 1–2 summaries + the Nemotron probes), `artefacts/arm3-coder30b/` and `artefacts/arm4-nemotron/` (arm.json + all 10 manager artefacts each), `morgues/` (all 20 new morgues + the spot-check control), `splice_rig.py`, `verify_bench.py`.
- On the Oracle, `~/qw-residents/`: `manager-bench.py`, `arms/`, `runs/<arm>-<seed>/` (rc.txt, output/driver logs, morgue, saves), `results-arm3-coder30b.json`, `results-arm4-nemotron.json`, `spotcheck.json`, `play.log`. Rounds 1–2 trees untouched; qw and the crawl binary shared with round 2's tree by path, unmodified.
- On the Thor, `~/qw-residents/`: `manager-bench.py` + `arms/` (the generation-side originals). No Thor service was restarted, reconfigured, or loaded/unloaded by this lane; the endpoints were called sequentially, 24 generation calls in total (20 briefs, 2 transport smokes, 1 budget probe, 1 thinking diagnostic — each itemised in the process log).
- Reproduce one game: `python3 /home/ubuntu/qw-rematch/scripts/drive.py out.log drv.log 1800 /home/ubuntu/qw-rematch/crawl-032/crawl-ref/source/crawl -lua-max-memory 128 -no-throttle -rc <run>/rc.txt -rcdir /home/ubuntu/qw-rematch/qw -dir <run> -morgue <run>/morgue -seed <seed>` under any pty. Same rc + same seed → same game; three rounds of spot-checks and forty identical-game receipts are standing on it.
