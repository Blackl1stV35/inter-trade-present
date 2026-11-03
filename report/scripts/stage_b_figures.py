"""Stage B: figure clean-up for report v5.
For each embedded figure: erase the in-chart note (THEORETICAL ILLUSTRATION footers and two analyst notes),
add a headline above the plot, keep the rest of the figure unchanged, and update the inline size in the docx.
Source images are the six figures in the v4 docx (report/media-v4/); outputs replace the media in the docx.
Run from the repository root:  python -I -X utf8 report/scripts/stage_b_figures.py
"""
import io
import os

import docx
import numpy as np
from docx.oxml.ns import qn
from PIL import Image, ImageDraw, ImageFont

PATH = 'report/inter-trade-report.docx'
SRC = 'report/media-v4'
FONT = ImageFont.truetype('C:/Windows/Fonts/timesbd.ttf', 60)
WHITE = (255, 255, 255)

# (media name in docx, erase boxes (x0,y0,x1,y1) in source pixels, headline)
FIGS = {
    'image3.png': ([(0, 1098, 2048, 1140)], 'Negative production externality: private and social marginal cost (illustrative)'),
    'image4.png': ([(0, 1116, 2048, 1160)], 'Carbon-related import cost with partial pass-through (illustrative)'),
    'image2.png': ([], 'German manufacturing: real GVA and production, 1995 to 2025'),
    'image1.png': ([(250, 122, 1175, 152)], 'German crude-steel output and rolled-steel market supply, 2012 to 2025'),
    'image5.png': ([], 'Direct extra-EU Chapter 72 exports and imports, 1999 to 2025'),
    'image6.png': ([(262, 650, 1262, 728)], 'Chapter 72 trade values and import unit value, 2017 to 2025'),
}
BAND = 130  # height of the headline band added above the plot


def process(name, erase, headline):
    im = Image.open(os.path.join(SRC, name)).convert('RGB')
    arr = im
    for x0, y0, x1, y1 in erase:
        ImageDraw.Draw(arr).rectangle([x0, y0, x1, y1], fill=WHITE)
    w, h = arr.size
    out = Image.new('RGB', (w, h + BAND), WHITE)
    out.paste(arr, (0, BAND))
    draw = ImageDraw.Draw(out)
    tw = draw.textlength(headline, font=FONT)
    draw.text(((w - tw) / 2, 30), headline, font=FONT, fill=(38, 52, 68))
    buf = io.BytesIO()
    out.save(buf, format='PNG', optimize=True)
    return buf.getvalue(), out.size


d = docx.Document(PATH)
rels = d.part.rels
sizes = {}
for name, (erase, headline) in FIGS.items():
    blob, size = process(name, erase, headline)
    sizes[name] = size
    for rel in rels.values():
        if rel.reltype.endswith('/image') and os.path.basename(rel.target_ref) == name:
            rel.target_part._blob = blob
            print('updated', name, size)

# keep each picture's width; scale the height to the new aspect ratio
W_EMU = {}
for blip in d.element.body.iter(qn('a:blip')):
    rid = blip.get(qn('r:embed'))
    target = os.path.basename(rels[rid].target_ref)
    if target not in sizes:
        continue
    inline = blip
    while inline is not None and inline.tag != qn('wp:inline'):
        inline = inline.getparent()
    ext = inline.find(qn('wp:extent'))
    cx, cy = int(ext.get('cx')), int(ext.get('cy'))
    w, h = sizes[target]
    new_cy = int(round(cx * h / w))
    ext.set('cy', str(new_cy))
    for a_ext in inline.iter(qn('a:ext')):
        if a_ext.get('cy') is not None:
            a_ext.set('cy', str(new_cy))
    print(target, 'height EMU', cy, '->', new_cy)
d.save(PATH)
print('saved')
