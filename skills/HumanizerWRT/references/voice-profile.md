# Building and applying a voice profile

Read this before **rewrite** or **full** mode. The research reason it exists: generic
"make this sound human" is a provably ill-posed objective. Human writing is not a
distribution to move toward. It is a pile of idiolects. Every generic evasion method
tested (paraphrase, detector-guided DPO, adversarial prompting) failed against
style-embedding detectors. The one approach that worked conditioned on **a specific named
author's samples**.

So: the profile is not a nicety. It is the thing that makes the rewrite work at all.

---

## 1. Get samples

**Ask for 3 to 5 pieces the author wrote themselves, in the same register as the target.**
Register matters more than volume: their Slack messages will not profile their conference
paper.

Good sources, roughly in order of usefulness:
- Prior pieces of the same genre (the ideal)
- Long emails or Slack/Discord messages they wrote without editing
- Personal blog posts, newsletter issues, README prose, PR descriptions
- Voice-note transcripts: excellent for stance and rhythm, poor for punctuation

**Explicitly exclude anything AI-assisted.** A profile built on AI-edited samples encodes
the very register you are trying to remove. Ask directly; people often forget that the
draft they "just tidied up with ChatGPT" is contaminated.

### When there are no samples

Say so, and degrade honestly rather than silently:

> No samples means no voice target, so this will be a generic downshift, cutting the AI
> register rather than moving toward yours. That fixes layers 1 to 4 and leaves layer 5
> mostly untouched. Three or four things you've written would change the result
> substantially. Want to proceed without, or dig some up?

A generic downshift is still worth doing. It is just a weaker claim, and should be
described as one.

---

## 2. Measure what's measurable

```bash
python3 scripts/stylo.py profile sample1.md sample2.md sample3.md --json > voice.json
```

With three or more samples this prints a **median baseline plus the observed range** per
marker. The range matters as much as the median: it tells you how much this author varies,
which is itself part of the voice. An author whose `sent_len_cv` ranges 0.6 to 0.9 writes
differently from one pinned at 0.7 every time.

With one sample, the tool says so. Treat the numbers as indicative and lean on §3.

**The panel is proxies, not the papers' exact operationalisations.** It is built for
*relative* comparison (this author vs this candidate), not absolute verdicts. Do not
report a raw marker value as evidence of anything on its own.

---

## 3. Read what isn't measurable

The script cannot see the things that matter most. Read the samples yourself and write
down, in the author's own examples:

**Lexicon**
- Words they reach for repeatedly (everyone has 5 to 10). Note them; reuse them.
- Words they never use. Register ceiling: what's the fanciest word here?
- Do they swear, joke, use jargon, use brand names?

**Sentences**
- Shortest sentence in the samples. This is the permission level for fragments.
- Do they start sentences with And/But/So? Use one-line paragraphs? Rhetorical questions?
- Where do they put the main clause, front-loaded or held to the end?

**Stance** (the §5 layer, and the hardest to fake)
- Do they hedge or assert? What does their uncertainty *sound* like?
- First person: "I", "we", or absent?
- Do they argue causally ("because…") or assert conclusions?
- Are they inside the events or looking back at them?
- What do they do when something is bad, soften it or say it?

**Structure**
- How do they open? Almost nobody opens the way an LLM does.
- How do they end? Many good writers just stop. LLMs never do.
- Do they use headers, lists, bold? At what density?

**Tics**: every writer has them. Find at least two. A profile without tics is incomplete,
because tics are precisely what a smoothed rewrite destroys.

---

## 4. Apply

Rewrite with the profile in context. Order matters. Work the restore list first (see
`markers.md`, the priority table).

Then verify:

```bash
python3 scripts/stylo.py diff voice.json candidate.md
```

Output is sorted by largest divergence. Read it as a worklist, not a score. Two rules for
reading it:

- **Chase the restore markers first**: `contraction_per_k`, `function_word_pct`,
  `first_person_per_k`, `causal_connective_per_k`. These resist prompting hardest and
  matter most.
- **Do not optimise to zero divergence.** Matching an author's median exactly on every
  marker is itself unnatural, because their own samples don't do that (check the ranges). Land
  inside the author's observed range, not on their median.

---

## 5. Failure modes to watch for

**Voice-preserving prompts can backfire into performing voice.** Documented: Claude under
an explicit voice-preserving instruction produced *more* literary stylization than under a
generic one, treating "preserve voice" as licence to render voice more emotionally
legible. If the output feels like a heightened version of the author (more lyrical, more
introspective, more *writerly*), that is this failure, and it is worse than a flat
rewrite. Cut back toward the samples.

**Voice-preserving prompts only reduce normalization by ~32%**, and direction is unchanged
on 85% of markers. Prompting alone will not get you there; that is why the diff step
exists.

**Register calibration runs both ways.** Contraction density *decreases* in oral-history
transcripts and slightly *increases* in already-formal recollections. The model normalises
toward a common register from whichever side you start on. If the author writes more
formally than the model's default, the fix is not "add contractions". Check the diff.

**Editing beats generating, and you should prefer it.** Human-written-then-lightly-edited
text sits far closer to its human source (0.80 AUROC) than generated text does (0.97), and
moves entropy in the *opposite* direction. Where the author has a real draft, edit it.
Reserve full rewrites for when there is nothing else to work with, and say which one
you did.
