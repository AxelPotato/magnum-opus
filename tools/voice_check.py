#!/usr/bin/env python3
"""Count the softeners in the essay, and guard its sharp lines.

The book got mellow one reader run at a time: each run swapped a sharp line
for a cushion that cost nobody anything. This script makes that drift
visible. It counts five kinds of softener per part, lists every hit, and
checks that the lines in tools/voice_protected.txt marked SHARP are still in
the book. A SHARP line is cut only with Alex's word.

What it counts (a rough instrument, read the hits before acting on them):
  if-then      a step's own conclusion put behind a condition
               ("if you accept that, then"); an "if" at the edge of what
               nobody can prove (the axiom, death) is honest, and those
               lines are GUARD
  dont         a disclaimer built on a negative ("I'm not against",
               "I don't want to knock", "you don't have to", "I don't mean")
  reassure     comfort nobody asked for ("nothing is wrong with you",
               "nobody is doing it wrong", "to be clear")
  apology      the author apologizing for a claim ("I'm afraid", "I wish I
               could", "I admit", "or at least I think")
  hedge        "I think", "I suspect", "as far as I can see/tell"
               (Alex keeps several of these on purpose; they are counted,
               not condemned)

Lines in voice_protected.txt marked GUARD are deliberate limits or safety
lines (for example "That never means letting people hurt you"). Their hits
are not counted.

Usage:
  python tools/voice_check.py                 counts for the working tree
  python tools/voice_check.py --list          and every hit, with line numbers
  python tools/voice_check.py --against main  before and after, per kind
"""
import argparse
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PARTS = [
    ("P0", "essay/part-0-intro.md"),
    ("P1", "essay/part-1-rational.md"),
    ("P2", "essay/part-2-spiritual.md"),
    ("P3", "essay/part-3-practical.md"),
    ("FAQ", "essay/faq.md"),
]
KINDS = {
    "if-then": [
        r"\bif you accept\b",
        r"\bif it's right\b",
        r"\bif something carries over\b",
        r"\bif whatever I do\b",
        r"\bif your life is going well\b",
    ],
    "dont": [
        r"\bI'm not (?:against|saying|claiming|trying to)\b",
        r"\bI don't want to (?:knock|skip|say)\b",
        r"\bI don't mean\b",
        r"\byou don't (?:have|need) to\b",
        r"\bI won't (?:make|tell)\b",
    ],
    "reassure": [
        r"\bnothing is wrong with you\b",
        r"\bnobody (?:is doing|did) (?:it|anything) wrong\b",
        r"\bto be clear\b",
        r"\bdon't worry\b",
        r"\bwhich everyone does\b",
    ],
    "apology": [
        r"\bI'm afraid\b",
        r"\bI wish I could\b",
        r"\bI(?:'ll| will| have to)? admit\b",
        r"\bto be honest\b",
        r"\bor at least I think\b",
        r"\bbefore that sounds\b",
        r"\blet me be careful\b",
    ],
    "hedge": [
        r"\bI think\b(?! of)",
        r"\bI suspect\b",
        r"\bas far as I can (?:see|tell)\b",
    ],
}
PROTECTED = ROOT / "tools" / "voice_protected.txt"


def read_protected():
    sharp, guard = [], []
    if PROTECTED.exists():
        for raw in PROTECTED.read_text(encoding="utf-8").splitlines():
            line = raw.strip()
            if line.startswith("SHARP:"):
                sharp.append(line[6:].strip())
            elif line.startswith("GUARD:"):
                guard.append(line[6:].strip())
    return sharp, guard


def text_of(path, ref=None):
    if ref is None:
        return (ROOT / path).read_text(encoding="utf-8")
    out = subprocess.run(["git", "show", f"{ref}:{path}"], cwd=ROOT,
                         capture_output=True, text=True)
    if out.returncode:
        sys.exit(f"git show {ref}:{path} failed: {out.stderr.strip()}")
    return out.stdout


def body(text):
    """Drop the Sources list at the end of a part."""
    return re.split(r"^## Sources\s*$", text, flags=re.M)[0]


def scan(ref=None):
    _, guard = read_protected()
    hits, words = [], {}
    for part, path in PARTS:
        text = body(text_of(path, ref))
        words[part] = len(re.findall(r"[A-Za-z']+", text))
        for n, line in enumerate(text.splitlines(), 1):
            for kind, pats in KINDS.items():
                for pat in pats:
                    for m in re.finditer(pat, line, flags=re.I):
                        around = line[max(0, m.start() - 60):m.end() + 60]
                        if any(g.lower() in line.lower() and
                               m.group(0).lower() in g.lower() for g in guard):
                            continue
                        hits.append((part, n, kind, around.strip()))
    return hits, words


def table(hits, words):
    rows = {}
    for part, _, kind, _ in hits:
        rows.setdefault(part, {}).setdefault(kind, 0)
        rows[part][kind] += 1
    return rows


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--list", action="store_true", help="print every hit")
    ap.add_argument("--against", metavar="REF", help="compare with a git ref")
    args = ap.parse_args()

    hits, words = scan()
    now = table(hits, words)
    before = table(*scan(args.against)) if args.against else None

    kinds = list(KINDS)
    print("part  " + "  ".join(f"{k:>8}" for k in kinds) + "     all  per 1k words")
    tot_now = tot_before = 0
    for part, _ in PARTS:
        cells = []
        for k in kinds:
            a = now.get(part, {}).get(k, 0)
            if before is not None:
                b = before.get(part, {}).get(k, 0)
                cells.append(f"{b:>3}>{a:<4}")
            else:
                cells.append(f"{a:>8}")
        n = sum(now.get(part, {}).values())
        tot_now += n
        line = f"{part:<5} " + "  ".join(cells)
        if before is not None:
            b = sum(before.get(part, {}).values())
            tot_before += b
            line += f"  {b:>3}>{n:<4}"
        else:
            line += f"  {n:>6}"
        line += f"  {1000 * n / max(words[part], 1):6.2f}"
        print(line)
    if before is not None:
        print(f"all softeners: {tot_before} in {args.against}, {tot_now} now")
    else:
        print(f"all softeners: {tot_now}")

    if args.list:
        print()
        for part, n, kind, around in hits:
            print(f"{part}:{n:<4} {kind:<9} ...{around}...")

    sharp, _ = read_protected()
    book = "\n".join(text_of(p) for _, p in PARTS)
    missing = [s for s in sharp if s not in book]
    if missing:
        print("\nSHARP lines no longer in the book (cut only with Alex's word):")
        for s in missing:
            print(f"  - {s}")
        sys.exit(1)
    elif sharp:
        print(f"\nAll {len(sharp)} SHARP lines are still in the book.")


if __name__ == "__main__":
    main()
