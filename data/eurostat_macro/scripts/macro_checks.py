"""Checks and derived tables for the macro / employment pull.

Usage:
    python -I -X utf8 macro_checks.py TIDY_DIR

Produces in TIDY_DIR:
    datasetF_vs_current_vintage.csv   workbook Dataset F (Jan 2026 first estimate) vs live Eurostat nama_10_gdp
    nama_10_gdp_pct_from_levels_check.csv   CLV_PCH_PRE vs percent change recomputed from CLV20_MEUR levels
    emp_sub_industries_2015_2025.csv  wide table, thousand persons, DE, EMP_DC (and SAL_DC) by NACE
    emp_sub_industries_changes.csv    2015->2025 and 2022->2025 absolute and % change, sub-industry share of Section C
    eu27_vs_de_mfg_share.csv          PC_TOT share, DE vs EU27_2020, 1995-latest, and recomputed from CP_MEUR for 2015+
"""
import csv
import sys
from collections import defaultdict

T = sys.argv[1]


def rd(name):
    with open(f"{T}/{name}", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


# ---------- Dataset F vs live ----------
gdp = rd("nama_10_gdp_DE_tidy.csv")
g = {}
for r in gdp:
    g[(r["unit"], r["na_item"], r["time"])] = (r["value"], r["flag"])

workbook_F = [
    # label, workbook value (Jan 2026 first estimate), eurostat na_item(s) shown, note
    ("GDP", 0.2, "B1GQ"),
    # Jan 2026 press release row is 'Final consumption expenditure of households and NPISHs' = 1.4 -> like-for-like is P31_S14_S15
    ("Household consumption (C) = households and NPISH (like-for-like with Jan 2026 release)", 1.4, "P31_S14_S15"),
    ("Households only (P31_S14), shown for definition note", None, "P31_S14"),
    ("Government consumption (G)", 1.5, "P3_S13"),
    ("Gross fixed capital formation", -0.5, "P51G"),
    ("Exports of goods and services (X)", -0.3, "P6"),
    ("Imports of goods and services (M)", 3.6, "P7"),
]
with open(f"{T}/datasetF_vs_current_vintage.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["indicator", "eurostat_na_item", "workbook_2025_real_growth_pct_Jan2026_first_estimate",
                "eurostat_2025_CLV_PCH_PRE_live_21Oct2026", "flag", "difference_live_minus_workbook", "status"])
    for label, old, item in workbook_F:
        v, f = g.get(("CLV_PCH_PRE", item, "2025"), ("", ""))
        if old is None:
            w.writerow([label, item, "", v, f, "", "no workbook counterpart (definition note)"])
            continue
        diff = round(float(v) - old, 6)
        w.writerow([label, item, old, v, f, diff, "unchanged" if abs(diff) < 1e-9 else "REVISED"])

# ---------- recompute pct change from levels ----------
with open(f"{T}/nama_10_gdp_pct_from_levels_check.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["na_item", "year", "CLV20_MEUR_prev", "CLV20_MEUR", "pct_change_from_levels",
                "CLV_PCH_PRE_published", "abs_diff", "flag"])
    maxdiff = 0
    for item in ["B1GQ", "P31_S14", "P31_S14_S15", "P3", "P3_S13", "P51G", "P6", "P61", "P62", "P7", "P71", "P72"]:
        for y in range(2016, 2026):
            a = g.get(("CLV20_MEUR", item, str(y - 1)))
            b = g.get(("CLV20_MEUR", item, str(y)))
            p = g.get(("CLV_PCH_PRE", item, str(y)))
            if not (a and b and p and a[0] != "" and b[0] != "" and p[0] != ""):
                continue
            calc = (float(b[0]) / float(a[0]) - 1) * 100
            d = abs(calc - float(p[0]))
            maxdiff = max(maxdiff, d)
            w.writerow([item, y, a[0], b[0], round(calc, 3), p[0], round(d, 3), p[1]])
print("max abs diff recomputed vs published CLV_PCH_PRE (pp):", round(maxdiff, 3))

# net-export contribution 2025 (approximate, chain-linked levels)
gdp24 = float(g[("CLV20_MEUR", "B1GQ", "2024")][0])
x24, x25 = float(g[("CLV20_MEUR", "P6", "2024")][0]), float(g[("CLV20_MEUR", "P6", "2025")][0])
m24, m25 = float(g[("CLV20_MEUR", "P7", "2024")][0]), float(g[("CLV20_MEUR", "P7", "2025")][0])
print("approx net export contribution 2025 (pp of 2024 GDP, CLV20 levels):", round(((x25 - x24) - (m25 - m24)) / gdp24 * 100, 2))

# ---------- employment sub-industries ----------
emp = rd("emp_de_subind_tidy.csv")
tab = defaultdict(dict)
flags = defaultdict(dict)
for r in emp:
    y = int(r["time"])
    if y < 2015:
        continue
    key = (r["na_item"], r["nace_r2"])
    tab[key][y] = r["value"]
    flags[key][y] = r["flag"]
years = list(range(2015, 2026))
with open(f"{T}/emp_sub_industries_2015_2025.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["na_item", "nace_r2", "unit"] + [str(y) for y in years] + ["flags_2023_2025"])
    for key in sorted(tab, key=lambda k: (k[0], k[1])):
        fl = ";".join(f"{y}:{flags[key].get(y, '')}" for y in (2023, 2024, 2025))
        w.writerow([key[0], key[1], "THS_PER"] + [tab[key].get(y, "") for y in years] + [fl])

with open(f"{T}/emp_sub_industries_changes.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["na_item", "nace_r2", "latest_year_available", "flag_latest", "emp_2015", "emp_2019", "emp_2022", "emp_latest",
                "chg_2015_latest_ths", "chg_2015_latest_pct", "chg_2019_latest_ths", "chg_2019_latest_pct",
                "chg_2022_latest_ths", "chg_2022_latest_pct", "share_of_section_C_latest_year_pct"])
    for key in sorted(tab, key=lambda k: (k[0], k[1])):
        t = {y: v for y, v in tab[key].items() if v != ""}
        if not t:
            continue
        ly = max(t)
        try:
            a15, a19, a22, al = (float(t[2015]), float(t[2019]), float(t[2022]), float(t[ly]))
        except (KeyError, ValueError):
            continue
        share = ""
        cl = tab.get(("EMP_DC", "C"), {}).get(ly, "")
        if key[0] == "EMP_DC" and key[1] not in ("TOTAL", "B-E", "C") and cl != "":
            share = round(al / float(cl) * 100, 1)
        w.writerow([key[0], key[1], ly, flags[key].get(ly, ""), a15, a19, a22, al,
                    round(al - a15, 1), round((al / a15 - 1) * 100, 1),
                    round(al - a19, 1), round((al / a19 - 1) * 100, 1),
                    round(al - a22, 1), round((al / a22 - 1) * 100, 1), share])

# ---------- EU27 vs DE share ----------
sh = rd("gva_share_eu27_de_tidy.csv")
lv = rd("gva_levels_eu27_de_tidy.csv")
share = defaultdict(dict)
for r in sh:
    share[int(r["time"])][r["geo"]] = (r["value"], r["flag"])
cp = {}
for r in lv:
    cp[(r["geo"], r["nace_r2"], int(r["time"]))] = r["value"]
with open(f"{T}/eu27_vs_de_mfg_share.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["year", "DE_share_pc_tot", "DE_flag", "EU27_2020_share_pc_tot", "EU27_flag",
                "DE_recomputed_C_over_TOTAL_CP_MEUR", "EU27_recomputed_C_over_TOTAL_CP_MEUR"])
    for y in sorted(share):
        de = share[y].get("DE", ("", ""))
        eu = share[y].get("EU27_2020", ("", ""))
        def rec(geo):
            c, t = cp.get((geo, "C", y)), cp.get((geo, "TOTAL", y))
            return round(float(c) / float(t) * 100, 2) if c and t else ""
        w.writerow([y, de[0], de[1], eu[0], eu[1], rec("DE"), rec("EU27_2020")])
print("done")
