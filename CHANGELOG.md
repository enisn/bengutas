# Changelog

Font versions follow the OpenType `head.fontRevision` convention: `2.000` is released as tag `v2.0.0`.

## 2.000 (v2.0.0) — 2026-11-05

Major epigraphic redesign of **Bengutas Display** and refinement of **Bengutas Sans**, grounded in paleographic research on the 8th-century *Kül Tigin*, *Bilge Khagan*, and *Tonyukuk* stelae.

- **Orkhon Composite-Bow (*Yay*) Curves (`Bengutas Display`):** Replaced V1's polygonal 12-to-36-segment straight facets with authentic high-tension quadratic composite-bow (*yay*) curves on `O, C, D, G, B, P, Q, R, S, U` and numerals `0, 2, 3, 5, 6, 8, 9`, inspired by Orkhon `𐰖` (*y¹*), `𐰣` (*n¹*), `𐰏` (*g²*), `𐰉` (*b¹*), `𐰘` (*y²*), `𐰦` (*nt*), and `𐰽` (*s¹*).
- **Pointed Stela-Arch Enclosures (`O, Q, C, G, U, S, 0, 8`):** Opposing bow curves now meet at a crisp pointed stela-arch crest at the crown (`y=72`) and base (`y=812`), eliminating flat octagonal tops and Bold-weight polygon "thorn" artifacts.
- **Acute `35°–42°` Chisel V-Notches & *Tamga* Barbs (`E, F, H, I, J, K, L, M, N, T, V, W, X, Y, Z`):** Replaced V1's `90°` orthogonal junctions with deep 50–60 UPM acute chisel V-notches where arms and crossbars join vertical pillars, plus upward/downward *tamga* barbs inspired by `𐰀` (*a*), `𐰃` (*i*), `𐰚` (*k²*), `𐰞` (*l¹*), and `𐰔` (*z*).
- **Fixed Backwards `Z/z` & Broken Numerals (`9, 2, 3, Q, W`):** Corrected `Z` (`U+005A`) and `z` (`U+007A`) so the diagonal slashes top-right to bottom-left with authentic Orkhon barbs (`𐰔`); rebuilt `9` (`U+0039`), `2` (`U+0032`), `3` (`U+0033`), and `Q` (`U+0051`) to full cap height (`y=72..812`); unified `W` (`U+0057`) stroke weight across all four legs.
- **Diamond-Chisel Punctuation & Symbols (`⁚`):** Redesigned 35 punctuation, currency, bracket, and arrow glyphs in `Bengutas Display` to use 45° diamond chisel dots (`. , : ; ! ? … · •`, matching the Orkhon word divider `⁚`) and taut bow/chisel geometry (`$ € ₺ £ & % ‰ @ ( ) [ ] { } ← → ↑ ↓ ↔ ↕`), plus diamond-chisel Turkish diacritics (`İ, Ö, Ü, Ğ, Ç, Ş, Â, Î, Û`).
- **Petite Small-Caps (`a–z`) & Turkish `locl` Sync:** Regenerated all 26 petite small-caps (`a–z`), 9 Turkish lowercase glyphs (`ç, ğ, ı, ö, ş, ü, â, î, û`), and `i.loclTRK` from the V2 masters.
- **Bengutas Sans V2 Refinements:** Sharpened the upper stem-head chisel bevels on `I, İ, L, H, E, F, l, ı` to `36°–38°`.
- **Clean Bold Stroke Expansion (`src/build.py`):** Added pre- and post-expansion `removeOverlap()`, `correctDirection()`, and degenerate-contour filtering around `changeWeight(32)` so every acute V-notch and bow curve compiles cleanly in Bold.
- **Documentation & Live Specimen (`README.md`, `docs/index.html`, `docs/banner.png`):** Added comparative paleographic documentation explaining the Germanic wood-rune fallacy vs. Orkhon stone epigraphy (*yay* curves + acute chisel V-notches) and the 6 morphological patterns of Bengutas V2. Removed unused legacy `src/regular_glyphs.json` and `src/bold_glyphs.json`.

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
