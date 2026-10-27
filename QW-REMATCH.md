# The qw Rematch — REMATCH.md

**Headline: vocabulary precision DID arrive with size — 10 of 10 configs valid, zero errors of any class, against the 0.6B's 3 of 10 — and it changed almost nothing. Nine of the ten managed games are event-for-event identical to stock (morgue-diffed), because the 7B manager's idea of a plan was to spell the stock defaults longhand and copy the prompt's worked example. The one game it genuinely steered, it steered to the worst managed result of either round: seed 102, dead at XL 1 in 88 turns, score 2 vs control 462. Managed median fell to 81 vs control 128. Round 1's illiterate manager, on the three seeds it could write for, out-managed the literate one.**

Setting: the identical experiment to round 1 (QW-MANAGER.md), one variable changed. Dungeon Crawl Stone Soup 0.32.1 (source build) on the Oracle, played by stock qw @ 8698adc under the same pty driver, same 10 seeds (101–110), same 5 frozen briefs, same prompt byte-for-byte, same mechanical validator, same caps (1,800 s wall / 200,000 turns). The manager is the Oracle farm's `llm-big` member — Qwen2.5-7B-Instruct Q4_K_M — swapped in for round 1's `llm` (Qwen3-0.6B). Control receipts are round 1's, reused after a determinism spot-check (see Process). All artefacts live in `~/qw-rematch/` on the Oracle; per-run receipts in `results.json` beside this file.

---

## PROCESS — how this was actually done, in the order it happened

*Casey's doctrine (2026-10-26): "Document well as you go. The process means more than the product." This section is the process record, kept as a first-class part of the deliverable — dead ends and failures included, at the same care as the successes. Entries follow the session's real sequence; times are Oracle UTC.*

**1. Read round 1 first, then check the farm (Oct 27, ~05:25 UTC).** Round 1's failure census, from its results.json: validity 3/10 (seeds 101, 102, 110); errors = `Runes:` for the grammar's `Rune:` in 5 configs, a hallucinated god (`Mgazlal`), `Stock`/`STOCK` offered as a god in 2 configs, a combo pasted into the goals field (`Run:GrHu`), the prompt's parenthetical description of `Normal` echoed as a token, and two invented tokens (`Shrine`, `Runestone`). The farm check came next: `llm-big` was **already registered** by the scale-up lane (Qwen2.5-7B-Instruct Q4_K_M, split GGUF, hashes verified at registration) — no wait was needed. Two registry facts shaped the run: the member answers via the farm.py CLI only (the :8770 shim was deliberately not restarted by the registering lane; round 1's manager also called the CLI, so the call route is identical), and its politeness default is 2 threads with one call at a time (peak RSS ~8.9 GiB — concurrent calls would approach the box's RAM ceiling). The farm was called, never reconfigured, exactly as ordered.

**2. The rig is round 1's rig, diffed (05:31 UTC).** The scripts were copied to `~/qw-rematch/` on the Oracle (round 1's tree untouched; qw and the crawl build are symlinked, not duplicated). The diff of the copied `manager.py` against round 1's is exactly three lines: the docstring, `'llm'` → `'llm-big'` in the farm call, and the briefs path. `briefs.json` and `drive.py` are md5-identical to round 1's. The farm's own dispatch was read to confirm the call contract is uniform: `_call_llm_big` differs from `_call_llm` only in model path and output cap (`-n 256` vs `-n 128` — the bigger model gets more room to answer, and needed none of it); same temperature 0.7, same raw-prompt completion mode, same echo-stripping. The only experimental variable is the model. One discrepancy found and recorded rather than smoothed over: round 1's MANAGER.md prints brief texts that are *paraphrases* of `briefs.json`; the file is what both rounds actually ran, and the file is what this round used, byte-identical.

**3. Validator re-verification (05:33–05:36 UTC).** Round 1 recorded "unit-tested 10/10" for its validator but left no test file behind, so a fresh 10-case test was written against the copied `validate()` — round 1's failure modes as cases, plus valid/STOCK/canonicalisation cases. First run: 9/10, and the failure was **the test's bug, not the validator's**: the stock-as-god case fed `GODS: Stock` bare, which the validator correctly treats as the STOCK sentinel; round 1's real failures (confirmed in its raw outputs) were `Stock`/`STOCK` as one member of a god list ("Beogh, Qazlal, Stock"). The test was corrected to the real failure shape and re-run: **10/10**. The validator code itself was never touched — it is round 1's by construction.

**4. Determinism spot-check — controls reused, stated (05:38 UTC).** Pre-registered in the runner: re-run control seed 101; if it reproduces round 1 exactly, reuse round 1's control receipts for all 10 seeds; if not, re-run the whole control arm. It reproduced **exactly** — score 49, XL 3, 1,156 turns, killed by an iguana — so the control column below is round 1's receipts, and only the managed arm is new. Every comparison in this document inherits that statement.

**5. Phase 1 — the manager calls (05:40–05:57 UTC).** Ten calls, sequential, nice priority, one at a time. **10 of 10 VALID.** The price is part of the result: 932.5 s of LLM wall in total (mean 93.2 s per brief) against round 1's 93.0 s total — the 7B generates at ~3.5 tok/s on this shared CPU box where the 0.6B managed ~22 tok/s. Precision arrived at ten times the manager-phase cost. The pattern was visible by seed 105 and complete by 110 (full census in Results): the model never once used the `STOCK` keyword it was offered — it spelled the stock defaults longhand. Same-brief seed pairs returned byte-identical configs twice over (103=104; 107=108; 109=110). The GOALS for all four B4/B5 seeds are the prompt's own worked example, verbatim.

**6. Phase 2 — the games (05:57–06:07 UTC).** All ten managed games played unattended under the same caps; none approached either cap (the longest, managed 106, ran 576.4 s / 16,969 turns — its output kept flowing, no stall; the boring move, waiting, was again the right one). Total managed game wall ≈ 684 s. Then the shock in the receipts, which the rest of this document exists to explain: **nine of the ten managed games are identical to their controls** — score, XL, turns, killer, gold, kills all equal — and the one divergence is a catastrophe (seed 102: 2 vs 462).

**7. Referee pass.** results.json was not taken on trust. (a) The managed-108 morgue was read directly: 1,405 points, XL 8, slain by Duvessa on D:5, 4,661 turns; it matches the recorded receipt field for field. (b) Morgue diffs: round-2 managed 107 and 110 diffed against round-1 control 107 and 110 — **identical line for line except the turn-0 qw status lines that echo the rc itself** (the loaded goal list; 110 also echoes its god list). The managed plan was verifiably loaded into the game, and the game then unfolded exactly as stock, event for event, across 190+ lines of morgue. (c) Seed 102's mechanism was read from qw.lua's source rather than theorised (see the case study below).

---

## Design — what "identical" means here

- **One variable.** Manager model: Qwen3-0.6B (round 1) → Qwen2.5-7B-Instruct (round 2), both Q4_K_M GGUFs served by the same farm, same llama-cli, same temperature, same prompt. Everything else — seeds, briefs file, validator, rc surgery (`mkrc.py`), driver, caps, scoring — is round 1's, copied and diffed (Process §2–3).
- **Arms.** *Control*: round 1's stock receipts (qw's proven default: combo `GrBe.handaxe`, gods Trog/Okawaru/Makhleb, goal `Normal` via the "3 Runes" set), reused per the spot-check. *Managed*: the same rc machinery with the manager's validated values substituted. Invalid → stock rc and **counted as a fallback** — this round there were none to count.
- **Receipts per run.** Morgue file, score, XL, turns, absdepth, place, god, killer, gold, kills, wall-clock; plus the manager artefact (prompt, raw output, parsed config, validity, errors, LLM wall) for every seed. All 10 managed morgues and all 10 manager artefacts are copied beside this file (`morgues/`, `artefacts/`).

## Results — per-seed, three arms

Control and round-1 managed are round 1's receipts; round-2 managed is this run's.

| Seed | Brief | Control | R1 managed (0.6B) | R1 valid? | R2 managed (7B) | R2 valid? | R2 vs control |
|---|---|---|---|---|---|---|---|
| 101 | B1-survival | 49 | **575** | yes | 49 | yes | identical game |
| 102 | B1-survival | 462 | **1,613** | yes | **2** | yes | **LOSS (−460)** |
| 103 | B2-rune-rush | 2 | 2 | fallback | 2 | yes | identical game |
| 104 | B2-rune-rush | 348 | 348 | fallback | 348 | yes | identical game |
| 105 | B3-orb-sprint | 64 | 64 | fallback | 64 | yes | identical game |
| 106 | B3-orb-sprint | 49 | 49 | fallback | 49 | yes | identical game |
| 107 | B4-methodical | 158 | 158 | fallback | 158 | yes | identical game |
| 108 | B4-methodical | 1,405 | 1,405 | fallback | 1,405 | yes | identical game |
| 109 | B5-zealot | 98 | 98 | fallback | 98 | yes | identical game |
| 110 | B5-zealot | 216 | 36 | yes | 216 | yes | identical game |

"Identical game" is a measured claim, not shorthand for "same score": score, XL, turns, killer, gold and kills all equal, and for seeds 107/110 the full morgue text is identical to control except the rc-echo lines (Process §7). Round 2's pairwise record against control: **0 wins, 1 loss, 9 ties**.

## Aggregates

| | Control (n=10, R1 receipts) | R1 managed, 0.6B (n=10) | R2 managed, 7B (n=10) |
|---|---|---|---|
| **Configs valid** | — | **3 / 10** | **10 / 10** |
| Fallbacks (counted) | — | 7 | 0 |
| Median score | 128 | 128 | **81** |
| Mean score | 285.1 | 434.8 | 239.1 |
| Median depth (absdepth) | 3.5 | 3.0 | 3.0 |
| Median turns | 2,506.5 | 2,801.5 | 2,058.5 |
| Wins / runes | 0 / 0 | 0 / 0 | 0 / 0 |
| Manager cost (LLM wall, total) | — | 93.0 s (mean 9.3 s) | 932.5 s (mean 93.2 s) |

On the three seeds round 1 actually managed (101, 102, 110) — the only head-to-head where both managers steered — the comparison is unflattering to size: round 1's managed scores were 575 / 1,613 / 36 (mean 741.3); round 2's on the same seeds are 49 / 2 / 216 (mean 89.0). Round 2's whole-arm median (81) sits below control (128) for exactly one reason: seed 102. Remove it and round 2 is control, replayed nine times and lost once — which is the finding, not a caveat on it.

## The error census — did `Runes:` die?

| Error class | Round 1 (0.6B) | Round 2 (7B) |
|---|---|---|
| `Runes:` for `Rune:` | 5 configs, 7 tokens | **0** |
| Hallucinated god | 1 (`Mgazlal`) | **0** |
| `Stock`/`STOCK` as a god-list member | 2 configs | **0** |
| Combo pasted into goals (`Run:GrHu`) | 1 | **0** |
| Prompt prose echoed as a token | 1 (`Normal (the bot's proven…)`) | **0** |
| Invented tokens (`Shrine`, `Runestone`) | 1 config, 2 tokens | **0** |
| Missing/malformed lines | 0 | 0 |
| **Total validator errors** | **13 across 7 configs** | **0 across 10 configs** |

`Runes:` is dead. Every member of round 1's menagerie is dead. What replaced them is not a new error class — the validator has nothing to count — but a new failure *mode*, visible only in the configs and the morgues:

## The config census — what the 7B actually wrote

- **7 distinct configs for 10 seeds / 5 briefs.** Same-brief pairs came back identical three times (103=104, 107=108, 109=110): at temperature 0.7 the 7B's answer to a brief is a point, not a distribution.
- **Combo: `GrBe.handaxe` 10/10** — the stock combo, every time, spelled out. The `STOCK` keyword the prompt offers was used **0 times in 30 lines**; the model wrote the defaults longhand instead (combo longhand 10/10, god list longhand 10/10).
- **Gods: the stock trio (Trog, Okawaru, Makhleb) 8/10.** The only deviation is B5-zealot's two seeds: Beogh, Cheibriados, Hepliaklqana — *exactly the god list the 0.6B produced for seed 101 in round 1*, a cross-model, cross-round convergence on the same "safe strong gods" answer. (As in round 1, no managed run lived long enough for god choice to matter; all three B5/B1 god lists went unworshipped in play — the morgues show qw's own altar-driven Trog conversions, not the managers'.)
- **Goals: the prompt's worked example, verbatim, 4/10** (seeds 107–110: `D:1-11, Lair, D:12-15, Orc, Rune:Shoals, Rune:Snake, Vaults:1-4, Depths, Vaults:5, Shopping, Zot:1-4, Win`); a compressed form of the same example 2/10 (103/104); `Normal`-first lists 4/10 (101, 102, 105, 106). The briefs' fingerprints are faint: B2's pair kept the Shoals dive, B3's 106 is the terse `Normal, Orb, Win`, B1's 102 is the disaster below. Mostly, the model answered the *prompt*, not the *brief*.

## Case study — seed 102, the one game the manager actually steered

The verbatim config (B1-survival — "a long-lived run that dies late and safe beats a fast run that gambles"):

```
COMBO: GrBe.handaxe
GODS: Trog, Okawaru, Makhleb
GOALS: Normal, Escape, Hells
```

The morgue, verbatim:

```
 Seeded DCSS version 0.32.1 (console) character file.

Game seed: 102 (custom seed)

2 qw the Trooper (level 1, 0/14 HPs)
             Began as a Gargoyle Berserker on Oct 27, 2026.
             Was a Follower of Trog.
             Frozen to death by an endoplasm (5 damage)
             ... on level 1 of the Dungeon.
             The game lasted 00:00:00 (88 turns).
```

The mechanism, read from qw.lua's source (line numbers from the stock tree): a goal list is executed in order, and `Normal` is a *completable* item — `goal_complete()` returns true for it when `goal_normal_next()` has nothing to propose, and `choose_goal()` then promotes the next item to standing order. Stock qw never exposes this: its "3 Runes" goal set is the single string `Normal`, final and alone. In seed 102's list, `Normal` sat non-final, and the item behind it was `Escape` — qw's leave-the-dungeon goal, which carries its own travel and combat handling (`plan_go_command()`'s Escape branch; `goal_status == "Escape"` checks throughout). That Normal completed almost immediately on this seed's D:1 is the only path the source offers to an Escape standing order, and the morgue is what that order looks like: an XL-1 berserker dead in 88 turns to a D:1 endoplasm, having gained no gold and no level — the precise opposite of its brief. The same structural risk sat unused in seeds 101, 105 and 106 (all `Normal`-non-final lists): there, Normal kept proposing steps until death, the following items never became standing orders within those runs, and the games are stock's to the last morgue line. A validator can only check that tokens are legal; `Escape` is legal. Nothing in round 1's discipline — correctly — repaired it.

## Honest verdict

**The rematch's question is answered, completely: yes, vocabulary precision arrives with size.** 3/10 → 10/10; thirteen validator errors → zero; every named failure of round 1 — the pluralised rune, the invented god, the pasted combo, the echoed prose — is simply gone at 7.6B. If the programme needed a config-writer that never embarrasses the validator, it has one, at ten times the per-call wall-clock of the 0.6B on this box.

**And the rematch's lesson is that precision was the floor, not the event.** (The chess-box season said the same of legality: sliver's spotless record went 0/4.) The 7B bought its perfect validity with total strategic deference: stock combo 10/10, stock gods 8/10, the prompt's example as the plan 4/10, seven distinct answers to five different briefs. Where round 1's 0.6B *gambled* — changing the combo on all three of its valid configs — it won two of three and posted the best run of either round (1,613). The 7B changed effectively nothing: nine stock replays and one self-inflicted disaster, for a managed median *below* the control it was supposed to beat (81 vs 128) and a mean below both control (239.1 vs 285.1) and round 1's managed arm (434.8). On the evidence of these ten seeds, the bigger manager is a better *clerk* and a worse *manager*.

What the two rounds together actually establish, stated at its true strength:

1. **The binding constraint moves with size.** At 0.6B it is the lexicon — the model knows the shape and cannot spell the grammar. At 7B it is *anchoring* — the model spells perfectly and anchors on the prompt's defaults and example, so the artefact it produces is the prompt's own answer handed back. Neither constraint is the bot, the validator, or the plumbing; both rounds ran those flawlessly.
2. **Legality is not steerage.** A config can be valid, loaded, and announced in the morgue's own status lines — and still not change a single in-game event, because the plan it encodes is the plan the bot already had. "Managed" needs a behavioural definition (the game must diverge), not just a provenance one (a config was written). Nine of this round's ten runs pass provenance and fail behaviour; round 1's seven fallbacks failed provenance honestly and said so. The two failure shapes are mirror images, and only one of them is visible without morgues.
3. **The next lever is not a bigger brain.** It is a prompt and a brief that price deference: forbid the worked example's reuse, require each line to deviate from stock or justify itself, or score the manager on divergence-with-survival rather than validity. Round 1's closing suggestion stands, now with two rounds of evidence behind it: screen seeds for stock qw reaching the Lair, and make the GOALS list — not the combo, not the spelling — the thing being tested.

Caveats, kept with the results: one call per brief at temperature 0.7 is a sample, not a distribution — though the three identical same-brief pairs suggest the 7B's distribution under this prompt is narrow. Control receipts are round 1's, reused on a one-seed spot-check that matched exactly. And the field stayed weak in both rounds: no wins, no runes, nothing past D:6 in any managed run of either round — qw's ceiling on these seeds bounds what any manager could have shown.

**Bottom line:** the 0.6B manager couldn't write a legal order (3/10) but meant something by the ones it wrote; the 7B manager writes legal orders perfectly (10/10) and means almost nothing by them — it hands qw back its own defaults in longhand and lets the dungeon do what it was going to do anyway, except once, when it talked a berserker into leaving and got him frozen by an endoplasm on his way out. Vocabulary precision arrives with size. Management, so far, does not.

## Artefacts & reproduction

- On the Oracle, `~/qw-rematch/`: `scripts/` (manager.py — diff vs round 1 is 3 lines; test_validator.py — 10/10; run_rematch.py; mkrc.py; drive.py; briefs.json, md5-identical to round 1), `runs/<arm>-<seed>/` (rc.txt, manager.json for managed runs, output.log, driver.log, morgue/, saves/), `results.json`, `results-partial.json`, `experiment.log`. Round 1's tree (`~/qw-manager/`) is untouched; qw and the crawl binary are shared with it by symlink.
- Local copies in `~/workspace/qw-rematch/`: this file, `results.json` (round 2's full receipts, with round 1's control receipts embedded as `control_round1` and the spot-check verdict recorded), `morgues/` (all 10 managed morgues + the spot-check control), `artefacts/manager-<seed>.json` (all 10 manager artefacts), `PROCESS-LOG.md` (the running log this document's Process section folds in), `experiment.log`.
- Reproduce one game exactly as in round 1, from `~/qw-rematch/`: `python3 scripts/drive.py out.log drv.log 1800 ~/qw-rematch/crawl-032/crawl-ref/source/crawl -lua-max-memory 128 -no-throttle -rc <run>/rc.txt -rcdir ~/qw-rematch/qw -dir <run> -morgue <run>/morgue -seed <seed>` under any pty. Same rc + same seed → same game; that is what the spot-check and the nine identical morgues are standing on.
- Untouched, as ordered: the farm service and the Oracle's tunnels (the farm was called via its CLI, never reconfigured; `llm-big` was registered by another lane and merely consumed). Nothing outside `~/qw-rematch/` on the Oracle and `~/workspace/qw-rematch/` locally.
