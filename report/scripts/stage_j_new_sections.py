"""Stage J (one-shot): add Figures 2.7 to 2.9 and their text to report v5.
  - 2.4.3 (balance of payments): Figure 2.7, Chapter 72 balance by partner group, 1999 to 2025
  - 2.4.5 (new heading): Figure 2.8, exports by destination group, and the comparison of extra-EU and intra-EU prices and volumes
  - 2.6 (GDP): Figure 2.9, real GDP index and annual growth, 1995 to 2025
Run once from the repository root, after the three figures are rendered:
  python -I -X utf8 report/scripts/stage_j_new_sections.py
Not part of build_report.ps1: it inserts content, so it refuses to run twice.
"""
import copy

import docx
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm

PATH = 'report/inter-trade-report.docx'
FIG = 'report/chart-materials/figures-gnuplot'
WIDTH = Cm(15.52)  # the width of the six existing figures

d = docx.Document(PATH)
P = d.paragraphs
assert not any(p.text.startswith('2.4.5 ') for p in P), 'stage J already applied'
assert P[123].text == '' and P[124].text.startswith('Figure 2.5') and P[125].text.startswith('Direct extra-EU')
assert P[137].text.startswith('The balance of payments records') and P[138].text.startswith('2.4.4')
assert P[141].text.startswith('The SMARD') and P[142].text.startswith('2.5 ')
assert P[160].text.startswith('GDP = C') and P[161].text.startswith('Table 2.1')

PIC, CAP, BODY, H3 = P[123], P[124], P[125], P[138]   # templates: picture, italic caption, justified text, Heading 3


def clone(template, text):
    """A copy of the template paragraph (paragraph format and first-run format kept) holding only the given text."""
    el = copy.deepcopy(template._p)
    runs = el.findall(qn('w:r'))
    for r in runs[1:]:
        el.remove(r)
    for child in list(runs[0]):
        if child.tag != qn('w:rPr'):
            runs[0].remove(child)
    t = OxmlElement('w:t')
    t.set(qn('xml:space'), 'preserve')
    t.text = text
    runs[0].append(t)
    return docx.text.paragraph.Paragraph(el, template._parent)


def picture(path):
    el = copy.deepcopy(PIC._p)
    for child in list(el):
        if child.tag != qn('w:pPr'):
            el.remove(child)
    para = docx.text.paragraph.Paragraph(el, PIC._parent)
    para.add_run().add_picture(path, width=WIDTH)
    return para


def insert_after(anchor, items):
    for item in items:
        anchor._p.addnext(item._p)
        anchor = item
    return anchor


# ---- 2.4.3: Figure 2.7 (balance of payments, partner groups)
bop = [
    clone(BODY, 'Figure 2.7 places the all-partner balance beside its two partner groups. It uses the Comext extract behind '
                'Figures 2.5 and 2.6, with values in euros. The extra-EU balance is the value of exports to non-EU partners less '
                'imports recorded by origin. The intra-EU balance is the value of exports to other Member States less imports '
                'recorded by consignment. The all-partner balance is the sum of the two groups.'),
    picture(f'{FIG}/fig27_bop_partner_balance.png'),
    clone(CAP, 'Figure 2.7  Germany: Chapter 72 trade balance by partner group, 1999 to 2025 (value, EUR billion). Source: '
               'Eurostat (2026c), DS-045409. The two groups use different import recording rules, so the series is not the '
               'national-accounts trade balance.'),
    clone(BODY, 'The extra-EU balance was positive in every year from 1999 to 2025. It rose from EUR 1.6 billion in 1999 to '
                'EUR 4.5 billion in 2022 and was EUR 3.8 billion in 2025. The intra-EU balance was negative in 26 of the 27 years, '
                'reaching a deficit of EUR 6.4 billion in 2018 and narrowing to EUR 1.7 billion in 2025. The all-partner balance was '
                'negative in 12 years, including 2007, 2008 and 2011 and each year from 2013 to 2019. It was positive in 2023 to '
                '2025, reaching EUR 2.5 billion in 2024 and EUR 2.2 billion in 2025.'),
    clone(BODY, 'These are product-group goods balances. They are not the balance of payments, which also records services and '
                'income, and they are not the whole-economy trade balance used in the GDP identity in Section 2.6. The values are '
                'nominal, so price changes contribute to them alongside volume changes. The extra-EU balance is the part of this '
                'product balance recorded against non-EU partners. The intra-EU balance is recorded against other Member States.'),
]
insert_after(P[137], bop)

# ---- 2.4.5: external effects of EU policy on exports by destination (new subsection, before Section 2.5)
eu = [
    clone(H3, '2.4.5 External effects of EU policy: export prices and volumes by destination'),
    clone(BODY, 'This subsection asks whether EU climate policy has raised the price of German steel sold to non-EU markets, and '
                'whether those markets now take less of it. The EU ETS charges emissions from production in the EU, whatever the '
                'destination of the steel, so allowance costs enter the prices of exports to both groups of partners. The CBAM '
                'applies to imports into the EU and not to exports from it. A comparison of extra-EU and intra-EU destinations '
                'therefore tests whether non-EU buyers respond differently from EU buyers. It is a descriptive comparison and not '
                'an estimate of the policy effect.'),
    clone(BODY, 'Figure 2.8 compares the Chapter 72 exports of Germany to the two destination groups from 1999. The series starts '
                'six years before the ETS launch, so the years 1999 to 2004 give a pre-policy reference, although the partner '
                'groups and the economic cycle change over the period. Panel A indexes export tonnes to 1999 = 100. Panel B shows '
                'the nominal unit value.'),
    picture(f'{FIG}/fig28_eu_export_destinations.png'),
    clone(CAP, 'Figure 2.8  Germany: Chapter 72 exports by destination group, 1999 to 2025. Panel A: net mass index (1999 = 100). '
               'Panel B: nominal unit value (EUR per tonne). Source: Eurostat (2026c), DS-045409. Unit value is export value '
               'divided by net mass for each group. It is not a fixed-product price index.'),
    clone(BODY, 'Extra-EU export tonnes fell from 8.3 million in 2012 to 4.7 million in 2025, a fall of 43%. Intra-EU export tonnes '
                'stayed between 23.6 and 26.3 million in every year from 2012 to 2025, and were 24.5 million in 2025. The extra-EU '
                'share of export tonnes averaged 22.7% over 2005 to 2008 and 17.5% over 2020 to 2025, and it was 16.0% in 2025.'),
    clone(BODY, 'Nominal unit values rose for both groups after 2004 and again in 2021 and 2022, so the general price movement is '
                'common to both destinations. The ratio of the extra-EU to the intra-EU unit value stayed between 1.2 and 1.5 in '
                'every year. It averaged about 1.3 in each period from 1999 to 2025, and it was 1.36 in 2025. The data therefore '
                'show no widening of the price premium for exports to non-EU markets after the ETS launch. Unit values include '
                'product mix, so this is a weak test of price pass-through.'),
    clone(BODY, 'The fall in extra-EU tonnes is larger than the change in intra-EU tonnes since 2012, which is consistent with '
                'weaker sales to non-EU markets. The largest one-year fall in the series came between 2012 and 2013, when the third '
                'ETS phase began. That timing is consistent with a policy effect, but the same years also include changes in demand '
                'and import competition that these data do not measure. The later falls during the 2020 pandemic and in 2022 show '
                'that other events also shape both groups.'),
    clone(BODY, 'We therefore answer the two questions only in part. Unit values for steel sold to non-EU markets have risen since '
                '2004, in step with unit values for intra-EU sales. Tonnes sold to non-EU markets have fallen relative to intra-EU '
                'tonnes since 2012, and that difference is the clearest pattern. Attributing it to the ETS or the CBAM needs a '
                'counterfactual and product-level price data, which this report does not have. The CBAM cannot be assessed from '
                'these series, because it applies to imports into the EU, and its definitive phase starts in 2026, after the last '
                'annual observation.'),
]
insert_after(P[141], eu)

# ---- 2.6: Figure 2.9 (real GDP index and growth, with the policy dates)
gdp = [
    picture(f'{FIG}/fig29_gdp_timeline.png'),
    clone(CAP, 'Figure 2.9  Germany: real GDP index and annual real growth, 1995 to 2025. Source: Eurostat (2026d), nama_10_gdp '
               '(B1GQ, chain-linked 2020 prices). Growth for 2023 to 2025 is provisional. The dashed lines mark the ETS launch '
               '(2005) and the start of CBAM reporting (2023). They mark dates, not causal effects.'),
    clone(BODY, 'Figure 2.9 sets the policy dates beside the economic cycle. Real GDP fell by 5.6% in 2009 and by 4.0% in 2020. It '
                'was 5.1% higher in 2025 than in 2020, after growth of 4.0% in 2021 and 1.9% in 2022. Growth was close to zero in '
                '2023 to 2025, at provisional values of -1.0%, 0.0% and 0.2%. Growth was positive in 17 of the 21 years from 2005 to '
                '2025 and negative only in 2009, 2020 and 2023.'),
    clone(BODY, 'The growth series is national context and not a measure of steel-policy effects, because it covers all sectors '
                'and steel policy affects only part of the economy. The policy dates do not coincide with a visible break in the '
                'aggregate growth path, which is dominated by the 2009 and 2020 shocks.'),
]
insert_after(P[160], gdp)

d.save(PATH)
print('inserted: 2.4.3 (Figure 2.7), 2.4.5 (Figure 2.8), 2.6 (Figure 2.9); pictures now', len(d.inline_shapes))
