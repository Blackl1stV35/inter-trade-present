"""Stage A of the v5 audit edits: text only.

Applies the review points to report/inter-trade-report.docx in place:
  - Section 1.2 keeps Objectives only (no research question); research-register wording removed
  - no reference to the slide presentation (text, citations, references, Appendix C)
  - no "rather than" contrast sentences
  - year intervals written as "2005 to 2012"; em dashes removed from chapter and appendix headings
  - Appendix C removed; Appendix B heading merged; 2017 origin import value corrected to 6,933 kt
Run from the repository root:  python -I -X utf8 report/scripts/stage_a_text.py
"""
import copy
import re

import docx
from docx.oxml.ns import qn

PATH = 'report/inter-trade-report.docx'
d = docx.Document(PATH)
P = d.paragraphs  # indexes below refer to the v4 layout; deletions happen last


def set_text(p, new):
    """Replace a paragraph's text, keeping the first run's formatting (all runs must share it)."""
    runs = p.runs
    key = lambda r: (r.bold, r.italic, r.font.size, r.font.name)
    assert all(key(r) == key(runs[0]) for r in runs), ('mixed formatting', p.text[:60])
    runs[0].text = new
    for r in runs[1:]:
        r._r.getparent().remove(r._r)


def edit(p, pairs):
    old = p.text
    new = old
    for a, b in pairs:
        assert a in new, ('not found', a[:70], '|', old[:70])
        new = new.replace(a, b)
    set_text(p, new)


E = {}  # index -> list of (old, new) pairs applied in order

E[14] = [('This report examines how', 'This report describes how'),
         ('Selected origin-based, energy-cost, emissions-proxy and provisional 2026 indicators connect the analysis to the companion presentation, with their source boundaries identified.',
          'Selected origin-based, energy-cost, emissions-proxy and provisional 2026 indicators are drawn from the sources listed in Section 1.3, with their source boundaries identified.')]
E[53] = [("The report examines mechanisms and evidence relevant to a long-term green manufacturing economy, rather than assuming that a positive net effect has already occurred.",
          "The report describes mechanisms and observed evidence relevant to a long-term green manufacturing economy. It does not assume that a positive net effect has already occurred.")]
E[60] = [('The companion presentation also supplies an origin-based trade compilation, selected electricity-price observations and an ETS-derived emissions-intensity proxy. These indicators are included with their stated periods and definitions. Origin-based imports are attributed to the presentation\'s Destatis compilation, while directly recorded extra-EU flows are reproduced from Eurostat. Appendix C explains which supplementary observations are presentation-reported and which can be independently reproduced from the cited extracts (Sirithienthong et al., 2026; Destatis, n.d.).',
          'Three supplementary indicators come from sources other than the Eurostat and WV Stahl extracts: an origin-based Chapter 72 compilation (Destatis, n.d.), selected SMARD industrial electricity prices (Bundesnetzagentur, 2026) and an ETS-derived emissions-intensity proxy (UBA/DEHSt, 2026). Each is shown with its stated period and definition. Directly recorded extra-EU flows are reproduced from Eurostat (2026c).')]
E[61] = [('For each empirical graph, the report identifies', 'For each graph, the report identifies'),
         ('while a shift of demand or supply requires additional evidence about its determinants.', 'while a shift of demand or supply cannot be read from quantities alone.'),
         (', and Appendix C links selected claims to permissible interpretations.', '.')]
E[64] = [('Allocation is linked to rules and benchmarks rather than an unrestricted reimbursement of every firm\'s emissions.',
          'Allocation is linked to rules and benchmarks, not to an unrestricted reimbursement of every firm\'s emissions.')]
E[65] = [('The system constrains covered emissions rather than setting a quota on tonnes of steel.', 'The system constrains covered emissions; it does not set a quota on tonnes of steel.')]
E[68] = [('Germany applies the EU framework rather than setting an independent national CBAM tariff', 'Germany applies the EU framework and does not set an independent national CBAM tariff')]
E[79] = [('These are the selected milestones shown in the presentation, not import-tax rates.', 'These are selected milestones, not import-tax rates.')]
E[93] = [('EU ETS implements a cap-and-trade system rather than the fixed corrective charge assumed in this illustration.',
          'EU ETS is a cap-and-trade system; the fixed corrective charge in this illustration is a simplification.')]
E[99] = [('rather than treating the illustration\'s arrows as evidence that those exact changes occurred in Germany.',
          '. The illustration\'s arrows are not evidence that those exact changes occurred in Germany.')]
E[115] = [('A different indicator in the presentation is an ETS-derived proxy', 'A different indicator is an ETS-derived proxy'),
          ('The presentation supplies the earlier selected proxy values; their numerator and output boundaries must be retained before extending the series (Sirithienthong et al., 2026, slide 12; UBA/DEHSt, 2026).',
           'The earlier proxy values come from the same UBA/DEHSt and WV Stahl series; their numerator and output boundaries must be retained before extending the series (UBA/DEHSt, 2026).')]
E[116] = [('in the presentation\'s selected post-2013 proxy', 'in the selected post-2013 proxy')]
E[124] = [('The presentation\'s origin-based Chapter 72 compilation records non-EU-origin imports of about 6,935 kt in 2017',
           'The origin-based Chapter 72 compilation (Destatis, n.d.) records non-EU-origin imports of about 6,933 kt in 2017'),
          ('The presentation also reports direct extra-EU imports as 8.1% of all import tonnes in 2024 and 6.1% in 2025.',
           'Direct extra-EU imports were 8.1% of all import tonnes in 2024 and 6.1% in 2025.'),
          ('(Sirithienthong et al., 2026, slides 6 and 8; Destatis, n.d.).', '(Destatis, n.d.; Eurostat, 2026c).')]
E[131] = [('consistent with the presentation\'s wider steel-trade context', 'consistent with the wider steel-trade context')]
E[132] = [("Using the presentation's rounded origin-based import figure", "Using the rounded origin-based import figure"),
          ("This explains the presentation's origin-based-import balance alongside", "This gives the origin-based balance alongside"),
          ('(Sirithienthong et al., 2026, slide 9; Eurostat, 2026c).', '(Destatis, n.d.; Eurostat, 2026c).')]
E[135] = [("These monthly observations reproduce the presentation's rounded direct-trade figures.", "These monthly observations match the rounded direct-trade totals in the Eurostat extract.")]
E[136] = [("Relative to the same months of 2025, the presentation additionally reports a 6.1% increase in origin-based imports",
           "Relative to the same months of 2025, the origin-based series shows a 6.1% increase in imports"),
          ('These are presentation-reported provisional observations', 'These are provisional observations'),
          ('(Sirithienthong et al., 2026, slides 6 and 9).', '(Destatis, n.d.; Eurostat, 2026c).')]
E[137] = [("The presentation's supplementary electricity-price series is", "The SMARD industrial electricity-price series is"),
          ('it reports 17.3 ct/kWh', 'it shows 17.3 ct/kWh'),
          ('This provides the energy-cost context used in the slides.', 'This provides the energy-cost context for this section.'),
          ('Because the presentation does not fully specify the consumption band, contract population and tax treatment, these figures are attributed to that compilation rather than treated as a verified price paid by every steel plant.',
           'Because SMARD does not state the consumption band, contract population or tax treatment, these figures are attributed to SMARD (Bundesnetzagentur, 2026) rather than treated as a verified price paid by every steel plant.'),
          ('(Sirithienthong et al., 2026, slide 6).', '')]
E[149] = [('rather than an assertion that none occurred.', '. The evidence does not show that none occurred.')]
E[151] = [("The presentation's broader supplier network also includes", "The wider supplier set also includes")]
E[167] = [('Earlier research offers separate evidence about ETS.', 'Earlier studies offer separate evidence about ETS.'),
          ('It is external research on earlier ETS phases, not this report\'s own regression, a Germany-only steel estimate or evidence about CBAM\'s 2026 effects (OECD, 2023).',
           'It concerns earlier ETS phases. It is not a regression estimated in this report, a Germany-only steel estimate or evidence about CBAM\'s 2026 effects (OECD, 2023).')]
E[168] = [('consistent with a transition under pressure rather than a completed policy success or failure.', 'consistent with a transition under pressure, not a completed policy success or failure.')]
E[169] = [('Some supplementary origin, electricity and early intensity observations are attributed to the presentation compilation, as detailed in Appendix C.',
           'Some supplementary origin, electricity and early intensity observations come from the sources named in Section 1.3.')]
E[173] = [('The origin-based import decline reported in the presentation is smaller,', 'The origin-based import decline is smaller,')]
E[179] = [('Support should reward additional outcomes rather than expenditure that would have occurred anyway.', 'Support should reward additional outcomes, not expenditure that would have occurred anyway.')]
E[186] = [('examine local conditions rather than inferring them from a national average.', 'examine local conditions and not infer them from a national average.')]
E[187] = [("This makes the presentation's recommendation to retain carbon receipts", 'This makes the recommendation to retain carbon receipts')]
E[192] = [('These are monitoring triggers rather than outcomes already demonstrated.', 'These are monitoring triggers, not outcomes already demonstrated.')]
E[20] = [('1.2 Objectives and research question', '1.2 Objectives')]
E[54] = [('1.2 Objectives and research question', '1.2 Objectives')]

for idx, pairs in E.items():
    edit(P[idx], pairs)

# 1.2: the research question paragraph goes; the objectives sentence stays
set_text(P[55], 'The objectives are to explain the two policies, describe production and trade developments, compare theoretical mechanisms with observed indicators, and propose practical conditions for future implementation.')
edit(P[56], [('clearly identifies whole-economy context or missing evidence elsewhere.', 'clearly labels whole-economy context or data gaps elsewhere.')])

# chapter and appendix headings: two centred lines, "Chapter 1" then the title (style of the approved sample)
from docx.enum.text import WD_ALIGN_PARAGRAPH


def two_line_heading(p, label, title):
    """Set p to the label and insert a bold centred title line after it, both centred."""
    assert '—' in p.text or p.text.strip() in (label, 'Appendix B'), (p.text[:40])
    set_text(p, label)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    t_el = copy.deepcopy(p._p)
    p._p.addnext(t_el)
    tp = docx.text.paragraph.Paragraph(t_el, p._parent)
    set_text(tp, title)
    tp.alignment = WD_ALIGN_PARAGRAPH.CENTER
    return tp


two_line_heading(P[49], 'Chapter 1', 'Introduction and Details of the Policy')
two_line_heading(P[85], 'Chapter 2', 'Economic Evidence and Discussion')
two_line_heading(P[170], 'Chapter 3', 'Conclusion and Suggestions')
two_line_heading(P[239], 'Appendix A', 'Manufacturing Data')
set_text(P[245], 'Appendix B')
P[245].alignment = WD_ALIGN_PARAGRAPH.CENTER
assert P[246].text.startswith('Matched Trade Data')
P[246].alignment = WD_ALIGN_PARAGRAPH.CENTER

# new SMARD reference, inserted after the BMW reference (alphabetical order)
bmw = P[196]
assert bmw.text.startswith('BMW Group.')
new_ref = copy.deepcopy(bmw._p)
bmw._p.addnext(new_ref)
new_ref_p = docx.text.paragraph.Paragraph(new_ref, bmw._parent)
set_text(new_ref_p, 'Bundesnetzagentur. (2026). SMARD industrial electricity prices: data series behind the electricity-price observations [Data set]. Retrieved October 22, 2026.')

# Appendix C and the presentation-draft reference go
ref_presentation = P[230]
assert ref_presentation.text.startswith('Sirithienthong')
ref_presentation._p.getparent().remove(ref_presentation._p)
toc_c = P[41]
assert toc_c.text.startswith('Appendix C')
toc_c._p.getparent().remove(toc_c._p)

start = P[253]
assert start.text.startswith('Appendix C')
body = d.element.body
tbl_c = [t for t in d.tables if t.rows[0].cells[0].text.startswith('Claim or question')]
assert len(tbl_c) == 1
tbl_c[0]._tbl.getparent().remove(tbl_c[0]._tbl)
remove = False
for p in list(d.paragraphs):
    if p._p is start._p:
        remove = True
    if remove:
        p._p.getparent().remove(p._p)


# year intervals: "2005–2012" becomes "2005 to 2012" (runs keep their formatting)
year = re.compile(r'(\d{4})–(\d{4})')
def fix_runs(par):
    for r in par.runs:
        if '–' in r.text:
            r.text = year.sub(r'\1 to \2', r.text).replace('2026a–d', '2026a to d')

for par in d.paragraphs:
    fix_runs(par)
for t in d.tables:
    for row in t.rows:
        for cell in row.cells:
            for par in cell.paragraphs:
                fix_runs(par)

d.save(PATH)

left = [p.text[:80] for p in docx.Document(PATH).paragraphs if re.search(r'presentation|slide|companion|Sirithienthong|rather than|Appendix C|research question|—', p.text)]
print('paragraphs with leftover terms:', left)
print('saved', PATH)
