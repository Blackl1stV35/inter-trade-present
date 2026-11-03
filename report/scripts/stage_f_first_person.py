"""Stage F: first-person wording (we, our) for the report's own claims, on the user-edited v11 base (KU logo already placed).
Run from the repository root:  python -I -X utf8 report/scripts/stage_f_first_person.py
"""
import docx

PATH = 'report/inter-trade-report.docx'
d = docx.Document(PATH)
P = d.paragraphs
PAIRS = [
    ('This report describes how', 'In this report, we describe how'),
    ('It explains policy design', 'We explain policy design'),
    ('It recommends retaining', 'We recommend retaining'),
    ('The evidence shows adjustment pressures', 'Our evidence shows adjustment pressures'),
    ('The report describes mechanisms and observed evidence', 'We describe mechanisms and observed evidence'),
    ('It does not assume that a positive net effect', 'We do not assume that a positive net effect'),
    ('The objectives are to explain', 'Our objectives are to explain'),
    ('The report addresses exports', 'We address exports'),
    ('It uses steel-specific observations', 'We use steel-specific observations'),
    ('It does not treat a national indicator', 'We do not treat a national indicator'),
    ('The analysis is descriptive.', 'Our analysis is descriptive.'),
    ('It does not establish that reducing German steel output', 'We do not establish that reducing German steel output'),
    ('It also does not prove that ETS', 'We also do not prove that ETS'),
    ('It would therefore be incorrect to describe', 'We therefore consider it incorrect to describe'),
    ('The report therefore does not interpret', 'We therefore do not interpret'),
    ('The report therefore does not claim that all low-carbon', 'We therefore do not claim that all low-carbon'),
    ('The report therefore discusses fiscal channels', 'We therefore discuss fiscal channels'),
    ('The evidence supports three findings.', 'We draw three findings from the evidence.'),
    ('The report supports the proposed slower', 'We support the proposed slower'),
    ('The evidence here supports conditional', 'Our evidence supports conditional'),
    ('The evidence does not show that none occurred.', 'We do not find evidence that none occurred.'),
]
done = set()
for p in P:
    text = p.text
    new = text
    for a, b in PAIRS:
        if a in new:
            new = new.replace(a, b)
            done.add(a)
    if new != text:
        runs = p.runs
        key = lambda r: (r.bold, r.italic, r.font.size, r.font.name)
        assert all(key(r) == key(runs[0]) for r in runs), ('mixed formatting', text[:50])
        runs[0].text = new
        for r in runs[1:]:
            r._r.getparent().remove(r._r)
missing = [a for a, _ in PAIRS if a not in done]
print('not found:', missing)
d.save(PATH)
print('saved')
