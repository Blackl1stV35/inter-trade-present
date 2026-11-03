"""Figure 2.6: direct extra-EU Chapter 72 nominal trade values and import unit value, 2017 to 2025.

Sources: Eurostat Comext DS-045409 (reporter DE, partner EXT_EU27_2020, HS Chapter 72, nominal EUR).
Values from data/comext_exports/slide_table_2017_2025.csv (extra-EU Chapter 72 trade, EUR million);
unit value (EUR per net tonne) from data/comext_exports/ch72_extra_eu_imports_1999_2025.csv.
Unit value is total import euros divided by net tonnes; it reflects product mix and is not a fixed-product price index.
Run from the repository root:  python -I -X utf8 report/chart-materials/scripts/fig26_trade_unit_value.py
Output: report/chart-materials/figures-rebuilt/fig26_trade_unit_value.png
"""
import csv
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'], 'font.size': 14})
OUT = 'report/chart-materials/figures-rebuilt'
os.makedirs(OUT, exist_ok=True)
YEARS = range(2017, 2026)

exports, imports = {}, {}
for r in csv.DictReader(open('data/comext_exports/slide_table_2017_2025.csv', encoding='utf-8')):
    y = int(r['year'])
    if y in YEARS:
        exports[y] = float(r['extra_eu_ch72_exports_eur_m']) / 1000
        imports[y] = float(r['extra_eu_ch72_imports_eur_m']) / 1000

unit = {}
for r in csv.DictReader(open('data/comext_exports/ch72_extra_eu_imports_1999_2025.csv', encoding='utf-8')):
    y = int(r['year'])
    if y in YEARS:
        unit[y] = float(r['unit_value_eur_per_t'])

fig, (top, bottom) = plt.subplots(2, 1, figsize=(12.8, 8.0), dpi=150, sharex=True)
top.plot(list(YEARS), [exports[y] for y in YEARS], color='#2B5C98', lw=2.2, label='Exports')
top.plot(list(YEARS), [imports[y] for y in YEARS], color='#167A67', lw=2.2, label='Imports')
top.set_ylabel('Trade value (EUR billion)')
top.axvline(2023, color='#B26A00', ls='--', lw=1.2)
top.legend(loc='upper left', frameon=False)
top.grid(alpha=0.25)
bottom.plot(list(YEARS), [unit[y] for y in YEARS], color='#167A67', marker='o', lw=2.2)
bottom.set_ylabel('Import unit value (EUR/t)')
bottom.axvline(2023, color='#B26A00', ls='--', lw=1.2)
bottom.set_xlabel('Year')
bottom.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(os.path.join(OUT, 'fig26_trade_unit_value.png'))
print('wrote fig26; 2025 exports EUR bn =', round(exports[2025], 3), 'imports =', round(imports[2025], 3), 'unit =', unit[2025])
