#!/usr/bin/env python3
"""Stylometric marker panel for HumanizerWRT. Stdlib only.

Measures the markers that the literature found robust (see
references/ai-vs-human-writing.md). All measures are proxies computed by regex,
not the exact operationalisations in the source papers. They are for
*relative* comparison (author baseline vs candidate), not absolute verdicts.

  profile FILE...        marker panel per file + pooled author baseline
  audit FILE             marker panel + register-independent flags (--band to score
                         each marker against a human reference distribution)
  diff BASELINE CAND     candidate against a baseline (file or .json from profile)
  independence FILE...   shared phrasing ACROSS documents: the cross-document tell

Add --json for machine-readable output.

One document per file. Several documents concatenated into one file will produce a
misleading `volatility_decay`, because the first/second-half split then measures the
order you stitched them in rather than any single document's arc. Pass them as
separate files to `profile` instead. That is what it is for.
"""
import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path

# --- lexicons -----------------------------------------------------------------

# Kobak et al. 2024 "common set": 10 words, Delta=0.134 on their own.
MARKERS_COMMON = """across additionally comprehensive crucial enhancing exhibited
insights notably particularly within""".split()

# High-yield extract of Kobak's 291-word rare set + Reinhart et al. 2025 overuse table.
MARKERS_RARE = """accentuate adept akin align aligns alongside amidst boast bolster
burgeoning camaraderie commendable compelling consequently craft crafted crucially
culminating delve delves delving discern elevate elucidate embark embracing
emphasize employing empowers enabling encompass endeavor enhance enhances ensuring
evolving exceptional exploration facilitate facilitates fleeting foster fostering
foundational garnered groundbreaking grapple harness heightened hinder holistic
illuminating ignite imperative inherent innovative integral interconnectedness
interplay intricacies intricate invaluable leverage leveraging meticulous
meticulously multifaceted navigating nuanced necessitates notable noteworthy
offering palpable paving pinpoint pioneering pivotal poised predominantly pressing
profound realm refine remarkable renowned resonate revolutionize robust scrutinize
seamless seamlessly shedding showcase showcases showcasing signifying solace
spanning streamline substantiated surpass swift tailored tapestry testament
thorough transformative uncharted underscore underscores underscoring unlocking
unparalleled unravel unspoken unveil uphold vibrant versatility""".split()

# Wu et al. 2026 verbal-tic taxonomy: opener / hedge / filler phrases.
TIC_PHRASES = [
    r"that'?s a (?:great|excellent|fantastic) question", r"\bgreat question\b",
    r"\bexcellent (?:question|observation|point)\b", r"^\s*(?:absolutely|certainly)[!.]",
    r"i (?:completely|totally) understand", r"it'?s (?:important|worth) (?:to note|noting)",
    r"\bi have to be honest\b", r"let me walk you through",
    r"\bdive (?:deep )?into\b", r"\bat the end of the day\b",
    r"\bit'?s worth remembering\b", r"\bin today'?s (?:world|landscape)\b",
]

FILLER_TRANSITIONS = ["furthermore", "moreover", "additionally", "consequently",
                      "notably", "importantly", "ultimately", "overall"]

FUNCTION_WORDS = set("""a about above after again against all am an and any are as at be
because been before being below between both but by can cannot could did do does doing
down during each few for from further had has have having he her here hers herself him
himself his how i if in into is it its itself just me more most my myself no nor not of
off on once only or other others ought our ours ourselves out over own same she should so
some such than that the their theirs them themselves then there these they this those
through to too under until up very was we were what when where which while who whom why
will with would you your yours yourself yourselves""".split())

FIRST_PERSON = set("i me my mine myself we us our ours ourselves".split())

# Possessive 's is not a contraction, and the two are not separable by shape
# (it's vs John's). Count the unambiguous suffixes, plus a whitelist for the
# pronoun+'s forms that are always contractions.
CONTRACTION = re.compile(
    r"\b\w+['’](?:t|re|ve|ll|d|m)\b"
    r"|\b(?:it|that|there|here|what|who|he|she|let|this|how|where|one)['’]s\b", re.I)
NOMINALISATION = re.compile(r"\b\w{4,}(?:tion|sion|ment|ness|ity|ance|ence|ism)s?\b", re.I)
PARTICIPIAL = re.compile(r",\s+\w+ing\b")
TRICOLON = re.compile(r"\b[\w'-]+,\s+[\w'-]+,?\s+(?:and|or)\s+[\w'-]+\b")
NOT_X_BUT_Y = re.compile(
    # "not just X but Y" / "not merely X, but rather Y"
    r"\bnot (?:just|only|merely|simply)\b[^.;!?]{0,90}?\bbut\b"
    # "not just X — it is Y" / "not X, it's Y": the dash and comma variants
    r"|\bnot (?:just|only|merely|simply)\b[^.;!?]{0,90}?(?:—|\s--?\s|,)\s*it(?:'|’)?s?\b"
    r"|\bit(?:'|’)?s not\b[^.;!?]{0,60},\s*it(?:'|’)?s\b", re.I)
# Dashes used as a rhetorical break. Two traps, both hit during testing:
# `\s` swallows the newline in a markdown bullet, so every list item counted as a
# dash; and an *indented* bullet still matches even with horizontal-only whitespace,
# which no fixed-width lookbehind can express in Python's re. So strip leading list
# markers first, then match. En dash counts too, because it is the same move.
LIST_MARKER = re.compile(r"^[ \t]*[-*+][ \t]", re.M)
EM_DASH = re.compile(r"[—–]|[^\S\n]--?[^\S\n]")
CURLY = re.compile(r"[‘’“”]")
WORD = re.compile(r"[A-Za-z][A-Za-z'’-]*")
SENT_SPLIT = re.compile(r"(?<=[.!?])[\"'”’)\]]*\s+")


def dash_count(text):
    """Rhetorical dashes, with markdown list markers neutralised first."""
    return len(EM_DASH.findall(LIST_MARKER.sub("  ", text)))


# --- measures -----------------------------------------------------------------

def mattr(tokens, window=200):
    """Moving-average type-token ratio: length-robust lexical diversity."""
    if len(tokens) <= window:
        return len(set(tokens)) / len(tokens) if tokens else 0.0
    ratios = [len(set(tokens[i:i + window])) / window
              for i in range(len(tokens) - window + 1)]
    return statistics.fmean(ratios)


def _mtld_pass(tokens, threshold=0.72):
    factors, types, count = 0.0, set(), 0
    for tok in tokens:
        types.add(tok)
        count += 1
        if len(types) / count <= threshold:
            factors += 1
            types, count = set(), 0
    if count:
        ttr = len(types) / count
        factors += (1 - ttr) / (1 - threshold) if ttr < 1 else 0
    return len(tokens) / factors if factors else float(len(tokens))


def mtld(tokens):
    """Measure of Textual Lexical Diversity (McCarthy & Jarvis 2010), bidirectional.

    Returns None below ~100 tokens: with too few tokens the TTR never crosses the
    threshold, no factor completes, and the result is just the token count wearing
    a hat. MATTR degrades more gracefully on short text; prefer it there.
    """
    if len(tokens) < 100:
        return None
    val = (_mtld_pass(tokens) + _mtld_pass(tokens[::-1])) / 2
    return None if val >= len(tokens) else val


def cv(values):
    """Coefficient of variation: the burstiness proxy."""
    if len(values) < 2:
        return 0.0
    m = statistics.fmean(values)
    return statistics.stdev(values) / m if m else 0.0


FENCED = re.compile(r"```.*?```", re.S)
INLINE_CODE = re.compile(r"`[^`\n]*`")


def panel(text):
    """Compute the full marker panel for one text.

    Code is stripped first: fenced blocks and inline spans. The rules being measured
    are about prose, and exempt code identifiers, log strings and config values, so
    counting a dash or a marker word inside backticks is a false positive.
    """
    text = INLINE_CODE.sub(" ", FENCED.sub(" ", text))
    words = WORD.findall(text)
    if not words:
        return {"tokens": 0, "sentences": 0, "_marker_hits": {}}
    lower = [w.lower() for w in words]
    n = len(words)
    per_k = lambda c: round(1000 * c / n, 2)

    sents = [s for s in SENT_SPLIT.split(text.strip()) if WORD.search(s)]
    slen = [len(WORD.findall(s)) for s in sents] or [0]
    half = max(1, len(slen) // 2)

    hits_common = [w for w in lower if w in set(MARKERS_COMMON)]
    hits_rare = [w for w in lower if w in set(MARKERS_RARE)]
    tics = sum(len(re.findall(p, text, re.I | re.M)) for p in TIC_PHRASES)

    return {
        "tokens": n,
        "sentences": len(sents),
        # Layer 3: rhythm. AI: high diversity, low variance, variance flattens late.
        "mattr": round(mattr(lower), 4),
        "mtld": round(mtld(lower), 1) if mtld(lower) else None,
        "sent_len_mean": round(statistics.fmean(slen), 1),
        "sent_len_cv": round(cv(slen), 3),
        "sent_len_cv_2nd_half": round(cv(slen[half:]), 3),
        # Needs enough sentences for each half's CV to mean anything. Below ~12 the
        # ratio is noise, and on text concatenated from several documents it measures
        # the stitching order rather than any one document's arc; it produced a
        # false flag exactly that way during testing.
        "volatility_decay": round(cv(slen[half:]) / cv(slen[:half]), 3)
        if len(slen) >= 12 and cv(slen[:half]) else None,
        # Layer 2: syntax. AI: nominal, participial, up-register.
        "nominalisation_per_k": per_k(len(NOMINALISATION.findall(text))),
        "participial_per_k": per_k(len(PARTICIPIAL.findall(text))),
        "mean_word_len": round(statistics.fmean(len(w) for w in words), 2),
        "long_word_pct": round(100 * sum(len(w) >= 8 for w in words) / n, 1),
        # Layer 1 + 5: lexicon and register. AI: strips these.
        "function_word_pct": round(100 * sum(w in FUNCTION_WORDS for w in lower) / n, 1),
        "first_person_per_k": per_k(sum(w in FIRST_PERSON for w in lower)),
        "contraction_per_k": per_k(len(CONTRACTION.findall(text))),
        # Layer 5: reasoning made explicit vs compressed into abstraction.
        "causal_connective_per_k": per_k(sum(
            lower.count(w) for w in ("because", "since", "therefore", "so", "thus"))),
        # Punctuation.
        "comma_per_k": per_k(text.count(",")),
        "em_dash_per_k": per_k(dash_count(text)),
        "semicolon_per_k": per_k(text.count(";")),
        "curly_quotes": len(CURLY.findall(text)),
        # Layer 4: rhetorical formulae.
        "tricolon_per_k": per_k(len(TRICOLON.findall(text))),
        "not_x_but_y": len(NOT_X_BUT_Y.findall(text)),
        "filler_transition_per_k": per_k(sum(lower.count(w) for w in FILLER_TRANSITIONS)),
        # Layer 1: marker vocabulary.
        "marker_common_per_k": per_k(len(hits_common)),
        "marker_rare_per_k": per_k(len(hits_rare)),
        "verbal_tics": tics,
        "_marker_hits": dict(Counter(hits_common + hits_rare).most_common()),
    }


# Register-independent flags. Each is (key, test, message). Thresholds are
# advisory heuristics, NOT empirical cutoffs: no published human reference
# distribution exists for these proxies. Treat as "look here", not "verdict".
FLAGS = [
    ("marker_rare_per_k", lambda v: v > 6,
     "Marker vocabulary is dense. Kobak's excess-style words are ~66% verbs; check "
     "each hit reads as this author's word rather than the register's default."),
    ("marker_common_per_k", lambda v: v > 18,
     "High rate of the 10 common markers (across/additionally/crucial/notably/...). "
     "These carry more of the signal than the exotic words do."),
    ("verbal_tics", lambda v: v > 0,
     "Sycophantic opener / hedge / filler phrase present. Sycophancy correlates with "
     "perceived naturalness at r=-0.87 (Wu et al. 2026): the strongest single tell."),
    ("tricolon_per_k", lambda v: v > 4,
     "Frequent three-item lists. Multiple expert annotators flagged 'groupings of "
     "three with suspicious consistency' independently."),
    ("not_x_but_y", lambda v: v > 0,
     "'Not just X but Y' construction. Named directly by expert annotators."),
    ("sent_len_cv", lambda v: v < 0.45,
     "Low sentence-length variance. Human distributions are more scattered "
     "(Munoz-Ortiz 2024); uniformity is the tell, not length itself."),
    ("volatility_decay", lambda v: v is not None and v < 0.75,
     "Sentence-length variance flattens in the second half. AI shows 24-32% lower "
     "late-sequence volatility; human writing stays variable throughout."),
    ("contraction_per_k", lambda v: v < 1,
     "Near-zero contractions. AI rewriting cuts contraction density ~31% and this "
     "resists voice-preserving prompts; restore them if the register allows."),
    ("filler_transition_per_k", lambda v: v > 8,
     "Dense filler transitions (furthermore/moreover/additionally)."),
    ("em_dash_per_k", lambda v: v > 0,
     "Em/en dash present. Budget is zero: rewrite as a comma, colon, parenthesis or "
     "full stop. Stricter than the evidence requires (the research finding is that "
     "~3 per paragraph is the tell, not the character itself): a deliberate house "
     "rule, set because a zero budget needs no judgement call."),
    ("participial_per_k", lambda v: v > 12,
     "Frequent present participial clauses. GPT-4o uses these at 5.3x the human "
     "rate (d=1.38): the largest single Biber-feature gap measured."),
    ("nominalisation_per_k", lambda v: v > 55,
     "Noun-heavy. Instruction tuning trains one informationally dense register and "
     "applies it to every genre (Reinhart et al. 2025)."),
]


def flags_for(p):
    out = []
    for key, test, msg in FLAGS:
        v = p.get(key)
        if v is not None and test(v):
            out.append((key, v, msg))
    return out


# --- cross-document independence -----------------------------------------------
#
# Every blind test of this skill was lost on the same evidence: not any single
# sentence, but a lattice of phrasing shared between separately generated texts.
# "had not opened the blinds since March" in three of them. "boiling point of
# water" as the disenchantment image in two. A verbatim exchange in two more. One
# judge put it plainly: it ranked on whether the files were independent of each
# other, not on quality, and several machine texts were better written than the
# humans it placed above them.
#
# A single-document panel cannot see this, and will happily report a clean score
# on ten texts sharing one skeleton. This does.

# Measured on 159 human same-prompt pairs from r/WritingPrompts, pre-2018: 1.9%
# of pairs share any span at all. A 160th pair carried 11 and is almost certainly
# a repost, which is why the share-rate is reported rather than the mean.
HUMAN_PAIR_SHARE_PCT = 1.9


def _spans(tokens, lo=5, hi=14):
    """All word n-grams in a token list, longest first."""
    out = {}
    for n in range(hi, lo - 1, -1):
        for i in range(len(tokens) - n + 1):
            out.setdefault(tuple(tokens[i:i + n]), 0)
            out[tuple(tokens[i:i + n])] += 1
    return out


def _contentful(span, need=3):
    """Reject stock English.

    A 4-word span carrying two content words ("for a long time", "at the kitchen
    table") is ordinary phrasing, not convergence. Requiring five words and three
    content words keeps the evidence blind judges actually cited ("the boiling
    point of water", "covered every wall of the apartment") and drops the noise.
    """
    return sum(1 for w in span if w not in FUNCTION_WORDS) >= need


def shared_spans(a, b, lo=5, hi=14):
    """Maximal word sequences occurring in both token lists.

    Maximal means not contained inside a longer shared span, so one 7-word match
    is reported once rather than as four overlapping 4-grams.
    """
    sa, sb = set(_spans(a, lo, hi)), set(_spans(b, lo, hi))
    common = {s for s in (sa & sb) if _contentful(s)}
    maximal = []
    for s in sorted(common, key=len, reverse=True):
        if not any(_is_sub(s, m) for m in maximal):
            maximal.append(s)
    return maximal


def _is_sub(short, long_):
    n, m = len(short), len(long_)
    return n < m and any(long_[i:i + n] == short for i in range(m - n + 1))


def content_words(tokens, minlen=5):
    return {w for w in tokens if len(w) >= minlen and w not in FUNCTION_WORDS}


# --- human reference bands -----------------------------------------------------

BANDS_FILE = Path(__file__).resolve().parent.parent / "references" / "human-bands.json"


def load_bands():
    try:
        return json.loads(BANDS_FILE.read_text(encoding="utf-8"))
    except Exception:
        return None


def band_report(p, doc):
    """Score each marker against the human p10..p90 band.

    Returns (rows, inside, deviation). The headline number is *deviation*: how far
    outside the band a text sits, summed and measured in band-widths. A plain count
    of markers-in-band was tried first and is misleading, because it scores a 9%
    overshoot the same as a 4x one. On the pilot set a control text scored 13 of 14
    in-band while carrying a single em-dash overshoot of ~3 band-widths, and both a
    blind human-ranking and a centroid-distance measure placed it near the bottom.
    Deviation agrees with them; the count does not.

    The target is to land INSIDE the band, not at the median. Real human texts sit
    outside about one band on average, so scoring 'in' everywhere means the text is
    more average than a person, which is its own tell.
    """
    rows, inside, deviation = [], 0, 0.0
    for m, b in doc["bands"].items():
        v = p.get(m)
        if v is None:
            continue
        lo, mid, hi = b["p10"], b["p50"], b["p90"]
        width = (hi - lo) or 1
        if v > hi:
            where, off = "above", (v - hi) / width
        elif v < lo:
            where, off = "below", (lo - v) / width
        else:
            where, off = "in", 0.0
        inside += where == "in"
        deviation += off
        rows.append((m, v, lo, mid, hi, where, off))
    return rows, inside, deviation


# --- output -------------------------------------------------------------------

ORDER = [k for k in panel("a b. c d.") if not k.startswith("_")]


def show(p, title=None):
    if title:
        print(f"\n{title}")
        print("-" * len(title))
    for k in ORDER:
        v = p.get(k)
        print(f"  {k:<26} {'-' if v is None else v}")
    if p.get("_marker_hits"):
        top = ", ".join(f"{w}({c})" if c > 1 else w
                        for w, c in list(p["_marker_hits"].items())[:14])
        print(f"  {'marker words':<26} {top}")


def pooled(panels):
    """Author baseline: median of each marker across samples, plus spread."""
    out = {}
    for k in ORDER:
        vals = [p[k] for p in panels if p.get(k) is not None]
        if vals:
            out[k] = round(statistics.median(vals), 3)
            if len(vals) > 1:
                out[f"{k}__range"] = [round(min(vals), 3), round(max(vals), 3)]
    return out


def read(path):
    return Path(path).read_text(encoding="utf-8", errors="replace")


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    FLAGSET = {"--json", "--band"}
    cmd, args = argv[1], [a for a in argv[2:] if a not in FLAGSET]
    as_json = "--json" in argv[2:]
    as_band = "--band" in argv[2:]

    if cmd == "profile":
        if not args:
            print("profile needs at least one file", file=sys.stderr)
            return 2
        panels = [panel(read(f)) for f in args]
        base = pooled(panels)
        if as_json:
            print(json.dumps({"baseline": base, "samples": dict(zip(args, panels))},
                             indent=2))
            return 0
        for f, p in zip(args, panels):
            show(p, Path(f).name)
        if len(panels) > 1:
            print(f"\nAUTHOR BASELINE (median of {len(panels)} samples)")
            print("-" * 40)
            for k in ORDER:
                if k in base:
                    r = base.get(f"{k}__range")
                    print(f"  {k:<26} {base[k]}" + (f"   [{r[0]} .. {r[1]}]" if r else ""))
        else:
            print("\nOne sample only. Three or more gives a usable baseline; with one, "
                  "treat these as indicative and lean on the audit flags instead.")
        return 0

    if cmd == "audit":
        if len(args) != 1:
            print("audit needs exactly one file", file=sys.stderr)
            return 2
        p = panel(read(args[0]))
        doc = load_bands() if as_band else None
        if as_band and not doc:
            print(f"no band file at {BANDS_FILE}", file=sys.stderr)
            return 2
        if as_json:
            out = {"panel": p, "flags": [
                {"marker": k, "value": v, "note": m} for k, v, m in flags_for(p)]}
            if doc:
                rows, inside, dev = band_report(p, doc)
                out["band"] = {"register": doc["register"], "n": doc["n"],
                               "deviation": round(dev, 3),
                               "inside": inside, "of": len(rows),
                               "markers": [{"marker": m, "value": v, "p10": lo, "p50": md,
                                            "p90": hi, "where": w, "off": round(o, 3)}
                                           for m, v, lo, md, hi, w, o in rows]}
            print(json.dumps(out, indent=2))
            return 0
        show(p, Path(args[0]).name)
        if doc:
            rows, inside, dev = band_report(p, doc)
            print(f"\nHUMAN BAND   deviation {dev:.2f} band-widths   ({inside}/{len(rows)} in band)")
            print(f"  reference: {doc['register']}, n={doc['n']}")
            print("  " + "-" * 66)
            for m, v, lo, md, hi, w, o in sorted(rows, key=lambda r: -r[6]):
                mark = "   " if w == "in" else ("^^ " if w == "above" else "vv ")
                tail = f"  +{o:.2f}w" if o else ""
                print(f"  {mark}{m:<24}{v:>9}   band {lo:g} .. {hi:g}{tail}")
            print("\n  Deviation is the number to watch, not the in-band count: a count "
                  "\n  scores a 9% overshoot the same as a 4x one. Human reference texts "
                  "\n  run about 0.1. Aim inside the band, not at the median, because a "
                  "\n  text inside every band is more average than a person.")
        fl = flags_for(p)
        print(f"\nFLAGS ({len(fl)})")
        print("-" * 40)
        for k, v, m in fl:
            print(f"  [{k} = {v}]\n    {m}")
        if not fl:
            print("  none of the register-independent heuristics tripped.")
        print("\n  Flags are 'look here', not a verdict. There is no published human "
              "\n  reference distribution for these proxies, and formal human writing "
              "\n  legitimately trips several of them (see dossier 8.2).")
        return 0

    if cmd == "diff":
        if len(args) != 2:
            print("diff needs BASELINE and CANDIDATE", file=sys.stderr)
            return 2
        b = args[0]
        base = (json.loads(read(b))["baseline"] if b.endswith(".json") else panel(read(b)))
        cand = panel(read(args[1]))
        rows = []
        for k in ORDER:
            bv, cvv = base.get(k), cand.get(k)
            if bv is None or cvv is None or not isinstance(bv, (int, float)):
                continue
            delta = cvv - bv
            pct = (100 * delta / bv) if bv else None
            rows.append((k, bv, cvv, delta, pct))
        if as_json:
            print(json.dumps([{"marker": k, "baseline": b_, "candidate": c_,
                               "delta": round(d, 3),
                               "pct": None if p is None else round(p, 1)}
                              for k, b_, c_, d, p in rows], indent=2))
            return 0
        print(f"\n{Path(args[1]).name} vs baseline {Path(b).name}")
        print(f"  {'marker':<26} {'baseline':>10} {'candidate':>10} {'delta':>9} {'%':>8}")
        print("  " + "-" * 66)
        for k, b_, c_, d, p in sorted(rows, key=lambda r: -abs(r[4] or 0)):
            print(f"  {k:<26} {b_:>10} {c_:>10} {d:>+9.2f} "
                  f"{'-' if p is None else format(p, '>+7.1f')}")
        print("\n  Largest divergences first. Move the candidate toward the baseline by "
              "\n  restoring what was stripped (contractions, function words, first "
              "\n  person, causal connectives) before touching anything else.")
        return 0

    if cmd == "independence":
        if len(args) < 2:
            print("independence needs two or more files", file=sys.stderr)
            return 2
        docs = []
        for f in args:
            t = INLINE_CODE.sub(" ", FENCED.sub(" ", read(f)))
            docs.append((Path(f).name, [w.lower() for w in WORD.findall(t)]))

        pairs = []
        for i in range(len(docs)):
            for j in range(i + 1, len(docs)):
                sp = shared_spans(docs[i][1], docs[j][1])
                cw = content_words(docs[i][1]) & content_words(docs[j][1])
                pairs.append((docs[i][0], docs[j][0], sp, cw))

        # A phrase shared by every document is the prompt talking, not the model.
        # Convergence lives in spans shared by some but not all.
        n_doc = len(docs)
        phrase_df = Counter()
        for _, _, sp, _ in pairs:
            for s in sp:
                phrase_df[s] += 1
        conv = [(s, sum(1 for _, toks in docs if _is_sub(s, tuple(toks)) or tuple(toks) == s
                        or " ".join(s) in " ".join(toks)))
                for s in phrase_df]
        conv = [(s, d) for s, d in conv if 2 <= d < n_doc or (d == n_doc and n_doc == 2)]
        conv.sort(key=lambda x: (-x[1], -len(x[0])))

        span_counts = [len(sp) for _, _, sp, _ in pairs]
        score = statistics.fmean(span_counts) if span_counts else 0.0
        # Share-rate is the robust statistic. The mean is dominated by outliers:
        # in the human reference one repost pair carried 11 spans and tripled it.
        rate = 100 * sum(1 for c in span_counts if c) / len(span_counts) if span_counts else 0.0

        if as_json:
            print(json.dumps({
                "documents": [d[0] for d in docs],
                "convergence": round(score, 2),
                "share_rate_pct": round(rate, 1),
                "human_reference_pct": HUMAN_PAIR_SHARE_PCT,
                "pairs": [{"a": a, "b": b, "shared_spans": len(sp),
                           "spans": [" ".join(s) for s in sp[:12]],
                           "shared_content_words": sorted(cw)[:40]}
                          for a, b, sp, cw in pairs],
                "convergent_phrases": [{"phrase": " ".join(s), "documents": d}
                                       for s, d in conv[:40]]}, indent=2))
            return 0

        print(f"\nINDEPENDENCE   {len(docs)} documents, {len(pairs)} pairs")
        print(f"  {rate:.1f}% of pairs share a span   "
              f"(human same-prompt reference: {HUMAN_PAIR_SHARE_PCT}%)")
        print(f"  convergence: {score:.2f} spans per pair "
              f"(5 words or longer, 3+ content words)")
        if rate > HUMAN_PAIR_SHARE_PCT * 2:
            print(f"  ^^ {rate / HUMAN_PAIR_SHARE_PCT:.1f}x the human rate")
        print("  " + "-" * 66)
        for a, b, sp, cw in sorted(pairs, key=lambda p: -len(p[2])):
            if not sp:
                continue
            print(f"  {a} <-> {b}   {len(sp)} shared")
            for s in sp[:6]:
                print(f"      \"{' '.join(s)}\"")
        if conv:
            print(f"\n  phrases recurring across documents:")
            for s, d in conv[:12]:
                print(f"    {d} docs   \"{' '.join(s)}\"")
        if not any(sp for _, _, sp, _ in pairs):
            print("  no shared spans found.")
        print("\n  A phrase in every document is the prompt talking. Convergence is what "
              "\n  is shared by some and not all. This is the layer blind judges actually "
              "\n  convicted on, and no single-document panel can see it.")
        return 0

    print(f"unknown command: {cmd}", file=sys.stderr)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
