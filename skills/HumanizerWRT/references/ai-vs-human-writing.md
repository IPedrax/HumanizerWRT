# How AI writing differs from human writing: the evidence base

Research dossier for **HumanizerWRT**. Compiled 2026-09-08 from ~40 peer-reviewed and
preprint studies (PNAS, Science, ACL/EMNLP/ICML, Artificial Intelligence Review, PubMed).
Every claim here is sourced. Where studies conflict, the conflict is stated rather than
averaged away.

Reading order: §0 is the whole dossier in one page. §1 explains *why* the differences
exist, which is what makes them predictable. §2 to §6 are the five layers of difference,
ordered from surface to deep. §7 is what human readers actually notice. §8 to §10 are the
traps: the places where the obvious inference is wrong, and where naive humanizing
makes things worse.

---

## 0. Executive summary

**Seven findings that should drive the design of anything called a "humanizer":**

1. **The tell is not one thing, it is a stack.** Lexicon, syntax, rhythm, discourse, and
   stance each carry independent signal. Fixing only the vocabulary layer (the thing
   every consumer "AI humanizer" does) leaves the other four intact. Expert human
   readers detect paraphrased AI text *more* often than unparaphrased AI text
   (88% vs 69.8% of explanations cite AI vocabulary), because paraphrase reshuffles
   words while preserving the deeper shape. [Russell 2025]

2. **Instruction tuning causes it, not scale.** Llama-3 *base* models write at
   near-human rates on Biber's 66 lexicogrammatical features; their instruction-tuned
   siblings do not. Bigger models are not more human: GPT-4o deviates further from
   humans than GPT-4o-mini on several features. The "AI voice" is an artifact of
   RLHF/DPO, and it is traceable to *typicality bias* in preference data: annotators
   systematically prefer familiar text. [Reinhart et al. 2025 PNAS; Zhang et al. 2025]

3. **"More sophisticated" is the wrong direction.** Every documented LLM tendency (
   richer vocabulary, longer words, more nominalization, more commas, fewer
   contractions, more abstraction) points the same way: *up-register*. Humanizing is
   almost always a **downshift**, not an upgrade. [van Nuenen 2026]

4. **Lexical diversity is the strongest single discriminator, and its direction is
   counter-intuitive.** Within a document, AI text has *higher* type-token ratio and
   *higher* entropy than human text, roughly 2 SD and 1 SD respectively. AI avoids
   repeating a word; humans repeat words constantly. Across many documents, the
   relationship inverts: AI collapses onto a narrow shared vocabulary while a set of
   human authors sprawls. See §8.1. Getting this backwards is the single most common
   error in humanizing advice. [Shan et al. 2026; El Attar et al. 2026]

5. **Generic "make this sound human" does not work.** Optimizing against a generic
   "machine" signal is ill-posed, because human writing is not a distribution. It is a
   pile of idiolects. DPO against a detector, DIPPER paraphrase, and adversarial
   prompting all degrade FastDetectGPT and Binoculars while leaving *style-embedding*
   detectors at 64 to 66 AUROC-degraded-to-96. What actually closes the gap is conditioning
   on **a specific named human author's samples**. [Rivera Soto et al. 2026]

6. **AI *editing* leaves a different, much fainter trace than AI *generation*.**
   AI-generated text separates from human text at AUROC 0.97 on stylometry alone.
   AI-*edited* human text separates from its human source at only 0.80, and it moves in
   the *opposite* direction from the generation footprint on entropy. Human-first,
   lightly-edited is not "weak AI text"; it is a categorically different object.
   [Shan et al. 2026]

7. **The gap human readers report is mostly about substance, not style.** Across 16
   datasets and 9 languages, the main human-machine gaps are *concreteness* and
   *cultural nuance*. Expert annotators cite originality (23.7%), quotes (22.3%), and
   clarity (19.5%) alongside vocabulary. A humanizer that only touches surface form is
   solving the small half of the problem. [Wang et al. 2025; Russell et al. 2025]

---

## 1. Why AI writes the way it does

Understanding the mechanism matters because it tells you which tells are stable (worth
building rules around) and which are model-of-the-month artifacts.

### 1.1 Typicality bias in preference data → mode collapse

Post-training alignment reduces output diversity. The usual explanation blamed the
algorithm; Zhang et al. (2025) show the driver is **data-level**: human annotators rating
preference pairs systematically favor familiar, prototypical text, a well-replicated
effect in cognitive psychology (mere-exposure, processing fluency). RLHF therefore
sharpens the model onto the mode of "what reads as unsurprising."

Consequences documented across the literature:

- Aligned models show **lower entropy in token predictions** and cluster tightly in
  embedding space. [Mohammadi 2024]
- Instruction-tuned models restrict randomness via an "implicit blueprint," trading away
  next-token world-modeling for coherent long-form generation. [Li et al. 2024]
- Even at temperature 1.0, structural formatting (role markers, chat templates) induces
  **diversity collapse** independent of sampling. [Li et al. 2025]
- Across many generations, LLM novels show *compressed formal variation* relative to a
  human corpus in the same target style. The question is not whether one passage passes,
  but whether twenty passages sprawl the way twenty human texts do. [2608.12630]

### 1.2 The lexical overuse puzzle

"Delve," "intricate," "underscore." Their spike is real and enormous: `delve` at +1,500%
across six scholarly databases 2015→2024, `underscore` +1,000%, `intricate` +700%.
[Kousha & Thelwall 2025]

Why these words? Juzek & Ward (2024) tested and **failed to find support** for the
training-data-frequency explanation. The best-supported account is **Learning from Human
Feedback**: Zheng (2025) emulated the LHF procedure on Llama and reproduced the lexical
preference experimentally. So the overused vocabulary is not inherited from the corpus.
It is *manufactured by preference tuning*.

Practical corollary: the specific words rotate as labs patch them (arXiv abstracts show
`delve` frequency **dropping** from early 2024, right after it was publicly named, while
`significant` kept climbing [Liang et al. 2025]). Word blocklists decay. The generating
mechanism does not.

### 1.3 Genre misalignment

Reinhart et al. (2025, PNAS) frame the deepest version of the problem: instruction tuning
trains one **informationally dense, noun-heavy register** and applies it everywhere. The
model does not modulate for genre the way humans do. Words that are unremarkable in
literary fiction (`tapestry`, `camaraderie`, `solace`) become conspicuous in a news
article or a lab report. The failure is not "wrong words". It is **wrong register for
this genre**, which is why the same output can read fine as a blog post and absurd as a
patient note.

---

## 2. Layer 1: Lexicon

### 2.1 The excess-vocabulary corpus (strongest quantitative source)

Kobak et al. (2024/2025) analyzed **15.1M PubMed abstracts, 2010 to 2024**, using an
excess-mortality-style counterfactual. Findings:

- 454 excess words in 2024 vs a pre-LLM baseline where **no single word** ever exceeded
  the δ>0.01 gap between 2013 and 2019.
- The Covid-era excess was **content words** (nouns: `remdesivir`, `lockdown`). The 2024
  excess is **style words**: of 379, **66% verbs and 14% adjectives**.
- Top frequency *ratios*: `delves` r=28.0, `underscores` r=13.8, `showcasing` r=10.7.
- Top frequency *gaps* (common words, higher absolute impact): `potential` δ=0.052,
  `findings` δ=0.041, `crucial` δ=0.037.
- Lower bound on LLM-processed 2024 abstracts: **13.5%**. Heterogeneous by subgroup:
  0.05 for UK/Australia, ~0.20 for China/South Korea/Taiwan, 0.25 for *Sensors*, 0.07 for
  Nature/Science/Cell. LLM usage correlates negatively with venue prestige.

**The ten highest-impact common markers** (Kobak's optimized "common set", Δ=0.134 on its
own): `across, additionally, comprehensive, crucial, enhancing, exhibited, insights,
notably, particularly, within`.

Note what that list is: mostly *ordinary words*. This is why blocklists of exotic words
(`tapestry`, `delve`) catch so little: the bulk of the signal is in mundane connectives
and intensifiers used at unnatural density.

The full 291-word rare set is in the source paper's Figure S6; high-yield extract:

> accentuates, adept, akin, aligns, alongside, amidst, bolster, burgeoning, capabilities,
> commendable, compelling, comprehending, consequently, crafted, culminating, delve,
> demonstrating, discern, elevate, elucidate, embracing, emphasize, employing, empowers,
> enabling, encompass, endeavors, enhances, ensuring, evolving, exhibiting, exceptional,
> exploration, facilitates, fostering, foundational, garnered, groundbreaking, harness,
> heightened, hinder, illuminating, imperative, inherent, innovative, integrates,
> interconnectedness, interplay, intricacies, intricate, invaluable, leveraging,
> meticulous, multifaceted, navigating, necessitates, notable, noteworthy, nuanced,
> offering, paving, pinpoint, pioneering, pivotal, poised, predominantly, pressing,
> profound, realm, refine, remarkable, renowned, revolutionize, robust, scrutinize,
> seamless, seamlessly, shedding, showcase, signifying, spanning, streamline,
> substantiated, surpass, swift, tailored, testament, thorough, transformative,
> uncharted, underscore, unlocking, unparalleled, unravel, unveil, uphold, versatility

### 2.2 Per-model overuse rates (parallel-corpus evidence)

Reinhart et al. (2025) measured words-per-1,000 against matched human text in the same
genre. Rates are **multiples of human usage**:

| Word | GPT-4o | 4o-mini | Llama-3-70B-Inst | Llama-3-8B-Inst |
|---|---|---|---|---|
| camaraderie | 162× | 171× | 24× | 23× |
| tapestry | 155× | 147× |   |   |
| intricate | 119× | 129× | 27× |   |
| underscore | 107× |   |   |   |
| unspoken | 102× |   |   |   |
| amidst | 100× | 90× |   |   |
| palpable | 95× | 145× | 47× | 48× |
| solace | 95× |   |   |   |
| unease |   |   | 63× | 101× |

`tapestry` appeared in **23%** of GPT-4o outputs; `amidst` in **27%**. Critically, the
**Llama base models show none of this**: the vocabulary bias is introduced by
instruction tuning, not by the training corpus.

### 2.3 Verbal tics (conversational register)

Wu et al. (2026): 160,000 responses, 8 frontier models, EN + ZH. Taxonomy:

| Category | Examples |
|---|---|
| Sycophantic openers | "That's a great question!", "Excellent observation!", "Absolutely!" |
| Pseudo-empathetic affirmations | "I completely understand your concern" |
| Hedging phrases | "It's important to note that…", "I have to be honest" |
| Overused vocabulary | delve, tapestry, nuanced, multifaceted |
| Filler transitions | "Furthermore", "Moreover", "Let me walk you through this step by step" |

Key dynamics:
- Tics **accumulate over a conversation**: ~**+110% from turn 1 to turn 20**. Long chat
  sessions produce progressively more formulaic text.
- Highly **task-dependent**: emotional-support prompts mean tic rate 0.55, role-play 0.49,
  debate 0.39, vs translation 0.09 and code 0.13. Subjective tasks are 4 to 6× worse.
- Human raters, N=120: sycophancy correlates with *perceived naturalness* at
  **r = −0.87**. Flattery is the single most legible robot signal.
- Higher temperature reduces tic rate but does not eliminate it.

### 2.4 Synonym avoidance

The sharpest concrete tell in the whole literature, from expert annotators: humans write
`says` over and over. AI reaches for `notes`, `explains`, `observes`, `emphasizes`.
[Russell et al. 2025] Same for the AI habit of never repeating a noun within a paragraph.
This is a *direct consequence* of the lexical-diversity inflation in §8.1.

---

## 3. Layer 2: Syntax and grammar

### 3.1 Biber features (the strongest study: n≈66,000 chunks, 6 models, 2 corpora)

Reinhart et al. (2025, PNAS) built parallel human/LLM corpora across six genres
(academic, news, fiction, spoken, blogs, TV/film scripts) and measured Douglas Biber's
66 lexicogrammatical features. A random forest separated 7 sources at 66% (chance 14%);
only **4.2% of LLM texts were misclassified as human**.

GPT-4o vs human, rate ratios with paired Cohen's *d*:

| Feature | Ratio | *d* | What it looks like |
|---|---|---|---|
| Present participial clauses | **5.3×** | 1.38 | "Bryan, *leaning* on his agility, dances around the ring, *evading* Show's blows." |
| Nominalizations | **2.1×** | 1.23 | "promoting sustainable consumption *patterns*" |
| 'that' clauses as subject | **2.6×** | 0.77 | "That the results held was surprising." |
| Phrasal coordination | **1.9×** | 0.81 | "X and Y, A and B" stacked noun phrases |
| Agentless passive | **~0.5×** |   | GPT-4o uses *half* the human rate |

Model-specific splits worth knowing: GPT-4o **avoids** clausal coordination while all
Llama-3 variants overuse it; GPT-4o overuses downtoners (`barely`, `nearly`) while Llama
avoids them. Do not treat "AI syntax" as one thing.

### 3.2 Constituents and dependencies (news domain)

Muñoz-Ortiz et al. (2024, *Artificial Intelligence Review*), 6 LLMs across 3 families:

- Human sentences are **longer on average**, but LLM **constituents are longer**: LLMs
  pack more into each phrase.
- Human texts show **more optimized dependency distances** (shorter head-dependent links,
  the cross-linguistically attested efficiency pressure).
- LLM output uses more **numbers, symbols, and auxiliaries** (an "objective" veneer) and
  more **pronouns**.
- Human sentence-length distributions are **more scattered** (see §4).

### 3.3 Syntactic uniformity

Argumentative essays, ChatGPT vs English native speakers: ChatGPT shows **lower
variability across multiple syntactic-complexity measures**: "more uniform and
formulaic." [PMC12316247] The signal is not that AI syntax is simple or complex; it is
that AI syntax has **low variance**.

---

## 4. Layer 3: Rhythm and information flow

### 4.1 The stylometric footprint (cleanest study: 45,000 texts, 8 LLMs, 5 domains)

Shan, Lee & Hao (2026) trained a logistic regression on 14 interpretable features.
Human vs AI-generated accuracy: **91.7% global**, 92.5 to 95.8% per domain, 79.5 to 99.1% per
model. Of 14 features, only **three** carry stable signal, and only two are robust across
every leave-one-out fold:

| Feature | Direction in AI text | Magnitude | Stability |
|---|---|---|---|
| **Lexical diversity** | **higher** | ~**+2 SD** | top-5 in 13/14 conditions |
| **Entropy** | **higher** | ~**+1 SD** | top-5 in 12/14 conditions |
| Burstiness | higher | 3rd by importance | *not* stable across domains |
| everything else |   |   | condition-dependent noise |

Robustness checks: feature rankings hold across temperatures 0.3/0.7/1.0 (mean Spearman
ρ=0.89); leave-one-LLM-out ρ=0.92; leave-one-domain-out ρ=0.83. Proprietary models
confirm the pattern (Gemini-3-Flash 82.1%, GPT-5.4-mini 78.6%) though secondary features
shift. **GPT-OSS-120B is the outlier at 79.5%**: some models are markedly more
human-like stylometrically.

Independent confirmation from a much larger feature sweep: El Attar et al. (2026) ran
**284 features × 27 LLMs × 10 domains**. Dropping the lexical-richness group costs
−13.1% F1 in-domain and **−27.7% out-of-domain**: an order of magnitude more than any
other group (next worst: information, −1.8%). On fully unseen domain+model pairs,
**lexical-richness features alone beat the full 284-feature model by +14.3% F1**. Every
other "known" linguistic indicator turned out to be model- or domain-contingent.

### 4.2 Burstiness and sentence-length variance

"Burstiness" is the folk term for variance in sentence length and predictability. Human
texts have **more scattered sentence-length distributions** [Muñoz-Ortiz 2024]. But two
caveats matter:

- Burstiness ranked 3rd in global importance yet **did not remain stable** across domains
  and generators [Shan et al. 2026]. It is a real signal, not a reliable one.
- **Late-Stage Volatility Decay**: across 120k samples, AI text shows log-probability
  fluctuations that *stabilize as generation proceeds*, with AI showing **24 to 32% lower
  volatility in the second half of a sequence**. Human writing stays variable throughout.
  [2601.04833] This is a more precise version of "burstiness": the tell is not average
  variance but *variance that flattens out toward the end*.

### 4.3 Uniform Information Density

The psycholinguistic UID hypothesis holds that speakers distribute information evenly.
The relevant twist: **model-generated responses follow UID *more* strictly than human
responses do** [Giulianelli et al. 2023]. Human information contours fluctuate, driven
by syntactic constraints, audience design, keeping the reader interested, and possibly an
implicit pressure toward periodicity [Tsipidi et al. 2025]. Perfectly even information
flow reads as machine-like.

There is also a bitter trap here: professional and legal drafting conventions push human
writers *onto the same low-perplexity, low-burstiness manifold LLMs occupy*. EPC Article
84 requires patent claims to be "clear and concise," which makes competent human patent
prose look statistically synthetic. [2607.13044]

---

## 5. Layer 4: Discourse and rhetoric

### 5.1 Structural tells

- **Groupings of three.** Multiple expert annotators independently flagged AI's habit of
  listing exactly three items, "with suspicious consistency." [Russell et al. 2025]
- **"Not X, but Y."** Named directly by annotators: *"the comparison of 'it's not just
  this, it's this'… along with listings of specifically three ideas."*
- **Templated transitions and paragraph-boundary similarity.** LLMs produce inflated
  inter-sentence transition variance driven by *recurring similarity bursts at paragraph
  boundaries*, formalized as Relational Over-Regularization, validated at p<0.001 across
  four benchmarks. [2608.26694]
- **Generic introductions and cheerful summary conclusions.** AI intros "essentially tell
  you what the entire article is about"; human intros open on an oblique detail.
  Annotators cite introductions in 7.3% of explanations. [Russell et al. 2025]
- **Discourse-structure repetition across documents.** QUDsim shows LLM texts on
  *different topics* reuse the same underlying discourse skeleton, invisible in any
  single document, glaring across a set. [2504.09373]

### 5.2 Quotes and named entities

Underrated and highly diagnostic. Annotators cite quotes in **22.3%** of explanations:

- AI quotes are placed in the **same position every time** (e.g. always paragraph-final).
- "Every expert speaks the same way and it's too homogenous with the text."
- Human quotes are short, awkwardly fitted, and don't perfectly state either side's view.
- **63.3% of GPT-4o and 70% of Claude-3.5-Sonnet articles contained the name "Emily" or
  "Sarah."** After humanization, models switched to real people's names but over-used
  titles (Dr., Prof.) far beyond human rates.

### 5.3 Punctuation

- **Em dashes.** Genuinely elevated in LLM output, to the point that OpenAI shipped a fix
  in Nov 2025. Note the *reason* it is a tell: not the dash itself (skilled human writers
  love it) but **density**: roughly three per paragraph. [TechCrunch 2025]
- **Curly quotes and apostrophes** where a human typing in a plain editor would produce
  straight ones.
- **Comma inflation.** AI rewriting increases comma frequency by **+67%** (d=+1.40), from
  ~8 to ~13 per text. [van Nuenen 2026]
- **Absence of dashes/ellipses in the human sense.** Annotators cite the *variety* of
  human punctuation ("dashes, brackets, quotes intermixed with sentences, and short
  spurts of comma sections") as a human signal. [Russell et al. 2025]

### 5.4 Grammatical over-correctness

AI text is "usually grammatically perfect"; human text "often contains minor errors."
Cited in 24.8% of expert explanations. This does **not** license fabricating typos (see
§10.2), but it does mean that aggressive copy-editing of human text pushes it toward the
AI side of the boundary.

---

## 6. Layer 5: Content, stance and emotion

This is the layer surface humanizers never touch, and per §0.7 it may be the larger half.

### 6.1 Concreteness and cultural nuance

Across **16 datasets, 9 languages, 9 domains**, 19 annotators reached 87.6% detection
accuracy, much higher than the near-chance findings of earlier studies. The gaps they
were exploiting: **concreteness** and **cultural nuance**. [Wang et al. 2025]

### 6.2 Emotional range

- Humans show **stronger negative emotions**: fear, disgust, and **less joy**.
  [Muñoz-Ortiz 2024]
- Human Yelp reviews show higher anger/disgust intensity and more low-valence tokens; AI
  reviews describing *the same negative experiences* skew high-valence with few or no
  anger signals. [El Attar et al. 2026]
- AI story arcs are "homogeneously positive and lack tension." [2407.13248]
- Annotators: AI "avoids darker or more mature topics," spends little time on the horrors
  and pivots to "hopeful quotes and potential cures." [Russell et al. 2025]

### 6.3 Epistemic-rhetorical miscalibration

LLMs display **rhetorical intensity out of proportion to epistemic grounding**: they
sound more certain than their evidence warrants, quantified via form-meaning divergence
and genuine-to-performed epistemic ratio across 0.6M tokens. [2604.19768] Related: prior
work finds ChatGPT-4 produces more nominalizations, **fewer human subjects, and fewer
epistemic stance markers** than human writers. [Jiang & Hyland 2024]

### 6.4 Narrative stance: the deepest measured shift

van Nuenen (2026), 300 personal narratives × 3 frontier models × 3 prompt conditions:

| Stance marker | Cohen's *d* | Direction |
|---|---|---|
| Retrospective framing ("looking back", "I now realize") | **+0.49** | ↑ |
| Abstraction density (abstract nouns: "situation", "realization") | **+0.58** | ↑ |
| Eventive clause density (action/perception verbs) | −0.31 | ↓ |
| First-person eventive ("I walked", "I saw") | −0.29 | ↓ |
| Causal connectives ("because", "as a result") | **−0.47** | ↓ |

Two linked movements: **embedded → distanced** narration, and **explicit causal reasoning
→ compressed interpretive abstraction**. In the author's phrase, the narrator who emerges
from AI revision is *"one who has already understood, whose backward-looking wisdom is
presumed rather than argued through causal reasoning."*

That is arguably the single most useful sentence in this dossier for a humanizer's
purposes.

---

## 7. What human readers actually notice

Russell et al. (2025) is the most operationally valuable study here. Five annotators who
*frequently use LLMs for writing* read 300 articles, labelled them, and wrote
paragraph-length justifications. Their **majority vote misclassified 1 of 300**: matching
the best commercial detector (Pangram) and beating GPTZero, Binoculars, Fast-DetectGPT and
RADAR. They stayed accurate against GPT-4o, Claude-3.5-Sonnet, o1-Pro, DIPPER paraphrase,
*and* a purpose-built humanizer.

Coded taxonomy of 1,500 explanations:

| Clue | Freq | Substance |
|---|---|---|
| **Vocabulary** | 53.1% | Repetitive, unnatural, or overly complex wording |
| **Sentence structure** | 35.9% | "not only… but also", groupings of three, uniform length |
| **Grammar & punctuation** | 24.8% | Too perfect; avoids dashes and ellipses |
| **Originality** | 23.7% | "Safe," no surprises, no humor; annotator gets bored |
| **Quotes** | 22.3% | Over-formal, homogenous with body text, identical placement |
| **Clarity** | 19.5% | Over-explains, telling rather than showing |
| Formality |   | Consistent register, no code-switching |
| AI names |   | Emily / Sarah / Dr. X |
| Tone | 9.3% | Uniformly neutral-to-positive, "inherent positivity bias" |
| Introductions | 7.3% | Generic; announces the whole article up front |
| Factuality | 7.2% | Confident errors |
| Topics | 3.1% | Avoids violence, graphic detail, moral ugliness |

Two findings from this study deserve to be design constraints:

- **Humanization did not fool the expert majority (still perfect on all 60 articles).**
  It only lowered their *confidence*. The prompt-based humanizer was itself derived from
  these experts' own stated clue-lists, and still failed.
- **Over-indexing on informality causes false positives.** Annotator 3, who treated
  contractions, slang, `just` and `actually` as human signals, was consistently fooled by
  o1-Pro. Adding casual markers is not humanizing; it is a different costume.

Counterpoint on how much this generalizes: untrained non-experts perform at **chance**
[Clark et al. 2021], and reviewers identified ChatGPT abstracts at **50%** [PMID
38627032]. Detection skill is a function of *heavy LLM exposure*, not intelligence or
domain expertise.

---

## 8. Measurement traps

### 8.1 The lexical-diversity paradox: read this twice

Three findings that look contradictory:

- Shan et al. 2026: AI-generated text has lexical diversity **~2 SD above** human.
- Muñoz-Ortiz 2024: human news text has **more variety of vocabulary** than LLM output.
- van Nuenen 2026: LLM rewriting **increases** MTLD +53% and Honoré's R +33%.
- 2412.10271: LLMs **fail to match** human linguistic diversity.

They are all correct, at different units of analysis:

**Within one document**, AI has higher diversity. It refuses to repeat. It reaches for a
synonym rather than saying `says` twice. Type-token ratio goes up.

**Across a set of documents**, AI has far lower diversity. Twenty AI essays share a
vocabulary; twenty human essays do not. van Nuenen states the resolution precisely:
*"Vocabulary diversity increases, but the distribution of that vocabulary becomes less
text-specific."* PCA confirms it: originals occupy a broad cloud, rewrites cluster
tightly; Claude reduced variance in **78% of 58 stylometric features**, median reduction
26%.

**Design consequence:** the instruction "use richer, more varied vocabulary" moves text
*toward* the AI signature on both counts. The correct instruction is nearly the opposite:
*let the same word repeat when repetition is what a person would do*, and let the
document's vocabulary be idiosyncratic to its subject rather than broadly literate.

### 8.2 Detectors are biased, and the bias is structural

- GPT detectors misclassify **non-native English writing as AI** at high rates
  [Liang et al. 2023, *Patterns*]. The foundational result, still replicating.
- The mechanism is not a calibration bug. A fine-tuned detector **does not learn an
  AI-vs-human boundary; it amplifies an inherited typicality axis** (predictability under
  a language model) that already existed pre-training. Consequence: detectors rate the
  median formal native-speaker essay as **99.5% likely AI** while clearing genuine
  high-temperature AI at 10.5%. `chatgpt-detector-roberta` flags 56% of formal essays at
  a 1% false-alarm rate. [2605.21653]
- Professional *editing* of a genuinely human manuscript raises its AI score, with authorship
  unchanged, linguistic form changed. [2608.26710]
- Detectors cannot distinguish permitted AI *editing* from full AI *drafting*: light
  "refine this abstract" edits are flagged 38 to 80%, while unmodified 2023 to 25 human
  originals are flagged 9 to 15%, with non-STEM far above STEM (p<0.001). [2608.11256]
- Structural argument: in real assessment the assessor does not know the individual
  student's writing distribution, making the null hypothesis **composite**: which places
  a mathematical floor under the false-positive rate. [2603.20254]

Bias has also been found along gender, race/ethnicity, ELL status, dialect, formality, and
grade level [2512.09292; BAID 2512.11505].

### 8.3 Diffusion models break the assumptions

LLaDA (diffusion-based) matches human text on perplexity and burstiness, producing high
false-negative rates for detectors built on autoregressive assumptions. [2507.10475]
Everything in §4 is calibrated on autoregressive generation.

### 8.4 Base models read as human

GPTZero and Pangram judge **base-model** output overwhelmingly human, while
instruction-tuned output from the same family is flagged. [2605.19516] Consistent with
§1.1. It is the alignment layer that is detectable.

---

## 9. What does *not* work

Documented failures, so the skill does not reinvent them:

| Approach | Result |
|---|---|
| Paraphrasing (DIPPER, GPT-4o) | Degrades FastDetectGPT/Binoculars; **StyleDetect holds at 96 AUROC**. Expert humans detect it *more* often. [Krishna 2023; Rivera Soto 2026; Russell 2025] |
| Detector-guided DPO | Beats the targeted detector; **style detectors unaffected** (65→65). [Nicks 2024; Rivera Soto 2026] |
| Adversarial prompting (OUTFOX) | Style AUROC 99. |
| Generic style transfer (TinyStyler) | Style AUROC 87; helps, insufficient alone. |
| Word-level blocklists | Words rotate. `delve` frequency **fell** in arXiv abstracts right after it was publicly named; `significant` kept rising. [Liang et al. 2025] |
| Adding contractions/slang/informality | Fooled exactly one annotator, who was the *least* accurate. [Russell 2025] |
| Iterative paraphrase | Creates a "laundering region": semantic displacement with generation patterns preserved. [PADBen 2511.00416] |
| "Voice-preserving" prompts | Reduce effect magnitude by only 32%; **direction unchanged on 85% of markers**. First-person pronouns and function words are the *most resistant* (~10 to 15% reduction). [van Nuenen 2026] |

The theoretical reason, stated best by Rivera Soto et al.: *"Human writing is not a
monolith; each author has her own idiosyncratic style… Without specifying a specific human
author as a target, generic optimization fails to converge to a valid human stylistic
fingerprint."*

Also worth internalizing: **19 commercial "AI humanizer" tools** were qualitatively
assessed for meaning preservation; many mangle it, and a data-augmented detector
(DAMAGE) catches humanized text at low FPR. [2501.03437]

---

## 10. What does work

### 10.1 Condition on a specific human author

The only approach that evaded *every* detector tested, including style-embedding
detectors, was a paraphraser jointly optimizing for (a) undetectability and (b) adherence
to **a named human author's style**, using in-context exemplars of that author's writing.
[Rivera Soto et al. 2026]

Corollary for skill design: **HumanizerWRT should be a voice-matching tool.** Its primary
input is not "make this human" but "make this sound like *this* person, whose samples are
attached." Everything in §2 to §6 becomes the checklist of *what to measure in the sample and
carry across*, not a set of global rules.

### 10.2 Prefer subtraction to addition

The asymmetry finding from van Nuenen (2026) is the most actionable single result for
prompt design: **users have more leverage over what the model adds than over what it
removes.** Voice-preserving prompts cut additive tendencies (emotion words, word length:
~55% reduction) far more effectively than subtractive ones (first-person pronouns,
function words: ~10 to 15%).

Practical translation:
- Explicit "do not add" instructions work. "Preserve" instructions largely don't.
- The reliable move is **restoring what was stripped**: contractions, function words,
  first-person density, causal connectives, eventive verbs, not decorating what's there.
- Watch for the perverse case: Claude under a *voice-preserving* prompt produced **more**
  literary stylization than under a generic one, treating "preserve voice" as a licence to
  render voice more emotionally legible. Instructions to preserve voice can backfire into
  performing voice.

### 10.3 The honest ceiling: multi-document detection

Even the successful style-aware attack evades only in the **single-document** regime. As
sample count grows the distributions separate again:

| Samples | Baseline AUROC | After attack |
|---|---|---|
| N=1 | 0.865 | 0.545 |
| N=5 | 0.9995 | 0.608 |
| N=10 | 1.000 | 0.676 |
| N=25 | 1.000 | 0.780 |
| N=50 | 1.000 | 0.882 |

[Rivera Soto et al. 2026, Reddit, newer generators Qwen3/Mistral-Nemo]

No text-level intervention makes a *body of work* look human. This is a hard limit and the
skill should say so rather than imply otherwise.

### 10.4 Editing beats generating

The strategic finding. Shan et al. (2026), 273,420 AI-edited texts, 31 prompts, 8 edit
categories, measured against their human sources:

| | Human vs AI-generated | AI-edited vs AI-generated | **Human vs AI-edited** |
|---|---|---|---|
| Stylometric LR | 0.97 | 0.98 | **0.80** |

AI-edited text stays **near its human source** in stylometric space, and a three-class
classifier misclassifies it as Human far more often than as AI-gen. It is *not* a midpoint.
The editing footprint is also directionally *different*: lexical diversity rises only
d=+0.24 and entropy **falls** d=−0.28 (versus the joint rise that marks generation). The
dominant editing signal is lexical density, d=**−3.10**: AI editing strips content words
relative to function words.

Caveat, and it is a real one: EditLens, a neural editing-aware detector, separates
human-from-edited at **0.97 AUROC** where stylometry gets 0.80. The stylometric safety of
edited text does not extend to purpose-built editing detectors, and separation grows with
edit ratio.

---

## 11. Positioning: what this skill should and should not be

The research forces a fork, and it is worth being explicit about which side is defensible.

**Not defensible, and also doesn't work:** a detector-evasion tool for passing AI text off
as human in a setting where that is prohibited. §9 shows the technical failure; §8.2 shows
the collateral harm: every advance in evasion pushes institutions toward detectors that
are already misfiring on non-native speakers, ELL students, and anyone who writes formally.

**Defensible, well-supported, and much more useful:** a **craft tool** that fixes the
actual defect the research documents: that LLM prose is registrally misaligned, lexically
inflated, emotionally flattened, epistemically overconfident, structurally formulaic, and
stripped of the person who was supposed to be writing it. Reinhart et al. make exactly
this argument: their intention was explicitly *not* to build detectors or police students,
but to identify "specific teachable moments in the revision of machine-generated text."

The two goals overlap heavily in *method* and diverge completely in *framing*. Framing it
as craft also produces the better tool, because it forces the §6 content layer: specificity,
concreteness, emotional honesty, causal reasoning, embedded rather than retrospective
stance, which is where the real quality gap lives and which surface evasion never touches.

Practical guardrails worth baking in:
- Do not fabricate typos, errors, or false hesitation. Grammatical imperfection is a
  *correlate* of human authorship, not a cause; manufacturing it is dishonest and
  annotators read it as costume.
- Do not invent personal anecdotes, quotes, or specifics the author did not supply. The
  §6.1 concreteness gap is real, but it closes by *asking the author for the detail*, not
  by hallucinating it.
- State the limits plainly: no rewriting makes a body of work look human (§10.3), and
  detectors will produce false positives on genuine human writing regardless (§8.2).

---

## Bibliography

Ordered by how much weight this dossier puts on them.

**Primary**
- Reinhart, A., Markey, B., Laudenbach, M., Pantusen, K., Yurko, R., Weinberg, G., Brown, D.W. (2025). *Do LLMs write like humans? Variation in grammatical and rhetorical styles.* **PNAS** 122(8):e2422455122. arXiv:2410.16107
- Shan, Z., Lee, Y., Hao, S. (2026). *AI Writers Have a Consistent Stylometric Footprint, but AI Editors Do Not.* arXiv:2608.27855
- El Attar, Y., Dönmez, E., Maurer, M., Falenska, A. (2026). *A Systematic Analysis of Linguistic Features in AI-Generated Text Detection Across Domains and Models.* arXiv:2606.04177
- Russell, J. et al. (2025). *People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text.* arXiv:2501.15654
- Rivera Soto, R.A., Chen, B., Andrews, N. (2026). *Attacks on Machine-Text Detectors Retain Stylistic Fingerprints.* ICML. arXiv:2505.14608
- van Nuenen, T. (2026). *Voice Under Revision: LLMs and the Normalization of Personal Narrative.* arXiv:2604.22142
- Kobak, D. et al. (2024/2025). *Delving into LLM-assisted writing in biomedical publications through excess vocabulary.* arXiv:2406.07016 / PMC12219543
- Muñoz-Ortiz, A., Gómez-Rodríguez, C., Vilares, D. (2024). *Contrasting Linguistic Patterns in Human and LLM-Generated News Text.* **Artificial Intelligence Review** 57. arXiv:2308.09067

**Mechanism**
- Zhang et al. (2025). *Verbalized Sampling: How to Mitigate Mode Collapse and Unlock LLM Diversity.* arXiv:2510.01171
- Zheng (2025). *Word Overuse and Alignment in LLMs: The Influence of Learning from Human Feedback.* arXiv:2508.01930
- Juzek, T., Ward, Z. (2024). *Why Does ChatGPT "Delve" So Much?* arXiv:2412.11385
- Mohammadi (2024). *Creativity Has Left the Chat: The Price of Debiasing Language Models.* arXiv:2406.05587
- Kirk et al. (2023). *Understanding the Effects of RLHF on LLM Generalisation and Diversity.* arXiv:2310.06452
- Li et al. (2025). *The Price of Format: Diversity Collapse in LLMs.* arXiv:2505.18949
- Wu, S. et al. (2026). *The Rise of Verbal Tics in LLMs.* arXiv:2604.19139
- Cheng, M. et al. (2026). *Sycophantic AI Decreases Prosocial Intentions and Promotes Dependence.* **Science** 391(6792).

**Corpus / diachronic**
- Kousha, K., Thelwall, M. (2025). *How much are LLMs changing the language of academic papers after ChatGPT?* arXiv:2509.09596
- Liang, W. et al. (2025). *Human-LLM Coevolution: Evidence from Academic Writing.* arXiv:2502.09606
- (2025). *Large language models reshape the language of science.* arXiv:2504.12317
- (2026). *AI-Associated Lexical Shifts Across 34 Languages.* arXiv:2605.25358
- Yakura, H. et al. (2024). *Empirical evidence of LLM influence on human spoken communication.* arXiv:2409.01754

**Detection & evasion**
- Mitchell, E. et al. (2023). *DetectGPT.* ICML. arXiv:2301.11305
- Bao, G. et al. (2024). *Fast-DetectGPT.* arXiv:2310.05130
- Hans, A. et al. (2024). *Spotting LLMs With Binoculars.* arXiv:2401.12070
- Krishna, K. et al. (2023). *Paraphrasing evades detectors of AI-generated text, but retrieval is an effective defense (DIPPER).* arXiv:2303.13408
- Sadasivan, V.S. et al. (2025). *Can AI-Generated Text be Reliably Detected?* arXiv:2303.11156
- (2025). *DAMAGE: Detecting Adversarially Modified AI Generated Text.* arXiv:2501.03437
- (2026). *Base Models Look Human To AI Detectors.* arXiv:2605.19516
- (2026). *When AI Settles Down: Late-Stage Stability.* arXiv:2601.04833
- (2026). *Relational Over-Regularization.* arXiv:2608.26694
- (2025). *Can You Detect the Difference? (diffusion vs AR).* arXiv:2507.10475

**Bias & fairness**
- Liang, W. et al. (2023). *GPT detectors are biased against non-native English writers.* **Patterns**. arXiv:2304.02819 / PMC10382961
- (2026). *Amplifying, Not Learning: The Price of OOD Generalization in AI-Text Detection.* arXiv:2605.21653
- (2026). *Style as a Confound: False Positives in AI Detection of Non-Native Academic Writing.* arXiv:2608.26710
- (2026). *Why AI Detection Fails for Academic Integrity.* arXiv:2608.11256
- (2026). *AI Detectors Fail Diverse Student Populations.* arXiv:2603.20254
- (2025). *Identifying Bias in Machine-generated Text Detection.* arXiv:2512.09292
- (2025). *BAID: A Benchmark for Bias Assessment of AI Detectors.* arXiv:2512.11505

**Human perception**
- Clark, E. et al. (2021). *All That's 'Human' Is Not Gold.* arXiv:2107.00061
- Wang, Y. et al. (2025). *Is Human-Like Text Liked by Humans? Multilingual Human Detection and Preference.* arXiv:2502.11614
- Jakesch, M. et al. (2023). *Human heuristics for AI-generated language are flawed.* **PNAS**. PMC10089155

**Discourse & content**
- (2025). *QUDsim: Quantifying Discourse Similarities in LLM-Generated Text.* arXiv:2504.09373
- (2024). *Are Large Language Models Capable of Generating Human-Level Narratives?* arXiv:2407.13248
- (2026). *Saying More Than They Know: Epistemic-Rhetorical Miscalibration.* arXiv:2604.19768
- Jiang, F.K., Hyland, K. (2024). *Does ChatGPT argue like students? Bundles in argumentative essays.* **Applied Linguistics**.
- Markey, B., Brown, D.W., Laudenbach, M., Kohler, A. (2024). *Dense and disconnected: Analyzing the sedimented style of ChatGPT-generated text at scale.* **Written Communication** 41:571 to 600.
- (2026). *The Cost of Perfect English: Pragmatic Flattening and the Erasure of Authorial Voice in L2 Writing.* arXiv:2605.13055

**Information theory**
- Giulianelli, M. et al. (2023). *How do decoding algorithms distribute information in dialogue responses?* arXiv:2303.17006
- Tsipidi, E. et al. (2025). *The Harmonic Structure of Information Contours.* arXiv:2506.03902
- Meister, C. et al. (2021). *Revisiting the Uniform Information Density Hypothesis.* arXiv:2109.11635
