# Consistency pass: how to re-run it

The two rule changes that came before this pass (sim-ships, compilations) both
revealed that **later catalogue files had drifted from earlier ones**. The drift was
found by accident, because a rule change happened to expose it.

This file records the checks so drift can be found on purpose instead.

## The 16 checks

Each maps to a rule in [the ruleset](RULES.md). All are machine-verifiable from
the tables themselves.

| # | Check | Rule it enforces |
|---|---|---|
| R0 | Status is one of `Stranded` / `Ported` / `Sim-ship`; every row has exactly 12 columns | Table schema |
| R1 | Rows sorted by Year, then Title | Table schema |
| R2 | `Stranded` rows leave `Also On` empty | Status semantics |
| R3 | `Ported` / `Sim-ship` rows have a non-empty `Also On` | Status semantics |
| R4 | No row is `Ported` whose `Also On` is PC-only | PC is not a catalogued platform |
| R5 | `Sim-ship` rows say "same day" in `Also On` | Sim-ship definition |
| R6 | No Excluded row gives "compilation" as the reason | Compilations count |
| R7 | No Excluded row gives "arcade first" as the reason | Arcades are out of scope |
| R8 | No Excluded row gives "simultaneous" as the reason | Sim-ships are included |
| R9 | Every `Stranded` row has an explanatory note | Notes column rule |
| R10 | Header counts match actual row counts, and statuses sum to the total | Maintenance |
| R11 | Every file has Debut games / Excluded / Sources / Coverage gaps / Last verified | File structure |
| R12 | No broken internal links | |
| R13 | **Sim-ship reciprocity**: a `Sim-ship` must appear in every co-launch platform's file that exists | Never pick a canonical platform |
| R14 | A literal pipe in a cell is written `\|`; an unescaped one splits the row into extra cells | Table schema |
| R15 | Every row in a table carries the same number of cells as its header | Table schema |
| R16 | A row flagged `⚠ Contested` has its argument written out in the Contested table | Contested |

**R13 is the one that catches the most.** In its first run it found 16 sim-ships
present in only one file, including three where a note said "Also catalogued under X"
and the row in X had never been added.

## What the first full pass found

Run 2026-07-29, after the compilations change:

| Finding | Count | Nature |
|---|---|---|
| Unsorted tables | 17 files | Cosmetic; newer files were appended without re-sorting |
| Sim-ship present in only one file | 16 | **Real**: broke the no-canonical-platform rule |
| Excluded as "simultaneous" | 5 | **Real**: contradicted the sim-ship rule |
| Excluded as "arcade first" | 2 | **Real**: one was also in its own table, a direct contradiction |
| `Ported` justified by a PC port alone | 1 | **Real**: contradicted the PC rule |
| Escaped pipes in `Also On` | 4 | **Real**: silently broke column parsing |
| Title spelled two ways across files | 1 | `Nier` vs `NieR` |

Two rule *gaps* were also exposed, and are now settled in the skill:

- **`Sim-ship` outranks `Ported`.** A game can launch same-day on two consoles and
 reach a third later. `Forza Horizon 5` did. The status stays `Sim-ship` because that
 describes its debut; later platforms go in `Also On`.
- **Arcade-derived exclusions must cite the real reason.** `Ikaruga` on GameCube was
 excluded "arcade first" when arcades are out of scope; the actual disqualifier is
 that the Dreamcast version reached home first.

## When to run it

- After any rule change, before assuming the change is applied.
- After adding a batch of platforms.
- Before claiming the repo is consistent or complete.

The pass is cheap and reads only the tables. It cannot check facts, whether a game
really shipped on a given date is not machine-verifiable, so it complements
per-file verification rather than replacing it.
