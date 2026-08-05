#!/usr/bin/env python3
"""Check every catalogue file for the structural mistakes that render silently.

GitHub is forgiving about malformed markdown: a heading glued to the end of a
table row is shown as table text, a row with the wrong number of cells is shown
with a column missing, and a link to a file that no longer exists is shown as an
ordinary link. All three look fine on the page and are wrong in the data.

These are structure checks only. Whether a game genuinely debuted on a platform
is a research question no script can answer; see CONSISTENCY.md for the rule
checks that go with these.

Usage:  ./tools/validate.py          # report and exit non-zero on any failure
        ./tools/validate.py --quiet  # only print failures
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOGS = ROOT / "catalogs"

DEBUT_HEADER = (
    "| Title | Year | Developer | Publisher | Genre | Players | Online "
    "| Status | Also On | Language | Notes |"
)
EXPECTED_CELLS = 11
VALID_STATUS = {"Stranded", "Ported", "Sim-ship"}

SEPARATOR_RE = re.compile(r"^\|[\s:|-]+\|$")
# A pipe that is not backslash-escaped. "Xbox Series X\|S" is a literal pipe in
# a cell, not a column break.
CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")
H1_RE = re.compile(r"^#\s+(\S.*?)\s*$")
DEBUT_COUNT_RE = re.compile(r"\|\s*\*\*Debut games\*\*\s*\|\s*\*{0,2}(\d+)")
# Markdown links to a path, ignoring anchors-only and absolute URLs.
LINK_RE = re.compile(r"\[[^\]]*\]\((?!https?://|#)([^)#]+)(#[^)]*)?\)")


def anchor(heading: str) -> str:
    """GitHub's heading-to-anchor slug: lowercase, drop anything that is not a
    word character, space or hyphen, then spaces to hyphens. An em dash is
    dropped but its surrounding spaces are not, which is why real anchors in
    this repo contain a double hyphen."""
    text = heading.strip().lstrip("#").strip()
    text = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"\s", "-", text)


def check_file(path: Path) -> list[str]:
    problems: list[str] = []
    lines = path.read_text(encoding="utf-8").splitlines()
    rel = path.relative_to(ROOT)

    # --- the catalogue heading -------------------------------------------
    if sum(1 for ln in lines if H1_RE.match(ln)) != 1:
        problems.append(f"{rel}: expected exactly one catalogue H1")

    # --- headings glued to the end of a table row -------------------------
    # This is the failure that motivated the check: GitHub renders "| ... | ##
    # Contested" as a cell containing "## Contested", so the heading vanishes
    # from the outline and the section becomes unlinkable.
    for i, line in enumerate(lines, 1):
        if line.startswith("|") and re.search(r"\|\s*#{1,6}\s+\S", line):
            problems.append(f"{rel}:{i}: heading glued to a table row")
        if line.startswith("|") and re.search(r"\|\s{2,}[A-Z][a-z]+ [a-z]+", line):
            stripped = line.rstrip()
            if not stripped.endswith("|"):
                problems.append(f"{rel}:{i}: paragraph glued to a table row")
        # Two header rows on one line. This renders as one row with spare cells
        # rather than as two, so the second field is present in the file and
        # missing from the page, and any tooling that reads the header by line
        # cannot see it at all. Found once in game-boy.md, where it hid the
        # backward-compatibility note for months.
        if re.match(r"\|\s*\*\*[^*]+\*\*\s*\|.*\|\s*\|\s*\*\*[^*]+\*\*\s*\|", line):
            problems.append(f"{rel}:{i}: two header rows glued onto one line")

    # --- the debut table --------------------------------------------------
    starts = [i for i, ln in enumerate(lines) if ln.startswith(DEBUT_HEADER)]
    if len(starts) != 1:
        problems.append(f"{rel}: expected exactly one debut table, found {len(starts)}")
        return problems
    start = starts[0]

    if not SEPARATOR_RE.match(lines[start + 1].strip()):
        problems.append(f"{rel}:{start + 2}: debut header is not followed by a separator")
        return problems

    rows = 0
    for lineno, line in enumerate(lines[start + 2:], start=start + 3):
        line = line.rstrip()
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in CELL_SPLIT_RE.split(line)[1:-1]]
        if len(cells) != EXPECTED_CELLS:
            problems.append(
                f"{rel}:{lineno}: {len(cells)} cells, expected {EXPECTED_CELLS}")
            continue
        rows += 1
        status = re.sub(r"[*`]", "", cells[7]).strip()
        if status not in VALID_STATUS:
            problems.append(f"{rel}:{lineno}: unknown status {status!r}")
        if not cells[0].strip():
            problems.append(f"{rel}:{lineno}: empty title")

        # Status and Also On have to agree. Nothing enforced this before, and
        # the documentation had drifted to describe a placeholder character the
        # data has never actually used.
        if status == "Stranded" and cells[8]:
            problems.append(f"{rel}:{lineno}: Stranded but Also On is "
                            f"{cells[8][:30]!r}, expected empty")
        if status in ("Ported", "Sim-ship") and not cells[8]:
            problems.append(f"{rel}:{lineno}: {status} but Also On is empty")

    if rows == 0:
        problems.append(f"{rel}: debut table has no rows")

    # --- the file's own declared count ------------------------------------
    declared = [int(m.group(1)) for ln in lines for m in [DEBUT_COUNT_RE.search(ln)] if m]
    if not declared:
        problems.append(f"{rel}: Summary table has no 'Debut games' count")
    elif declared[0] != rows:
        problems.append(
            f"{rel}: Summary says {declared[0]} debut games, table has {rows}")

    return problems


def check_rules(path: Path) -> list[str]:
    """Two rules the ruleset states and nothing was checking.

    R5: `Sim-ship` means the same day, not the same year. A row that says
    "same window" is admitting it does not meet the rule, and three of them
    have sat that way since the first pass.

    And a file must not argue with itself: if the Contested table records a
    verdict of Exclude, the game cannot also be sitting in the debut table.
    """
    problems: list[str] = []
    rel = path.relative_to(ROOT)
    text = path.read_text(encoding="utf-8")
    lines = text.splitlines()

    starts = [i for i, l in enumerate(lines) if l.startswith(DEBUT_HEADER)]
    if not starts:
        return problems

    debut: set[str] = set()
    for lineno, line in enumerate(lines[starts[0] + 2:], start=starts[0] + 3):
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in CELL_SPLIT_RE.split(line)[1:-1]]
        if len(cells) != EXPECTED_CELLS:
            continue
        title = re.sub(r"[*`]", "", cells[0]).strip()
        debut.add(title.lower())
        status = re.sub(r"[*`]", "", cells[7]).strip()
        if status == "Sim-ship" and "same day" not in cells[8].lower():
            problems.append(f"{rel}:{lineno}: {title!r} is Sim-ship but Also On says "
                            f"{cells[8][:40]!r}; the rule is same day, not same year")

    section = re.search(r"^## Contested\n(.*?)(?=^## |\Z)", text, re.S | re.M)
    if section:
        for line in section.group(1).splitlines():
            if not line.startswith("|") or SEPARATOR_RE.match(line.strip()):
                continue
            cells = [c.strip() for c in CELL_SPLIT_RE.split(line)[1:-1]]
            if len(cells) >= 3 and "exclude" in re.sub(r"[*`]", "", cells[2]).lower():
                title = re.sub(r"[*`]", "", cells[0]).strip()
                if title.lower() in debut:
                    problems.append(f"{rel}: Contested says exclude {title!r}, but it is "
                                    f"in the debut table")
    return problems


def check_glued(path: Path) -> list[str]:
    """A table row must end at its final pipe.

    Anything after it is prose or a heading that the writer meant to put on the
    next line. GitHub folds it into the last cell, so the section heading
    disappears from the outline and the paragraph is displayed as table data.
    Checked in every markdown file, not only the catalogues: the ruleset carries
    the same tables and drifted the same way.
    """
    problems = []
    rel = path.relative_to(ROOT)
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.rstrip()
        if not line.startswith("|") or line.endswith("|"):
            continue
        tail = line.rsplit("|", 1)[1].strip()
        if not tail:
            continue
        kind = "heading" if tail.startswith("#") else "text"
        problems.append(f"{rel}:{i}: {kind} runs past the end of a table row: {tail[:40]!r}")
    return problems


def check_links(paths: list[Path]) -> list[str]:
    """Relative links must resolve, and any anchor must match a real heading."""
    problems: list[str] = []
    anchors: dict[Path, set[str]] = {}

    for path in ROOT.rglob("*.md"):
        if ".git" in path.parts:
            continue
        anchors[path.resolve()] = {
            anchor(ln) for ln in path.read_text(encoding="utf-8").splitlines()
            if ln.startswith("#")
        }

    for path in paths:
        rel = path.relative_to(ROOT)
        for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            for match in LINK_RE.finditer(line):
                target = (path.parent / match.group(1)).resolve()
                if not target.exists():
                    problems.append(f"{rel}:{i}: broken link to {match.group(1)}")
                    continue
                frag = match.group(2)
                if frag and target in anchors and frag[1:] not in anchors[target]:
                    problems.append(f"{rel}:{i}: link anchor {frag} not found in "
                                    f"{match.group(1)}")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--quiet", action="store_true", help="only print failures")
    args = ap.parse_args()

    catalogs = sorted(CATALOGS.glob("*.md"))
    if not catalogs:
        print(f"error: no catalogues found under {CATALOGS}", file=sys.stderr)
        return 2

    docs = sorted(p for p in ROOT.glob("*.md"))
    problems: list[str] = []
    for path in catalogs:
        problems += check_file(path)
        problems += check_rules(path)
    for path in catalogs + docs:
        problems += check_glued(path)
    problems += check_links(catalogs + docs)

    if problems:
        print(f"{len(problems)} problem(s) across {len(catalogs)} catalogues:",
              file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1

    if not args.quiet:
        print(f"{len(catalogs)} catalogues, {len(docs)} docs: no structural problems")
    return 0


if __name__ == "__main__":
    sys.exit(main())
