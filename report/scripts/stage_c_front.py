"""Stage C: front matter for report v5.
  - KU logo placeholder on the cover (the logo file was not in the workspace; insert it there later)
  - page-number footer from page 2 (cover unnumbered)
  - Table of Contents and List of Figures rebuilt as dot-leader lines with page numbers
Page numbers are read from a PDF export made by Microsoft Word, in two passes so the numbers match Word's layout.
Run from the repository root:  python -I -X utf8 report/scripts/stage_c_front.py
"""
import json
import os
import re
import subprocess

import docx
import fitz
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT, WD_TAB_LEADER
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor, Twips

PATH = 'report/inter-trade-report.docx'
PDF = os.path.abspath('report/inter-trade-report.pdf')

TOC = [  # (line shown, search text in the body, level)
    ('Chapter 1  Introduction and Details of the Policy', 'Introduction and Details of the Policy', 0),
    ('1.1 Background and significance', '1.1 Background and significance', 1),
    ('1.2 Objectives', '1.2 Objectives', 1),
    ('1.3 Scope, data and method', '1.3 Scope, data and method', 1),
    ('1.4 EU ETS: legal framework and operation', '1.4 EU ETS: legal framework', 1),
    ('1.5 CBAM: coverage, obligations and pricing', '1.5 CBAM: coverage', 1),
    ('1.6 Policy timeline and related measures', '1.6 Policy timeline and related', 1),
    ('1.7 Economic rationale and supporting policies', '1.7 Economic rationale', 1),
    ('Chapter 2  Economic Evidence and Discussion', 'Economic Evidence and Discussion', 0),
    ('2.1 Theoretical channels and interpretation of graphs', '2.1 Theoretical channels', 1),
    ('2.2 German manufacturing trends', '2.2 German manufacturing trends', 1),
    ('2.3 Steel production and market use', '2.3 Steel production and market use', 1),
    ('2.4 Exports, imports and trade balances', '2.4 Exports, imports and trade balances', 1),
    ('2.5 Cleaner-material investment and company cases', '2.5 Cleaner-material investment', 1),
    ('2.6 GDP components, fiscal revenue and employment', '2.6 GDP components', 1),
    ('2.7 Overall assessment and limitations', '2.7 Overall assessment', 1),
    ('Chapter 3  Conclusion and Suggestions', 'Conclusion and Suggestions', 0),
    ('3.1 Conclusion', '3.1 Conclusion', 1),
    ('3.2 Suggestions', '3.2 Suggestions', 1),
    ('3.3 Monitoring and future assessment', '3.3 Monitoring and future assessment', 1),
    ('References', 'References', 0),
    ('Appendix A  Manufacturing Data', 'Manufacturing Data', 0),
    ('Appendix B  Matched Trade Data and Calculations', 'Matched Trade Data and Calculations', 0),
    ('Appendix C  Chart Generating Code', 'Chart Generating Code', 0),
]
LOF = [  # (line shown, search text of the caption in the body)
    ('Figure 2.1  Negative production externality and carbon pricing (illustration)', 'Figure 2.1 Negative production'),
    ('Figure 2.2  Carbon-related import cost and partial pass-through (illustration)', 'Figure 2.2 Carbon-related import cost'),
    ('Figure 2.3  German manufacturing real GVA and production, 1995 to 2025', 'Figure 2.3 German manufacturing'),
    ('Figure 2.4  German crude-steel production and rolled-steel market supply, 2012 to 2025', 'Figure 2.4 German crude-steel'),
    ('Figure 2.5  Direct extra-EU Chapter 72 exports and imports, 1999 to 2025', 'Figure 2.5 Germany: direct'),
    ('Figure 2.6  Direct extra-EU Chapter 72 trade values and unit value, 2017 to 2025', 'Figure 2.6 Direct extra-EU Chapter 72 nominal'),
    ('Figure 2.7  Germany: Chapter 72 trade balance with extra-EU partners, intra-EU partners and all partners, 1999 to 2025 (value, EUR billion)', 'Figure 2.7 Germany: Chapter 72 trade balance'),
    ('Figure 2.8  Germany: Chapter 72 export volume index and nominal unit value by destination group, 1999 to 2025', 'Figure 2.8 Germany: Chapter 72 export volume'),
    ('Figure 2.9  Germany: real GDP index (2020 = 100) and annual real growth, 1995 to 2025', 'Figure 2.9 Germany: real GDP index'),
]
TEXT_W = Twips(11909 - 2 * 1440)


def new_par(text, bold=False, size=12, center=False, indent=0, tab=False, italic=False, color=None):
    p = OxmlElement('w:p')
    para = docx.text.paragraph.Paragraph(p, None)
    pf = para.paragraph_format
    pf.space_after = Pt(4)
    if tab:
        pf.tab_stops.add_tab_stop(TEXT_W, WD_TAB_ALIGNMENT.RIGHT, WD_TAB_LEADER.DOTS)
    if indent:
        pf.left_indent = Twips(360 * indent)
    if center:
        para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = para.add_run(text)
    r.bold = bold
    r.italic = italic
    r.font.size = Pt(size)
    r.font.name = 'Times New Roman'
    if color:
        r.font.color.rgb = RGBColor(*color)
    return p


def add_page_field(par):
    run = par.add_run()
    parts = [('w:fldChar', 'begin', None), ('w:instrText', None, ' PAGE '), ('w:fldChar', 'separate', None),
             ('w:t', None, '2'), ('w:fldChar', 'end', None)]
    for tag, attr, text in parts:
        el = OxmlElement(tag)
        if tag == 'w:fldChar':
            el.set(qn('w:fldCharType'), attr)
        elif tag == 'w:instrText':
            el.set(qn('xml:space'), 'preserve')
            el.text = text
        else:
            el.text = text
        run._r.append(el)


def build(pages):
    d = docx.Document(PATH)
    body = d.element.body
    kids = list(body)
    toc_head = next(p for p in d.paragraphs if p.text.strip() == 'Table of Contents')
    first_chapter = next(p for p in d.paragraphs if p.text.strip() == 'Chapter 1')
    a, b = kids.index(toc_head._p), kids.index(first_chapter._p)
    for el in kids[a + 1:b]:
        if el.tag == qn('w:p'):
            body.remove(el)
    anchor = toc_head._p
    new = []
    for text, _, lvl in TOC:
        new.append(new_par(text + '\t' + str(pages.get('toc:' + text, '')), bold=(lvl == 0), indent=lvl, tab=True))
    new.append(new_par('List of Figures', bold=True, size=14))
    for text, _ in LOF:
        new.append(new_par(text + '\t' + str(pages.get('lof:' + text, '')), tab=True))
    for el in new:
        anchor.addnext(el)
        anchor = el
    # cover: logo placeholder above the title; footer numbers from page 2
    sec = d.sections[0]
    sec.different_first_page_header_footer = True
    fp = sec.footer.paragraphs[0]
    for r in list(fp.runs):
        r._r.getparent().remove(r._r)
    fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_page_field(fp)
    d.save(PATH)


def export_pdf():
    cmd = ("$w = New-Object -ComObject Word.Application; $w.Visible = $false; $w.DisplayAlerts = 0; "
           "$doc = $w.Documents.Open('%s', $false, $true); "
           "$doc.ExportAsFixedFormat('%s', 17); $doc.Close($false); $w.Quit()") % (os.path.abspath(PATH), PDF)
    subprocess.run(['powershell', '-NoProfile', '-Command', cmd], check=True)


def find_pages():
    doc = fitz.open(PDF)
    texts = [re.sub(r'\s+', ' ', pg.get_text()) for pg in doc]
    norm = lambda s: re.sub(r'\s+', ' ', s)
    lof_page = next(i for i, t in enumerate(texts) if 'List of Figures' in t and 'Figure 2.1' in t)
    body_start = next(i for i, t in enumerate(texts) if i > lof_page and 'Introduction and Details of the Policy' in t)
    out = {}
    cur = body_start
    for text, search, _ in TOC:
        for i in range(cur, len(texts)):
            if norm(search) in texts[i]:
                out['toc:' + text] = i + 1
                cur = i
                break
        else:
            raise SystemExit('not found in PDF: ' + search)
    for text, search in LOF:
        for i in range(body_start, len(texts)):
            if norm(search) in texts[i]:
                out['lof:' + text] = i + 1
                break
        else:
            raise SystemExit('caption not found: ' + search)
    return out


if __name__ == '__main__':
    build({})
    export_pdf()
    pass1 = find_pages()
    build(pass1)
    export_pdf()
    pass2 = find_pages()
    print('page numbers stable between passes:', pass1 == pass2)
    json.dump(pass2, open('report/toc-pages.json', 'w', encoding='utf-8'), indent=1, ensure_ascii=False)
    print('entries:', len(pass2))
