"""Figure 2.1: negative production externality, private and social marginal cost (illustrative).

Invented values, not German data. Demand P = 120 - Q; private marginal cost PMC = 20 + Q;
external cost per unit = 20, so social marginal cost SMC = PMC + 20 = 40 + Q.
Run from the repository root:  python -I -X utf8 report/chart-materials/scripts/fig21_externality.py
Output: report/chart-materials/figures-rebuilt/fig21_externality.png
"""
import os

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams.update({'font.family': 'serif', 'font.serif': ['Times New Roman', 'DejaVu Serif'], 'font.size': 15})
OUT = 'report/chart-materials/figures-rebuilt'
os.makedirs(OUT, exist_ok=True)

DEMAND, PMC_INTERCEPT, EXTERNAL = 120.0, 20.0, 20.0
q = np.linspace(0, 100, 401)
demand = DEMAND - q
pmc = PMC_INTERCEPT + q
smc = pmc + EXTERNAL

q_market = (DEMAND - PMC_INTERCEPT) / 2           # demand = PMC: Q = 50
p_market = DEMAND - q_market                      # P = 70
q_social = (DEMAND - PMC_INTERCEPT - EXTERNAL) / 2  # demand = SMC: Q = 40
p_social = DEMAND - q_social                      # P = 80

fig, ax = plt.subplots(figsize=(12.8, 6.0), dpi=150)
ax.plot(q, demand, color='#263444', lw=2.6, label='Demand: D')
ax.plot(q, pmc, color='#2B5C98', lw=2.6, label='Private marginal cost: PMC')
ax.plot(q, smc, color='#167A67', lw=2.6, label='Social marginal cost: SMC = PMC + 20')
ax.fill_between(q, pmc, smc, where=(q >= q_social) & (q <= q_market), color='#E8B4B4', alpha=0.6, lw=0)
ax.plot([q_social, q_social], [0, p_social], ':', color='#167A67')
ax.plot([q_market, q_market], [0, p_market], ':', color='#2B5C98')
ax.plot([0, q_social], [p_social, p_social], ':', color='#167A67')
ax.plot([0, q_market], [p_market, p_market], ':', color='#2B5C98')
ax.scatter([q_social, q_market], [p_social, p_market], color=['#167A67', '#2B5C98'], zorder=5)
ax.annotate('Social optimum: Q = 40', (q_social, p_social), (12, 92), color='#167A67')
ax.annotate('Market: Q = 50, P = 70', (q_market, p_market), (56, 52), color='#2B5C98')
ax.annotate('Marginal external cost = 20', (78, 110), (55, 128), color='#167A67')
ax.set_xlim(0, 100)
ax.set_ylim(0, 145)
ax.set_xlabel('Quantity (illustrative units)')
ax.set_ylabel('Price / marginal cost (index)')
ax.legend(loc='upper right', frameon=False)
ax.grid(alpha=0.25)
fig.tight_layout()
fig.savefig(os.path.join(OUT, 'fig21_externality.png'))
print('wrote fig21_externality.png; market Q, P =', q_market, p_market, '; social Q, P =', q_social, p_social)
