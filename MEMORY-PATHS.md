# Memory That Asks the Questions

*A study of memory structures that don't just store and fetch, but generate the
next question — so the walker walks into the right answer because the path
itself asks the right questions along the way.*

**SuperInstance — research note, 2026-10-26.**

## Headline

The single strongest "the path asks the question" mechanism in the literature
is **FLARE's forward-looking trigger** (Jiang et al., 2023): during
generation, the model drafts its *next* sentence tentatively; if that draft
contains low-probability tokens — the walker's own continuation faltering —
the draft itself becomes a retrieval query, the retrieved evidence rewrites
the sentence, and the walk resumes. The question is not posed by a planner in
advance; it is *emitted by the path at the exact point of need*, in the
walker's own words. Every other strong system in this study is a variation on
one of three moves FLARE makes explicit: **(1) let a faltering prediction
formulate the query** (Nemori's prediction-error gating at write time,
Generative Agents' reflection questions, the liquid chart's surprise),
**(2) let the walk re-aim the search mid-path** (Think-on-Graph's per-hop
relation choice, IRCoT's thought-as-query, HippoRAG's spreading activation),
or **(3) let the store talk back and restructure itself** (Luhmann's
Zettelkasten, A-MEM's evolving notes, Voyager's automatic curriculum — the
only system that generates genuinely *new* questions, new tasks, at the
frontier of what its memory can almost do).

## Process — how this study was made

Written as the work happened, per the standing doctrine.

- **Route.** Local context first (the liquid-world-model README, THOR-TEST,
  the observatory follow-up, the day-cycle R&D note, the Pincher scout), then
  six search sweeps in the brief's territory order, preferring arXiv papers
  and project docs; secondary surveys used only for triangulation and for
  claims attributed to them. ~40 pages/results opened or read in full text;
  30 sources cited in `sources.json`.
- **Dead ends.** (a) Bush's 1945 essay itself: I read the Memex through
  strong secondary treatments rather than the Atlantic text — the trail
  mechanics are not in dispute, but the citation is to the summaries, and
  says so. (b) A YouTube talk on A-MEM was considered and skipped: the paper
  is short and primary; a talk would have added performance, not evidence.
  (c) Several 2026-dated survey preprints with implausible arXiv numbering
  turned up in results; I used them only where their claims could be
  cross-checked against the primary papers, and never as sole support.
- **Disappointments.** Vendor benchmark claims in this field are a food
  fight (Zep's LoCoMo 84% → Mem0's correction 58.44% → Zep's counter
  75.14%); all vendor numbers below are labelled vendor numbers. The
  "hippocampal" branding in otherwise good work oversells an analogy the
  papers themselves state more carefully. And the most-cited ancestor,
  Luhmann, is routinely flattened into "take atomic notes" — the actual
  essay is about *surprise as a design requirement*, which most summaries
  drop. The primary text (in translation) was worth the detour.

## The axis

Every system below is graded on one question: **does the memory structure
generate the next question?**

- **3 — The walk asks.** Traversal/retrieval itself produces a question,
  task, or probe the walker did not arrive with.
- **2 — The walk re-aims.** The question is fixed, but what the path
  encounters mid-walk changes what gets asked next, or the store restructures
  itself between walks.
- **1 — Need-shaped fetch.** Retrieval is state-dependent (decay, tiers,
  activation), but the question comes from outside the memory.
- **0 — Store and fetch.** Excellent plumbing; the memory never asks
  anything.

Grades are about this axis only. A 0 here can still be the right tool for
most jobs — it just isn't what Casey asked about.

---

## 1. The ancestors

### Memex trails (Bush, 1945) — grade 1

- **Structure.** A personal store of documents on microfilm, joined by
  *associative trails*: hand-built chains of links between items, with the
  researcher's annotations in the margins. Trails can be shared, dropped into
  another memex, and amplified there.
- **How the walk works.** You follow a trail a past self (or a colleague)
  laid down. The trail *is* a frozen inquiry: a sequence of "this, because
  of this, leads to this."
- **Does the path ask?** Weakly. A trail confronts you with your past self's
  associations in an order your present question didn't choose — mild
  serendipity, and Bush's hope of "wholly new forms of encyclopedias… with a
  mesh of associative trails running through them." But the trail never
  grows a new branch on its own; every question in it was asked by a human,
  once. It is the shape of the idea, not the engine.
- **What breaks.** Trails are hand-laid: the linking cost is paid in human
  attention, forever, and trails fossilize the interests of the day they
  were made.

### Luhmann's Zettelkasten (1981 essay) — grade 3

- **Structure.** ~90,000 atomic paper slips in a *fixed placement order*
  (feste Stellordnung) — deliberately **not** a topical hierarchy. Each slip
  has a branching address (…/1a, /1b…) so new notes insert *inside* ongoing
  trains of thought. Value lives in the web of cross-references, not in any
  note.
- **How the walk works.** You enter anywhere — a keyword register, a
  remembered address — and follow references. Because placement is fixed but
  meaning isn't, you constantly meet notes in contexts their writer (you,
  years ago) didn't foresee.
- **Does the path ask?** This is the one system in the study *designed* so
  that it does. Luhmann's own criterion, from the primary essay: "One
  fundamental requirement for communication is that the partners can
  surprise each other… Information occurs when we compare a message or
  entry against other possibilities." He chose the open, non-topical
  structure specifically to build **chance** into the system, rejected
  systematic order because it would fix in advance what could be found, and
  described the result as a "second memory, an alter ego" that acquires "a
  life of its own" and *answers back*. The walk asks because the structure
  guarantees re-encounter under foreign comparison-schemas: every note is a
  question posed by a past self who was thinking about something else.
- **What breaks.** It needs years and critical mass before it talks (Luhmann
  is explicit: at first it's "just a container to retrieve things from"),
  and the linking discipline is a lifetime habit, not an install. In
  software terms: cold-start is brutal, and there's no compression — the
  human is the only summarizer.

## 2. Agent memory architectures

### Generative Agents (Park et al., 2023) — grade 2.5

- **Structure.** A *memory stream*: an append-only natural-language log of
  observations, each with creation and last-access timestamps. On top of
  it, *reflections* — higher-level inferences — are stored back into the
  same stream, and plans with them.
- **How the walk works.** Retrieval scores every memory by recency
  (exponential decay ≈0.995/hr), importance (an LLM-rated 1–10 at write
  time), and relevance (embedding similarity to the current focus).
- **Does the path ask?** Half of it genuinely does. When the summed
  importance of recent observations crosses a threshold, **reflection
  fires — and its first step is to generate questions**: the model is
  prompted for the most salient high-level *questions* the recent
  observations raise about a person or topic, retrieves against those
  questions, and only then writes insights (with pointers to the evidence).
  The memory periodically interrogates itself. What keeps it from a 3: the
  trigger is a scalar threshold, the questions serve believability rather
  than truth, and nothing checks a reflection against the world afterward.
- **What breaks.** Retrieval is a linear scan scored per query — fine for
  25 simulated villagers, not for a lifetime. Reflections can be wrong and
  then *self-reinforce*: later reflections build on earlier ones, and the
  survey literature flags exactly this failure (a false lesson, once
  stored, steers every future retrieval; no contradiction-checking or
  expiry is built in).

### MemGPT / Letta (Packer et al., 2023–) — grade 1.5

- **Structure.** OS-style tiers: *core memory* (small, always in context,
  self-edited in blocks), *recall memory* (searchable history), *archival
  memory* (cold vector store). The agent pages its own memory in and out
  with tool calls. Letta adds *sleep-time agents* that reorganize memory
  asynchronously while the primary agent idles.
- **How the walk works.** The agent decides, mid-task, what to search for
  and what to promote into core. Memory management is part of the action
  space, not a background pipeline.
- **Does the path ask?** The questions still come from the task; the memory
  system is a very good librarian who also reshelves at night. The
  sleep-time pass is the germ of question-generation ("what should the
  learned context become?") but in practice it consolidates rather than
  interrogates. Grade reflects real self-direction in *placement*, none in
  *inquiry*.
- **What breaks.** Self-editing is self-trusting: the agent can overwrite a
  good block with a bad one, injected content can instruct it to, and
  debugging a memory the agent rewrote is archaeology. Also the honest
  embarrassment from the benchmark literature: a Letta agent given plain
  **filesystem tools** scored 74.0% on LoCoMo against Mem0's specialized
  infrastructure at 68.5% — much of the category's sophistication is
  outperformed by an agent that can iteratively search and read its own
  notes. The walk matters more than the store. Remember that; it returns
  in the prototype.

### CoALA (Sumers et al., 2023) — framing, not a system

The taxonomy the field now shares: working / episodic / semantic /
procedural memory, with retrieval, reasoning, and grounding actions over
them. It asks no questions itself, but it's the map that lets you see who
else doesn't either: most "memory" products implement exactly one cell of
CoALA's table (usually semantic) and market the whole grid. CoALA also
surfaces a real label conflict the field still hasn't resolved — Reflexion's
stored text is filed as *episodic* by its authors and *semantic* by CoALA —
which matters when a vendor's "episodic memory" claim needs auditing.

### MemoryBank (Zhong et al., 2023) — grade 1

- **Structure.** A long-term store for companion chat, with an Ebbinghaus
  forgetting-curve updater: retention R = e^(−t/S); each recall increments
  strength S and resets the clock. Global user portrait + per-event
  summaries ride on top.
- **How the walk works.** Standard similarity retrieval — over a store whose
  *contents* have been shaped by decay and by past retrievals.
- **Does the path ask?** No — but it does something subtler than most
  fetch-stores: **what you walked before changes what exists to walk to**.
  Use-dependent availability is a primitive form of the path mattering.
  That's a 1, honestly earned, and it's the same trick the liquid chart's
  fog decay already plays.
- **What breaks.** The borrowed human forgetting curve is an aesthetic
  choice, not a validated transfer; decay deletes the rarely-used, which in
  real lives is often the rarely-used-*but-critical*.

### Reflexion (Shinn et al., 2023) — grade 2

- **Structure.** An episodic buffer of *verbal self-critiques*: after a
  failed trial, the agent writes a natural-language post-mortem ("I failed
  because…; next time…"), stored and prepended to the next attempt.
- **How the walk works.** No walk — a stack of lessons, re-read whole.
- **Does the path ask?** The stored item is the *answer to an implicit
  question the failure posed* ("what went wrong, what changes?"), and it
  re-aims the next attempt's behavior concretely (91% pass@1 HumanEval vs
  80% GPT-4 baseline in the paper). But the question is set by the task's
  pass/fail signal, not generated by the memory; cross-task, the buffer is
  inert. A strong 2 within a task, a 0 across tasks.
- **What breaks.** Entrenchment: a wrong self-critique biases every later
  trial, and the agent stops collecting the evidence that would overturn it
  — the survey literature names this *self-reinforcing error* as reflective
  memory's central unsolved risk.

### ExpeL (Zhao et al., 2024) — grade 1.5

- **Structure.** Offline: run many training tasks (Reflexion-style),
  *contrast* successes against failures, and distill the difference into a
  pool of natural-language "insights" (rules of thumb) plus a vector store
  of successful trajectories. At test time: insights + nearest successful
  trajectories go in the prompt.
- **Does the path ask?** At write time, genuinely: the contrastive step
  asks the discriminative question — *what differed between the run that
  worked and the run that didn't?* — which is a better question than
  "summarize today." At read time it's ordinary similarity fetch. The
  ablation is instructive for us: abstract insights helped most on
  knowledge tasks, concrete retrieved trajectories on procedural ones —
  different memory *kinds* for different question kinds.
- **What breaks.** Insights over-generalize (a rule learned in one context
  applied blindly in another), the pool is static after training, and
  nothing retires an insight that the world has stopped rewarding.

### Voyager (Wang et al., 2023) — grade 3

- **Structure.** Three parts: an **automatic curriculum**, an ever-growing
  **skill library** of executable code (each skill indexed by an embedding
  of its description, composable — new skills call old ones), and an
  iterative prompting loop with environment feedback and self-verification.
- **How the walk works.** The curriculum agent, given the agent's current
  state and inventory, *proposes the next task* — aiming at the frontier:
  things not yet done but now plausibly within reach. Attempted tasks
  produce either a verified new skill (stored) or feedback that re-queues
  the task. Skills retrieved by similarity when a new task resembles an old
  one.
- **Does the path ask?** Yes — the strongest *learning-timescale* version
  in this study. The curriculum is an explicit question-generator
  conditioned on what memory can almost do: it asks "what is the nearest
  thing you cannot yet do?" and the library's growth keeps changing the
  answer. This is why Voyager compounds (3.3× more unique items, tech-tree
  milestones up to 15.3× faster, and the library transfers to a fresh
  world) while Reflexion plateaus: Voyager's memory doesn't just answer
  questions, it *manufactures the next one at the right difficulty*.
- **What breaks.** The curriculum is an LLM prompt, not a principle — its
  sense of "frontier" is vibes backed by a strong model; with weaker models
  the proposals degrade. Skill retrieval is description-similarity, so
  structurally-similar-but-differently-described skills are missed (the
  exact gap ELITE later attacks by retrieving on planning traces). And
  nothing prunes: the library only grows.

## 3. Graph-structured retrieval

### HippoRAG / HippoRAG 2 (Gutiérrez et al., 2024/2025) — grade 2

- **Structure.** An LLM reads the corpus into a schemaless knowledge graph
  of triples — the "artificial hippocampal index," by analogy to
  hippocampal indexing theory (neocortex holds the content; the
  hippocampus holds a graph of pointers and associations). HippoRAG 2 adds
  the passages themselves as first-class graph nodes linked to their
  concepts ("contains" edges), fixing v1's lossy separation of concepts
  from context.
- **How the walk works.** Literal walking: the query's entities become
  seed nodes, and **Personalized PageRank** spreads activation through the
  graph, resetting preferentially to the seeds. Multi-hop evidence arrives
  in one retrieval step because the walk crosses intermediate nodes nobody
  named in the query. HippoRAG 2 adds a one-step LLM "recognition memory"
  filter over candidate triples before the walk. Reported: +3 to +20 points
  over RAG baselines on MuSiQue/2WikiMultiHopQA, ~7% over the best dense
  retriever on associative tasks in v2, at 10–30× lower cost than iterative
  retrievers like IRCoT.
- **Does the path ask?** The walk retrieves by a need the walker couldn't
  articulate: pattern completion surfaces bridge entities that were in
  *neither* the query nor any single passage. That's the strongest form of
  re-aiming short of generating a question — the answer set is reshaped by
  the graph's structure mid-walk. It stays a 2 because the question itself
  never changes; PPR has no opinion about what to ask next, only about
  what's connected.
- **What breaks.** The graph is only as good as LLM triple extraction;
  synonymy edges are embedding guesses; and HippoRAG 2's own framing names
  the concept–context trade-off: graph-only versions *lost* factual recall
  to plain RAG until passages were made nodes. A graph walk over a badly
  extracted graph is a confident stroll through a wrong map.

### Microsoft GraphRAG (Edge et al., 2024) — grade 1

- **Structure.** LLM-extracted entity graph → hierarchical **Leiden
  communities** → an LLM-written summary ("community report") for every
  community at every level. Query time: *local search* around entities, or
  *global search*: map-reduce over community summaries, each producing a
  scored partial answer.
- **Does the path ask?** Mostly no, and the marketing should be audited:
  global search does not *walk* anything at query time — it reads
  precomputed summaries in parallel. The real achievement is different and
  worth naming correctly: GraphRAG **pre-answers the question "what is this
  corpus about?" at every scale**, so a vague global question ("main
  themes across 3,000 reports") becomes answerable at all. The community
  structure changes which questions are *askable*, not which are asked.
- **What breaks.** Indexing cost is the design, not a bug: an LLM reads
  everything and summarizes every cluster; updates historically meant
  partial-to-full rebuilds (the pain LazyGraphRAG later exists to defer).
  For a living memory — new episodes hourly — that cost wall is the whole
  story.

### RAPTOR (Sarthi et al., 2024) — grade 1.5

- **Structure.** Recursively cluster chunks and summarize clusters into a
  **tree**: leaves are text, upper nodes are abstractions of everything
  beneath them. Retrieval (in the better-performing "collapsed tree" mode)
  searches all levels at once.
- **Does the path ask?** It changes the *altitude* at which a question gets
  answered — a thematic question lands on a summary node, a detail question
  falls through to leaves, and one query can do both. The tree gives the
  walker somewhere to go *up* when the leaves don't add up, which is a
  primitive re-aim. But the tree is static once built, summaries inherit
  summarizer error at every level, and nothing in the walk suggests a
  better question.

### PathRAG (Chen et al., 2025) — grade 1

- **Structure/walk.** From query entities, enumerate relational paths in
  the indexing graph, prune by a resource-flow score (decay per hop,
  divided by node degree, early stop below a threshold), and present the
  surviving paths *as paths* in the prompt, best path last.
- **Does the path ask?** No — but it makes the walk *legible*: the answer
  arrives with its route attached, so a human or a checker can see exactly
  which chain of relations claims what. That legibility matters to us
  (receipts!), and the pruning insight is portable: **the failure mode of
  graph retrieval is redundancy, not insufficiency** — hubs flood naive
  walks. As question-generation, though, it's fetch with good manners.
- **What breaks.** Path counts explode with length and hubs; hub-pruning
  occasionally prunes the answer itself.

### Think-on-Graph (Sun et al., 2023/2024) — grade 2.5

- **Structure/walk.** The LLM itself walks a knowledge graph by **beam
  search**: at each hop it chooses which relations to explore, then which
  entities to keep, then judges whether the accumulated paths suffice to
  answer — or walks deeper. Explore → prune → judge, repeat, with the
  reasoning trace *being* the path.
- **Does the path ask?** Yes, in micro: each hop is a decision that
  reformulates the search ("of these relations, which one could possibly
  lead toward the answer?"), and the sufficiency judgment is the walker
  deciding whether it needs to ask more. The top question is fixed, which
  caps it at 2.5 — but within that, this is path-as-reasoning in the
  literal sense: the intermediate questions are generated by what the
  previous hop found.
- **What breaks.** Cost: up to ~2ND + D + 1 LLM calls per question, and
  the walker's judgment is the model's judgment — a wrong pruning at hop 1
  is unrecoverable at hop 3. ToG-2 and Plan-on-Graph exist precisely to
  patch these (text-grounded pruning; sub-goals, memory, backtracking) —
  which tells you the failure modes were load-bearing.

### Zep / Graphiti (Rasmussen et al., 2025) — grade 1.5

- **Structure.** Episodes (raw inputs, never rewritten) → extracted
  entities and fact edges → community summaries, all under a **bi-temporal
  model**: every edge carries valid-time (when the fact was true in the
  world) and transaction-time (when the system learned/superseded it).
  Contradiction doesn't delete; it invalidates — the old edge gets an
  `invalid_at` and stays queryable.
- **Does the path ask?** Retrieval is hybrid fetch (cosine + BM25 + BFS +
  rerank; notably, one independent practitioner reports the practical win
  is co-location of an entity with its facts, *not* traversal). But the
  temporal structure changes what is askable — "what did we believe on
  March 1st?" is a first-class query — and at *write* time the system
  genuinely re-aims: a new fact forces the question "does this kill
  something we currently hold?" That's the contradiction surfacing the
  brief asked about, implemented as invalidation rather than discovery.
  Half a grade of credit for the write side; the read side is fetch.
- **What breaks.** The graph is built by an LLM: entity resolution and
  temporal extraction are model judgments, so the audit trail's quality is
  the extractor's quality. Vendor-reported benchmarks (94.8% DMR, +18.5%
  LongMemEval) should be read as vendor numbers — and the LoCoMo dispute
  with Mem0 (84% → 58.44% → 75.14%, each side "correcting" the other)
  shows what this field's scoreboards are worth without independent reruns.

### G-Memory (Zhang et al., 2025) — grade 1.5

- **Structure/walk.** For multi-agent systems: a three-tier graph —
  *interaction* graphs (what the team actually did), *query* graphs, and
  *insight* graphs (generalized lessons). A new query triggers
  **bi-directional traversal**: up to insights, down to the condensed
  trajectories that earned them.
- **Does the path ask?** The two-direction walk is the notable move: an
  insight arrives with its evidence attached (descend to check it), and a
  raw trajectory arrives with its lesson attached (ascend to generalize).
  That's altitude-shifting in both directions — like RAPTOR, but over
  *experience* instead of documents. Still traversal toward a fixed query.
  Relevant to us because the fleet is a MAS: whose memory is whose is a
  real question in our house, and G-Memory is the one design here that
  starts from the team's trajectories rather than one agent's stream.

## 4. Self-organizing memory

### A-MEM (Xu et al., 2025) — grade 2.5

- **Structure.** Explicitly Zettelkasten-inspired: each memory becomes an
  atomic **note** with structured attributes (contextual description,
  keywords, tags). On arrival, a new note retrieves its nearest neighbors,
  an LLM decides which links to create — and then the distinctive move,
  **memory evolution**: the same LLM pass *rewrites the neighbors'*
  contexts, keywords, and tags in light of the new note.
- **Does the path ask?** The store restructures itself between walks: a
  note you retrieve next month is not the note that was written, because
  everything learned since has re-contextualized it. That is Luhmann's
  mechanism — re-encounter under changed comparison-schemas — implemented
  with an LLM as the re-writer. It beats prior SOTA on LoCoMo across six
  base models (authors' evaluation). Why not a 3: retrieval itself is
  still similarity-led, and evolution is unsupervised — nothing checks a
  rewrite against the episode it rewrites, so drift compounds silently.
  A-MEM has Luhmann's mutability without either Luhmann's patience or a
  ledger. (Our Pincher discipline — *the model is a claimant, the ledger
  is the truth* — is exactly the missing guard; see §7.)
- **What breaks.** Every insert costs LLM calls over a neighborhood; at
  scale the evolution pass is the budget. And LoCoMo is short, synthetic
  conversation — "evolves well over 35 sessions" is not "evolves well over
  a life."

### Two newer directions worth a line each

- **Retrieval-driven reconsolidation** (2025–26 preprint literature):
  treat *retrieval itself* as a write event — a memory that gets recalled
  becomes labile and is re-stored in its current context. This closes the
  loop A-MEM leaves open (evolution on read, not just on write) and is the
  closest machine analogue yet to how biological memory actually updates.
  Early, lightly evaluated — noted, not endorsed.
- **Learned graph edges (ACGM line)**: memory construction as a learned
  decision process — edges optimized by policy gradient on *downstream
  task success*, so the retrieval topology itself adapts to what worked.
  The obvious endpoint of the whole graph section: if the walk is what
  matters, train the walk's ground. Also the obvious risk: the topology
  overfits to yesterday's tasks.

## 5. Retrieval that interrogates

### FLARE (Jiang et al., 2023) — grade 3

- **Structure.** Not a memory store — a *protocol* between a generator and
  any corpus. Iteratively: generate a **temporary next sentence**; if it
  contains low-probability tokens, use that sentence as the query, retrieve,
  and regenerate the sentence conditioned on what came back.
- **Does the path ask?** This is the purest mechanism in the study, and the
  headline for a reason. Two design decisions do all the work:
  (1) the trigger is the walker's own uncertainty, measured at the point
  of continuation — retrieval happens *because the path faltered*, never
  on a schedule or a fixed plan; (2) the query is **forward-looking** —
  not what was just said, but a draft of what is about to be needed. The
  path asks its question in its own future tense, and the answer is
  allowed to change the sentence that asked. Nothing else surveyed
  generates questions with this little machinery and this precise timing.
- **What breaks.** The trigger is only as honest as the model's
  calibration: a confidently wrong continuation never fires retrieval
  (the known FLARE failure; later work notes tentative-span errors
  compound into hallucinated queries). And it has no memory across
  generations — every document starts the walk from zero. FLARE is a
  *gait*, not a *home*. The interesting question for us is what happens
  when that gait walks a persistent chart (see §8).

### IRCoT (Trivedi et al., 2023) & Self-Ask (Press et al., 2023) — grades 2.5 / 2

- **IRCoT** interleaves chain-of-thought with retrieval: each generated
  reasoning sentence becomes the next retrieval query; retrieved passages
  steer the next sentence. Reasoning and retrieval genuinely alternate —
  the path re-aims every step. Costs scale linearly in hops, and the
  literature names its drift failure precisely: *entity drift*, where a
  pronoun in a follow-up query loses its referent and retrieval wanders.
- **Self-Ask** makes the questions explicit ("Follow up: …"), answering
  each before proceeding. Cleaner to audit than IRCoT, but the
  decomposition is more front-loaded — the follow-ups are the model's
  plan, less often the path's surprise. Both are gaits again, not stores;
  both compose with HippoRAG (the HippoRAG paper itself reports
  complementary gains from the combination).

### HyDE (Gao et al., 2022) — grade 2

- **Structure.** Given a query, the LLM first *hallucinates an answer
  document* — explicitly fake, possibly wrong in detail — embeds *that*,
  and retrieves real documents near the fabrication. The encoder's
  bottleneck filters the false details; the relevance pattern survives.
- **Does the path ask?** Inverted, and clever: instead of asking the
  corpus a question, you show it a **picture of the answer** and ask
  "what do you have that looks like this?" For walkers whose needs are
  easier to recognize than to state — most needs, most of the time — this
  is the right shape of query. It's a one-step trick, not a walk; grade 2
  for the inversion, which §8 steals outright.

## 6. Predictive framings — memory as a model you query by walking it

Light touch, two anchors, one honest bridge.

- **Predictive processing / active inference** (Rao & Ballard's predictive
  coding, generalized by Friston's free-energy principle): perception is
  not recording; a generative model predicts incoming signal and only
  *prediction error* propagates. Action is the other error-canceller:
  move so the world matches the prediction. The hippocampal evidence fits
  the same shape — place-cell sequences *preplay* candidate trajectories
  before decisions (Johnson & Redish; Pfeiffer & Foster; reviewed by
  Pezzulo et al.): the brain literally **walks its map in simulation
  first**, and the walk's outcome steers the real one. Memory, in this
  framing, is not consulted — it is *run*, and running it is what thinking
  is.
- **Nemori** (Ma, Nan & Wu, 2025; ACL 2026) is the one engineering system
  here built directly on that principle. Two cascades: raw interaction →
  coherent episodes; then each episode is compared against an
  **anticipatory schema** synthesized from existing knowledge, and *only
  the prediction-error residual* — what the schema failed to anticipate —
  is distilled into semantic memory. Its framing question is the right
  one: not "what's important?" (designer heuristics, importance scores)
  but "**what deserves memory? — what could we not have predicted?**"
  Predictable content is redundant *by definition*; the store keeps
  surprise. Its authors ground it in event segmentation theory and the
  free-energy principle (the Predict–Calibrate principle).
- **The JEPA bridge — stated as analogy, with our own receipt as the
  ground.** JEPA-family models predict in *representation* space: given a
  context and an action, predict the embedding of what comes next, never
  decoding pixels. A memory you can query by walking is exactly a model
  that, at each node, can score candidate next-steps by predicted
  representation — preplay with a learned value function. We do not have
  to take this on faith from the JEPA literature: **our own V-JEPA probe
  (this programme, 2026-10-26) measured it** — frozen V-JEPA pair
  embeddings + action + a fitted readout classified transitions
  (stayed/moved/blocked) at 0.976 against 0.711 for the best
  after-view-only readout, with the margin concentrated exactly in
  stayed-vs-arrived, the distinction a snapshot cannot make. And the
  probe's disciplines transfer: the signal needed a *fitted* readout
  (raw similarity scored 0.72) — in predictive language, the walk needs a
  learned head, which is precisely what a night phase is for; and the
  cheap/expensive split the numbers argued (I-JEPA pairs nightly, V-JEPA
  for the doubtful) is a budget policy for simulation depth. What we
  should *not* claim: that JEPA embeddings constitute a question-asker.
  They supply the simulator. The questions still come from disagreement
  between simulation and chart — which is prediction error again, wearing
  our clothes.

## 7. Honest negatives — where the "walk" is marketing

- **Mem0's "graph memory."** The base product is LLM fact-extraction over
  a vector store — competent fetch, honestly a 1 on this axis (its
  ADD/UPDATE/DELETE reconciliation is real work). The graph is a separate
  paid tier, and independent practitioners report the vector and graph
  stores don't inform each other ("getting Elena's rich facts requires a
  separate vector search… the two stores don't talk"). Buying "graph
  memory" here buys a second silo with edges in it.
- **GraphRAG's query-time "traversal."** Vendor decks describe walking the
  graph; global search actually map-reduces precomputed summaries. The
  walk happened at *index* time, at index-time prices. If your memory
  changes hourly, you are re-paying the walk constantly or walking a
  stale map.
- **"Hippocampal" as a brand.** HippoRAG's mechanism is PageRank over
  extracted triples; the neuroscience is a design metaphor the paper
  states carefully and the coverage states breathlessly. The system earns
  its grade on the walk's results, not on the analogy.
- **Believability benchmarks for memory.** Generative Agents' evaluation
  is believability, not correctness; LoCoMo/LongMemEval numbers across
  this study are small, synthetic, and (per the Zep–Mem0 public dispute)
  actively contested between vendors. Treat every score quoted above as
  "the authors' measurement on a proxy task," including the ones I like.
- **Reflection without a referee.** Reflexion, ExpeL, and Generative
  Agents all let the model grade its own homework into permanent storage.
  The survey literature's warning deserves repeating as a rule: a stored
  false lesson doesn't just sit there — it *steers future retrieval*,
  suppressing the evidence that would correct it. Any memory that rewrites
  itself (A-MEM included) without an append-only ground truth underneath
  is a rumor mill with good indexing. This is the one place our house
  discipline is ahead of the literature: Pincher/zero's *model is a
  claimant, the ledger is the truth* — claims verified against a ledger
  before they commit — is exactly the guard the self-organizing-memory
  papers are missing.

## 8. What we steal, and for which of our machines

| # | Idea (source) | Steal it for | The move |
|---|---|---|---|
| 1 | Spreading-activation walk over the index (HippoRAG PPR) | **liquid chart recall (essence tier)** | The chart is already a graph: places, exits, conditional edges (`opens_with: brass key`). Recall becomes PPR seeded at (current place, goal-belief), with edge weights = charted confidence × fog factor. The essence answer is the walk's top neighborhood, not a key lookup — and bridge places surface the way bridge entities do in HippoRAG. |
| 2 | Faltering triggers the query (FLARE) | **lwm policy + priced recall** | The chart already computes the falter signals: fog-decayed confidence, low-trust observations, margin-ties (THOR-TEST's 0.3-trust matches). Rule: when the walk reaches a place whose effective confidence is low *or* two prototypes tie, that — and only that — authorizes spending the 12-unit truth recall or a re-observation probe. Retrieval budget spent at points of measured ignorance, never uniformly. |
| 3 | Frontier curriculum (Voyager) + the chart's uncharted set | **lwm day cycle; fleet morning alignment** | The framework already enumerates what it knows it hasn't charted — Casey's day-cycle note calls the map of ignorance the curriculum; Voyager is the existence proof that an explicit frontier-proposer compounds. Morning alignment = a proposed probe list ranked (uncharted × fog × surprise-density), generated from the chart, not written by hand. |
| 4 | Prediction-error gating (Nemori) | **dream() / nightly testimony** | Before testimony, the day-model *reconstructs* the day from essence + chart (its anticipatory schema). Only the residual — events the model cannot reconstruct — earns semantic storage as lessons. Implements "nothing leaves without testifying" as predict–calibrate, and gives "the story is the maintenance schedule" a mechanism: the story *is* the residual. |
| 5 | Bi-temporal invalidation (Graphiti) | **chart belief history; Pincher zero** | The chart keeps both versions of every belief but can't yet answer "what did we believe on day 1?" Add valid-time intervals to belief revisions (the append-only history already has the data). For zero: claims get validity windows, so a superseded claim is invalidated, never deleted — the ledger stays the truth, now with a clock. |
| 6 | Link-and-evolve, ledger-guarded (A-MEM + Luhmann) | **fleet lesson files (AGENTS.md lessons, MEMORY.md)** | New lessons should link to the old lessons they extend or contradict, and propose re-contextualizations of them — but as *claims against the ledger*, committed only when verified, old text never silently rewritten. A-MEM's evolution with zero's referee: the Zettelkasten that can talk back, on a leash of receipts. |

Deliberately *not* stolen: GraphRAG's precompute-everything indexing (our
stores are small and alive; the cost wall buys nothing at our scale), Mem0's
extraction pipeline (our records are already structured at write time), and
any self-rewriting memory without the ledger guard (§7).

## 9. Prototype: **The Faltering Walk** — a question-generating recall over the liquid chart

**Artefact:** `lwm` as it stands (stdlib only), seed-7 dungeon first, then
the Thor visual world reusing the existing I-JEPA prototype chart.

**Mechanics.**
1. Build the walk graph from the chart: nodes = places; edges = believed
   exits, weighted by charted confidence × fog factor (0.9^fogged days) ×
   conditional satisfaction (an `opens_with` edge weighs full if the key
   is charted-held, near-zero otherwise).
2. `walk_recall(start, goal_belief)`: Personalized PageRank seeded at the
   start place and the goal place. Output is *not* an answer — it's a
   ranked **question list**, scored by activation × disagreement, where
   disagreement at a node = (a) two high-activation paths implying
   different destinations for the same exit, (b) prototype margin-tie
   (the observatory failure mode), (c) effective confidence below the
   trust floor (fog/never-verified), (d) an uncharted exit on a
   high-activation route.
3. The probe policy spends the existing purse (reflex 1 / essence 4 /
   truth 12) strictly in question-list order: fog questions buy a
   re-observation; contradiction questions buy a truth-tier recall of the
   exact testified event; uncharted-exit questions go to the next day's
   alignment as proposed probes (Voyager move, §8.3). Nothing is probed
   that the walk didn't rank.
4. HyDE move, inverted for charts: to seed the walk toward a goal place
   never visited, generate the place's *hypothetical description* from
   essence ("a room with treasure, past a locked door") and match it
   against prototypes/descriptions — the picture of the answer as bait.

**Cost.** One focused build in `lwm/tiers.py` + `lwm/policy.py` — PPR on a
13-node graph is arithmetic, not infrastructure; no new dependencies, no
rack calls for the dungeon version. The Thor version reuses existing
prototypes and receipts. Grading the question lists is the real cost:
~an hour of human/agent judgment per world.

**What would prove it works.** Against the current deliberately-dumb
policy as control, on both worlds:
- **Question quality:** the walk's top-3 questions include the known live
  issues (twin pair; locked door pre-key; the foggiest believed route) —
  judged blind against a hand-written list.
- **Next-day surprises per recall unit spent:** question-ranked probing
  must beat "probe nearest uncharted exit" (the shipped policy) on
  surprises avoided per unit of purse. 
- **Steps-to-goal honesty check:** improvement must come from the chart,
  not the walker — S1 machinery byte-identical, per the THOR-TEST
  attribution discipline.

**Falsifier, stated in advance:** if question-ranked probing does not beat
the dumb policy on surprises-per-unit, the walk is decoration — keep PPR
recall (§8.1) as a plain retrieval improvement, publish the negative, and
the chart goes back to asking nothing. A result either way is a receipt;
a walk that only *feels* smarter is the failure mode this whole study
exists to avoid.

---

*Sources: see `sources.json` (30 entries, each with what was taken from
it). Grades are this study's, argued from the cited mechanisms; benchmark
figures are the original authors' unless flagged as vendor claims.*
