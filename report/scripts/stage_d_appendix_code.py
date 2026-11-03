"""Stage D: drop the KU logo placeholder and add Appendix C (chart generating code) to report v5.
The code listings are copied from report/chart-materials/scripts/ so the report and the repository match.
Run from the repository root:  python -I -X utf8 report/scripts/stage_d_appendix_code.py
"""
import copy

import docx
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Pt, RGBColor

PATH = 'report/inter-trade-report.docx'
SCRIPTS = 'report/chart-materials/scripts/'
LISTINGS = [
    ('Figure 2.1: negative production externality', 'report/chart-materials/gnuplot/fig21_externality.gp'),
    ('Figure 2.2: carbon-related import cost', 'report/chart-materials/gnuplot/fig22_import_cost.gp'),
    ('Figure 2.3: German manufacturing real GVA and production', 'report/chart-materials/gnuplot/fig23_manufacturing.gp'),
    ('Figure 2.4: crude steel and rolled market supply', 'report/chart-materials/gnuplot/fig24_steel_output_supply.gp'),
    ('Figure 2.5: direct extra-EU Chapter 72 exports and imports', 'report/chart-materials/gnuplot/fig25_direct_trade_volume.gp'),
    ('Figure 2.6: Chapter 72 trade values and import unit value', 'report/chart-materials/gnuplot/fig26_trade_unit_value.gp'),
    ('Rendering all six figures', 'report/chart-materials/gnuplot/render_all.ps1'),
]
d = docx.Document(PATH)

# 1. drop the logo placeholder
for p in list(d.paragraphs):
    if p.text.startswith('[Kasetsart University logo'):
        p._p.getparent().remove(p._p)


def para(text, size=10, bold=False, font='Courier New', center=False, page_break=False, color=None, space_after=0):
    p = d.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    p.paragraph_format.page_break_before = page_break
    if center:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(text)
    r.font.name = font
    r.font.size = Pt(size)
    r.bold = bold
    if color:
        r.font.color.rgb = RGBColor(*color)
    return p


# 1b. remove an earlier Appendix C so the script can be re-run
start = next((p for p in d.paragraphs if p.text.strip() == 'Appendix C'), None)
if start is not None:
    kids = list(d.element.body)
    for el in kids[kids.index(start._p):]:
        if el.tag != qn('w:sectPr'):
            d.element.body.remove(el)

# 2. Appendix C heading in the same two-line style as the other appendices
para('Appendix C', size=14, bold=True, font='Times New Roman', center=True, page_break=True)
para('Chart Generating Code', size=14, bold=True, font='Times New Roman', center=True, space_after=10)
para('The code below produces the figures of Chapter 2. Each script reads its sample data and writes its PNG to the output folder named at the top of the script. '
     'All six figures are drawn with GNUplot 6.0.5 in Times New Roman, the serif font of the report.',
     size=11, font='Times New Roman', space_after=8)

# 3. one listing per figure, monospace, light grey panel
for title, fname in LISTINGS:
    para(title, size=11, bold=True, font='Times New Roman', space_after=3)
    code = open(fname, encoding='utf-8').read().rstrip('\n').split('\n')
    for line in code:
        p = para(line if line else ' ', size=8)
        pPr = p._p.get_or_add_pPr()
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), 'F4F5F7')
        pPr.append(shd)
    para('', size=6)

d.save(PATH)
print('Appendix C added; logo placeholder removed')
