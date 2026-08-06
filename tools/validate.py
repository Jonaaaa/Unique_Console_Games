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
    "| Status | Also On | Language | Availability | Notes |"
)
EXPECTED_CELLS = 12
EXCLUDED_HEADER = "| Title | Year | Why excluded |"
CONTESTED_HEADER = "| Title | Year | Verdict | Case for including | Case against |"
VALID_STATUS = {"Stranded", "Ported", "Sim-ship"}
# Whether it can still be bought, which is a different question from
# whether it ever left the platform. See RULES.md#availability-whether-it-can-still-be-bought.
VALID_AVAILABILITY = {"Sold", "Backup"}

SEPARATOR_RE = re.compile(r"^\|[\s:|-]+\|$")
# A pipe that is not backslash-escaped. "Xbox Series X\|S" is a literal pipe in
# a cell, not a column break.
CELL_SPLIT_RE = re.compile(r"(?<!\\)\|")
H1_RE = re.compile(r"^#\s+(\S.*?)\s*$")
DEBUT_COUNT_RE = re.compile(r"\|\s*\*\*Debut games\*\*\s*\|\s*\*{0,2}(\d+)")
# Markdown links to a path, ignoring anchors-only and absolute URLs.
LINK_RE = re.compile(r"\[[^\]]*\]\((?!https?://|#)([^)#]+)(#[^)]*)?\)")
# Sentence boundary: a stop followed by something that starts a new sentence.
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z`\u201c(*])")


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
        availability = re.sub(r"[*`]", "", cells[10]).strip()
        if availability not in VALID_AVAILABILITY:
            problems.append(f"{rel}:{lineno}: availability {availability!r} is not one of "
                            f"{', '.join(sorted(VALID_AVAILABILITY))}")
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


def check_notes(path: Path) -> tuple[int, int]:
    """Count rows with no note and rows too short to be one.

    RULES.md requires a sentence per row saying what the release is and why its
    status is what it is.

    An empty cell is now an error: the backlog reached zero on 2026-08-05, so
    the only way to add one is to write a row without a note, which is the thing
    the rule exists to stop. A note under forty characters is still only
    reported, because "short" is a judgement and some rows genuinely say what
    they need to in a few words.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.startswith(DEBUT_HEADER)]
    if not starts:
        return 0, 0
    missing = thin = 0
    for line in lines[starts[0] + 2:]:
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in CELL_SPLIT_RE.split(line)[1:-1]]
        if len(cells) != EXPECTED_CELLS:
            continue
        note = cells[11]
        if not note:
            missing += 1
        elif len(note) < 40:
            thin += 1
    return missing, thin


def check_qualifies(path: Path) -> list[str]:
    """Flag Excluded rows that say the title qualifies but give it no debut row.

    The Excluded table carries disambiguations: rows saying "this does qualify,
    here is why you might think otherwise". Those only make sense if the game is
    actually in the debut table. Where it is not, the file is asserting that a
    game belongs and then not listing it, which silently understates the counts.

    Group rows that say "not separately tabled" are deliberate and exempt; see
    RULES.md on what the Excluded table holds.
    """
    lines = path.read_text(encoding="utf-8").splitlines()
    starts = [i for i, ln in enumerate(lines) if ln.startswith(DEBUT_HEADER)]
    if not starts:
        return []
    titles = []
    for line in lines[starts[0] + 2:]:
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in CELL_SPLIT_RE.split(line)[1:-1]]
        if len(cells) == EXPECTED_CELLS:
            titles.append(cells[0].lower())
    blob = " | ".join(titles)

    excluded = [i for i, ln in enumerate(lines) if ln.startswith(EXCLUDED_HEADER)]
    if not excluded:
        return []
    problems = []
    for lineno, line in enumerate(lines[excluded[0] + 2:], excluded[0] + 3):
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in CELL_SPLIT_RE.split(line)[1:-1]]
        if len(cells) != 3 or not cells[2].startswith("Qualif"):
            continue
        if "not separately tabled" in cells[2]:
            continue
        # The first distinctive word of the title is enough to spot the row.
        key = re.split(r"[,/]", cells[0])[0].strip().lower()
        if key and key not in blob:
            rel = path.relative_to(ROOT)
            problems.append(f"{rel}:{lineno}: {cells[0]!r} is marked as qualifying "
                            f"but has no debut row")
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


def check_contested(path: Path) -> list[str]:
    """A row flagged Contested has its argument written out in that section.

    The marker is a link, so `check_links` confirms the heading exists and stops
    there. It cannot tell whether the section says anything about this game, and
    for nine rows across five files it did not: `gamecube.md` flagged two games
    against a Contested table that held a header and nothing else, from the
    first commit onward. A reader following the link found an empty table.
    """
    problems = []
    rel = path.relative_to(ROOT)
    lines = path.read_text(encoding="utf-8").splitlines()

    def titles(header: str, width: int) -> list[str]:
        try:
            start = next(i for i, ln in enumerate(lines) if ln.startswith(header))
        except StopIteration:
            return []
        out = []
        for line in lines[start + 2:]:
            if not line.startswith("|"):
                break
            cells = [c.strip() for c in CELL_SPLIT_RE.split(line)[1:-1]]
            if len(cells) == width:
                out.append(re.sub(r"[^a-z0-9]", "", re.sub(r"[`*]", "", cells[0]).lower()))
        return out

    argued = [t for t in titles(CONTESTED_HEADER, 5) if t]
    try:
        start = next(i for i, ln in enumerate(lines) if ln.startswith(DEBUT_HEADER))
    except StopIteration:
        return problems
    for lineno, line in enumerate(lines[start + 2:], start + 3):
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in CELL_SPLIT_RE.split(line)[1:-1]]
        if len(cells) != EXPECTED_CELLS or "[Contested]" not in cells[11]:
            continue
        title = re.sub(r"[^a-z0-9]", "", re.sub(r"[`*]", "", cells[0]).lower())
        # A Contested row may cover two games at once ("Zero Racers / D-Hopper"),
        # so containment either way counts as the argument being made.
        if not any(title in a or a in title for a in argued):
            problems.append(f"{rel}:{lineno}: {cells[0]!r} is flagged Contested but the "
                            f"Contested table says nothing about it")
    return problems


def check_repeats(path: Path) -> list[str]:
    """A note must not make the same point twice in consecutive sentences.

    The failure is always the same shape: a short note was written, a fuller
    sentence was written later to replace it, and the old one was never
    deleted. `Fire Emblem` read "The series' first Western release. The series'
    first Western release, which is why its Japanese numbering is seven." for
    as long as the row existed. Seventeen catalogue notes were in that state.

    Compared on content words of five letters or more, so shared articles and
    prepositions do not trigger it.

    Reported rather than failed. It is a word-overlap heuristic over prose and
    two notes trip it honestly: `Star Fox Adventures` and `WarioWare: Twisted!`
    each make two different points that happen to share their proper nouns.
    The list is a worklist, not a verdict.
    """
    problems = []
    rel = path.relative_to(ROOT)
    try:
        start = next(i for i, ln in enumerate(path.read_text(encoding="utf-8").splitlines())
                     if ln.startswith(DEBUT_HEADER))
    except StopIteration:
        return problems
    lines = path.read_text(encoding="utf-8").splitlines()
    for lineno, line in enumerate(lines[start + 2:], start + 3):
        if not line.startswith("|"):
            break
        cells = [c.strip() for c in CELL_SPLIT_RE.split(line)[1:-1]]
        if len(cells) != EXPECTED_CELLS:
            continue
        sentences = [s for s in SENTENCE_RE.split(cells[11]) if len(s.split()) >= 5]
        for first, second in zip(sentences, sentences[1:]):
            a = set(re.findall(r"[a-z]{5,}", first.lower()))
            b = set(re.findall(r"[a-z]{5,}", second.lower()))
            # Three content words minimum, or the arithmetic is meaningless: a
            # sentence with one long word shares 100% of it the moment the next
            # sentence repeats that word, which is how `Re:coded` and `Star Fox
            # Adventures` were being reported for saying two different things.
            if min(len(a), len(b)) >= 3 and len(a & b) / min(len(a), len(b)) >= 0.6:
                problems.append(f"{rel}:{lineno}: {cells[0]!r} says the same thing twice: "
                                f"{first[:48]!r} then {second[:48]!r}")
                break
    return problems


def check_ragged(path: Path) -> list[str]:
    """Every row in a table carries the same number of cells as its header.

    `check_glued` above catches prose that runs past a row's final pipe, but it
    cannot see the case that actually happened twice here: the trailing text
    itself ended in a pipe, so the row still looked terminated. What gave both
    away was the cell count. `xbox-series.md` had a paragraph folded into the
    last row of its summary table, and README's platform index had an unescaped
    pipe in `Xbox Series X|S` splitting that row into six cells.

    A literal pipe in a cell is written `\\|`; see RULES.md and CONSISTENCY.md R14.
    """
    problems = []
    rel = path.relative_to(ROOT)
    width = None
    for i, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
        line = line.rstrip()
        if not line.startswith("|"):
            width = None
            continue
        cells = len(CELL_SPLIT_RE.split(line)) - 2
        if width is None:            # this row is the header
            width = cells
            continue
        if not line.strip("|-: "):   # the |---|---| separator
            continue
        if cells != width:
            problems.append(f"{rel}:{i}: table header has {width} cells, this row "
                            f"has {cells}; an unescaped pipe or glued text")
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
        problems += check_ragged(path)
    for path in catalogs:
        problems += check_contested(path)
    problems += check_links(catalogs + docs)

    # Collected before the failure check below, not after: an empty note is an
    # error now, so it has to reach `problems` while that list is still read.
    thin = 0
    worst: list[tuple[int, str]] = []
    for path in catalogs:
        empty, short = check_notes(path)
        thin += short
        if empty:
            problems.append(f"{path.relative_to(ROOT)}: {empty} row(s) with an "
                            f"empty Notes cell; see RULES.md#notes")
        if short:
            worst.append((short, f"{path.stem} ({short} thin)"))

    qualifying: list[str] = []
    repeats: list[str] = []
    for path in catalogs:
        qualifying += check_qualifies(path)
        repeats += check_repeats(path)

    if problems:
        print(f"{len(problems)} problem(s) across {len(catalogs)} catalogues:",
              file=sys.stderr)
        for problem in problems:
            print(f"  {problem}", file=sys.stderr)
        return 1

    if not args.quiet:
        print(f"{len(catalogs)} catalogues, {len(docs)} docs: no structural problems")
        if qualifying:
            print(f"  {len(qualifying)} row(s) marked as qualifying with no debut row:")
            for q in qualifying:
                print(f"    {q}")
        if repeats:
            print(f"  {len(repeats)} note(s) that may say the same thing twice:")
            for r in repeats:
                print(f"    {r}")
        if thin:
            # Reported, not enforced: see check_notes. The list is the worklist.
            print(f"  every row has a note; {thin} are under 40 characters")
            for _, label in sorted(worst, reverse=True)[:5]:
                print(f"    {label}")
        else:
            print("  every row has a note")
    return 0


if __name__ == "__main__":
    sys.exit(main())
