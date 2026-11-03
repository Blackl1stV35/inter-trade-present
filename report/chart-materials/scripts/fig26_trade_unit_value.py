"""Figure 2.6: direct extra-EU Chapter 72 nominal trade values and import unit value, 2017 to 2025.

Sources: Eurostat Comext DS-045409 (reporter DE, partner EXT_EU27_2020, HS Chapter 72, nominal EUR).
Values from data/comext_exports/slide_table_2017_2025.csv (extra-EU Chapter 72 trade, EUR million);
unit value (EUR per net tonne) from data/comext_exports/ch72_extra_eu_imports_1999_2025.csv.
Unit value is total import euros divided by net tonnes; it reflects product mix and is not a fixed-product price index.
Set DATA_DIR and OUT_DIR at the top of the script, then run:  python -I -X utf8 <this script>
Output: OUT_DIR/<name>.png (same styling and headline as the report figure)
"""
import csv
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

DATA_DIR = 'data'  # folder with the sample data files named in each script
OUT_DIR = 'figures-rebuilt'  # folder for the PNG output
plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'], 'font.size': 16})
os.makedirs(OUT_DIR, exist_ok=True)
HEADLINE = 'Chapter 72 trade values and import unit value, 2017 to 2025'
DARK, BLUE, TEAL, AMBER = '#263444', '#2B5C98', '#167A67', '#B26A00'
YEARS = list(range(2017, 2026))

exports, imports, unit = {}, {}, {}
for r in csv.DictReader(open(os.path.join(DATA_DIR, 'comext_exports/slide_table_2017_2025.csv'), encoding='utf-8')):
    y = int(r['year'])
    if y in YEARS:
        exports[y] = float(r['extra_eu_ch72_exports_eur_m']) / 1000
        imports[y] = float(r['extra_eu_ch72_imports_eur_m']) / 1000
for r in csv.DictReader(open(os.path.join(DATA_DIR, 'comext_exports/ch72_extra_eu_imports_1999_2025.csv'), encoding='utf-8')):
    y = int(r['year'])
    if y in YEARS:
        unit[y] = float(r['unit_value_eur_per_t'])

fig, (top, bottom) = plt.subplots(2, 1, figsize=(12.8, 7.2), dpi=160, sharex=True)
fig.suptitle(HEADLINE, fontsize=24, fontweight='bold', color=DARK, y=0.975)
top.plot(YEARS, [exports[y] for y in YEARS], color=BLUE, lw=2.8, label='Exports')
top.plot(YEARS, [imports[y] for y in YEARS], color=TEAL, lw=2.8, label='Imports')
top.set_ylabel('Trade value (EUR billion)')
top.set_ylim(0, 9)
top.set_yticks([0, 2, 4, 6, 8])
top.axvline(2023, color=AMBER, ls='--', lw=1.4)
top.legend(loc='upper left', frameon=False)
bottom.plot(YEARS, [unit[y] for y in YEARS], color=TEAL, lw=2.8, marker='o', ms=5)
bottom.set_ylabel('Import unit value (EUR/t)')
bottom.set_ylim(400, 1500)
bottom.set_yticks(range(400, 1401, 200))
bottom.axvline(2023, color=AMBER, ls='--', lw=1.4)
bottom.set_xticks(YEARS)
bottom.set_xlabel('Year')
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(os.path.join(OUT_DIR, 'fig26_trade_unit_value.png'))
print('wrote fig26; 2025 exports EUR bn =', round(exports[2025], 3), 'imports =', round(imports[2025], 3), 'unit =', unit[2025])
