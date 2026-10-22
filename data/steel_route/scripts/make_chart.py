# make_chart.py: draws chart_proposal_cleaner_steel.png from chart_data_cleaner_steel_indicators.csv (matplotlib).
import csv
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

R = 'D:/Workspace/inter-trade-present/data/steel_route/'
rows = list(csv.DictReader(open(R + 'chart_data_cleaner_steel_indicators.csv', encoding='utf-8')))
cols = list(rows[0].keys())
yr = [int(r['year']) for r in rows]
ele = [float(r[cols[1]]) if r[cols[1]] else None for r in rows]
ets_t = [(int(r['year']), float(r[cols[4]])) for r in rows if r[cols[4]]]
wv_t = [(int(r['year']), float(r[cols[5]])) for r in rows if r[cols[5]]]

fig, (a1, a2) = plt.subplots(1, 2, figsize=(11, 4.6), gridspec_kw={'width_ratios': [1.35, 1]})
c1, c2, c3 = '#1f4e79', '#b35900', '#555555'

# panel 1: electric-arc share
a1.plot(yr, ele, color=c1, marker='o', ms=3.5, lw=1.6)
a1.set_ylim(0, 60)
a1.set_xlim(1998.5, 2025.5)
a1.set_ylabel('percent of German crude steel')
a1.set_title('Electric-arc (scrap-based) share of crude steel, 1999-2025', fontsize=10.5, loc='left')
a1.grid(axis='y', color='#dddddd', lw=0.8)
for y, v, dy in [(1999, 29.2, 5), (2009, 34.7, 5), (2023, 27.7, -9), (2025, 30.5, 5)]:
    a1.annotate(f'{v:.1f}', (y, v), textcoords='offset points', xytext=(0, dy * 1.6), ha='center', fontsize=8.5, color=c1)
a1.text(2009, 52, '2009: recession cut blast-furnace output', ha='center', fontsize=8, color=c3)
a1.text(1999, 6, 'EU27 2025 for comparison: 45.8 percent (Italy 90.1, Spain 71.7)', fontsize=8, color=c3)
a1.spines[['top', 'right']].set_visible(False)

# panel 2: CO2 per tonne
a2.plot([p[0] for p in ets_t], [p[1] for p in ets_t], color=c2, marker='o', ms=3.5, lw=1.6, label='ETS-reported emissions of iron and steel installations / crude steel (derived)')
a2.plot([p[0] for p in wv_t], [p[1] for p in wv_t], color=c1, marker='s', ms=3.5, lw=1.6, label='WV Stahl specific CO2, incl. purchased power, excl. coke ovens')
a2.set_ylim(0, 1.8)
a2.set_xlim(2012.5, 2025.5)
a2.set_ylabel('t CO2 per t crude steel')
a2.set_title('CO2 per tonne of crude steel, 2013-2025', fontsize=10.5, loc='left')
a2.grid(axis='y', color='#dddddd', lw=0.8)
for (y, v) in [ets_t[0], ets_t[-1]]:
    a2.annotate(f'{v:.2f}', (y, v), textcoords='offset points', xytext=(0, -13), ha='center', fontsize=8.5, color=c2)
for (y, v) in [wv_t[0], wv_t[-1]]:
    a2.annotate(f'{v:.2f}', (y, v), textcoords='offset points', xytext=(0, 7), ha='center', fontsize=8.5, color=c1)
a2.legend(loc='upper left', fontsize=7.2, frameon=False, bbox_to_anchor=(0.0, 0.98))
a2.spines[['top', 'right']].set_visible(False)

fig.suptitle('Has German steel become cleaner? Outcome indicators (descriptive, not a policy effect)', fontsize=12, x=0.01, ha='left', y=0.995)
note = ('Sources: worldsteel Steel Statistical Yearbooks 2009/2018/2019-20 and World Steel in Figures 2021; WV Stahl crude-steel revision tables 2021-2025 and Daten und Fakten 2020-2026; DEHSt VET reports 2014-2024; '
        'UBA table of 2026-09-24. ETS series uses the third-trading-period scope (2013-2025); it excludes process-gas emissions released at power plants (17-22 Mt in the years read: 2013, 2014, 2019, 2020). The two lines use different boundaries; compare trends, not levels.')
fig.text(0.01, 0.005, note, fontsize=6.8, color=c3, wrap=True, ha='left', va='bottom')
fig.tight_layout(rect=(0, 0.075, 1, 0.95))
fig.savefig(R + 'chart_proposal_cleaner_steel.png', dpi=160)
print('saved')
