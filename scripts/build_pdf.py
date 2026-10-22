"""Build the proposal PDF from a Markdown file: Markdown -> HTML (TH Sarabun New) -> Microsoft Edge headless -> PDF.

usage: python -I -X utf8 scripts/build_pdf.py outline/final-outline-proposal.md outline/final-outline-proposal.pdf
Run from the repo root. Images use paths relative to the repo root (e.g. graphs/out/fig2_import_cost_redraw.png).
"""
import os
import subprocess
import sys

import markdown

EDGE_CANDIDATES = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
]

CSS = """
@page { size: A4; margin: 17mm 16mm 18mm 16mm; @bottom-center { content: counter(page) " / " counter(pages); font-family: 'TH Sarabun New'; font-size: 12pt; color: #78828C; } }
html { font-family: 'TH Sarabun New', sans-serif; font-size: 16pt; color: #263444; }
body { line-height: 1.22; margin: 0; }
h1 { font-size: 27pt; line-height: 1.1; margin: 0 0 4pt 0; color: #263444; font-weight: bold; }
h2 { font-size: 21pt; margin: 18pt 0 5pt 0; border-bottom: 1.2pt solid #78828C; padding-bottom: 2pt; font-weight: bold; break-after: avoid; }
h3 { font-size: 17.5pt; margin: 13pt 0 3pt 0; font-weight: bold; break-after: avoid; }
h4 { font-size: 16pt; margin: 9pt 0 2pt 0; font-weight: bold; break-after: avoid; }
p { margin: 3pt 0 5pt 0; }
ul, ol { margin: 2pt 0 5pt 0; padding-left: 20pt; }
li { margin: 1pt 0; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 9pt 0; font-size: 14.5pt; line-height: 1.12; }
th, td { border: 0.8pt solid #9AA3AB; padding: 2.5pt 5pt; vertical-align: top; text-align: left; }
th { background: #EEF0F2; font-weight: bold; }
tr { break-inside: avoid; }
img { max-width: 100%; height: auto; display: block; margin: 5pt auto; border: 0.6pt solid #DADFE3; }
code { font-family: 'TH Sarabun New', sans-serif; font-size: 15pt; background: #F3F4F6; padding: 0 2pt; }
blockquote { margin: 5pt 0; padding: 3pt 9pt; border-left: 3pt solid #B26A00; background: #FBF6EE; }
hr { border: 0; border-top: 0.8pt solid #C8CED3; margin: 10pt 0; }
.small { font-size: 13pt; color: #5b6670; }
.pagebreak { break-before: page; }
strong { font-weight: bold; }
"""


def font_face_css(root):
    """Load TH Sarabun New from the project copy (tools/fonts, made by scripts/env.ps1): headless Edge cannot see per-user fonts."""
    reg = os.path.join(root, "tools", "fonts", "thsarabunnew-webfont.ttf")
    bold = os.path.join(root, "tools", "fonts", "thsarabunnew_bold-webfont.ttf")
    if not (os.path.exists(reg) and os.path.exists(bold)):
        raise SystemExit("TH Sarabun New copies missing in tools/fonts; dot-source scripts/env.ps1 first")
    u = lambda p: "file:///" + p.replace("\\", "/")
    return (
        "@font-face { font-family: 'TH Sarabun New'; src: url('%s') format('truetype'); font-weight: normal; font-style: normal; }\n"
        "@font-face { font-family: 'TH Sarabun New'; src: url('%s') format('truetype'); font-weight: bold; font-style: normal; }\n"
        % (u(reg), u(bold))
    )


def find_edge():
    for p in EDGE_CANDIDATES:
        if os.path.exists(p):
            return p
    raise SystemExit("Microsoft Edge not found")


def main():
    src, out_pdf = sys.argv[1], sys.argv[2]
    root = os.getcwd()
    with open(src, encoding="utf-8") as f:
        text = f.read()
    html_body = markdown.markdown(text, extensions=["tables", "fenced_code", "attr_list", "sane_lists", "md_in_html"])
    base = "file:///" + root.replace("\\", "/") + "/"
    html = (
        "<!doctype html><html lang='en'><head><meta charset='utf-8'><base href='%s'>"
        "<title>%s</title><style>%s</style></head><body>%s</body></html>"
        % (base, os.path.basename(src), font_face_css(root) + CSS, html_body)
    )
    html_path = os.path.join(root, os.path.splitext(out_pdf)[0] + ".build.html")
    with open(html_path, "w", encoding="utf-8") as f:
        f.write(html)
    cmd = [
        find_edge(), "--headless=new", "--disable-gpu", "--no-pdf-header-footer",
        "--print-to-pdf=" + os.path.abspath(out_pdf),
        "--virtual-time-budget=20000",
        "file:///" + html_path.replace("\\", "/"),
    ]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=240)
    if r.returncode != 0 or not os.path.exists(out_pdf):
        print(r.stdout, r.stderr)
        raise SystemExit("Edge failed to print the PDF")
    os.remove(html_path)
    print("wrote", out_pdf, os.path.getsize(out_pdf), "bytes")


if __name__ == "__main__":
    main()
