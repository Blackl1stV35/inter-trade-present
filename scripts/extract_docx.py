"""Dump text (paragraphs + tables, in document order) and media list of .docx files.

usage: python -I extract_docx.py <out_dir> <docx> [<docx> ...]
"""
import sys
import zipfile
import re
import os
import xml.etree.ElementTree as ET

W = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"
NS = {"w": W}


def q(tag):
    return "{%s}%s" % (W, tag)


def para_text(p):
    out = []
    for node in p.iter():
        if node.tag == q("t"):
            out.append(node.text or "")
        elif node.tag == q("tab"):
            out.append("\t")
        elif node.tag == q("br"):
            out.append("\n")
    style = ""
    ppr = p.find("w:pPr", NS)
    if ppr is not None:
        ps = ppr.find("w:pStyle", NS)
        if ps is not None:
            style = ps.get(q("val")) or ""
        num = ppr.find("w:numPr", NS)
        if num is not None:
            out.insert(0, "  - ")
    return style, "".join(out)


def walk(body, lines, depth=0):
    for child in body:
        if child.tag == q("p"):
            style, text = para_text(child)
            if not text.strip():
                continue
            prefix = ""
            m = re.match(r"Heading(\d)", style or "")
            if m:
                prefix = "#" * int(m.group(1)) + " "
            elif style == "Title":
                prefix = "TITLE: "
            lines.append(prefix + text)
        elif child.tag == q("tbl"):
            lines.append("[TABLE]")
            for tr in child.findall("w:tr", NS):
                cells = []
                for tc in tr.findall("w:tc", NS):
                    cell_lines = []
                    walk(tc, cell_lines, depth + 1)
                    cells.append(" / ".join(cell_lines))
                lines.append(" | ".join(cells))
            lines.append("[/TABLE]")
        elif child.tag == q("sdt"):
            content = child.find("w:sdtContent", NS)
            if content is not None:
                walk(content, lines, depth)


def main():
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    for path in sys.argv[2:]:
        name = os.path.splitext(os.path.basename(path))[0]
        with zipfile.ZipFile(path) as z:
            names = z.namelist()
            root = ET.fromstring(z.read("word/document.xml"))
            body = root.find("w:body", NS)
            lines = []
            walk(body, lines)
            media = [n for n in names if n.startswith("word/media/")]
            extras = [n for n in names if re.match(r"word/(comments|footnotes|endnotes|header\d*|footer\d*)\.xml", n)]
            txt = "\n".join(lines)
            for ex in extras:
                r = ET.fromstring(z.read(ex))
                t = " ".join((x.text or "") for x in r.iter(q("t"))).strip()
                if t:
                    txt += "\n\n[%s]\n%s" % (ex, t)
            safe = re.sub(r"[^A-Za-z0-9_.-]+", "_", name)
            with open(os.path.join(out_dir, safe + ".txt"), "w", encoding="utf-8") as f:
                f.write(txt)
            print("%s: %d lines, %d chars, media=%s, extras=%s" % (name, len(lines), len(txt), media, extras))


if __name__ == "__main__":
    main()
