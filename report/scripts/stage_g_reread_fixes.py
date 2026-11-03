"""Stage G: fixes from the full re-read of report v12.
Run from the repository root:  python -I -X utf8 report/scripts/stage_g_reread_fixes.py
"""
import copy

import docx
from docx.oxml.ns import qn

PATH = 'report/inter-trade-report.docx'
d = docx.Document(PATH)
PAIRS = [
    ('We explain policy design and relates', 'We explain policy design and relate'),
    ('but the report does not establish a net German GDP', 'but we do not establish a net German GDP'),
    ('We use steel-specific observations where available and clearly labels', 'We use steel-specific observations where available and clearly label'),
    ('used to assess real developments, . The illustration', 'used to assess real developments. The illustration'),
    ('Crucially, the announcement schedules', 'The announcement schedules'),
    ('deliveries to those customers are not verified in the cited evidence, . We do not find', 'deliveries to those customers are not verified in the cited evidence. We do not find'),
]
changed = []
for p in d.paragraphs:
    text = p.text
    new = text
    for a, b in PAIRS:
        if a in new:
            new = new.replace(a, b)
            changed.append(a[:40])
    if new != text:
        runs = p.runs
        if len(runs) == 0 or len(p._p.findall(qn('w:hyperlink'))) == 0:
            runs[0].text = new
            for r in runs[1:]:
                r._r.getparent().remove(r._r)
        else:
            raise SystemExit('hyperlink paragraph needs manual handling: ' + text[:60])
print('changed:', len(changed), 'of', len(PAIRS))

# reference: the SMARD entry was copied from the BMW paragraph with its hyperlink; rebuild it as a plain entry
for p in d.paragraphs:
    if p.text.startswith('BMW Group. (2021, October 20). BMW Group secures') and 'Bundesnetzagentur' in p.text:
        for child in list(p._p):
            if child.tag != qn('w:pPr'):
                p._p.remove(child)
        r = p.add_run('Bundesnetzagentur. (2026). SMARD industrial electricity prices: data series behind the electricity-price observations [Data set]. Retrieved October 22, 2026.')
        print('reference fixed')
        break
d.save(PATH)
