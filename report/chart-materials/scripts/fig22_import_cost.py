"""Figure 2.2: carbon-related import cost with partial pass-through and a domestic cost increase (illustrative).

Invented values, not German data. Demand P = 120 - Q; domestic supply S: P = 20 + Q;
domestic supply after a 10-unit cost rise S': P = 30 + Q. Delivered import price P0 = 40 before the carbon cost.
Full pass-through of c = 20 would give 60 (dotted benchmark, not assumed); partial pass-through gives P1 = 50.
Run from the repository root:  python -I -X utf8 report/chart-materials/scripts/fig22_import_cost.py
Output: report/chart-materials/figures-rebuilt/fig22_import_cost.png (same styling and headline as the report figure)
"""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'], 'font.size': 16})
OUT = 'report/chart-materials/figures-rebuilt'
os.makedirs(OUT, exist_ok=True)
HEADLINE = 'Carbon-related import cost with partial pass-through (illustrative)'
DARK, BLUE, TEAL, GREY = '#263444', '#2B5C98', '#167A67', '#78828C'

q = np.linspace(0, 100, 401)
P0, P1, FULL = 40.0, 50.0, 60.0
q_s0 = P0 - 20
q_s1 = P1 - 30
q_d1 = 120 - P1
q_d0 = 120 - P0

fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=160)
fig.suptitle(HEADLINE, fontsize=24, fontweight='bold', color=DARK, y=0.975)
ax.plot(q, 120 - q, color=DARK, lw=2.8, label='D: demand')
ax.plot(q, 20 + q, color=BLUE, lw=2.8, label='S: initial supply')
ax.plot(q, 30 + q, color=TEAL, lw=2.8, ls='--', label="S': domestic cost +10")
ax.axhline(FULL, color=GREY, ls=':', lw=1.6)
ax.text(100, FULL + 2.5, 'Full pass-through benchmark (not assumed)', ha='right', color=GREY)
ax.axhline(P1, color=TEAL, lw=1.8)
ax.axhline(P0, color=BLUE, lw=1.8)
ax.plot([q_s0, q_s0], [0, P0], ':', color=BLUE, lw=1.4)
ax.plot([q_d0, q_d0], [0, P0], ':', color=BLUE, lw=1.4)
ax.plot([q_s1, q_s1], [0, P1], ':', color=TEAL, lw=1.4)
ax.plot([q_d1, q_d1], [0, P1], ':', color=TEAL, lw=1.4)
ax.scatter([q_s0, q_d0], [P0, P0], color=BLUE, zorder=5, s=60)
ax.scatter([q_s1, q_d1], [P1, P1], color=TEAL, zorder=5, s=60)
ax.annotate('', (q_d1, 33), (q_s1, 33), arrowprops=dict(arrowstyle='<->', color=TEAL, lw=2))
ax.text((q_s1 + q_d1) / 2, 36, 'Imports after = 50', ha='center', color=TEAL)
ax.annotate('', (q_d0, 22), (q_s0, 22), arrowprops=dict(arrowstyle='<->', color=BLUE, lw=2))
ax.text((q_s0 + q_d0) / 2, 25, 'Imports before = 60', ha='center', color=BLUE)
ax.set_xlim(0, 100)
ax.set_ylim(0, 135)
ax.set_xticks([0, q_s0, q_d1, q_d0, 100])
ax.set_xticklabels(['0', r'$Q_{S0} = Q_{S1}$' + '\n20', r'$Q_{D1}$' + '\n70', r'$Q_{D0}$' + '\n80', '100'])
ax.set_yticks([0, P0, P1, FULL, 100, 135])
ax.set_yticklabels(['0', r'$P_0 = 40$', r'$P_1 = 50$', r'$P_0 + c = 60$', '100', '135'])
ax.set_xlabel('Quantity of steel (illustrative units)')
ax.set_ylabel('Price / marginal cost (index)')
ax.legend(loc='lower center', bbox_to_anchor=(0.5, 1.0), ncol=3, frameon=False)
fig.tight_layout(rect=(0, 0, 1, 0.90))
fig.savefig(os.path.join(OUT, 'fig22_import_cost.png'))
print('wrote fig22_import_cost.png; imports before =', q_d0 - q_s0, '; after =', q_d1 - q_s1)
