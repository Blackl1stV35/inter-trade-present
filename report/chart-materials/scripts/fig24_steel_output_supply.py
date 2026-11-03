"""Figure 2.4: German crude-steel production and rolled-steel market supply, 2012 to 2025.

Sources: crude steel from data/steel_route/chart_data_cleaner_steel_indicators.csv (WV Stahl, 2025 value set to the
first estimate of 34.1 Mt used in the report text; the later revision of 34.3 Mt is noted in the outline);
market supply of rolled steel from data/german_sources/wv_stahl/marktversorgung_walzstahl_by_edition_2010_2025.csv,
using the latest edition available for each year.
The two series are different product measures and must not be subtracted.
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
HEADLINE = 'German crude-steel output and rolled-steel market supply, 2012 to 2025'
DARK, BLUE, TEAL, AMBER = '#263444', '#2B5C98', '#167A67', '#B26A00'
YEARS = list(range(2012, 2026))
FIRST_ESTIMATE_2025 = 34.1  # value used in the report text

crude = {}
for r in csv.DictReader(open(os.path.join(DATA_DIR, 'steel_route/chart_data_cleaner_steel_indicators.csv'), encoding='utf-8')):
    if r['crude_steel_Mt'] and int(r['year']) in YEARS:
        crude[int(r['year'])] = float(r['crude_steel_Mt'])
crude[2025] = FIRST_ESTIMATE_2025

market, rank = {}, {}
for r in csv.DictReader(open(os.path.join(DATA_DIR, 'german_sources/wv_stahl/marktversorgung_walzstahl_by_edition_2010_2025.csv'), encoding='utf-8')):
    y = int(r['year'])
    if y in YEARS and r['market_supply_rolled_steel_mt']:
        if y not in rank or r['edition'][:4] > rank[y]:
            rank[y] = r['edition'][:4]
            market[y] = float(r['market_supply_rolled_steel_mt'])

fig, (top, bottom) = plt.subplots(2, 1, figsize=(12.8, 7.2), dpi=160, sharex=True)
fig.suptitle(HEADLINE, fontsize=24, fontweight='bold', color=DARK, y=0.975)
top.plot(YEARS, [crude[y] for y in YEARS], color=BLUE, lw=2.8)
top.set_ylabel('Crude steel (Mt)')
top.set_ylim(20, 46)
top.set_yticks(range(25, 46, 5))
top.axvline(2023, color=AMBER, ls='--', lw=1.4)
top.text(2024.6, crude[2025] + 1.3, f'{crude[2025]:.1f}', color=BLUE)
bottom.plot(YEARS, [market[y] for y in YEARS], color=TEAL, lw=2.8)
bottom.set_ylabel('Rolled market supply (Mt)')
bottom.set_ylim(20, 46)
bottom.set_yticks(range(20, 46, 5))
bottom.axvline(2023, color=AMBER, ls='--', lw=1.4)
bottom.text(2024.6, market[2025] + 1.3, f'{market[2025]:.1f}', color=TEAL)
bottom.set_xticks([2012, 2015, 2017, 2020, 2023, 2025])
bottom.set_xlabel('Year')
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(os.path.join(OUT_DIR, 'fig24_steel_output_supply.png'))
print('wrote fig24; crude 2025 =', crude[2025], '; market 2025 =', market[2025])
