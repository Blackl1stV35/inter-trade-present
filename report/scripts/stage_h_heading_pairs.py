"""Stage H: keep each two-line chapter heading ("Chapter N" / title) and its body on one page.
The title line must not start a new page; the chapter line starts the page and stays with the title.
Run from the repository root:  python -I -X utf8 report/scripts/stage_h_heading_pairs.py
"""
import re

import docx

PATH = 'report/inter-trade-report.docx'
d = docx.Document(PATH)
P = d.paragraphs
n = 0
for i, p in enumerate(P[:-1]):
    nxt = P[i + 1]
    first_is_label = re.fullmatch(r'(Chapter \d+|Appendix [A-Z])', p.text.strip())
    if p.style.name == 'Heading 1' and first_is_label and nxt.style.name == 'Heading 1':
        p.paragraph_format.page_break_before = True
        p.paragraph_format.keep_with_next = True
        nxt.paragraph_format.page_break_before = False
        nxt.paragraph_format.keep_with_next = True
        n += 1
    elif first_is_label and not nxt.text.strip() == '':
        pass
# Appendix C is plain Normal paragraphs: same treatment
for i, p in enumerate(P[:-1]):
    if p.style.name == 'Normal' and re.fullmatch(r'Appendix [A-Z]', p.text.strip()) and P[i + 1].text.strip() == 'Chart Generating Code':
        p.paragraph_format.page_break_before = True
        p.paragraph_format.keep_with_next = True
        P[i + 1].paragraph_format.keep_with_next = True
        n += 1
print('heading pairs fixed:', n)
d.save(PATH)
