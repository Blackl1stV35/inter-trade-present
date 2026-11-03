"""Stage E: put the rebuilt figures (report/chart-materials/figures-rebuilt) into the report.
Replaces the media of Figures 2.1, 2.2, 2.4 and 2.6 and keeps each picture's width (height follows the new aspect ratio).
Run from the repository root:  python -I -X utf8 report/scripts/stage_e_rebuilt_figures.py
"""
import os

import docx
from docx.oxml.ns import qn

PATH = 'report/inter-trade-report.docx'
NEW = 'report/chart-materials/figures-rebuilt'
# media name in the docx -> rebuilt file
MAP = {
    'image3.png': 'fig21_externality.png',    # Figure 2.1
    'image4.png': 'fig22_import_cost.png',    # Figure 2.2
    'image1.png': 'fig24_steel_output_supply.png',  # Figure 2.4
    'image6.png': 'fig26_trade_unit_value.png',     # Figure 2.6
    'image5.png': 'fig25_direct_trade_volume.png',  # Figure 2.5
    'image2.png': 'fig23_manufacturing.png',        # Figure 2.3
}
d = docx.Document(PATH)
sizes = {}
for rel in d.part.rels.values():
    if rel.reltype.endswith('/image'):
        name = os.path.basename(rel.target_ref)
        if name in MAP:
            data = open(os.path.join(NEW, MAP[name]), 'rb').read()
            rel.target_part._blob = data
            from PIL import Image
            import io
            sizes[name] = Image.open(io.BytesIO(data)).size
            print('replaced', name, '->', MAP[name], sizes[name])

rels = d.part.rels
for blip in d.element.body.iter(qn('a:blip')):
    rid = blip.get(qn('r:embed'))
    target = os.path.basename(rels[rid].target_ref)
    if target not in sizes:
        continue
    inline = blip
    while inline is not None and inline.tag != qn('wp:inline'):
        inline = inline.getparent()
    ext = inline.find(qn('wp:extent'))
    cx = int(ext.get('cx'))
    w, h = sizes[target]
    new_cy = int(round(cx * h / w))
    ext.set('cy', str(new_cy))
    for a_ext in inline.iter(qn('a:ext')):
        if a_ext.get('cy') is not None:
            a_ext.set('cy', str(new_cy))
    print(target, 'height set to', new_cy)
d.save(PATH)
print('saved')
