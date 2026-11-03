"""Figure 2.4: German crude-steel production and rolled-steel market supply, 2012 to 2025.

Sources: crude steel from data/steel_route/chart_data_cleaner_steel_indicators.csv (WV Stahl, latest revision);
market supply of rolled steel from data/german_sources/wv_stahl/marktversorgung_walzstahl_by_edition_2010_2025.csv,
using the latest edition available for each year.
The two series are different product measures and must not be subtracted.
Run from the repository root:  python -I -X utf8 report/chart-materials/scripts/fig24_steel_output_supply.py
Output: report/chart-materials/figures-rebuilt/fig24_steel_output_supply.png
"""
import csv
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'], 'font.size': 14})
OUT = 'report/chart-materials/figures-rebuilt'
os.makedirs(OUT, exist_ok=True)
YEARS = range(2012, 2026)

crude = {}
for r in csv.DictReader(open('data/steel_route/chart_data_cleaner_steel_indicators.csv', encoding='utf-8')):
    if r['crude_steel_Mt'] and int(r['year']) in YEARS:
        crude[int(r['year'])] = float(r['crude_steel_Mt'])

market = {}
edition_rank = {}
for r in csv.DictReader(open('data/german_sources/wv_stahl/marktversorgung_walzstahl_by_edition_2010_2025.csv', encoding='utf-8')):
    y = int(r['year'])
    if y in YEARS and r['market_supply_rolled_steel_mt']:
        rank = r['edition'][:4]  # latest edition year wins
        if y not in edition_rank or rank > edition_rank[y]:
            edition_rank[y] = rank
            market[y] = float(r['market_supply_rolled_steel_mt'])

fig, (top, bottom) = plt.subplots(2, 1, figsize=(12.8, 8.0), dpi=150, sharex=True)
top.plot(list(YEARS), [crude[y] for y in YEARS], color='#2B5C98', marker='o', ms=4, lw=2.2)
top.set_ylabel('Crude steel (Mt)')
top.axvline(2023, color='#B26A00', ls='--', lw=1.2)
top.text(2025, crude[2025], f'  {crude[2025]:.1f}', color='#2B5C98', va='center')
top.grid(alpha=0.25)
bottom.plot(list(YEARS), [market[y] for y in YEARS], color='#167A67', marker='o', ms=4, lw=2.2)
bottom.set_ylabel('Rolled market supply (Mt)')
bottom.axvline(2023, color='#B26A00', ls='--', lw=1.2)
bottom.text(2025, market[2025], f'  {market[2025]:.1f}', color='#167A67', va='center')
bottom.set_xlabel('Year')
bottom.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(os.path.join(OUT, 'fig24_steel_output_supply.png'))
print('wrote fig24; crude 2025 =', crude[2025], '; market 2025 =', market[2025])
