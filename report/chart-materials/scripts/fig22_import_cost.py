"""Figure 2.2: carbon-related import cost with partial pass-through and a domestic cost increase (illustrative).

Invented values, not German data. Demand P = 120 - Q; domestic supply S: P = 20 + Q;
domestic supply after a 10-unit cost rise S': P = 30 + Q; delivered import price P0 = 40 before the carbon cost;
the carbon cost c = 20 would give 60 at full pass-through (dotted benchmark, not assumed); with partial pass-through
the delivered price rises to P1 = 50.
Run from the repository root:  python -I -X utf8 report/chart-materials/scripts/fig22_import_cost.py
Output: report/chart-materials/figures-rebuilt/fig22_import_cost.png
"""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'], 'font.size': 15})
OUT = 'report/chart-materials/figures-rebuilt'
os.makedirs(OUT, exist_ok=True)

q = np.linspace(0, 100, 401)
demand = 120 - q
supply = 20 + q
supply_cost = 30 + q
P0, P1, FULL = 40.0, 50.0, 60.0
q_s0 = P0 - 20                 # supply at P0: Q = 20
q_s1 = P1 - 30                 # S' at P1: Q = 20 (the domestic cost rise offsets the price rise at this point)
q_d1 = 120 - P1                # demand at P1: Q = 70
q_d0 = 120 - P0                # demand at P0: Q = 80

fig, ax = plt.subplots(figsize=(12.8, 6.4), dpi=150)
ax.plot(q, demand, color='#263444', lw=2.6, label='D: demand')
ax.plot(q, supply, color='#2B5C98', lw=2.6, label='S: initial supply')
ax.plot(q, supply_cost, color='#167A67', lw=2.6, ls='--', label="S': domestic cost +10")
ax.axhline(FULL, color='#78828C', ls=':', lw=1.4)
ax.text(100, FULL + 2, 'Full pass-through benchmark (not assumed)', ha='right', color='#78828C')
ax.axhline(P1, color='#167A67', lw=1.6)
ax.axhline(P0, color='#2B5C98', lw=1.6)
ax.scatter([q_s0, q_s1, q_d0, q_d1], [P0, P1, P0, P1], color=['#2B5C98', '#167A67', '#2B5C98', '#167A67'], zorder=5)
ax.annotate('', (q_d1, 30), (q_s1, 30), arrowprops=dict(arrowstyle='<->', color='#167A67'))
ax.text((q_s1 + q_d1) / 2, 33, 'Imports after = 50', ha='center', color='#167A67')
ax.annotate('', (q_d0, 22), (q_s0, 22), arrowprops=dict(arrowstyle='<->', color='#2B5C98'))
ax.text((q_s0 + q_d0) / 2, 25, 'Imports before = 60', ha='center', color='#2B5C98')
ax.set_xlim(0, 100)
ax.set_ylim(0, 140)
ax.set_xlabel('Quantity of steel (illustrative units)')
ax.set_ylabel('Price / marginal cost (index)')
ax.legend(loc='upper right', frameon=False)
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(os.path.join(OUT, 'fig22_import_cost.png'))
print('wrote fig22_import_cost.png; imports before =', q_d0 - q_s0, '; after =', q_d1 - q_s1)
