"""Copy embedded images out of a .docx, named in document order.

usage: python -I extract_media.py <docx> <out_dir> <prefix>
"""
import os
import re
import sys
import zipfile
import xml.etree.ElementTree as ET

R_NS = "http://schemas.openxmlformats.org/officeDocument/2006/relationships"
REL_NS = "http://schemas.openxmlformats.org/package/2006/relationships"


def main():
    docx, out_dir, prefix = sys.argv[1:4]
    os.makedirs(out_dir, exist_ok=True)
    with zipfile.ZipFile(docx) as z:
        rels = ET.fromstring(z.read("word/_rels/document.xml.rels"))
        target = {r.get("Id"): r.get("Target") for r in rels.findall("{%s}Relationship" % REL_NS)}
        doc = z.read("word/document.xml").decode("utf-8")
        order = re.findall(r'r:embed="([^"]+)"', doc)
        seen = []
        for rid in order:
            t = target.get(rid)
            if t and t.startswith("media/") and t not in seen:
                seen.append(t)
        for i, t in enumerate(seen, 1):
            ext = os.path.splitext(t)[1]
            dest = os.path.join(out_dir, "%s-%02d%s" % (prefix, i, ext))
            with open(dest, "wb") as f:
                f.write(z.read("word/" + t))
            print(dest, "<-", t)


if __name__ == "__main__":
    main()
