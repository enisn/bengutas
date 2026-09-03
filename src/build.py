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

def compile_family(family_key, is_display=False):
    glyphs_db = glyphs_data.get(family_key, [])
    if not glyphs_db:
        print(f"Warning: No glyphs found for {family_key} in {PEN_PATH}!")
        return

    family_name = "Bengutas Display" if is_display else "Bengutas Sans"
    ps_prefix = "BengutasDisplay" if is_display else "BengutasSans"

    for weight_name, is_bold in [("Regular", False), ("Bold", True)]:
        font = fontforge.font()
        font.fontname = f"{ps_prefix}-{weight_name}"
        font.familyname = family_name
        font.fullname = f"{family_name} {weight_name}"
        font.weight = weight_name
        font.version = "1.005"
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
            # Import glyphs extracted directly from bengutas.pen
            for g_item in glyphs_db:
                u = g_item["unicode"]
                adv = g_item["advance"]
                d = g_item["d"]
                glyph_name = g_item["name"]
                
                if d and d.strip():
                    svg = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 1000"><path d="{d}" /></svg>'
                    svg_p = os.path.join(temp_dir, f"glyph_{u}.svg")
                    with open(svg_p, "w", encoding="utf-8") as tf:
                        tf.write(svg)
                        
                    g = font.createChar(u, glyph_name)
                    g.importOutlines(svg_p)
                    g.width = adv + (30 if is_bold else 0)
                    
                    if is_bold:
                        g.changeWeight(38, "auto", 0, 0, "auto")
                        
                    g.removeOverlap()
                    g.correctDirection()
                    
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
    compile_family("sans", is_display=False)
    print("=== All fonts built directly from bengutas.pen successfully! ===")
