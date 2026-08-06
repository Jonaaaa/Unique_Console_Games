#!/usr/bin/env python3
"""Prove the validator fires, by reintroducing each fault it claims to catch.

A check that reports nothing is indistinguishable from a check that cannot fire.
Three drafts of R18 passed a clean tree while catching nothing: one was
case-sensitive against a capitalised note, one had shredded its platform list on
spaces so `Game Boy` became `Game` and `Boy`, and one compared a whole capture
where it meant the first word. All three looked exactly like success.

Each case edits a real catalogue, runs the validator, and restores the file
whether or not the check passed. Nothing is left modified.

Usage:  ./tools/selftest.py
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# (file, text to find, what to replace it with, expected wording, label).
# An expectation prefixed "report:" is a check that names the fault in its
# output without failing the run, so it is looked for in a non-quiet run.
CASES = [
    ("catalogs/ps2.md", "| Ico | 2001", "| Ico | 20x1",
     "year", "a year that is not four digits"),
    ("catalogs/wii.md", "| Excite Truck | 2006", "| Excite Truck | 2006-2007",
     "year", "a year range with a hyphen instead of an en dash"),
    ("catalogs/ps2.md", "| No | Ported |", "| No | Portd |",
     "status", "a status outside the vocabulary"),
    ("catalogs/ps2.md", "|  | Sold | ", "|  | Availabl | ",
     "availability", "an availability outside the vocabulary"),
    ("catalogs/wii.md", "| **Debut games** |", "| **Debut games** | **999** |\n| x |",
     "debut", "a summary count that disagrees with the table"),
    ("catalogs/snes.md", "## Contested", "| glued | ## Contested",
     "glued", "a heading glued to the end of a table row"),
    ("README.md", "[Microsoft Xbox Series X\\|S]", "[Microsoft Xbox Series X|S]",
     "cells", "an unescaped pipe splitting a row"),
    ("catalogs/atari-lynx.md", "| Malibu Bikini Volleyball |",
     "| Scrapyard Dog | 1991 | Atari | Atari | Platformer | 1 | No | **Stranded** "
     "|  |  | Sold | Also on 7800. |\n| Malibu Bikini Volleyball |",
     "Stranded but its note", "a Stranded row whose note says the game moved"),
    ("catalogs/gamecube.md", "| Super Monkey Ball | 2001 | **Include** (`Ported`)",
     "| zzz | 2001 | **Include** (`Ported`)",
     "flagged Contested", "a Contested flag with no argument written"),
    ("catalogs/gba.md", "| The series' first Western release, which is why",
     "| The series' first Western release. The series' first Western release, which is why",
     "report:same thing twice", "a note that says the same thing twice"),
]


def main() -> int:
    failures = 0
    for rel, old, new, expect, label in CASES:
        path = ROOT / rel
        original = path.read_text(encoding="utf-8")
        if original.count(old) < 1:
            print(f"  SKIP  {label}: anchor gone from {rel}, update this case")
            failures += 1
            continue
        path.write_text(original.replace(old, new, 1), encoding="utf-8")
        try:
            reporting = expect.startswith("report:")
            cmd = ["./tools/validate.py"] + ([] if reporting else ["--quiet"])
            run = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
            output = (run.stdout + run.stderr).lower()
            if reporting:
                ok = expect[len("report:"):].lower() in output
                why = "the fault is not named in the report"
            else:
                ok = run.returncode != 0 and expect.lower() in output
                why = ("the validator passed with the fault present"
                       if run.returncode == 0 else "it failed for a different reason")
        finally:
            path.write_text(original, encoding="utf-8")
        print(f"  {'ok  ' if ok else 'FAIL'}  {label}")
        if not ok:
            print(f"          {why}")
            failures += 1

    print(f"\n{len(CASES) - failures}/{len(CASES)} checks proven to fire")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
