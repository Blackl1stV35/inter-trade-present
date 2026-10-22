"""Recompute the annual means and the key checks from the monthly SMARD CSVs in this folder.

Run:  python -I -X utf8 reproduce.py
Reads only the CSV files next to this script. No network access.
"""
import csv
import sys
from decimal import Decimal as D, ROUND_HALF_UP
from pathlib import Path

HERE = Path(__file__).resolve().parent
q2 = lambda x: D(x).quantize(D("0.01"), rounding=ROUND_HALF_UP)


def load(name):
    with open(HERE / name, encoding="utf-8", newline="") as f:
        return {r["month"]: r for r in csv.DictReader(f)}


v1 = load("smard_industrial_price_monthly_V1_article_2025-02-11.csv")
v2 = load("smard_industrial_price_monthly_V2_live_2026-10-22.csv")


def annual(data, col, year):
    vals = [D(r[col]) for m, r in data.items() if m.startswith(f"{year}-")]
    return (sum(vals) / D(len(vals)), len(vals)) if vals else (None, 0)


WO, WI = "price_without_reductions_ct_kwh", "price_with_reductions_ct_kwh"
# Figures printed in the text of the SMARD article of 11 Feb 2025
printed = {
    ("without", 2021): "21.77", ("without", 2022): "35.70", ("without", 2023): "19.63", ("without", 2024): "16.77",
    ("with", 2020): "5.92", ("with", 2021): "10.94", ("with", 2022): "29.01", ("with", 2023): "14.23", ("with", 2024): "10.47",
}
ok = True
print("Check 1: V1 monthly data reproduce the printed annual figures (tolerance 0.011 ct/kWh)")
for (case, y), p in printed.items():
    m, n = annual(v1, WO if case == "without" else WI, y)
    good = n == 12 and abs(m - D(p)) <= D("0.011")
    ok &= good
    print(f"  {case:8s} {y}: derived {q2(m)}  printed {p}  {'OK' if good else 'FAIL'}")

print("\nCheck 2: 2020 base values")
w20, _ = annual(v1, WO, 2020)
i20, _ = annual(v1, WI, 2020)
print(f"  2020 WITHOUT reductions (V1 derived): {q2(w20)}   2020 WITH reductions (V1 derived): {q2(i20)} (printed 5.92)")
print(f"  workbook '+77%': 10.47 / 5.92 - 1 = {(D('10.47') / D('5.92') - 1) * 100:.1f}% (both with-reductions)")
print(f"  no-concession 2024 vs 2020 (V1): {(D('16.77') / q2(w20) - 1) * 100:.1f}%   (V2: "
      f"{(annual(v2, WO, 2024)[0] / annual(v2, WO, 2020)[0] - 1) * 100:.1f}%)")

print("\nCheck 3: V2 (current data file) annual means, ct/kWh")
for y in range(2020, 2027):
    a, n = annual(v2, WO, y)
    b, _ = annual(v2, WI, y)
    print(f"  {y}: without {q2(a)}  with {q2(b)}  ({n} months)")

print("\nCheck 4: latest month in the file:", max(v2), v2[max(v2)][WO], v2[max(v2)][WI])
sys.exit(0 if ok else 1)
