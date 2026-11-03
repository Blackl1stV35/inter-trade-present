"""Figure 2.1: negative production externality, private and social marginal cost (illustrative).

Invented values, not German data. Demand P = 120 - Q; private marginal cost PMC = 20 + Q;
external cost per unit = 20, so social marginal cost SMC = PMC + 20 = 40 + Q.
Market: demand = PMC gives Q = 50, P = 70. Social optimum: demand = SMC gives Q = 40, P = 80.
Run from the repository root:  python -I -X utf8 report/chart-materials/scripts/fig21_externality.py
Output: report/chart-materials/figures-rebuilt/fig21_externality.png (same styling and headline as the report figure)
"""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'], 'font.size': 16})
OUT = 'report/chart-materials/figures-rebuilt'
os.makedirs(OUT, exist_ok=True)
HEADLINE = 'Negative production externality: private and social marginal cost (illustrative)'
DARK, BLUE, TEAL, RED = '#263444', '#2B5C98', '#167A67', '#E8B4B4'

DEMAND, PMC_INTERCEPT, EXTERNAL = 120.0, 20.0, 20.0
q = np.linspace(0, 100, 401)
demand = DEMAND - q
pmc = PMC_INTERCEPT + q
smc = pmc + EXTERNAL

q_market = (DEMAND - PMC_INTERCEPT) / 2
p_market = DEMAND - q_market
q_social = (DEMAND - PMC_INTERCEPT - EXTERNAL) / 2
p_social = DEMAND - q_social

fig, ax = plt.subplots(figsize=(12.8, 7.2), dpi=160)
fig.suptitle(HEADLINE, fontsize=24, fontweight='bold', color=DARK, y=0.975)
ax.plot(q, demand, color=DARK, lw=2.8, label='Demand: D')
ax.plot(q, pmc, color=BLUE, lw=2.8, label='Private marginal cost: PMC')
ax.plot(q, smc, color=TEAL, lw=2.8, label='Social marginal cost: SMC = PMC + 20')
ax.fill_between(q, pmc, smc, where=(q >= q_social) & (q <= q_market), color=RED, alpha=0.6, lw=0)
ax.plot([q_social, q_social], [0, p_social], ':', color=TEAL, lw=1.6)
ax.plot([q_market, q_market], [0, p_market], ':', color=BLUE, lw=1.6)
ax.plot([0, q_social], [p_social, p_social], ':', color=TEAL, lw=1.6)
ax.plot([0, q_market], [p_market, p_market], ':', color=BLUE, lw=1.6)
ax.scatter([q_social, q_market], [p_social, p_market], color=[TEAL, BLUE], zorder=5, s=60)
ax.annotate('Social optimum: Q = 40', (q_social, p_social), (12, 92), color=TEAL)
ax.annotate('Market: Q = 50, P = 70', (q_market, p_market), (56, 52), color=BLUE)
ax.annotate('', xy=(78, 120), xytext=(78, 100), arrowprops=dict(arrowstyle='<->', color=TEAL, lw=2.2))
ax.text(55, 128, 'Marginal external cost = 20', color=TEAL)
ax.set_xlim(0, 100)
ax.set_ylim(0, 145)
ax.set_xticks([0, 20, 40, 60, 80, 100])
ax.set_yticks(range(0, 141, 20))
ax.set_xlabel('Quantity (illustrative units)')
ax.set_ylabel('Price / marginal cost (index)')
ax.legend(loc='upper left', frameon=False)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(os.path.join(OUT, 'fig21_externality.png'))
print('wrote fig21_externality.png; market Q, P =', q_market, p_market, '; social Q, P =', q_social, p_social)
