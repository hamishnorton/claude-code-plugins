#!/usr/bin/env python3
"""Embed Andika font into a .docx file so it renders correctly on any OS.

Usage: python3 embed-fonts.py <file.docx> [fonts-dir]

The fonts-dir defaults to a 'fonts/andika/' directory next to this script.
Expects Andika-Regular.ttf, Andika-Bold.ttf, Andika-Italic.ttf, and
Andika-BoldItalic.ttf in that directory.
"""

import os
import sys
import tempfile
import uuid
import xml.etree.ElementTree as ET
import zipfile

# OOXML namespaces
W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
R = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
PKG_RELS = "http://schemas.openxmlformats.org/package/2006/relationships"
CT_NS = "http://schemas.openxmlformats.org/package/2006/content-types"

ET.register_namespace("w", W)
ET.register_namespace("r", R)
ET.register_namespace("", CT_NS)
ET.register_namespace("", PKG_RELS)

FONT_NAME = "Andika"

# Variant tag → TTF filename and OOXML embed element name
VARIANTS = {
    "regular":    ("Andika-Regular.ttf",    "embedRegular"),
    "bold":       ("Andika-Bold.ttf",       "embedBold"),
    "italic":     ("Andika-Italic.ttf",     "embedItalic"),
    "boldItalic": ("Andika-BoldItalic.ttf", "embedBoldItalic"),
}


def obfuscate_font(font_bytes):
    """Obfuscate font per OOXML spec (ECMA-376 §15.2.13).

    XOR the first 32 bytes with a 16-byte key derived from a GUID.
    Returns (obfuscated_bytes, guid_string).
    """
    guid = str(uuid.uuid4()).upper()
    hex_str = guid.replace("-", "")
    key = bytes.fromhex(hex_str)  # 16 bytes
    header = bytearray(font_bytes[:32])
    for i in range(32):
        header[i] ^= key[i % 16]
    return bytes(header) + font_bytes[32:], guid


def embed_fonts(docx_path, fonts_dir):
    """Embed Andika font variants into a .docx file in-place."""
    with tempfile.TemporaryDirectory() as tmpdir:
        extract_dir = os.path.join(tmpdir, "extracted")

        # Extract docx
        with zipfile.ZipFile(docx_path, "r") as zin:
            zin.extractall(extract_dir)

        # Create word/fonts/ directory
        word_fonts_dir = os.path.join(extract_dir, "word", "fonts")
        os.makedirs(word_fonts_dir, exist_ok=True)

        # Track relationship IDs and GUIDs for each variant
        embed_info = {}  # variant -> {rid, guid, odttf_name}
        rid_counter = 1

        for variant, (ttf_name, _embed_el) in VARIANTS.items():
            ttf_path = os.path.join(fonts_dir, ttf_name)
            if not os.path.exists(ttf_path):
                print(f"  Warning: {ttf_name} not found, skipping {variant}")
                continue

            with open(ttf_path, "rb") as f:
                font_bytes = f.read()

            obfuscated, guid = obfuscate_font(font_bytes)
            odttf_name = f"font{rid_counter}.odttf"
            rid = f"rIdFont{rid_counter}"

            with open(os.path.join(word_fonts_dir, odttf_name), "wb") as f:
                f.write(obfuscated)

            embed_info[variant] = {"rid": rid, "guid": guid, "odttf_name": odttf_name}
            rid_counter += 1

        if not embed_info:
            print(f"  No font files found in {fonts_dir}, skipping embedding")
            return

        # Update fontTable.xml
        ft_path = os.path.join(extract_dir, "word", "fontTable.xml")
        if os.path.exists(ft_path):
            ft_tree = ET.parse(ft_path)
            ft_root = ft_tree.getroot()
        else:
            ft_root = ET.Element(f"{{{W}}}fonts")
            ft_root.set(f"xmlns:r", R)
            ft_tree = ET.ElementTree(ft_root)

        # Find or create the font entry for Andika
        font_el = None
        for f in ft_root.findall(f"{{{W}}}font"):
            if f.get(f"{{{W}}}name") == FONT_NAME:
                font_el = f
                break

        if font_el is None:
            font_el = ET.SubElement(ft_root, f"{{{W}}}font")
            font_el.set(f"{{{W}}}name", FONT_NAME)
            charset = ET.SubElement(font_el, f"{{{W}}}charset")
            charset.set(f"{{{W}}}val", "00")
            family = ET.SubElement(font_el, f"{{{W}}}family")
            family.set(f"{{{W}}}val", "swiss")
            pitch = ET.SubElement(font_el, f"{{{W}}}pitch")
            pitch.set(f"{{{W}}}val", "variable")

        # Add embed elements for each variant
        for variant, info in embed_info.items():
            _ttf_name, embed_el_name = VARIANTS[variant]
            # Remove existing embed element if present
            existing = font_el.find(f"{{{W}}}{embed_el_name}")
            if existing is not None:
                font_el.remove(existing)
            embed_el = ET.SubElement(font_el, f"{{{W}}}{embed_el_name}")
            embed_el.set(f"{{{W}}}fontKey", f"{{{info['guid']}}}")
            embed_el.set(f"{{{R}}}id", info["rid"])

        ft_tree.write(ft_path, xml_declaration=True, encoding="UTF-8")

        # Create/update word/_rels/fontTable.xml.rels
        rels_dir = os.path.join(extract_dir, "word", "_rels")
        os.makedirs(rels_dir, exist_ok=True)
        ft_rels_path = os.path.join(rels_dir, "fontTable.xml.rels")

        rels_ns = PKG_RELS
        if os.path.exists(ft_rels_path):
            ET.register_namespace("", rels_ns)
            rels_tree = ET.parse(ft_rels_path)
            rels_root = rels_tree.getroot()
        else:
            rels_root = ET.Element(f"{{{rels_ns}}}Relationships")
            rels_tree = ET.ElementTree(rels_root)

        # Add relationship entries
        font_type = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/font"
        for _variant, info in embed_info.items():
            rel = ET.SubElement(rels_root, f"{{{rels_ns}}}Relationship")
            rel.set("Id", info["rid"])
            rel.set("Type", font_type)
            rel.set("Target", f"fonts/{info['odttf_name']}")

        ET.register_namespace("", rels_ns)
        rels_tree.write(ft_rels_path, xml_declaration=True, encoding="UTF-8")

        # Update [Content_Types].xml — add odttf content type
        ct_path = os.path.join(extract_dir, "[Content_Types].xml")
        ET.register_namespace("", CT_NS)
        ct_tree = ET.parse(ct_path)
        ct_root = ct_tree.getroot()

        # Check if odttf Default already exists
        has_odttf = any(
            d.get("Extension") == "odttf"
            for d in ct_root.findall(f"{{{CT_NS}}}Default")
        )
        if not has_odttf:
            default = ET.SubElement(ct_root, f"{{{CT_NS}}}Default")
            default.set("Extension", "odttf")
            default.set("ContentType", "application/vnd.openxmlformats-officedocument.obfuscatedFont")

        ct_tree.write(ct_path, xml_declaration=True, encoding="UTF-8")

        # Also ensure word/fontTable.xml is referenced in word/_rels/document.xml.rels
        doc_rels_path = os.path.join(extract_dir, "word", "_rels", "document.xml.rels")
        if os.path.exists(doc_rels_path):
            ET.register_namespace("", rels_ns)
            doc_rels_tree = ET.parse(doc_rels_path)
            doc_rels_root = doc_rels_tree.getroot()
            ft_rel_type = "http://schemas.openxmlformats.org/officeDocument/2006/relationships/fontTable"
            has_ft_rel = any(
                r.get("Type") == ft_rel_type
                for r in doc_rels_root.findall(f"{{{rels_ns}}}Relationship")
            )
            if not has_ft_rel:
                rel = ET.SubElement(doc_rels_root, f"{{{rels_ns}}}Relationship")
                rel.set("Id", "rIdFontTable")
                rel.set("Type", ft_rel_type)
                rel.set("Target", "fontTable.xml")
                doc_rels_tree.write(doc_rels_path, xml_declaration=True, encoding="UTF-8")

        # Repack docx
        with zipfile.ZipFile(docx_path, "w", zipfile.ZIP_DEFLATED) as zout:
            for dirpath, _dirnames, filenames in os.walk(extract_dir):
                for filename in filenames:
                    file_path = os.path.join(dirpath, filename)
                    arcname = os.path.relpath(file_path, extract_dir)
                    zout.write(file_path, arcname)


def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <file.docx> [fonts-dir]")
        sys.exit(1)

    docx_path = sys.argv[1]
    if not os.path.exists(docx_path):
        print(f"Error: {docx_path} not found")
        sys.exit(1)

    if len(sys.argv) >= 3:
        fonts_dir = sys.argv[2]
    else:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        fonts_dir = os.path.join(script_dir, "fonts", "andika")

    if not os.path.isdir(fonts_dir):
        print(f"Error: fonts directory not found: {fonts_dir}")
        sys.exit(1)

    print(f"Embedding {FONT_NAME} into {docx_path}...")
    embed_fonts(docx_path, fonts_dir)
    print("Done.")


if __name__ == "__main__":
    main()
