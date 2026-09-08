#!/usr/bin/env python3
"""Replicate the HumanizerWRT always-on block into CLAUDE.md. Stdlib only.

The block in references/always-on.md is the single source of truth. This script
splices it into CLAUDE.md between marker comments, idempotently: run it a hundred
times and the file changes at most once.

  install.py                    install/update ~/.claude/CLAUDE.md
  install.py --check            report status; exit 0 current, 1 stale/absent
  install.py --quiet            silent unless something actually changed (hook mode)
  install.py --uninstall        remove the block, leave the rest of the file alone
  install.py --target PATH      operate on a specific CLAUDE.md (repeatable)

Scope, deliberately narrow: it only ever touches CLAUDE.md files named on the command
line (default: the user's own global one), only ever the text between its own markers,
and only on this machine. It does not scan for other CLAUDE.md files, does not touch
project files unless asked, and never writes anywhere else. --uninstall reverses it
completely. Every write is atomic and backed up first.
"""
import argparse
import hashlib
import json
import os
import shutil
import sys
import time
from pathlib import Path

BEGIN = "<!-- humanizer-wrt:begin -->"
END = "<!-- humanizer-wrt:end -->"

HERE = Path(__file__).resolve().parent
SOURCE = HERE.parent / "references" / "always-on.md"
BACKUPS = Path.home() / ".claude" / "backups"


def canonical_block():
    body = SOURCE.read_text(encoding="utf-8").strip("\n")
    return f"{BEGIN}\n{body}\n{END}"


def digest(s):
    return hashlib.sha256(s.encode("utf-8")).hexdigest()[:12]


def locate(text):
    """Return (start, end) span of the existing block, or None."""
    i = text.find(BEGIN)
    if i == -1:
        return None
    j = text.find(END, i)
    if j == -1:
        return None
    return i, j + len(END)


def splice(text, block):
    """Insert or replace the block. Returns new text, or None if already identical."""
    span = locate(text)
    if span:
        start, end = span
        if text[start:end] == block:
            return None
        return text[:start] + block + text[end:]
    if not text.strip():
        return block + "\n"
    return text.rstrip("\n") + "\n\n" + block + "\n"


def strip_block(text):
    span = locate(text)
    if not span:
        return None
    start, end = span
    # Also swallow the blank line that install left in front of the block.
    while start > 0 and text[start - 1] == "\n" and text[max(0, start - 2)] == "\n":
        start -= 1
    out = text[:start].rstrip("\n") + "\n" + text[end:].lstrip("\n")
    return out if out.strip() else ""


def backup(path):
    """Copy the file aside before the first modification of the day."""
    if not path.exists():
        return None
    BACKUPS.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    dest = BACKUPS / f"{path.name}.humanizer-wrt.{stamp}.bak"
    shutil.copy2(path, dest)
    return dest


def write_atomic(path, text):
    """Temp file in the same directory, then rename. Never a half-written CLAUDE.md."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + f".humanizer-tmp-{os.getpid()}")
    try:
        tmp.write_text(text, encoding="utf-8")
        os.replace(tmp, path)
    finally:
        if tmp.exists():
            tmp.unlink()


def status(path, block):
    if not path.exists():
        return "absent"
    text = path.read_text(encoding="utf-8", errors="replace")
    span = locate(text)
    if not span:
        return "absent"
    return "current" if text[span[0]:span[1]] == block else "stale"


def main(argv=None):
    ap = argparse.ArgumentParser(add_help=True, description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--check", action="store_true", help="report only, never write")
    ap.add_argument("--quiet", action="store_true", help="print only on change")
    ap.add_argument("--uninstall", action="store_true", help="remove the block")
    ap.add_argument("--target", action="append", metavar="PATH",
                    help="CLAUDE.md to operate on (repeatable)")
    ap.add_argument("--json", action="store_true", help="machine-readable result")
    args = ap.parse_args(argv)

    if not SOURCE.exists():
        # Fail open. A broken install must never break the user's session.
        if not args.quiet:
            print(f"humanizer-wrt: source missing at {SOURCE}", file=sys.stderr)
        return 0

    block = canonical_block()
    targets = [Path(t).expanduser() for t in (args.target or [])]
    if not targets:
        targets = [Path.home() / ".claude" / "CLAUDE.md"]

    results = []
    for path in targets:
        before = status(path, block)
        action = "none"

        if args.check:
            pass
        elif args.uninstall:
            if path.exists():
                text = path.read_text(encoding="utf-8", errors="replace")
                out = strip_block(text)
                if out is not None:
                    backup(path)
                    write_atomic(path, out)
                    action = "removed"
        elif before != "current":
            text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
            out = splice(text, block)
            if out is not None:
                backup(path)
                write_atomic(path, out)
                action = "installed" if before == "absent" else "updated"

        results.append({"target": str(path), "before": before, "action": action,
                        "after": status(path, block), "digest": digest(block)})

    if args.json:
        print(json.dumps({"results": results}, indent=2))
    elif args.quiet:
        # Hook mode: say nothing unless the file actually moved.
        changed = [r for r in results if r["action"] != "none"]
        if changed:
            what = ", ".join(f"{r['action']} in {r['target']}" for r in changed)
            print(json.dumps({"systemMessage": f"HumanizerWRT always-on block {what}."}))
    else:
        for r in results:
            verb = {"none": "unchanged", "installed": "installed",
                    "updated": "updated", "removed": "removed"}[r["action"]]
            print(f"  {r['target']}\n    {r['before']} → {verb} (now: {r['after']}, "
                  f"block {r['digest']})")

    if args.check:
        return 0 if all(r["before"] == "current" for r in results) else 1
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as exc:  # fail open: a hook must never break a session
        print(f"humanizer-wrt install: {exc}", file=sys.stderr)
        sys.exit(0)
