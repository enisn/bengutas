# Bengü Taş (Bengutas) — Dual-Family Typography Collection

[![License: OFL-1.1](https://img.shields.io/badge/License-OFL_1.1-amber.svg)](https://opensource.org/licenses/OFL-1.1)
[![Online Demo](https://img.shields.io/badge/Live_Specimen-GitHub_Pages-brightgreen.svg)](https://enisn.github.io/bengutas/)
[![Formats](https://img.shields.io/badge/Formats-TTF_|_OTF_|_WOFF_|_WOFF2-blue.svg)](#formats)
[![Weights](https://img.shields.io/badge/Weights-Regular_(400)_|_Bold_(700)-orange.svg)](#weights)

**Bengü Taş (Bengutas)**, 1300 yıllık Orhun Yazıtları stellerinde (Kül Tigin, Bilge Kağan, Tonyukuk) sert granitin üzerine bronz ve demir keskilerle kazınan **kadim Türk taş kitabe geleneğini (lapidary / epigraphic)** modern dijital tipografiyle buluşturan özgün bir çift aileli (*dual-family*) yazı tipi koleksiyonudur.

> *« Üze Tengri basmasar, asra yer telinmeser, Türk budun, ilinin törünün kim artatı? »*  
> — **Bilge Kağan Yazıtı (MS 735)**

---

## 🏛️ Canlı Tipografi Vitrini (Live Specimen)

Fontu tarayıcınızda canlı olarak denemek, boyut ve ağırlıkları değiştirmek için interaktif vitrini ziyaret edebilirsiniz:  
👉 **[https://enisn.github.io/bengutas/](https://enisn.github.io/bengutas/)**

---

## ⚔️ Dual-Family (Çift Aile) Mimarisi

Koleksiyon, birbirini kusursuz tamamlayan iki bağımsız yazı tipi ailesinden oluşur:

### 1. `Bengutas Display` (Bengü Taş — Kitabe & Başlık Fontu)
* **Kullanım Alanı:** Oyun Logoları, Başlıklar, Bölüm İsimleri, Hükümdar Kartları, Banner'lar, Afişler.
* **Tasarım Felsefesi:** Dairesel pergel kavisleri tamamen reddedilir. Tüm harfler (`O, C, D, G, U, B, P` dahil) 45° ve 60° açılı sert taş keski fasetleriyle yontulmuştur.
* **Kahraman Damgalar:** `A` (Orhun 𐰀 damgası), `K` (Göktürk 𐰶 runu), `M & W` (Bengü Taş monoliti), `R & Q` (Göktürk 𐰺 runu ve hançer bacak), `S & Ş` (Göktürk 𐰽/𐰾 şimşek tamgası).
* **Petite Small-Caps:** Küçük harfle yazıldığında antik Roma ve Göktürk geleneklerine uygun olarak orantılı küçük majusküller (Small-Caps) devreye girer.

### 2. `Bengutas Sans` (Metin & UI Fontu)
* **Kullanım Alanı:** Oyun içi envanter açıklamaları, diyalog pencereleri, ayarlar menüleri, uzun gövde metinleri ve web arayüzleri.
* **Tasarım Felsefesi:** Gözü asla yormayan, yüksek okunabilirlikli kristal netliğinde modern grotesque yapı.

---

## 📂 Dosya ve Dizin Yapısı

```
bengutas/
├── bengutas.pen          # Orijinal vektör çizim kaynak dosyası (Pencil formatında)
├── dist/                 # Kullanıma hazır font dosyaları
│   ├── ttf/              # TrueType (.ttf) — Oyun motorları (Unity, Unreal, Godot) & Masaüstü
│   ├── otf/              # OpenType (.otf) — Grafik tasarım (Figma, Photoshop, Illustrator) & Baskı
│   └── web/              # Web fontları (.woff, .woff2) — Web siteleri & UI
├── docs/                 # GitHub Pages canlı test vitrini (index.html)
├── src/                  # Font derleme scriptleri ve kaynak vektör JSON verileri
│   ├── build.py          # FontForge derleyici scripti
│   ├── regular_glyphs.json
│   └── bold_glyphs.json
├── LICENSE               # SIL Open Font License 1.1
└── README.md
```

---

## 📦 Kurulum ve Kullanım

### 1. Masaüstü (Windows / macOS / Linux)
* `dist/ttf/` veya `dist/otf/` klasöründeki font dosyalarını açıp **Yükle (Install)** butonuna tıklayın.

### 2. Oyun Motorları (Unity / Unreal / Godot)
* **Unity:** `dist/ttf/` içerisindeki dosyaları Unity projenizin `Assets/.../Fonts/` klasörüne sürükleyin. TextMeshPro ile *Font Asset* oluşturup doğrudan kullanın.
* **Unreal Engine:** Font dosyalarını `Content/Fonts/` dizinine aktarıp Font Asset olarak bağlayın.
* **Godot:** `.ttf` dosyasını `res://fonts/` klasörüne koyup `Theme` veya `Label` üzerinde `DynamicFont` olarak atayın.

### 3. Web (@font-face CSS)
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

h1, h2, .game-title {
  font-family: 'Bengutas Display', sans-serif;
  letter-spacing: 1.5px;
}

body, p, .ui-description {
  font-family: 'Bengutas Sans', sans-serif;
}
```

---

## 📜 Lisans ve Kullanım Koşulları (License)

Bu font yazılımı **SIL Open Font License, Version 1.1 (OFL 1.1)** altında lisanslanmıştır.  
*(Ayrılmış Yazı Tipi Adları / Reserved Font Names: `Bengü Taş`, `Bengutas`)*

### ✅ Serbest Olanlar (Free for Commercial Use)
* **Oyunlar:** Bağımsız veya ticari oyunlarınızda (Steam, konsollar, mobil) ücretsiz ve telifsiz kullanabilirsiniz.
* **Uygulamalar & Web:** Ticari web sitelerinde, mobil uygulamalarda, yazılımlarda kullanabilirsiniz.
* **Görsel & Baskı:** Logo, afiş, kitap, ambalaj, tişört, yayın ve her türlü görsel materyalde özgürce kullanabilirsiniz.

### ❌ Yasak Olanlar (Resale Prohibited)
* **Font Dosyasını Satmak:** Bu font dosyalarını tek başına para karşılığı satamazsınız.
* **Değiştirip Satmak:** Fontu alıp küçük değişiklikler yaparak kendi fontunuzmuş gibi satışa sunamazsınız.

---

**Bengü Taş Project** © 2026. Designed with passion for steppe heritage and ancient history.
