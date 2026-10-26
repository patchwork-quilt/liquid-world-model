# Design — liquid-world-model

The thinking this framework is built from (Casey, 2026-10-26).

## The centre

The whole system could be many things — engines, harnesses,
bodies — but it is designed around one part: **the liquid model**,
the part of a mind whose job is to reconstruct what the game
engine of the world really looks like from an incomplete picture.
In the id / ego / superego reading it is closest to the superego:
the one trying to figure out what things *mean*, and the only one
willing to doubt **both** the senses **and** the thoughts — the
ego's readings and its own conclusions are evidence to it, never
verdicts.

A static world model (the game engine, the simulator) never
doubts itself; it just renders its rules. The liquid model is the
opposite kind of thing: it actively probes the edges of what it
can prove to itself, because the map of where it breaks is its
curriculum.

## The founding image

Zelda in a dungeon he hasn't charted, without the map item: every
room he enters, he starts to learn it. The chart the liquid model
keeps is drawn the same way — from presence, not from revelation —
and it holds three kinds of things: what has been **charted**
(entered, observed), what is **believed** (inferred, confidence
attached, correctable, with the wrong versions kept), and the
**uncharted**: exits seen but never taken, enumerated as facts.
Knowing the shape of your ignorance is most of the map.

Real-time strategy adds the second truth: **fog of war**. What
you stop looking at fogs over. The internal engine runs on a
budget — it is a framework of understanding, not a second copy of
the world — so beliefs go stale, and retrieval itself costs the
same moments everything else does.

## The memory tiers

One history, several doors, priced differently:

- **Reflex** — the quickest route: the day's hot trail and the
  distilled essence (the base model and its accumulated
  adaptations, the LoRA layer), possibly redacted to what a
  reflex may know. For the answer needed *now*.
- **Essence** — the chart as it stands: believed answers, fog
  and all.
- **Truth** — the slow route: the ledger, "when I think back on
  how it actually happened." The full testified record, opened
  when the question deserves the correct one and can wait.

Layers quicker than reflex and slower than truth both exist in
the wider fleet (the Pincher and Lever Runner projects work the
quick end); this framework names the seam they plug into.

## The day

The liquid model lives in days (see
research notes in the programme's R&D repo): wake with the day's
alignment; work with a model of the world that is mutable through
text; dream before sleeping — the day testifies, nothing leaves
without testifying — then flush the presence, keep the essence,
and let the next day's adaptation carry what the day taught.
Nodes with bodies (redshirts and growers) are where these days
are lived; this repo is the framework those nodes share.

## Provider slots (named, not built here)

- **Perception providers** at the trust-flag seam: JEPA-class
  models that read a scene and report both a reading and how far
  to trust it.
- **Distillation providers** at the dream seam: learned adapters
  (the nightly LoRA) replacing today's text-level distillation.

The framework's claim is narrower and stronger than either: give
it any engine through the contract, and the chart, the fog, the
tiers, and the day will behave the same way — measurably.
