"""Inspect every visual and the document that carries them. Exit code 1 on any failure.
Checks: each rendered figure has a clean border (nothing clipped at an edge), the report embeds exactly the rendered
PNGs, a contact sheet of all figures is written for viewing, and the report text has no em dash or "rather than".
Run from the repository root:  python -I -X utf8 report/scripts/verify_visuals.py
"""
import hashlib
import sys
import zipfile

from PIL import Image

FIG_DIR = 'report/chart-materials/figures-gnuplot'
DOCX = 'report/inter-trade-report.docx'
FIGS = ['fig21_externality.png', 'fig22_import_cost.png', 'fig23_manufacturing.png', 'fig24_steel_output_supply.png',
        'fig25_direct_trade_volume.png', 'fig26_trade_unit_value.png']
fails = []


def border_clear(path, margin=4):
    im = Image.open(path).convert('L')
    w, h = im.size
    px = im.load()
    for x in range(w):
        for y in list(range(margin)) + list(range(h - margin, h)):
            if px[x, y] < 200:
                return False
    for y in range(h):
        for x in list(range(margin)) + list(range(w - margin, w)):
            if px[x, y] < 200:
                return False
    return True


import docx
from docx.oxml.ns import qn
_d = docx.Document(DOCX)
_pics = [_d.part.rels[b.get(qn('r:embed'))].target_part.blob for b in _d.element.body.iter(qn('a:blip'))]
_h = lambda data: hashlib.sha1(data).hexdigest()
if len(_pics) != 7:
    fails.append(f'report has {len(_pics)} pictures, expected 7 (logo and six figures)')
else:
    if _h(_pics[0]) != _h(open('report/assets/ku-logo.png', 'rb').read()):
        fails.append('cover picture is not the KU logo')
    for fig, blob in zip(FIGS, _pics[1:]):
        path = f'{FIG_DIR}/{fig}'
        if not border_clear(path):
            fails.append(f'{fig}: content touches the image edge (clipped)')
        if _h(blob) != _h(open(path, 'rb').read()):
            fails.append(f'{fig}: report embeds a different image in its place')

sheet = Image.new('RGB', (1500, 3 * 420), 'white')
for i, fig in enumerate(FIGS):
    im = Image.open(f'{FIG_DIR}/{fig}').convert('RGB')
    im.thumbnail((495, 420))
    sheet.paste(im, ((i % 3) * 500, (i // 3) * 420))
sheet.save(f'{FIG_DIR}/contact-sheet.png')

import docx
text = ' '.join(p.text for p in docx.Document(DOCX).paragraphs)
if '—' in text:
    fails.append('report text contains an em dash')
if 'rather than' in text.lower():
    fails.append('report text contains "rather than"')

print('\n'.join(fails) if fails else 'visuals ok: 6 figures clean at the edges, embedded, contact sheet written')
sys.exit(1 if fails else 0)
