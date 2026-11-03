"""Stage A2: fixes found in the Stage A check (rather-than sentences, a doubled TOC entry).
Run from the repository root:  python -I -X utf8 report/scripts/stage_a2_text.py
"""
import docx

PATH = 'report/inter-trade-report.docx'
d = docx.Document(PATH)
P = d.paragraphs

PAIRS = {
    20: [('1.2 Objectives and research question1.2 Objectives', '1.2 Objectives')],
    51: [('These are shares of GVA rather than GDP.', 'These are shares of GVA, not GDP.')],
    84: [('opportunity cost, rather than treated as a benefit simply because it is large', 'opportunity cost, and not treated as a benefit simply because it is large')],
    138: [('attributed to SMARD (Bundesnetzagentur, 2026) rather than treated as a verified price', 'attributed to SMARD (Bundesnetzagentur, 2026) and not treated as a verified price')],
    155: [('delivered cost rather than a nationality label', 'delivered cost, not a nationality label')],
    163: [('activities rather than steel-sector tax payments', 'activities, not steel-sector tax payments')],
    184: [('as an integrated chain rather than separate headlines.', 'as an integrated chain, not as separate headlines.')],
    186: [('legal status rather than presented as already in force.', 'legal status, and not presented as already in force.')],
}
for idx, pairs in PAIRS.items():
    p = P[idx]
    text = p.text
    for a, b in pairs:
        assert a in text, (idx, a[:50], text[:60])
        text = text.replace(a, b)
    runs = p.runs
    runs[0].text = text
    for r in runs[1:]:
        r._r.getparent().remove(r._r)
d.save(PATH)
left = [i for i, p in enumerate(docx.Document(PATH).paragraphs) if ' rather than ' in p.text]
print('rather than left at paragraphs:', left)
