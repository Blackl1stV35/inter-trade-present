"""Figure 2.5: direct extra-EU Chapter 72 exports and imports, 1999 to 2025 (net mass, million tonnes).

Source: Eurostat Comext DS-045409 (reporter DE, partner EXT_EU27_2020, HS Chapter 72, net mass).
Sample data: ch72_extra_eu_exports_1999_2025.csv and ch72_extra_eu_imports_1999_2025.csv (net mass in thousand tonnes, converted to Mt).
Not the CBAM liability base.
Set DATA_DIR and OUT_DIR at the top of the script, then run:  python -I -X utf8 <this script>
Output: OUT_DIR/fig25_direct_trade_volume.png (same styling and headline as the report figure)
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
HEADLINE = 'Direct extra-EU Chapter 72 exports and imports, 1999 to 2025'
DARK, BLUE, TEAL, AMBER = '#263444', '#2B5C98', '#167A67', '#B26A00'


def series(name, column):
    rows = csv.DictReader(open(os.path.join(DATA_DIR, name), encoding='utf-8'))
    return {int(r['year']): float(r[column]) / 1000 for r in rows}  # kt to Mt


exports = series('comext_exports/ch72_extra_eu_exports_1999_2025.csv', 'net_mass_thousand_t')
imports = series('comext_exports/ch72_extra_eu_imports_1999_2025.csv', 'net_mass_thousand_t')
years = sorted(exports)

fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=160)
fig.suptitle(HEADLINE, fontsize=24, fontweight='bold', color=DARK, y=0.975)
ax.plot(years, [exports[y] for y in years], color=BLUE, lw=2.8, label='Exports')
ax.plot(years, [imports[y] for y in years], color=TEAL, lw=2.8, label='Direct extra-EU imports')
ax.axvline(2005, color=AMBER, ls='--', lw=1.4)
ax.axvline(2023, color=AMBER, ls='--', lw=1.4)
ax.annotate(f'{exports[2025]:.3f} Mt', (2025, exports[2025]), (2019.5, 7.7), color=BLUE,
            arrowprops=dict(arrowstyle='-', color=BLUE, lw=1))
ax.annotate(f'{imports[2025]:.3f} Mt', (2025, imports[2025]), (2019.5, imports[2025] - 0.85), color=TEAL,
            arrowprops=dict(arrowstyle='-', color=TEAL, lw=1))
ax.set_xlim(1999, 2025)
ax.set_ylim(0, 9)
ax.set_xticks(range(1999, 2026, 4))
ax.set_xticks(range(1999, 2026), minor=True)
ax.set_ylabel('Net mass (million tonnes)')
ax.set_xlabel('Year')
ax.legend(loc='upper right', frameon=False)
ax.grid(alpha=0.25)
fig.text(0.07, 0.02, 'Source: Eurostat Comext DS-045409. Germany, fixed extra-EU27_2020, HS72. Not the CBAM liability base.',
         fontsize=13, color='#78828C')
fig.tight_layout(rect=(0, 0.04, 1, 0.93))
fig.savefig(os.path.join(OUT_DIR, 'fig25_direct_trade_volume.png'))
print('wrote fig25; 2025 exports Mt =', round(exports[2025], 3), 'imports Mt =', round(imports[2025], 3))
