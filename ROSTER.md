# Platform roster — what is covered, and what is not

This file exists because completeness was once **claimed without a checkable basis**,
and PS4 and PS5 turned out to be missing. Every console and handheld considered is
listed below with a decision and a reason, so the roster can be audited rather than
trusted.

## Included (58 catalogue files)

See the table in [README.md](README.md). Every entry there is a TV-connected or
portable system with a commercial software library and removable media or a dedicated
first-party catalogue.

## Folded into a parent platform

Add-ons and peripherals do not get their own files — their software is catalogued in the
host platform's file, marked in the Notes column.

| Add-on | Folded into |
|---|---|
| Famicom Disk System | [nes.md](catalogs/nes.md) |
| Satellaview, Nintendo Power SF Memory | [snes.md](catalogs/snes.md) |
| Nintendo 64DD | [n64.md](catalogs/n64.md) |
| Sega CD, 32X | [genesis.md](catalogs/genesis.md) |
| CD-ROM², Super CD-ROM², Arcade Card, SuperGrafx | [turbografx-16.md](catalogs/turbografx-16.md) |
| Neo Geo CD | [neo-geo.md](catalogs/neo-geo.md) |
| Jaguar CD | [atari-jaguar.md](catalogs/atari-jaguar.md) |
| Intellivoice | [intellivision.md](catalogs/intellivision.md) |
| Advanced Pico Beena | [sega-pico.md](catalogs/sega-pico.md) |
| PSVR, PSVR2 | [ps4.md](catalogs/ps4.md), [ps5.md](catalogs/ps5.md) |
| Kinect | [xbox-360.md](catalogs/xbox-360.md), [xbox-one.md](catalogs/xbox-one.md) |
| Vectrex 3D Imager | [vectrex.md](catalogs/vectrex.md) |
| Game Boy Player, Super Game Boy, Transfer Pak | Backward compatibility — not catalogued |

## Hardware revisions — no separate files

These play identical libraries and have **no exclusive software**, so a catalogue for
them would be empty: Game Boy Pocket / Light, GBA SP / Micro, DS Lite, DSi (DSiWare is
folded into [nintendo-ds.md](catalogs/nintendo-ds.md)), New 3DS, PS one, PS2 Slim,
PS3 Slim, PS4 Pro, PS5 Pro, Switch Lite / OLED, Xbox One S / X, Genesis Model 2/3 /
Nomad, Master System II, Lynx II, Channel F System II, Wii mini.

The only revision pair that *is* split is **Game Boy vs Game Boy Color**, because the
GBC has ~570 exclusive "black cartridge" titles.

## Deliberately excluded, with reasons

| System | Reason |
|---|---|
| Dedicated / single-game consoles (Home Pong, Odyssey 100–4000, Coleco Telstar, tabletop LCD units) | No removable media and no software library — one fixed game per unit. |
| Game & Watch, Tiger handhelds, LCD tabletops | Single-game devices. Nintendo's Game & Watch reissues are compilations, not a platform. |
| Evercade, Analogue Pocket, retro "mini" consoles, Polymega | **Re-release platforms by definition.** Their libraries are compilations of games that debuted elsewhere, which fails the debut test for every title. They appear as `Also On` targets instead. |
| Steam Deck, ROG Ally, Nvidia Shield, Ouya, Amazon Fire TV | PC or Android devices. PC is not a catalogued platform, and Android titles are mobile-first. |
| Tapwave Zodiac, N-Gage 2.0 service | Palm OS and Symbian software platforms. The **original N-Gage hardware** is included (removable media, dedicated buttons); its 2008 download service is not. |
| iOS, Android | Mobile. Noted in `Also On` where relevant but never catalogued. |
| Amstrad GX4000 | Included in principle but **not yet written** — see Pending. |
| Gizmondo, Nuon, Xavix, LeapFrog, VTech, Didj | Included in principle but **not yet written** — see Pending. |
| Arcade hardware (MVS, Hyper Neo Geo 64, Naomi, Triforce, System 246) | Arcades are out of scope by rule — a cabinet is not a collectable home device. |
| Cloud-only services (Stadia, Luna, GeForce Now) | No hardware library; games debut on other platforms. |
| Intellivision Amico | Announced but never properly shipped; no library exists. |
| Sega Nomad, PC Engine GT / TurboExpress, Genesis Nomad | Portable revisions playing the parent library — backward compatibility. |

## Pending — known gaps, not yet written

Stated explicitly so they are not mistaken for completeness:

| System | Notes |
|---|---|
| Amstrad GX4000 (1990) | ~27 titles, nearly all Amiga/CPC computer conversions — likely to be as thin as the Atari 5200 and CD32 for the same reason. |
| Nuon (2000) | A DVD-player games platform; ~8 titles. |
| Gizmondo (2005) | ~14 titles; the company collapsed in fraud proceedings. |
| Xavix Port, LeapFrog, VTech, Didj | Children's TV-connected systems with real cartridge libraries. Same category question as [Sega Pico](catalogs/sega-pico.md), which **is** included — so consistency argues for adding them. |
| Watara Supervision, Mega Duck, Game.com, Gamate | 1990s budget handhelds with small commercial libraries. |
| Bandai Super Vision 8000, Epoch Cassette Vision, Casio PV-1000 | Early Japanese cartridge consoles. |

## How to keep this honest

When adding a platform, add a row here too. When claiming the roster is complete, the
claim should be checkable against this file — not asserted from memory.
