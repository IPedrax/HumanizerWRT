---
name: HumanizerWRT
description: >-
  Diagnose and remove the "AI voice" from writing, and write without it in the first
  place. Audits text against the five layers where LLM prose measurably diverges from
  human prose (lexicon, syntax, rhythm, discourse, stance), rewrites AI-drafted text
  toward a specific author's voice using samples of their own writing, or drafts
  in-register from the start. Use this whenever the user wants writing that doesn't
  read as AI-generated: "make this sound like me", "this reads like ChatGPT", "remove
  the AI tone", "humanize this", "why does this sound robotic", "de-slop this", "write
  this in my voice", "does this sound AI", "check this for AI tells", or when they hand
  over an LLM draft to polish. Also use when drafting anything long-form where the
  default assistant register would be wrong. Grounded in ~40 studies (PNAS, Science,
  ACL/ICML); ships a stdlib stylometry script for measurement rather than guesswork.
---

# HumanizerWRT

Fix the thing that actually makes LLM prose read as LLM prose. Not by swapping words for
synonyms (the research says that fails) but by measuring which of five layers has
drifted and moving it back, toward a named human's voice wherever one is available.

**Evidence base:** `references/ai-vs-human-writing.md`. Read it once if you want the why;
the operational files below are self-contained.

## The three findings that govern everything here

1. **Subtract, don't add.** Every documented LLM tendency is *up-register*: richer
   vocabulary, longer words, more nominalisation, +67% commas, −31% contractions, more
   abstraction. Humanizing is a downshift. And you have ~5× more leverage over what the
   model *adds* than over what it *removed*, so restore the stripped features first.

2. **Generic humanizing is a provably ill-posed objective.** Paraphrase, detector-guided
   DPO and adversarial prompting all fail against style-based detection, and expert
   readers spot *paraphrased* AI more often than raw AI. What works is conditioning on a
   specific author's samples. Ask for samples.

3. **Raising lexical variety moves text toward the AI signature, not away.** Within a
   document, AI already has ~2 SD *higher* lexical diversity than human writing. It
   refuses to repeat a word. "Improve the vocabulary" is backwards. See dossier §8.1;
   this is the most common error in humanizing advice and it is worth not making.

## Modes

Route on what the user gave you. When ambiguous, ask. Don't guess between rewriting their
text and drafting new text.

| Mode | Trigger | Do this |
|---|---|---|
| **audit** | "does this sound AI", "check this", or any text handed over for diagnosis | §A |
| **rewrite** | "make this sound like me", "humanize this" + an existing draft | §B |
| **draft** | writing something new where the assistant register would be wrong | §C |
| **full** | an AI draft plus a real desire for it to be good | §D, the default when both are present |

---

## §A: Audit

1. Save the text to a file. Run:
   ```bash
   python3 scripts/stylo.py audit draft.md
   ```
2. Read `references/markers.md`. Walk the five layers against the text by eye. The script
   catches Layers 1 to 4 partially and Layer 5 not at all, and Layer 5 is the larger half.
3. Report as: **the marker panel** (what was measured), **the flags** (where to look), and
   **the layer-5 read** (stance, concreteness, emotional range, epistemic calibration:
   your judgement, quoting lines).
4. Quote specific lines. "Layer 4: three-item lists in ¶2 and ¶4" beats a score.

Never report a verdict or a percentage-likely-AI. The script's flags are heuristics with
no published human reference distribution behind them, and formal human writing trips
several of them legitimately. Say "look here", not "this is AI".

---

## §B: Rewrite toward a voice

1. **Read `references/voice-profile.md` first.** It covers getting samples, what to
   measure, what to read by eye, and the failure modes.
2. Ask for 3 to 5 samples the author wrote themselves, in the same register. If there are
   none, say plainly that this becomes a generic downshift, fixing layers 1 to 4 and leaving
   layer 5 largely untouched, and offer to proceed anyway.
3. Profile: `python3 scripts/stylo.py profile s1.md s2.md s3.md --json > voice.json`
4. Rewrite using `references/markers.md`, in the priority order given there: restore →
   cut → break rhythm → stance.
5. Verify: `python3 scripts/stylo.py diff voice.json rewrite.md`. Chase the restore
   markers. Land *inside* the author's observed range, not on their median.

**Prefer editing to regenerating.** AI-edited human text sits far closer to its human
source (0.80 AUROC) than AI-generated text does (0.97), and moves entropy the opposite
way. Where the author has a real draft underneath, edit that. Say which you did.

---

## §C: Draft in-register

Load `references/markers.md` before writing, and hold to it while drafting rather than
generating-then-fixing. If voice samples exist, profile them first (§B steps 1 to 3). The
same profile works for drafting.

The high-yield constraints, in rough order of payoff:

- No sycophantic opener, no summary conclusion, no "it's important to note".
- Let words repeat. Say `says` twice. Reuse the noun.
- Genuinely short sentences next to genuinely long ones, and keep that variance going in
  the **second half**, where AI text flattens 24 to 32% and writers stop paying attention.
- No "not just X but Y". No three-item lists unless there really are three things.
- Unpack noun phrases into clauses. Cut participial clauses (AI: 5.3× human rate).
- Say *because*. Show the causal step instead of asserting the conclusion.
- Stay inside the events. Cut retrospective wisdom-framing and the abstract nouns that
  replace an argument.
- Let negative things stay negative. Don't resolve the tension.

---

## §D: Full pipeline

§A → §B → re-audit, then report what moved:

```bash
python3 scripts/stylo.py audit draft.md          # before
python3 scripts/stylo.py diff voice.json out.md  # against the author
python3 scripts/stylo.py audit out.md            # after
```

Show the before/after on the markers that changed and name what you could not fix without
input from the author. That last part is not optional. See G2.

---

## Guardrails

**G1. Never fabricate errors.** No inserted typos, fake hesitation, or manufactured
grammatical slips. Imperfection correlates with human authorship; manufacturing it is
dishonest and reads as costume. Corollary: leave the author's real irregularities alone,
because copy-editing them pushes genuine human writing toward the AI side.

**G2. Never invent specifics.** Concreteness is the largest measured human-machine gap,
and it closes by **asking the author** for the name, the number, the date, what actually
happened, not by inventing a plausible one. Flag the gap and ask. Fabricated quotes,
anecdotes, statistics or named experts are out of scope no matter how much they'd improve
the draft.

**G3. Informality is not humanity.** Contractions, slang, `just` and `actually` as
decoration fooled exactly one annotator in the literature, the least accurate one.
Downshift to the author's register, not into a costume.

**G4. State the limits, don't imply a guarantee.** No rewriting makes a *body of work*
look human: detection recovers from 0.55 AUROC at one sample to 0.88 at fifty. And
detectors misfire on genuine human writing regardless. They amplify a typicality axis,
rating the median formal native-speaker essay 99.5% likely AI while clearing real
high-temperature AI at 10.5%. If someone wants a guaranteed detector pass, tell them the
research says that isn't available, and that the false-positive problem lands hardest on
non-native speakers.

**G5. This is a craft tool.** Its job is prose that is specific, honest, well-calibrated
and sounds like its author. That happens to be the only approach that works technically,
and it's the one worth building. Decline requests to certify text as undetectable or to
launder authorship for submission where AI use is prohibited, and offer the rewrite
instead, which is usually what the person actually wanted.

---

## The always-on core

A skill is model-invoked, so it only fires when something in the request matches its
description. The highest-yield subset of the rules above is therefore replicated into
`CLAUDE.md`, which loads into every context: chat and code, every project, whether or
not this skill is invoked. `references/always-on.md` is the single source of truth for
that block; `scripts/install.py` splices it between marker comments.

```bash
python3 scripts/install.py             # install or update ~/.claude/CLAUDE.md
python3 scripts/install.py --check     # exit 0 current, 1 stale or absent
python3 scripts/install.py --uninstall # remove the block, leave the file otherwise intact
python3 scripts/install.py --target ./CLAUDE.md   # a specific file instead (repeatable)
```

A `SessionStart` hook in `~/.claude/settings.json` runs `--quiet` on every model load, so
the block reinstalls itself if it's deleted and updates itself if `always-on.md` changes.
Quiet mode prints nothing when the block is already current, and a `systemMessage` when it
actually changed something.

**Scope, deliberately narrow.** The installer touches only CLAUDE.md files named on the
command line (default: the user's own global one), only the text between its own markers,
and only on this machine. It doesn't scan for other CLAUDE.md files, doesn't touch project
files unless asked, and writes nowhere else. Every write is atomic and backed up to
`~/.claude/backups/` first. `--uninstall` reverses it completely.

**When editing the rules, edit `always-on.md`, never CLAUDE.md directly.** A hand-edit
inside the markers registers as drift and gets overwritten at the next session start.

## Files

| File | Load when |
|---|---|
| `references/markers.md` | Every mode. The operational five-layer checklist. |
| `references/voice-profile.md` | Before rewrite or full. Sample handling and failure modes. |
| `references/always-on.md` | Source of truth for the CLAUDE.md block. Edit here, not there. |
| `references/ai-vs-human-writing.md` | For the why, the numbers, or a citation. ~40 sources. |
| `scripts/stylo.py` | `audit` / `profile` / `diff`. Stdlib only, `--json` available. |
| `scripts/install.py` | Replicate the always-on block. `--check` / `--quiet` / `--uninstall`. |
