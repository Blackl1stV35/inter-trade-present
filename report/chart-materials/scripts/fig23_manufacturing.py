"""Figure 2.3: German manufacturing real GVA and production, 1995 to 2025.

Sample data: de_manufacturing_1995_2025.csv (Eurostat nama_10_a64 real GVA, chain-linked volume, 2020 = 100;
Eurostat sts_inpr_a production index, 2021 = 100). 2023 to 2025 GVA is provisional (Eurostat flag p).
The two panels have different base years and are different indicators.
Set DATA_DIR and OUT_DIR at the top of the script, then run:  python -I -X utf8 <this script>
Output: OUT_DIR/fig23_manufacturing.png (same styling and headline as the report figure)
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
HEADLINE = 'German manufacturing: real GVA and production, 1995 to 2025'
DARK, BLUE, TEAL, AMBER, GREY = '#263444', '#2B5C98', '#167A67', '#B26A00', '#78828C'

years, gva, prod = [], [], []
for r in csv.DictReader(open(os.path.join(DATA_DIR, 'workbook/de_manufacturing_1995_2025.csv'), encoding='utf-8')):
    years.append(int(r['year']))
    gva.append(float(r['real_gva_index_2020_100']))
    prod.append(float(r['production_index_2021_100']))

fig, (top, bottom) = plt.subplots(2, 1, figsize=(12.8, 9.0), dpi=160, sharex=True)
fig.suptitle(HEADLINE, fontsize=24, fontweight='bold', color=DARK, y=0.975)
top.plot(years, gva, color=BLUE, lw=2.8)
top.set_ylabel('Real GVA (2020 = 100)')
top.set_ylim(60, 120)
top.set_yticks(range(60, 121, 10))
bottom.plot(years, prod, color=TEAL, lw=2.8)
bottom.set_ylabel('Production (2021 = 100)')
bottom.set_ylim(60, 120)
bottom.set_yticks(range(60, 121, 10))
bottom.set_xlabel('Year')
bottom.set_xticks(range(1995, 2026, 5))
for ax in (top, bottom):
    ax.axvline(2005, color=AMBER, ls='--', lw=1.4)
    ax.axvline(2023, color=AMBER, ls='--', lw=1.4)
    ax.grid(axis='y', alpha=0.25)
top.text(2005.4, 117, 'ETS launch', color=AMBER)
top.text(2022.6, 117, 'CBAM reporting', color=AMBER, ha='right')
fig.text(0.07, 0.02, 'Source: Eurostat nama_10_a64 and sts_inpr_a. 2023 to 2025 GVA provisional.',
         fontsize=13, color=GREY)
fig.tight_layout(rect=(0, 0.04, 1, 0.93))
fig.savefig(os.path.join(OUT_DIR, 'fig23_manufacturing.png'))
print('wrote fig23; GVA 2025 =', gva[-1], '; production 2025 =', prod[-1])
