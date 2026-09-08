# The five-layer marker checklist

The working reference. Use for **audit** (what to look for) and **rewrite** (what to
change). Evidence and citations live in `ai-vs-human-writing.md`. This file is the
operational distillation.

**The one rule that governs all five layers:** AI writing is *up-register*. Almost every
fix is a **downshift**, and almost every fix is **subtraction**. You have far more
leverage over what the model adds than over what it removed (van Nuenen 2026: additive
tendencies drop ~55% under instruction, subtractive ones only ~10 to 15%). So work the
restore list first.

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
