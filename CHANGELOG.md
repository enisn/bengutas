# Changelog

Font versions follow the OpenType `head.fontRevision` convention: `1.100` is released as tag `v1.1.0`.

## 1.200 (v1.2.0) — 2026-11-04

Bengutas Display: Turkish-aware small-cap `i`.

- Lowercase `i` now renders as a dotless petite cap by default, consistent with the dotless petite-cap `j` and with small-cap convention (`Village` → VILLAGE).
- The dotted petite cap is kept as `i.loclTRK` and restored by the OpenType `locl` feature for Turkish, Azeri, Crimean Tatar, Kazakh and Tatar text (`Bilge` → BİLGE). `ı` is unchanged.
- New **Bengutas Display TR** build (`BengutasDisplayTR-Regular/Bold`) with the dotted `i` as default, for engines without `locl` support such as Unity TextMeshPro.
- The specimen's anatomy section demonstrates the `lang="en"` / `lang="tr"` switch.

## 1.100 (v1.1.0) — 2026-09-16

Expanded coverage from 127 to 157 glyphs in all four fonts (Bengutas Display and Bengutas Sans, Regular and Bold). Closes #1.

- Turkish circumflex vowels: Â â Î î Û û.
- Printable ASCII is now complete: ^ ` ~.
- Quotation and legal marks: « » ‹ › ©.
- Measurement marks: ′ ″ and the approximately-equal sign ≈.
- Arrows: ↔ ↕.
- Geometric and status marks for interface use: ▲ ▼ ▴ ▾ ◀ ▶ ● ○ ★ ✓ ✗.
- The specimen's character map lists the full set.

## 1.005 — 2026-09-04

The first public set: A–Z, petite small-caps, Turkish diacritics, numerals and core punctuation, with Orkhon chisel terminals in Display and double-chisel terminals in Sans. This version was not tagged.
