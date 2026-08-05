# Unique Console Games: the ruleset

The rules behind every catalogue here: what qualifies, how the table is shaped,
how contested cases are settled, and how to research a new platform. Read this
before adding a platform or auditing an existing file.
[`CONSISTENCY.md`](CONSISTENCY.md) lists the 14 checks that enforce it.

Build and maintain per-platform catalogues of the games each console **gave the
world first**. One markdown file per platform under `catalogs/`, table-driven.

**Purpose.** This is a *collecting guide*. The end goal is to own physical or
digital copies and play them on the original release hardware. So the question
each file answers is: **"which machine do I need on the shelf to play this game as
it first shipped?"** That is why debut is the test and why emulation and backward
compatibility never count; they are not the original device.

A game qualifies on **one** test: did it debut here? Whether it later appeared
elsewhere does not affect membership; it is recorded as an attribute, not used
as a filter.

## The inclusion test: did it debut here?

The platform must be the game's **first release anywhere, and the only platform
it launched on**. Nothing else matters for inclusion.

Disqualified:

| Reason | Example |
|---|---|
| **Port**: same game, later platform | `Bayonetta` on Wii U (Xbox 360/PS3, 2009) |
| **Remaster / HD edition** | `The Wind Waker HD`: the game is a 2002 GameCube release |
| **Remake**, however substantial | `Metroid: Samus Returns` remakes *Metroid II* (1991); `Pokémon Omega Ruby` remakes *Ruby* (2002) |

Not disqualified:

- **Compilations.** A compilation is a **new product** and debuts on the platform where
 that product first shipped. `Super Mario All-Stars` is an SNES debut; the NES games
 inside it keep their own separate NES entries. Judge the compilation on its own
 first-release date, not its contents'.

 This cuts both ways and both directions are already in use:
 - A compilation is itself catalogued as a debut where it first shipped.
 - A compilation is **also** a re-release vehicle for its contents, being folded
 into `WipEout Omega Collection` is what makes `WipEout 2048` `Ported`.

 Both statements are true at once and neither overrides the other.

- **A prior arcade release.** Arcades are **out of scope**; a cabinet is not a
 device anyone collects and plays at home, so an arcade original is invisible to
 this catalogue. `Street Fighter II` counts as an SNES debut; `Pokkén Tournament`
 counts as a Wii U debut. **But a prior release on another *home* platform still
 disqualifies**: NES `Donkey Kong` is excluded because the Atari 2600 and
 ColecoVision had it in 1982, not because of the 1981 cabinet.
- **Simultaneous multiplatform launches.** A same-day release counts as a debut on
 **every** platform it launched on. `Breath of the Wild` appears in both the Wii U
 and Switch catalogues. Mark it `Sim-ship` and list the co-launch platforms in
 `Also On`; a collector needs to know either machine will do.

 **Never pick a "canonical" platform for a sim-ship.** It is tempting to table the
 game once and write "catalogued under X" in the other platform's Excluded section.
 Do not do this. There is no lead platform for a same-day release, and a collector
 browsing the PS2 file needs to see `Killer7` there, not a pointer to the GameCube
 file. Duplication across catalogues is correct and intended for these entries.

 This applies however many platforms are involved. `Mortal Kombat` (1993) launched
 the same day on SNES, Genesis, Game Gear and Master System, so it belongs in all
 four files.
- **Sequels and spin-offs.** `Splatoon 2` is a new game. Splatoon's status is untouched.
- **Later ports of any kind.** `Mario Kart 8` reaching Switch in 2017 does not
 remove it; it debuted on Wii U and stays in the Wii U catalogue forever.
- **Enhanced editions on the same platform.** `Soul Sacrifice Delta` (Vita).
- **Staggered regional releases.** Use the earliest date worldwide as the debut.

### Same-day vs. shortly-after: the line that matters

`Sim-ship` means **same day**. It does not mean "also came out around then".
This distinction does most of the filtering work:

| Game | Wii U date | Elsewhere | Verdict |
|---|---|---|---|
| `Breath of the Wild` | 3 Mar 2017 | Switch, 3 Mar 2017 | **Sim-ship**: in both catalogues |
| `Assassin's Creed III` | 18 Nov 2012 | PS3/360, 30 Oct 2012 | **Excluded**: Wii U got a later port |
| `Call of Duty: Black Ops II` | 18 Nov 2012 | PS3/360, 13 Nov 2012 | **Excluded**: later port |
| `Mass Effect 3` | 18 Nov 2012 | PS3/360, Mar 2012 | **Excluded**: later port |

A console launch line-up is full of the second kind. Treat "released in the launch
window" as a port unless the dates actually match.

## Status: the exclusivity attribute

Every entry carries a `Status` recording where it stands **today**. This is
descriptive; it never affects membership.

| Status | Meaning |
|---|---|
| **Stranded** | Never officially released anywhere else, in any form. |
| **Ported** | Released elsewhere **later**. Fill `Also On` with platform + year. |
| **Sim-ship** | Launched the same day on other platforms. Fill `Also On` with the co-launch platforms. The entry appears in each of those platforms' catalogues too. |

**`Sim-ship` outranks `Ported`.** A game can do both, launch same-day on two consoles
and *then* reach a third years later. `Forza Horizon 5` sim-shipped on Xbox One and
Series X/S in 2021 and reached PS5 in 2025. Keep the status as `Sim-ship`, because that
is the fact about its *debut*, and list the later platforms in `Also On` alongside the
co-launch ones. Using `Ported` would hide that it had two debut platforms.

Status decays in one direction: `Stranded` → `Ported`, never back. When a port is
announced, change the status and fill `Also On`. **Never delete the row**, the
debut is a permanent historical fact.

### What counts as "released elsewhere"

Only officially licensed releases. Emulation is irrelevant: Cemu, Dolphin,
Ryujinx and flashcarts never change a status.

#### PC is not a catalogued platform

This repo catalogues **consoles and handhelds**, devices you collect and play on.
PC is not one of them, which has three consequences:

| Situation | Result |
|---|---|
| Console debut, later PC port | Still `Stranded`. Mention the PC release in `Notes`, leave `Also On` empty. |
| Console and PC **same day** | Counts as a console debut. Catalogue it on the console; PC does not make it a `Sim-ship`. |
| **PC first**, console later | **Excluded**: the game already existed. `Cave Story`, `Unepic`, `Gurumin`, SNES `Doom`. |

So a PC version never moves a game out of `Stranded`, but a PC version that came
*first* keeps it out of the catalogue entirely. Record PC availability in the Notes
so a reader knows the game is obtainable, just not on a second console.

#### Backward compatibility is NOT another platform

A later console running the *original release*: same SKU, disc, cartridge or
store entitlement, is backward compatibility. It does not change a status.
Otherwise the attribute collapses: nearly every PSP game runs on a Vita, every
Vita game on PlayStation TV, every Wii game on a Wii U, every Switch game on
Switch 2.

| Counts as another platform | Does not |
|---|---|
| A **port or remaster**: new build, new SKU (`Gravity Rush Remastered`) | Vita playing a **PSP** game |
| A **subscription re-release** that is a distinct store entry on a new platform (PS Plus Premium's PSP catalogue on PS4/PS5; NSO) | PS TV playing a **Vita** game |
| A **compilation** the game is folded into (`WipEout Omega Collection`) | Wii U playing a **Wii** disc |
| A **cross-buy twin** built for the other platform | Switch 2 playing a **Switch** cartridge |

The dividing line: did someone *build and ship a version for that platform*, or is
the new hardware merely running the old one?

## Contested cases

Some titles do not resolve cleanly. Do **not** silently pick a side, give them a
`Contested` section with the argument on each side. Under the debut rule the
recurring question is almost always *"is this a debut or a port?"*:

- **Handheld sibling versions.** `Super Mario Maker` (Wii U) vs
 `Super Mario Maker for Nintendo 3DS`; same game, gutted features, released later.
- **Shared-branding twins.** `Super Smash Bros. for Wii U` and `for Nintendo 3DS`
 ship under one name but are separate builds; the 3DS version came first by weeks,
 which matters under this rule.
- **Remake-or-sequel.** `Oreshika: Tainted Bloodlines`, `Castlevania: The Dracula X
 Chronicles`, `Tactics Ogre: Let Us Cling Together`.
- **Partial compilations.** `Ultimate NES Remix` (3DS) vs `NES Remix 1 & 2`.
- **Renamed enhanced re-releases.** `FAST Racing NEO` → `FAST RMX`.

Default to the stricter reading (assume it is a **port** and exclude it) then
record the counter-argument, so the catalogue never overclaims.

### Shelved games belong to the hardware they were built for

A game completed for platform X but first *released* years later on platform Y belongs
to **X** (the hardware it was written for) with the later release recorded as
`Ported`. `Star Fox 2` was finished for the SNES in 1995 and first sold on the SNES
Classic in 2017; it is an SNES debut that is now `Ported`. The Virtual Boy's
`Zero Racers` and `D-Hopper` follow the same rule.

The alternative (treating the delivery vehicle as the debut platform) would put a
1995 SNES cartridge's debut on 2017 hardware, which is not useful to anyone trying to
collect it. Before release, such a game is `Stranded`; after, it is `Ported`.

### Remakes are not debuts

A ground-up remake is tempting to treat as a new game: new engine, new art, often
new systems. Resist it. The test is *"is this the first release of this game?"*,
and for a remake the answer is no: the game already existed. `Metroid: Samus
Returns`, `Pokémon Omega Ruby and Alpha Sapphire`, `Fire Emblem Echoes`,
`Castlevania: The Dracula X Chronicles` and `Tactics Ogre: Let Us Cling Together`
are all **excluded**, however good they are and however exclusive they remain.

Apply this uniformly across platforms; it is the single easiest place for a
catalogue to drift into inconsistency.

## Table format

One table per platform, identical columns everywhere so files stay diff-able.

```markdown
| Title | Year | Developer | Publisher | Genre | Players | Online | Status | Also On | Language | Notes |
|---|---|---|---|---|---|---|---|---|---|---|
```

| Column | Rule |
|---|---|
| `Title` | Full official title, region-neutral (prefer NA naming, note PAL name if it differs). |
| `Year` | Year of first release **anywhere**, not the local region's date. |
| `Developer` | Studio. Multiple studios separated by `/`. |
| `Publisher` | Publisher at first release. |
| `Genre` | Short and consistent; reuse terms already in the file. |
| `Players` | Local player count: `1`, `1–4`, `1–5 (asym.)`. Use `asym.` for asymmetric second-screen designs. |
| `Online` | `Yes`, `No`, or `Dead (year)` where servers have shut down. |
| `Status` | `Stranded`, `Ported`, or `Sim-ship`. |
| `Also On` | Empty when stranded. Otherwise every platform with year: `Switch (2017), PC (2020)`. For `Sim-ship`, list the co-launch platforms and mark them, e.g. `Switch (2017, same day)`. |
| `Language` | The language the game shipped in, where it is known and worth stating. Japan-only releases are `Japanese`. Leave empty rather than assuming; an empty cell means unrecorded, not English. |
| `Notes` | One line. Prefer *why* it is stranded (hardware dependency, licensing, studio closure, server death) over review commentary. |

Sort by Year, then Title. Keep everything in **one** table; status is a column,
not a section. Splitting by status buries the point that these are all the same
kind of thing.

## Naming platforms

The `# ` heading is the platform's identity: it is what the README index links
to and what the sibling suggester shows as a label. It uses the full name, with
the manufacturer, because a list of sixty-eight of them is where an incomplete
name looks wrong. `Nintendo Game Boy`, not `Game Boy`, alongside the
`Nintendo 3DS` and `Sony PlayStation 2` that were already written that way.

Leave the manufacturer off only where the name already contains it
(`ColecoVision`, `Nintendo Entertainment System`) or where nobody has ever
prefixed it (`Atari 2600` is Atari's, and the name says so).

The `Also On` column follows the same rule, since it is a list of platforms.
Prose does not: "the Game Boy's defining trick" is better than the alternative,
and the short name is what people say.

## Per-platform file structure

`catalogs/<platform-slug>.md`:

1. **Header**: platform, lifespan, store/online status, backward-compat note,
 category spine used, date last verified, honest coverage statement.
2. **Summary**: total debut-exclusives, how many still stranded, and the
 one-paragraph story of *why this platform strands what it strands*.
3. **Debut-exclusive games**: the single main table.
4. **Contested**: the argument on both sides.
5. **Excluded**: titles commonly assumed to qualify but that fail the debut test,
 with the reason recorded so they are not re-added.
6. **Appendix**: long tails assessed in bulk rather than individually, clearly
 labelled and kept out of the counts.
7. **Sources**: links, with the date checked.

## Research method

1. Start from the platform's full release list (Wikipedia `List of <platform> games`)
; these do **not** mark exclusivity or debut, so they are only a spine.
2. Use Wikipedia's `Category:<Platform>-only games` where it exists. It is a good
 seed but it is **incomplete and noisy**, the Vita category contains ~20
 franchise articles for anime series that are not games at all, and categories
 miss titles that plainly qualify.
3. Treat "never ported" listicles as *leads, not facts*: they conflate "not on
 the successor console" with "exclusive". `ZombiU`, `Watch Dogs` and
 `Sonic Lost World` all appear on Wii U "never ported to Switch" lists; all
 three are multiplatform.
4. For each candidate, verify the **debut** specifically, an earlier release on
 another *home* console, PC or handheld is the most common disqualifier and the
 easiest to miss. Arcade originals are out of scope and never disqualify.
5. Re-verify `Stranded` entries on every pass. Status decays: `Xenoblade
 Chronicles X` was stranded until March 2025, `The Wonderful 101` until 2020,
 `Persona 3 Portable` until 2023.

## Maintenance

- Put the verification date in the header and update it every pass.
- When a stranded game gets ported, flip `Status` and fill `Also On`. Never delete.
- Long-tail budget/eShop titles are the usual coverage gap. State in the header
 what the catalogue does and does not claim to cover.
- When a tail is too large to verify title-by-title, group it by publisher in an
 appendix, label the confidence, and keep it out of the counts. Look for a
 categorical cause first, e.g. Nintendo denied RCMADIAX a Switch dev licence in
 2018, which strands all 33 of its Wii U titles at once.
- Where a platform's status is inherently unstable, say so loudly. PSP `Stranded`
 claims are undermined by the PS Plus Premium Classics catalogue, which rotates
 monthly with no published list.
