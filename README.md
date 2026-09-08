<div align="center">
  <img src="assets/icons/feather.svg" width="56" alt="" />
  <h1>HumanizerWRT</h1>
  <p><strong>Take the AI voice out of writing, or never put it there. Five measured layers, ~40 cited studies, and a zero-dependency stylometry script, so it is measurement rather than vibes.</strong></p>
</div>

Every consumer "AI humanizer" does the same thing: swap words for synonyms and hope. The research says that fails. Expert readers detect *paraphrased* AI more often than raw AI (88% vs 69.8% of explanations cite AI vocabulary), because paraphrase reshuffles the surface and leaves the shape underneath intact.

**HumanizerWRT** works the shape. It measures which of five layers has drifted, then moves that layer back, toward a named human's voice wherever samples exist. It also ships an always-on block that installs itself into `CLAUDE.md`, so the register rules apply to every response instead of only when a skill happens to trigger.

Grounded in **named research, cited and linked**: Reinhart et al. (PNAS 2025) on Biber features across 66,000 parallel chunks, Kobak et al. on 15.1M PubMed abstracts, Shan et al. on the stylometric footprint across 8 LLMs and 5 domains, Rivera Soto et al. (ICML) on why generic evasion is ill-posed, van Nuenen on what LLM revision does to personal narrative, and Russell et al. on what expert human readers actually notice.

Built for **Claude Code** (Windows / macOS / Linux). No dependencies; the scripts are stdlib Python.

---

## <img src="assets/icons/check.svg" width="20" align="absmiddle" alt="" /> Three findings that govern everything

The whole skill falls out of these, and two of them are counter-intuitive enough to be worth stating plainly.

1. **Subtract, don't add.** Every documented LLM tendency points one way: *up-register*. Richer vocabulary, longer words, more nominalisation, +67% commas, −31% contractions, more abstraction. Humanizing is a downshift. And you have roughly 5× more leverage over what a model *adds* than over what it *removed*, so the restore list comes first.

2. **Raising lexical variety moves prose toward the AI signature, not away.** Within a document, AI already sits ~2 SD *higher* on lexical diversity than human writing. It refuses to repeat a word. Humans write `says` five times; a model reaches for `notes`, `observes`, `emphasizes`. "Improve the vocabulary" is backwards, and it is the single most common error in humanizing advice.

3. **Generic humanizing is provably ill-posed.** Human writing is not a distribution to move toward. It is a pile of idiolects. Paraphrase, detector-guided DPO and adversarial prompting all defeat perplexity-based detectors while leaving style-embedding detectors untouched. What closes the gap is conditioning on **a specific author's samples**. So the skill asks for samples.

---

## <img src="assets/icons/layers.svg" width="20" align="absmiddle" alt="" /> The five layers

| Layer | What drifts | Examples from the evidence |
|---|---|---|
| **1. Lexicon** | Marker vocabulary, verbal tics, synonym-hunting | `delve` +1,500% across six databases; GPT-4o uses *tapestry* at 155× the human rate, in 23% of its outputs; sycophantic openers track *inversely* with perceived naturalness at r=−0.87 |
| **2. Syntax** | Noun-heavy, participial, up-register | Present participial clauses at **5.3×** the human rate (d=1.38); nominalisations 2.1×; agentless passive at *half* the human rate, so this one runs backwards |
| **3. Rhythm** | Diversity and entropy up, variance down | Lexical richness is the most robust discriminator found: dropping it costs −27.7% F1 out-of-domain, and on unseen model+domain pairs it *alone* beats a full 284-feature model by +14.3% |
| **4. Discourse** | Formulae and templated structure | Groupings of three "with suspicious consistency"; "not just X but Y"; similarity bursts at paragraph boundaries; 63.3% of GPT-4o articles named someone Emily or Sarah |
| **5. Stance** | Embedded → distanced, causal → abstract | Retrospective framing d=+0.49, abstraction density d=+0.58, causal connectives d=−0.47. The narrator who emerges from AI revision "has already understood" |

Layer 5 is the one surface humanizers never touch, and it is plausibly the larger half. Across 16 datasets and 9 languages, the main human-machine gaps readers report are **concreteness** and **cultural nuance**.

---

## <img src="assets/icons/sparkles.svg" width="20" align="absmiddle" alt="" /> What it does

- **Measures instead of guessing.** A 24-marker panel computes lexical diversity (MATTR, MTLD), entropy proxies, sentence-length variance, late-stage volatility decay, nominalisation and participial rates, function-word share, contraction and first-person density, causal connectives, tricolon and "not X but Y" counts, and marker-vocabulary hits. Stdlib only.
- **Scores against a real human distribution, not a hunch.** `--band` checks every marker against percentiles measured on 2,146 human stories written before ChatGPT existed, so no LLM contamination. The headline number is *deviation in band-widths*, because a plain in-band count scores a 9% overshoot the same as a 4x one. Human reference texts run about 0.1.
- **Catches the tell a single-document check cannot see.** `independence` compares your drafts against each other and reports shared phrasing, calibrated on 159 human same-prompt pairs. Every blind test of this skill was lost on that layer rather than on any single sentence.
- **Profiles a real person, not "human" in the abstract.** Feed it three to five things the author actually wrote and it builds a median baseline *plus the observed range*, because how much someone varies is itself part of their voice.
- **Reads the layer a script cannot.** Stance, concreteness, emotional range, epistemic calibration. The tool covers layers 1 to 4 partially and layer 5 not at all, and the skill says so rather than pretending the number is the answer.
- **Prefers editing to regenerating.** AI-edited human text sits far closer to its human source (0.80 AUROC) than AI-generated text does (0.97), and moves entropy the *opposite* way. Where a real draft exists underneath, it edits that, and it tells you which it did.
- **Installs its own rules.** The highest-yield subset replicates into `CLAUDE.md` between marker comments, and a `SessionStart` hook repairs the block if it is deleted and updates it when the source changes. Idempotent, atomic, backed up, and removable with one command.
- **Refuses to fabricate.** No invented typos, no manufactured hesitation, no plausible-sounding anecdotes, quotes or statistics. Concreteness is the largest measured gap and it closes by *asking the author* for the real detail. The skill flags the gap and asks.
- **States its limits.** No rewriting makes a *body of work* look human: detection recovers from 0.55 AUROC at one sample to 0.88 at fifty. And detectors misfire on genuine human writing regardless, rating the median formal native-speaker essay 99.5% likely AI while clearing real high-temperature AI at 10.5%.

---

## <img src="assets/icons/check.svg" width="20" align="absmiddle" alt="" /> What the testing found

Four rounds of blind evaluation. Four Claude variants wrote the same story under different conditions; real pre-2018 Reddit stories on the identical prompt went in alongside them; a separate model ranked every text for humanness without ever seeing which was which.

Mean rank is only comparable **within** a round, because each round used a different mix of texts. So here is each round's own contest, with humans scoring 1.50 in every single one:

| Round | Treatment | vs | Control | Paired wins |
|---|---|---|---|---|
| 1 | directions only **5.25** | beats | no skill 7.75 | 4 of 4 |
| 2 | numeric bands **5.25** | beats | no skill 7.75 | 4 of 4 |
| 3 | effort-limited **6.75** | beats | deliberately flawed 9.00 | 3 of 4 |
| 4 | sequential divergence **5.50** | beats | parallel + bands 7.50 | 3 of 4 |

**It reliably makes writing better.** It won its paired comparison in every round, 14 of 16 pairings overall, and never lost a round.

**It does not make writing human.** Across four rounds and 34 machine texts, **zero** passed as human. Every human text outranked every machine text, every time.

Three findings that changed the skill, each of them a surprise:

- **Fixing the surface buys nothing on its own.** Giving models the bands plus the checking tool cut deviation a hundredfold, from 0.91 band-widths to 0.009, better than the human reference texts. The blind ranking did not move at all: 5.25 before, 5.25 after. The tell simply relocated to discourse structure.
- **Faking human error makes it worse.** Planting amateur flaws on purpose was the worst condition tested, losing to the same models writing carefully. Genuine lapses "cluster with other sloppiness"; planted ones are "single, isolated, and always positioned at a dramatic hinge." Placed flaws land on a beat. Real flaws land on nothing.
- **The largest gain came from cross-document independence.** Generating in sequence, each model diverging in shape from what came before, took shared phrasing from 16.7% of pairs to 0.0%, below the human rate, and was the only intervention to move the judge's *confidence* rather than just its ordering.

Everything in this README that makes a claim about effectiveness has a number behind it. The full protocol, the negative results, and the judge's own reasoning are in [`markers.md`](skills/HumanizerWRT/references/markers.md).

---

## <img src="assets/icons/globe.svg" width="20" align="absmiddle" alt="" /> Four modes

Route on what you hand it. When it is ambiguous, it asks rather than guessing between rewriting your text and writing new text.

| Mode | You say | It does |
|---|---|---|
| **audit** | *"does this sound AI?"* | Runs the panel, walks the five layers by eye, quotes the lines. Never returns a verdict or a percentage |
| **rewrite** | *"make this sound like me"* | Asks for samples, profiles them, rewrites in priority order, then diffs the result against your baseline |
| **draft** | *"write this, but not in assistant voice"* | Holds the constraints while writing instead of generating then fixing |
| **full** | an AI draft and a real wish for it to be good | audit → rewrite → re-audit, and names what it could not fix without your input |

---

## <img src="assets/icons/download.svg" width="20" align="absmiddle" alt="" /> Install

### <img src="assets/icons/terminal.svg" width="17" align="absmiddle" alt="" /> Claude Code (any platform)

```bash
claude plugin marketplace add IPedrax/HumanizerWRT
```

```bash
claude plugin install humanizerwrt@humanizerwrt
```

### <img src="assets/icons/monitor.svg" width="17" align="absmiddle" alt="" /> From a local clone

```bash
claude plugin marketplace add ./HumanizerWRT && claude plugin install humanizerwrt@humanizerwrt
```

> **Restart Claude Code after installing**, then `/HumanizerWRT` is available and the skill auto-triggers on requests about AI-sounding writing.

**Optional, and the part that makes it non-optional.** A skill only fires when a request matches its description. To apply the register rules to *every* response instead:

```bash
python3 ~/.claude/skills/HumanizerWRT/scripts/install.py
```

That splices a block into `~/.claude/CLAUDE.md` between `<!-- humanizer-wrt:begin -->` markers. Add a `SessionStart` hook to `~/.claude/settings.json` and it repairs itself on every model load:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "python3 \"$HOME/.claude/skills/HumanizerWRT/scripts/install.py\" --quiet 2>/dev/null || true",
            "timeout": 10
          }
        ]
      }
    ]
  }
}
```

`--check` reports without writing, `--uninstall` removes it cleanly, `--target PATH` points at a different `CLAUDE.md`. It only ever touches files you name, only ever the text between its own markers, and backs up to `~/.claude/backups/` before every write.

---

## <img src="assets/icons/chat.svg" width="20" align="absmiddle" alt="" /> How to use it

Just describe the problem:

- *"this reads like ChatGPT, fix it"*
- *"why does this sound robotic?"*
- *"rewrite this in my voice, here are three posts I wrote"*
- *"check this for AI tells before I send it"*
- *"draft the launch email, not in assistant voice"*

Or run the tooling directly:

```bash
python3 scripts/stylo.py audit draft.md --band                # panel, flags, human bands
python3 scripts/stylo.py profile me1.md me2.md me3.md --json > voice.json
python3 scripts/stylo.py diff voice.json draft.md             # worklist, biggest gap first
python3 scripts/stylo.py independence a.md b.md c.md          # do your drafts converge?
```

```
$ python3 scripts/stylo.py audit draft.md --band

HUMAN BAND   deviation 2.94 band-widths   (13/14 in band)
  reference: short literary fiction, n=2146
  ^^ em_dash_per_k               22.54   band 0 .. 5.72  +2.94w
     contraction_per_k           20.49   band 0 .. 36.515

FLAGS (6)
  [marker_rare_per_k = 78.95]  Marker vocabulary is dense...
  [verbal_tics = 2]            Sycophantic opener present...
  [tricolon_per_k = 10.53]     Frequent three-item lists...
```

```
$ python3 scripts/stylo.py independence draft1.md draft2.md draft3.md draft4.md

INDEPENDENCE   4 documents, 6 pairs
  50.0% of pairs share a span   (human same-prompt reference: 1.9%)
  ^^ 26.3x the human rate
      "that's not my responsibility marcus said but his voice"
      "the equations covered every wall"
```

---

## <img src="assets/icons/settings.svg" width="20" align="absmiddle" alt="" /> How it works

**Measure → find the drifted layer → restore what was stripped → cut what was added → break the rhythm → fix the stance.** Restore comes first because those features resist prompting hardest.

```
skills/HumanizerWRT/
├── SKILL.md                        router: four modes, five guardrails
├── references/
│   ├── markers.md                  the five-layer checklist + measured target bands
│   ├── voice-profile.md            getting samples, what to measure, failure modes
│   ├── always-on.md                source of truth for the CLAUDE.md block
│   ├── human-bands.json            percentiles from 2,146 pre-2018 human stories
│   └── ai-vs-human-writing.md      the dossier: ~40 sources, conflicts flagged
└── scripts/
    ├── stylo.py                    audit / profile / diff / independence. stdlib
    └── install.py                  replicate the block. --check / --quiet / --uninstall
```

`SKILL.md` is a router. It carries the three governing findings, the mode table and the guardrails, then loads exactly one reference for the job. The dossier is only read when you want the why, a number, or a citation.

Where studies disagree, the dossier says so instead of averaging. The clearest case is lexical diversity, which runs *opposite* directions depending on whether you measure inside one document or across many. Getting that backwards is what makes most humanizing advice actively harmful.

---

## <img src="assets/icons/check.svg" width="20" align="absmiddle" alt="" /> Verify

```bash
claude plugin validate .
```

```bash
python3 skills/HumanizerWRT/scripts/install.py --check
```

```bash
python3 skills/HumanizerWRT/scripts/stylo.py audit README.md --band
```

---

## <img src="assets/icons/file.svg" width="20" align="absmiddle" alt="" /> A note on what this is for

This is a craft tool. Its job is prose that is specific, honest, well-calibrated and sounds like its author, which happens to be the only approach the research shows working anyway.

It is not a detector-evasion tool, and it will not certify text as undetectable. That is partly because the technique does not work at the level people want, and partly because every advance in evasion pushes institutions toward detectors that already misfire hardest on non-native speakers, English-language learners and anyone who writes formally.

---

## <img src="assets/icons/file.svg" width="20" align="absmiddle" alt="" /> License

HumanizerWRT is [MIT](LICENSE).

The research it summarises belongs to its authors and is cited, not reproduced. Full bibliography in [`ai-vs-human-writing.md`](skills/HumanizerWRT/references/ai-vs-human-writing.md).
