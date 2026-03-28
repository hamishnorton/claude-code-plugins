#!/usr/bin/env python3
"""Generate pandoc reference .docx templates for each year level (1-8).

Each template has year-appropriate font, size, line spacing, and letter spacing
baked into the Word styles. Used by pandoc --reference-doc for converting
markdown resources to properly formatted .docx files.
"""

import os
import subprocess
import tempfile
import xml.etree.ElementTree as ET
import zipfile

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR = os.path.join(SCRIPT_DIR, "templates")

# Word OOXML namespace
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
ET.register_namespace("w", W)
ET.register_namespace("r", R)

# Andika (SIL OFL) — designed for literacy, single-story a/g, excellent macron support.
# Embedded into output DOCX files post-pandoc so templates work on any OS.
EMBEDDED_FONT = "Andika"

# Year-level font settings from research
YEAR_SETTINGS = {
    1: {"body_size": 48, "heading_size": 56, "line_spacing": 480, "letter_spacing": 20},
    2: {"body_size": 44, "heading_size": 52, "line_spacing": 480, "letter_spacing": 20},
    3: {"body_size": 40, "heading_size": 48, "line_spacing": 420, "letter_spacing": 15},
    4: {"body_size": 36, "heading_size": 44, "line_spacing": 420, "letter_spacing": 10},
    5: {"body_size": 32, "heading_size": 40, "line_spacing": 360, "letter_spacing": 10},
    6: {"body_size": 28, "heading_size": 36, "line_spacing": 360, "letter_spacing": 0},
    7: {"body_size": 26, "heading_size": 34, "line_spacing": 360, "letter_spacing": 0},
    8: {"body_size": 24, "heading_size": 32, "line_spacing": 360, "letter_spacing": 0},
}
# Note: sizes are in half-points (Word convention). 24 half-points = 12pt.
# line_spacing is in 240ths of a line (240 = single, 360 = 1.5, 480 = double).
# letter_spacing is in half-points.


def w_tag(local):
    return f"{{{W}}}{local}"



def set_font_on_rpr(rpr, font_name):
    """Set the font on a run properties element, replacing theme refs with explicit fonts."""
    rfonts = rpr.find(w_tag("rFonts"))
    if rfonts is None:
        rfonts = ET.SubElement(rpr, w_tag("rFonts"))
    # Remove theme attributes and set explicit font
    for attr in list(rfonts.attrib.keys()):
        del rfonts.attrib[attr]
    rfonts.set(w_tag("ascii"), font_name)
    rfonts.set(w_tag("hAnsi"), font_name)
    rfonts.set(w_tag("eastAsia"), font_name)
    rfonts.set(w_tag("cs"), font_name)


def set_size_on_rpr(rpr, size_half_pts):
    """Set font size on run properties."""
    for tag_name in ("sz", "szCs"):
        el = rpr.find(w_tag(tag_name))
        if el is None:
            el = ET.SubElement(rpr, w_tag(tag_name))
        el.set(w_tag("val"), str(size_half_pts))


def set_letter_spacing_on_rpr(rpr, half_pts):
    """Set letter spacing (character spacing) on run properties."""
    if half_pts <= 0:
        # Remove spacing if present
        spacing = rpr.find(w_tag("spacing"))
        if spacing is not None:
            rpr.remove(spacing)
        return
    spacing = rpr.find(w_tag("spacing"))
    if spacing is None:
        spacing = ET.SubElement(rpr, w_tag("spacing"))
    spacing.set(w_tag("val"), str(half_pts))


def set_line_spacing_on_ppr(ppr, line_spacing_240ths):
    """Set line spacing on paragraph properties."""
    spacing = ppr.find(w_tag("spacing"))
    if spacing is None:
        spacing = ET.SubElement(ppr, w_tag("spacing"))
    spacing.set(w_tag("line"), str(line_spacing_240ths))
    spacing.set(w_tag("lineRule"), "auto")


def set_alignment_on_ppr(ppr, alignment="left"):
    """Set paragraph alignment (left-aligned for readability)."""
    jc = ppr.find(w_tag("jc"))
    if jc is None:
        jc = ET.SubElement(ppr, w_tag("jc"))
    jc.set(w_tag("val"), alignment)


def ensure_rpr(style_el):
    """Get or create rPr child of a style element."""
    rpr = style_el.find(w_tag("rPr"))
    if rpr is None:
        rpr = ET.SubElement(style_el, w_tag("rPr"))
    return rpr


def ensure_ppr(style_el):
    """Get or create pPr child of a style element."""
    ppr = style_el.find(w_tag("pPr"))
    if ppr is None:
        ppr = ET.SubElement(style_el, w_tag("pPr"))
    return ppr


# Styles that should use body text settings
BODY_STYLES = {"Normal", "BodyText", "FirstParagraph", "Compact", "BlockText"}

# Styles that should use heading settings
HEADING_STYLES = {"Title", "Subtitle", "Heading1", "Heading2", "Heading3", "Heading4", "Heading5"}


def modify_styles_xml(styles_xml_bytes, year_level):
    """Modify styles.xml with year-level-appropriate settings."""
    settings = YEAR_SETTINGS[year_level]
    font = EMBEDDED_FONT
    body_size = settings["body_size"]
    heading_size = settings["heading_size"]
    line_spacing = settings["line_spacing"]
    letter_spacing = settings["letter_spacing"]

    tree = ET.ElementTree(ET.fromstring(styles_xml_bytes))
    root = tree.getroot()

    # Update document defaults
    doc_defaults = root.find(w_tag("docDefaults"))
    if doc_defaults is not None:
        rpr_default = doc_defaults.find(f".//{w_tag('rPr')}")
        if rpr_default is not None:
            set_font_on_rpr(rpr_default, font)
            set_size_on_rpr(rpr_default, body_size)
            set_letter_spacing_on_rpr(rpr_default, letter_spacing)

        ppr_default = doc_defaults.find(f".//{w_tag('pPr')}")
        if ppr_default is None:
            ppr_default_container = doc_defaults.find(w_tag("pPrDefault"))
            if ppr_default_container is None:
                ppr_default_container = ET.SubElement(doc_defaults, w_tag("pPrDefault"))
            ppr_default = ET.SubElement(ppr_default_container, w_tag("pPr"))
        set_line_spacing_on_ppr(ppr_default, line_spacing)

    # Update individual styles
    for style in root.findall(w_tag("style")):
        style_id = style.get(w_tag("styleId"), "")
        style_type = style.get(w_tag("type"), "")

        if style_type != "paragraph":
            continue

        if style_id in BODY_STYLES:
            rpr = ensure_rpr(style)
            set_font_on_rpr(rpr, font)
            set_size_on_rpr(rpr, body_size)
            set_letter_spacing_on_rpr(rpr, letter_spacing)
            ppr = ensure_ppr(style)
            set_line_spacing_on_ppr(ppr, line_spacing)
            set_alignment_on_ppr(ppr, "left")

        elif style_id in HEADING_STYLES:
            rpr = ensure_rpr(style)
            set_font_on_rpr(rpr, font)
            # Headings are larger - scale up from heading_size
            if style_id == "Title":
                set_size_on_rpr(rpr, heading_size + 8)
            elif style_id in ("Subtitle", "Heading1"):
                set_size_on_rpr(rpr, heading_size + 4)
            elif style_id == "Heading2":
                set_size_on_rpr(rpr, heading_size)
            else:
                set_size_on_rpr(rpr, heading_size - 4)
            set_letter_spacing_on_rpr(rpr, letter_spacing)
            ppr = ensure_ppr(style)
            set_alignment_on_ppr(ppr, "left")

    return ET.tostring(root, xml_declaration=True, encoding="UTF-8")


def set_page_size_a4(document_xml_bytes):
    """Set page size to A4 (210mm x 297mm) in document.xml section properties."""
    tree = ET.ElementTree(ET.fromstring(document_xml_bytes))
    root = tree.getroot()

    body = root.find(w_tag("body"))
    if body is None:
        return document_xml_bytes

    sect_pr = body.find(w_tag("sectPr"))
    if sect_pr is None:
        sect_pr = ET.SubElement(body, w_tag("sectPr"))

    # A4: 210mm x 297mm = 11906 x 16838 twips
    pg_sz = sect_pr.find(w_tag("pgSz"))
    if pg_sz is None:
        pg_sz = ET.SubElement(sect_pr, w_tag("pgSz"))
    pg_sz.set(w_tag("w"), "11906")
    pg_sz.set(w_tag("h"), "16838")

    return ET.tostring(root, xml_declaration=True, encoding="UTF-8")


def generate_template(year_level, base_docx_path):
    """Generate a reference .docx template for a specific year level."""
    output_path = os.path.join(TEMPLATES_DIR, f"year-{year_level}-ref.docx")

    with tempfile.TemporaryDirectory() as tmpdir:
        # Extract base reference doc
        extract_dir = os.path.join(tmpdir, "extracted")
        with zipfile.ZipFile(base_docx_path, "r") as zin:
            zin.extractall(extract_dir)

        # Modify styles.xml
        styles_path = os.path.join(extract_dir, "word", "styles.xml")
        with open(styles_path, "rb") as f:
            styles_xml = f.read()

        modified_xml = modify_styles_xml(styles_xml, year_level)

        with open(styles_path, "wb") as f:
            f.write(modified_xml)

        # Set page size to A4 in document.xml
        doc_path = os.path.join(extract_dir, "word", "document.xml")
        with open(doc_path, "rb") as f:
            doc_xml = f.read()

        modified_doc = set_page_size_a4(doc_xml)

        with open(doc_path, "wb") as f:
            f.write(modified_doc)

        # Repack into .docx
        with zipfile.ZipFile(output_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for dirpath, dirnames, filenames in os.walk(extract_dir):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    arcname = os.path.relpath(file_path, extract_dir)
                    zout.write(file_path, arcname)

    return output_path


def main():
    os.makedirs(TEMPLATES_DIR, exist_ok=True)

    # Get pandoc's default reference doc
    with tempfile.NamedTemporaryFile(suffix=".docx", delete=False) as tmp:
        base_path = tmp.name

    try:
        subprocess.run(
            ["pandoc", "--print-default-data-file", "reference.docx"],
            stdout=open(base_path, "wb"),
            check=True,
        )

        print(f"Font: {EMBEDDED_FONT}\n")

        for year in range(1, 9):
            path = generate_template(year, base_path)
            settings = YEAR_SETTINGS[year]
            print(
                f"Created year-{year}-ref.docx  "
                f"({EMBEDDED_FONT}, {settings['body_size']//2}pt body, "
                f"{settings['line_spacing']/240:.1f}x spacing)"
            )
    finally:
        os.unlink(base_path)

    print(f"\nAll templates written to {TEMPLATES_DIR}/")


if __name__ == "__main__":
    main()
