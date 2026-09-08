# The five-layer marker checklist

The working reference. Use for **audit** (what to look for) and **rewrite** (what to
change). Evidence and citations live in `ai-vs-human-writing.md`. This file is the
operational distillation.

**The one rule that governs all five layers:** AI writing is *up-register*. Almost every
fix is a **downshift**, and almost every fix is **subtraction**. You have far more
leverage over what the model adds than over what it removed (van Nuenen 2026: additive
tendencies drop ~55% under instruction, subtractive ones only ~10 to 15%). So work the
restore list first.

## Targets, not directions

Every instruction below has a **band**, because a direction without a ceiling gets
overshot. This was measured, not assumed: in a pilot where four models drafted with and
without this checklist, the skill fixed everything it targeted (em dashes failed 4/4
without it and 0/4 among the models that obeyed the rule) and then overshot on
contractions, which got *worse* with the checklist than without it. Models given
"restore contractions" with no upper bound pushed to 53 per 1k against a human median
of 14.

Reference bands are in `human-bands.json` (n=2,146 human stories, pre-2018, so no LLM
contamination). **Register-specific: short literary fiction.** For anything else, profile
the author instead and use their range (`voice-profile.md`).

| Marker | Human p10 to p90 | Median | Failure mode to avoid |
|---|---|---|---|
| Contractions / 1k | **0 to 36** | 14 | Overshoot. Fiction is far less contraction-heavy than "sound casual" implies |
| Sentence-length CV | **0.48 to 0.84** | 0.64 | Overshoot. Above ~0.85 the variance is itself a pattern |
| Em/en dashes / 1k | **0 to 5.7** | 0 | House rule is 0; the band shows humans rarely exceed it anyway |
| Lexical diversity (MATTR) | **0.58 to 0.68** | 0.63 | Above the band means synonym-hunting |
| Function words % | **44.5 to 54.5** | 49.6 | Below the band means content-word stuffing |
| Nominalisations / 1k | **2.5 to 20** | 8.7 | Both ways. Zero is as unnatural as forty |
| Long words % | **5.5 to 12.5** | 8.3 | Undershoot. The downshift needs a floor too |
| Mean word length | **3.9 to 4.6** | 4.2 | Undershoot |
| Commas / 1k | **28 to 83** | 55 | Overshoot |
| First person / 1k | **4 to 105** | 55 | Very wide; POV choice dominates |
| Participials / 1k | **0 to 11** | 3.2 | Overshoot |
| Three-item lists / 1k | **0 to 2.9** | 0 | Overshoot |
| Marker vocabulary / 1k | **0 to 2** | 0 | Overshoot |
| Causal connectives / 1k | **0 to 10** | 3.9 | Undershoot |

Check with `python3 scripts/stylo.py audit draft.md --band`. Watch **deviation**, not the
in-band count: a count scores a 9% overshoot the same as a 4x one. Human reference texts
run a deviation around 0.1; the pilot's unaided drafts ran 2.7.

**Do not drive deviation to zero.** Real human texts sit outside about one band. A text
inside every band is more average than a person, and that is its own tell.

### The bands are necessary and not sufficient. This was measured.

Giving four models these bands plus the checking tool cut mean deviation from 0.91 band-widths
to 0.009, a hundredfold improvement, with three of four landing at exactly 0.00, which is
*better than the human reference texts* (0.056 and 0.091).

**The blind ranking did not move at all.** Mean rank of the skill group was 5.25 out of 10
before the bands existed and 5.25 after. Humans stayed at 1.50. One model hit 0.00 deviation
and still placed 9th of 10.

The judge explained why, and it is Layer 4, not Layer 1 to 3. It convicted the machine texts
on a shared *discourse skeleton*: a recluse who has not opened the blinds, an unremarkable
visitor in a cardigan, one long monologue arguing that certainty destroys faith, a quiet
closing gesture. Two texts independently opened with blinds unopened "since March"; two used
the identical "he didn't scream / he'd rehearsed this / it felt almost ___" beat.

So the bands close the surface layers and the tell simply relocates. This is §5.1 of the
dossier arriving in practice: LLM texts reuse the same discourse skeleton across a set,
invisible in any single document and obvious across several.

**What follows for how you use this.** Deviation is a floor, not a target. Passing it means
you have stopped losing on vocabulary, rhythm and punctuation. It says nothing about whether
the *shape* of the piece is one every model reaches for, and that is now the larger share of
what remains. Vary the structure, not the sentences: whose story it is, where it starts, what
the visitor wants, whether anything is resolved. If you are producing several pieces, check
them against each other, because the marker panel cannot see this and will happily report a
clean score on ten texts with one skeleton.

---

**Restore before you remove, and remove before you add:**

| Priority | Move | Why it comes first |
|---|---|---|
| 1 | Restore contractions, function words, first person, causal connectives | Most resistant to prompting; largest gap; nothing else works until these are back |
| 2 | Cut marker vocabulary, tics, formulae, nominalisation | High-signal, low-risk, mechanical |
| 3 | Break rhythm uniformity | Requires judgement; do after the lexicon settles |
| 4 | Restore stance and concreteness | Needs author input (§5), never invent |

---

## Layer 1: Lexicon

### Cut

**The ten common markers carry more signal than the exotic ones.** Ordinary words at
unnatural density: `across, additionally, comprehensive, crucial, enhancing, exhibited,
insights, notably, particularly, within`. A blocklist of `tapestry`/`delve` catches almost
nothing by comparison.

**High-rate overuse words** (Reinhart 2025, multiples of human rate): camaraderie 162×,
tapestry 155×, intricate 119×, underscore 107×, unspoken 102×, amidst 100×, palpable 95×,
solace 95×, fleeting 84×, unravel 83×, unease 63×.

**Verbal tics**: the strongest single tell (sycophancy ↔ perceived naturalness r=−0.87):
- Sycophantic openers: "That's a great question", "Absolutely!", "Excellent point"
- Pseudo-empathy: "I completely understand your concern"
- Hedges: "It's important to note that", "I have to be honest"
- Fillers: "Furthermore", "Moreover", "Let me walk you through this"

**Note:** tics accumulate ~110% from turn 1 to turn 20 of a conversation, and run 4 to 6 times
higher on subjective tasks than on technical ones. Long chat-derived drafts are worse.

### Restore

**Let words repeat.** The sharpest concrete tell in the literature: humans write `says`
over and over; AI reaches for `notes`, `explains`, `observes`, `emphasizes`. Same for
nouns. AI will not use the same noun twice in a paragraph. Repetition is not a defect to
be edited out; it is what a person does.

**Do not "improve" the vocabulary.** See dossier §8.1. Raising lexical variety moves the
text *toward* the AI signature, not away from it.

### Caution

Word lists decay. `delve` frequency *fell* in arXiv abstracts immediately after it was
publicly named, while `significant` kept rising. Treat the lists as examples of a
mechanism, not as the mechanism.

---

## Layer 2: Syntax

| Feature | AI rate vs human | Fix |
|---|---|---|
| Present participial clauses | **5.3×** (d=1.38) | ", leaning on his agility, dances" → split into finite clauses: "He leans on his agility. He dances…" |
| Nominalisations | **2.1×** (d=1.23) | "promoting sustainable consumption patterns" → "getting people to consume less" |
| 'that' clauses as subject | 2.6× (d=0.77) | "That the results held was surprising" → "The results held. That surprised us." |
| Phrasal coordination | 1.9× (d=0.81) | Unstack the noun phrases |
| Agentless passive | **0.5×**, AI uses *less* | Do not add passives; this one runs the other way |

Also: AI constituents are *longer* even though AI sentences are *shorter*; AI dependency
distances are less optimised than human ones. Practical translation: AI packs too much
into each phrase. Unpack phrases into clauses.

**Model-specific, do not overgeneralise:** GPT-4o avoids clausal coordination; all Llama-3
variants overuse it. GPT-4o overuses downtoners (`barely`, `nearly`); Llama avoids them.

---

## Layer 3: Rhythm and information

The two most robust discriminators in the entire literature are here.

- **Lexical diversity**: AI ~2 SD above human within a document. Robust across 8 LLMs,
  5 domains, 3 temperatures, 27 further LLMs and 10 further domains.
- **Entropy**: AI ~1 SD above human.

Dropping lexical-richness features costs −27.7% F1 out-of-domain; on unseen domain+model
pairs those features *alone* beat a full 284-feature model by +14.3%.

**Sentence-length variance.** Human distributions are more scattered. The tell is
uniformity, not length. Fix by writing genuinely short sentences (three words, four
words) next to genuinely long ones. Do not merely alternate; that produces its own
pattern.

**Late-stage volatility decay.** AI variance *flattens in the second half* of a piece:
24 to 32% lower late-sequence volatility, while human writing stays variable throughout.
Check the back half of any long draft specifically. This is where AI text gives itself
away and where writers stop paying attention.

**Uniform information density.** Model output follows UID *more strictly* than human
output. Perfectly even information flow reads as machine-made. Humans spike and lull.

*Caveat:* burstiness ranked 3rd globally but was **not stable** across domains and
generators. Real signal, unreliable one. Do not over-fit to it.

---

## Layer 4: Discourse and rhetoric

**The formulae**, each named directly by expert annotators:
- **"Not just X, but Y."** Also the dash and comma variants: `not just X — it is Y`.
- **Groupings of three.** "with suspicious consistency." Break to two or four, or make
  the third item non-parallel.
- **Templated transitions** at paragraph boundaries. LLMs show recurring similarity
  bursts exactly there (p<0.001 across four benchmarks).
- **The generic introduction** that announces the whole article, and the **cheerful
  summary conclusion**. Human intros open on an oblique detail and often just stop.

**Punctuation:**
- Em dash: the research finding is that the dash is fine and ~3 per paragraph is not.
  The house rule overrides it: budget 0, including en dashes and a spaced hyphen doing
  a dash's job. Rewrite as a comma, colon, parenthesis, or two sentences.
- Commas: AI rewriting inflates them +67% (d=+1.40), roughly 8 → 13 per text.
- Curly quotes/apostrophes where a plain editor would give straight ones.
- Human punctuation is *varied*: dashes, brackets, quotes, short comma bursts mixed.
  Annotators cite this variety as a human signal.

**Quotes and names** (cited in 22.3% of expert explanations, badly underrated):
- AI quotes sit in the same position every time, often paragraph-final.
- "Every expert speaks the same way and it's too homogenous with the text."
- Real quotes are short, awkwardly fitted, and don't neatly state either side's case.
- **63.3% of GPT-4o and 70% of Claude-3.5-Sonnet articles contained "Emily" or "Sarah."**
  Humanized output switches to real names but over-uses titles (Dr., Prof.).

**Grammatical over-correctness**: cited in 24.8% of explanations. This is a *correlate*,
not a lever. See guardrail G1.

**Across documents:** LLM texts on *different topics* reuse the same discourse skeleton
(QUDsim). Invisible in one document, glaring across a set. If producing several pieces,
vary the shape, not just the words.

---

## Layer 5: Stance, substance, emotion

The layer surface humanizers never touch, and plausibly the larger half of the problem.
Across 16 datasets and 9 languages the main human-machine gaps were **concreteness** and
**cultural nuance**.

### The narrative stance shift (the deepest measured effect)

| Marker | Cohen's *d* | Direction under AI |
|---|---|---|
| Retrospective framing ("looking back", "I now realize") | **+0.49** | ↑ |
| Abstraction density ("situation", "realization") | **+0.58** | ↑ |
| Eventive clauses (action/perception verbs) | −0.31 | ↓ |
| First-person eventive ("I walked", "I saw") | −0.29 | ↓ |
| Causal connectives ("because", "as a result") | **−0.47** | ↓ |

Two linked movements: **embedded → distanced**, and **explicit causal reasoning →
compressed abstraction**. The AI-revised narrator is *"one who has already understood,
whose backward-looking wisdom is presumed rather than argued through causal reasoning."*

**Fix:** put the narrator back inside the events. Restore the verbs of action and
perception. Make the reasoning explicit again: say *because*, show the step. Cut the
retrospective wisdom-framing and the abstract nouns that replaced the argument.

### Embodied and sensory language

Scored on 20,000 parallel stories across 19 models and twelve sensory axes (Lancaster
sensorimotor norms plus Brysbaert concreteness). Every model differs from humans on at
least 10 of 12 axes. **The direction flips by family**, so this is the one marker where
you must know which model wrote the draft:

| Generator | vs human | Fix |
|---|---|---|
| Llama, OLMo, Phi, Qwen | significantly **less** sensory language | Restore it: what was felt, smelled, heard, what the body did |
| GPT | between, GPT-4o closer to human than GPT-3.5 | Check before acting |
| Gemini | significantly **more** on most axes | Cut it back; it over-reaches into sensory register |

Visual and concreteness are the sharpest splitters, and the most important features when
a classifier separates human from model on sensory scores alone.

Same cause as everything else: probes show models represent sensory language fine
(concreteness R²≈0.85 in deep layers), but in the Anthropic RLHF data *rejected* responses
carry more of it on nearly every axis, correlating with per-family underuse at up to
r=0.92. They were trained out of it rather than never having learned it.

**Do not accept a single percentage for "AI" here.** Popular versions of this finding
assign one number to all models. The largest parallel-corpus study finds the direction
itself is generator-dependent, so no single figure can be right. Sensory strength scored
against a lexicon is also a different construct from the share of emotion expressions
using a bodily metaphor; figures from one do not transfer to the other.

### Emotional range

- Humans show **stronger fear and disgust, and less joy**.
- On identical negative experiences, AI reviews skew high-valence with few or no anger
  signals; human ones carry low-valence tokens and genuine irritation.
- AI story arcs are "homogeneously positive and lack tension."
- AI "avoids darker or more mature topics," pivoting to hopeful framing.

**Fix:** let the negative stay negative. Do not resolve the tension. Do not end up.

### Epistemic calibration

LLMs show rhetorical intensity out of proportion to their evidence, with fewer human
subjects and fewer epistemic stance markers. **Fix:** name who did what; say what you
don't know; let a claim be smaller than the sentence around it.

### Originality

23.7% of expert explanations. "Safe," no surprises, no humour, annotator gets bored. This
is not fixable by editing. It is fixable by having something to say, which is a §5 input
problem (see guardrail G2), not a style problem.

---

## Guardrails

**G1. Never fabricate errors.** Do not insert typos, false hesitation, or fake
grammatical slips. Imperfection *correlates* with human authorship; manufacturing it is
dishonest and reads as costume. Note the corollary: aggressive copy-editing pushes genuine
human writing *toward* the AI side, so leave the author's real irregularities alone.

**G2. Never invent specifics.** Concreteness is the largest measured gap, and it closes
by *asking the author* for the detail: the name, the number, the date, what actually
happened, not by hallucinating a plausible one. When a passage needs a specific that
isn't in the source, flag it and ask. Inventing quotes, anecdotes, statistics or named
experts is out of scope regardless of how much it would improve the output.

**G3. Informality is not humanity.** Adding contractions, slang, `just` and `actually`
fooled exactly one annotator, the least accurate one in the study. Downshift where the
author's register warrants it, not as a costume.

**G4. State the limits.** No rewriting makes a *body of work* look human: detection
recovers from 0.55 AUROC at one sample to 0.88 at fifty. And detectors produce false
positives on genuine human writing regardless. They amplify a typicality axis, rating the
median formal native-speaker essay 99.5% likely AI. Don't imply a guarantee that the
research says is unavailable.
