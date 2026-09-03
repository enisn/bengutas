# Bengü Taş (Bengutas)

<p align="center">
  <img src="docs/banner.png" alt="Bengü Taş Typeface Hero Banner" width="800">
</p>

<p align="center">
  <a href="https://opensource.org/licenses/OFL-1.1"><img src="https://img.shields.io/badge/License-OFL_1.1-amber.svg" alt="License: OFL-1.1"></a>
  <a href="https://enisn.github.io/bengutas/"><img src="https://img.shields.io/badge/Live_Specimen-GitHub_Pages-brightgreen.svg" alt="Online Specimen"></a>
  <a href="#formats"><img src="https://img.shields.io/badge/Formats-TTF_|_OTF_|_WOFF_|_WOFF2-blue.svg" alt="Formats"></a>
  <a href="#weights"><img src="https://img.shields.io/badge/Weights-Regular_(400)_|_Bold_(700)-orange.svg" alt="Weights"></a>
</p>

**Bengü Taş** (*Bengutas*) is an open-source, dual-family typographic system inspired by the 8th-century epigraphic stone inscriptions of the Orkhon Valley. It translates the severe, non-curvilinear chisel geometry of ancient Eurasian stelae into a refined modern Latin typeface.

> *Öd Teŋri yasar, kisi ogli qop ölgeli törümis.*  
> *"Time is ordained by Heaven; mortal man is born only to pass away."*  
> — **Kül Tigin Stela (AD 732)**

---

## 🏛️ Live Specimen & Interactive Tester

An interactive type specimen with live font switching, variable size controls, and full character maps is available at:  
👉 **[https://enisn.github.io/bengutas/](https://enisn.github.io/bengutas/)**

---

## 📐 The Dual-Family System

Bengutas is built as a complementary two-part system designed for contrasting editorial and display applications:

| Family | Classification | Intended Use | Distinctive Traits |
| :--- | :--- | :--- | :--- |
| **Bengutas Display** | Epigraphic Lapidary | Titles, Headers, Posters, Identity | Strictly non-curvilinear; all curved forms are chiseled with 45°/60° stone chamfers. Includes automatic petite small-caps for lowercase input. |
| **Bengutas Sans** | Contemporary Grotesque | Body Copy, UI, Editorial, Descriptions | Clean, neutral proportions with optimal legibility across small text sizes and screen environments. |

---

## 🔍 Design Philosophy

Ancient monument carvers working on hard basalt and granite stelae could not score freehand compass curves into stone. Instead, lines were struck with bronze and iron chisels in deliberate, faceted planes.

**Bengutas Display** honors this epigraphic logic:
* **Faceted Basalt Geometry:** Rounded letters (`O`, `C`, `D`, `G`, `U`, `B`, `P`) are sculpted as octagonal, chiseled stone rings rather than mechanical ellipses.
* **Chevron & Dagger Junctions:** Diagonals meet stems at sharp, incised stone-cut angles.
* **Petite Small-Caps:** In line with ancient monumental tradition, lowercase letters render as scaled, balanced majuscules.

---

## 📂 Repository Structure

```
bengutas/
├── bengutas.pen          # Vector master source file (Pencil format)
├── dist/                 # Ready-to-use production binaries
│   ├── ttf/              # TrueType format (.ttf)
│   ├── otf/              # OpenType format (.otf)
│   └── web/              # Web formats (.woff, .woff2)
├── docs/                 # Interactive specimen hosted via GitHub Pages (index.html)
│   ├── banner.png        # Typographic hero banner
│   └── index.html        # Live web tester
├── src/                  # Build toolchain and vector datasets
│   ├── build.py          # FontForge build script
│   ├── regular_glyphs.json
│   └── bold_glyphs.json
├── LICENSE               # SIL Open Font License 1.1
└── README.md
```

---

## 📦 Installation & Usage

### Desktop (macOS, Windows, Linux)
Download the `.ttf` or `.otf` files from `dist/ttf/` or `dist/otf/` and install them via your operating system's font manager.

### Web (@font-face CSS)
```css
@font-face {
  font-family: 'Bengutas Display';
  src: url('dist/web/BengutasDisplay-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
}

@font-face {
  font-family: 'Bengutas Sans';
  src: url('dist/web/BengutasSans-Regular.woff2') format('woff2');
  font-weight: 400;
  font-style: normal;
}

h1, h2, .headline {
  font-family: 'Bengutas Display', serif;
  letter-spacing: 1.5px;
}

body, p {
  font-family: 'Bengutas Sans', sans-serif;
}
```

---

## 📜 License

This font software is licensed under the **SIL Open Font License, Version 1.1 (OFL 1.1)**.  
Reserved Font Names: `Bengü Taş`, `Bengutas`.

* **Permitted:** Free to use in commercial and personal projects, applications, websites, games, printed publications, and brand identities without royalties.
* **Prohibited:** Neither the font software nor any of its components may be sold by itself, or repackaged and sold under a different name.

---

**Bengü Taş (Bengutas)** — Epigraphic Lapidary Typeface Project.
