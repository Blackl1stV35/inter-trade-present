"""Stage E: put the KU logo and the six GNUplot figures into the report, matched by position in the document
(cover logo first, then Figures 2.1 to 2.9 in order), so renumbered media parts cannot swap pictures.
Each picture keeps its width; height follows the image's aspect ratio.
Run from the repository root:  python -I -X utf8 report/scripts/stage_e_rebuilt_figures.py
"""
import io
import os

import docx
from docx.oxml.ns import qn
from PIL import Image

PATH = 'report/inter-trade-report.docx'
FIG = 'report/chart-materials/figures-gnuplot'
ORDER = ['report/assets/ku-logo.png'] + [f'{FIG}/{n}' for n in (
    'fig21_externality.png', 'fig22_import_cost.png', 'fig23_manufacturing.png',
    'fig24_steel_output_supply.png', 'fig25_direct_trade_volume.png', 'fig26_trade_unit_value.png',
    'fig27_bop_partner_balance.png', 'fig28_eu_export_destinations.png', 'fig29_gdp_timeline.png')]

d = docx.Document(PATH)
blips = list(d.element.body.iter(qn('a:blip')))
assert len(blips) == len(ORDER), f'expected {len(ORDER)} pictures, found {len(blips)}'
for blip, src in zip(blips, ORDER):
    data = open(src, 'rb').read()
    d.part.rels[blip.get(qn('r:embed'))].target_part._blob = data
    w, h = Image.open(io.BytesIO(data)).size
    inline = blip
    while inline is not None and inline.tag not in (qn('wp:inline'), qn('wp:anchor')):
        inline = inline.getparent()
    ext = inline.find(qn('wp:extent'))
    cx = int(ext.get('cx'))
    cy = int(round(cx * h / w))
    ext.set('cy', str(cy))
    for a_ext in inline.iter(qn('a:ext')):
        if a_ext.get('cy') is not None:
            a_ext.set('cy', str(cy))
    print(os.path.basename(src), 'placed', (w, h))
d.save(PATH)
