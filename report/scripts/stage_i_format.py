"""Stage I: report-wide typography. Times New Roman everywhere except the code listings (Courier New, untouched),
12 pt for body text, captions and notes (table cells stay 10 pt, headings keep their sizes), line spacing 1.15 for
everything except the code, and Appendix C's two-line heading as a real Heading 1 like Appendices A and B.
Run from the repository root:  python -I -X utf8 report/scripts/stage_i_format.py
"""
import re

import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt

PATH = 'report/inter-trade-report.docx'
TNR = 'Times New Roman'
d = docx.Document(PATH)


def set_fonts(rpr_owner_rpr):
    rf = rpr_owner_rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr_owner_rpr.insert(0, rf)
    for a in list(rf.attrib):
        del rf.attrib[a]
    for a in ('ascii', 'hAnsi', 'eastAsia', 'cs'):
        rf.set(qn('w:' + a), TNR)


def is_code(p):
    return any(r.font.name == 'Courier New' for r in p.runs)


# styles and document defaults
styles_el = d.styles.element
dd = styles_el.find(qn('w:docDefaults'))
if dd is not None:
    rpr = dd.find(qn('w:rPrDefault') + '/' + qn('w:rPr'))
    if rpr is not None:
        set_fonts(rpr)
for st in d.styles:
    if st.type == 1 and st.name != 'Courier':
        st.font.name = TNR
        rpr = st.element.get_or_add_rPr()
        set_fonts(rpr)

paras = list(d.paragraphs)
for t in d.tables:
    for row in t.rows:
        for cell in row.cells:
            paras.extend(cell.paragraphs)

# Appendix C heading -> Heading 1 pair
body = d.paragraphs
for i, p in enumerate(body[:-1]):
    if p.text.strip() == 'Appendix C' and body[i + 1].text.strip() == 'Chart Generating Code' and p.style.name != 'Heading 1':
        for q in (p, body[i + 1]):
            q.style = d.styles['Heading 1']
            q.alignment = 1
            for r in q.runs:
                r.font.size = Pt(14)
                r.bold = True
        p.paragraph_format.page_break_before = True
        p.paragraph_format.keep_with_next = True
        body[i + 1].paragraph_format.page_break_before = False
        body[i + 1].paragraph_format.keep_with_next = True

in_table = {id(p._p) for t in d.tables for row in t.rows for cell in row.cells for p in cell.paragraphs}
for p in paras:
    if is_code(p):
        continue
    heading = p.style.name.startswith('Heading')
    cover = p.paragraph_format.alignment == 1 and len(p.text) > 0 and p.runs and p.runs[0].font.size and p.runs[0].font.size.pt == 14 and not heading
    for r in p.runs:
        rpr = r._r.get_or_add_rPr()
        set_fonts(rpr)
        if heading or cover or id(p._p) in in_table:
            continue
        if r.font.size is None or r.font.size.pt != 12:
            r.font.size = Pt(12)
    p.paragraph_format.line_spacing = 1.15

# listing titles in Appendix C: bold 12 pt
for p in d.paragraphs:
    if re.match(r'(Figure 2\.\d: |Rendering all six)', p.text) and not is_code(p):
        for r in p.runs:
            r.bold = True
            r.font.size = Pt(12)
d.save(PATH)
print('typography applied')
