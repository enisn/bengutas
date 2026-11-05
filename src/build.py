import fontforge
import json
import os
import shutil
import tempfile
import re

PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PEN_PATH = os.path.join(PROJECT_DIR, "bengutas.pen")
DIST_DIR = os.path.join(PROJECT_DIR, "dist")
DOCS_DIR = os.path.join(PROJECT_DIR, "docs")

os.makedirs(os.path.join(DIST_DIR, "ttf"), exist_ok=True)
os.makedirs(os.path.join(DIST_DIR, "otf"), exist_ok=True)
os.makedirs(os.path.join(DIST_DIR, "web"), exist_ok=True)
os.makedirs(DOCS_DIR, exist_ok=True)

NOTDEF_SVG = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000">
  <path d="M 60 100 H 440 V 800 H 60 Z M 110 150 V 750 H 390 V 150 Z" />
</svg>'''

# Display renders lowercase as petite small-caps. A small capital I never carries
# a dot in Latin typography (petite-cap j is already dotless), so the default
# `i` is the dotless petite cap. The dotted petite cap drawn in bengutas.pen is
# kept as the unencoded glyph `i.loclTRK` and substituted back in by the OpenType
# `locl` feature for the Turkic languages whose uppercase i keeps its dot.
TURKIC_LANGS = ["TRK", "AZE", "CRT", "KAZ", "TAT"]

def build_locl_fea():
    systems = "\n".join(f"languagesystem latn {l};" for l in TURKIC_LANGS)
    rules = "\n".join(f"  language {l} exclude_dflt;\n  sub i by i.loclTRK;" for l in TURKIC_LANGS)
    return f"""languagesystem DFLT dflt;
languagesystem latn dflt;
{systems}

feature locl {{
  script latn;
{rules}
}} locl;
"""

def load_glyphs_from_pen(pen_file):
    """
    Parses bengutas.pen and extracts glyph dictionaries for Display and Sans.
    Returns: { 'display': [...], 'sans': [...] }
    """
    with open(pen_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    extracted = { "display": [], "sans": [] }
    
    def walk_tree(node, current_family=None):
        name = node.get("name", "")
        if "Bengutas Display" in name:
            current_family = "display"
        elif "Bengutas Sans" in name:
            current_family = "sans"
            
        # Check if this node is a glyph cell: e.g. 'U+0041 A'
        m = re.search(r"U\+([0-9A-Fa-f]{4})", name)
        if m and current_family:
            u = int(m.group(1), 16)
            adv = int(node.get("width", 500))
            svg_d = ""
            for child in node.get("children", []):
                if child.get("type") == "path" and child.get("geometry"):
                    svg_d = child.get("geometry")
                    break
            
            clean_name = name.split(" ")[-1] if " " in name else f"uni{u:04X}"
            extracted[current_family].append({
                "unicode": u,
                "name": clean_name,
                "advance": adv,
                "d": svg_d
            })
            return # Leaf glyph cell
            
        for child in node.get("children", []):
            walk_tree(child, current_family)
            
    for root_child in data.get("children", []):
        walk_tree(root_child)
        
    return extracted

def compile_family(family_key, is_display=False, turkish_default=False):
    """
    turkish_default=True builds the "Bengutas Display TR" variant: the dotted
    petite-cap i is the default glyph, for engines that do not honor the
    OpenType `locl` feature (e.g. Unity TextMeshPro). Assign it to the Turkish
    locale in such engines; everywhere else use the main family with lang tags.
    """
    glyphs_db = glyphs_data.get(family_key, [])
    if not glyphs_db:
        print(f"Warning: No glyphs found for {family_key} in {PEN_PATH}!")
        return

    family_name = "Bengutas Display" if is_display else "Bengutas Sans"
    ps_prefix = "BengutasDisplay" if is_display else "BengutasSans"
    if turkish_default:
        family_name += " TR"
        ps_prefix += "TR"

    # Display only: swap the encoded `i` outline for the dotless one and keep the
    # dotted outline as `i.loclTRK` (unencoded, reached through `locl`).
    i_dotted_d = None
    if is_display:
        by_u = {g["unicode"]: g for g in glyphs_db}
        if 0x69 in by_u and 0x131 in by_u:
            i_dotted_d = by_u[0x69]["d"]
            dotless_d = by_u[0x131]["d"]
            glyphs_db = [dict(g, d=(i_dotted_d if turkish_default else dotless_d)) if g["unicode"] == 0x69 else g
                         for g in glyphs_db]

    for weight_name, is_bold in [("Regular", False), ("Bold", True)]:
        font = fontforge.font()
        font.fontname = f"{ps_prefix}-{weight_name}"
        font.familyname = family_name
        font.fullname = f"{family_name} {weight_name}"
        font.weight = weight_name
        font.version = "2.000"
        font.copyright = "Copyright (c) 2026 Bengü Taş Type Project. Licensed under the SIL Open Font License, Version 1.1 (Reserved Font Names: 'Bengü Taş', 'Bengutas')."
        
        # Professional 1000 UPM Typographic Metrics
        font.em = 1000
        font.ascent = 800
        font.descent = 200
        
        font.os2_typoascent_add = 0
        font.os2_typodescent_add = 0
        font.hhea_ascent_add = 0
        font.hhea_descent_add = 0
        font.os2_winascent_add = 0
        font.os2_windescent_add = 0
        
        font.os2_typoascent = 800
        font.os2_typodescent = -200
        font.os2_typolinegap = 0
        font.os2_use_typo_metrics = 1
        
        font.hhea_ascent = 800
        font.hhea_descent = -200
        font.hhea_linegap = 0
        
        font.os2_winascent = 950
        font.os2_windescent = 250
        font.os2_weight = 700 if is_bold else 400
        
        temp_dir = tempfile.mkdtemp(prefix="ff_build_pen_")
        
        try:
            svg_counter = [0]
            def import_glyph(u, glyph_name, adv, d):
                svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><path d="{d}" /></svg>'
                svg_counter[0] += 1
                svg_p = os.path.join(temp_dir, f"glyph_{svg_counter[0]}.svg")
                with open(svg_p, "w", encoding="utf-8") as tf:
                    tf.write(svg)
                g = font.createChar(u, glyph_name)
                g.importOutlines(svg_p)
                g.width = adv + (30 if is_bold else 0)
                g.removeOverlap()
                g.correctDirection()
                if is_bold:
                    g.changeWeight(32, "auto", 0, 0, "auto")
                    g.removeOverlap()
                    clean_layer = fontforge.layer()
                    for c in g.foreground:
                        bb = c.boundingBox()
                        if len(c) >= 3 and (bb[2] - bb[0]) >= 4 and (bb[3] - bb[1]) >= 4:
                            clean_layer += c
                    g.foreground = clean_layer
                    g.correctDirection()
                return g

            # Import glyphs extracted directly from bengutas.pen
            for g_item in glyphs_db:
                if g_item["d"] and g_item["d"].strip():
                    import_glyph(g_item["unicode"], g_item["name"], g_item["advance"], g_item["d"])

            # Dotted petite-cap i for Turkic locales (Display only)
            if i_dotted_d and not turkish_default:
                i_adv = next(g["advance"] for g in glyphs_db if g["unicode"] == 0x69)
                import_glyph(-1, "i.loclTRK", i_adv, i_dotted_d)
                fea_p = os.path.join(temp_dir, "locl.fea")
                with open(fea_p, "w", encoding="utf-8") as tf:
                    tf.write(build_locl_fea())
                font.mergeFeature(fea_p)
                    
            # Space & non-breaking space
            space_width = 300 if is_bold else 280
            for sp_code in [32, 160]:
                sp = font.createChar(sp_code, "space" if sp_code == 32 else "nbspace")
                sp.width = space_width
                
            # .notdef fallback
            notdef_path = os.path.join(temp_dir, "notdef.svg")
            with open(notdef_path, "w", encoding="utf-8") as tf:
                tf.write(NOTDEF_SVG)
            notdef = font.createChar(-1, ".notdef")
            notdef.importOutlines(notdef_path)
            notdef.width = 500
            notdef.removeOverlap()
            notdef.correctDirection()
            
            # Generate binary formats
            ttf_p = os.path.join(DIST_DIR, "ttf", f"{font.fontname}.ttf")
            otf_p = os.path.join(DIST_DIR, "otf", f"{font.fontname}.otf")
            woff_p = os.path.join(DIST_DIR, "web", f"{font.fontname}.woff")
            woff2_p = os.path.join(DIST_DIR, "web", f"{font.fontname}.woff2")
            
            font.generate(ttf_p)
            font.generate(otf_p)
            font.generate(woff_p)
            try: font.generate(woff2_p)
            except: pass
            
            # Copy to docs for web specimen
            shutil.copy(woff2_p, os.path.join(DOCS_DIR, f"{font.fontname}.woff2"))
            shutil.copy(ttf_p, os.path.join(DOCS_DIR, f"{font.fontname}.ttf"))
            
            print(f"✓ Successfully built {font.fontname} ({len(glyphs_db)} glyphs from {os.path.basename(PEN_PATH)})")
            
        finally:
            shutil.rmtree(temp_dir, ignore_errors=True)

if __name__ == "__main__":
    print(f"=== BENGÜ TAŞ COMPILER: Reading Source of Truth from {PEN_PATH} ===")
    glyphs_data = load_glyphs_from_pen(PEN_PATH)
    print(f"Found {len(glyphs_data['display'])} Display glyphs and {len(glyphs_data['sans'])} Sans glyphs.")
    
    compile_family("display", is_display=True)
    compile_family("display", is_display=True, turkish_default=True)
    compile_family("sans", is_display=False)
    print("=== All fonts built directly from bengutas.pen successfully! ===")
