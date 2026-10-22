"""Turn the data tables in the workbook text dumps into tidy CSV files under data/workbook/.

usage: python -I -X utf8 scripts/build_workbook_csv.py
Run from the repo root. Tables are located by their section heading, so edits elsewhere do not break it.
"""
import csv
import os
import re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
UPDATE = os.path.join(ROOT, "sources", "text", "inter-trade-present-2-revised-research-brief.txt")
BASE = os.path.join(ROOT, "sources", "text", "inter-trade-present-base.txt")
OUT = os.path.join(ROOT, "data", "workbook")


def read_lines(path):
    with open(path, encoding="utf-8") as f:
        return f.read().split("\n")


def table_after(lines, heading_regex, occurrence=1):
    """Return rows (list of lists) of the first [TABLE] after the nth heading match."""
    seen = 0
    for i, line in enumerate(lines):
        if re.search(heading_regex, line):
            seen += 1
            if seen < occurrence:
                continue
            j = i
            while j < len(lines) and lines[j].strip() != "[TABLE]":
                j += 1
            rows = []
            j += 1
            while j < len(lines) and lines[j].strip() != "[/TABLE]":
                rows.append([c.strip() for c in lines[j].split("|")])
                j += 1
            return rows
    raise SystemExit("heading not found: " + heading_regex)


def num(s):
    s = s.replace("−", "-").replace(",", "")
    return float(s)


def write(name, header, rows):
    os.makedirs(OUT, exist_ok=True)
    path = os.path.join(OUT, name)
    with open(path, "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("wrote", os.path.relpath(path, ROOT), len(rows), "rows")


upd = read_lines(UPDATE)
base = read_lines(BASE)

# update tab 4.1: manufacturing 1995-2025
t = table_after(upd, r"^## 4\.1 Germany manufacturing")
write(
    "de_manufacturing_1995_2025.csv",
    ["year", "real_gva_index_2020_100", "production_index_2021_100", "manufacturing_share_of_total_gva_pct"],
    [[int(r[0]), num(r[1]), num(r[2]), num(r[3])] for r in t[1:]],
)

# update tab 4.2: direct extra-EU Chapter 72 imports 1999-2025
t = table_after(upd, r"^## 4\.2 Germany's direct extra-EU")
rows = []
for r in t[1:]:
    val, mass = num(r[1]), num(r[2])
    rows.append([int(r[0]), val, mass, round(val * 1000 / mass, 2)])  # EUR m / kt -> EUR per tonne
write("de_extra_eu_ch72_imports_1999_2025.csv", ["year", "import_value_eur_m", "net_mass_kt", "unit_value_eur_per_t"], rows)

# update tab appendix A: 2025 material profiles
t = table_after(upd, r"^# 6\. Appendix A")
write(
    "de_extra_eu_import_profiles_2025.csv",
    ["cn_code", "material_profile", "net_mass_kt", "import_value_eur_m"],
    [[r[0], r[1], num(r[2]), num(r[3])] for r in t[1:]],
)

# base Dataset A: crude steel
t = table_after(base, r"^## Dataset A")
write("de_crude_steel_2017_2025.csv", ["year", "crude_steel_mt"], [[int(r[0]), num(r[1])] for r in t[1:]])

# base Dataset B: all-partner steel mill products
t = table_after(base, r"^## Dataset B")
rows = []
for r in t[1:]:
    x, m = num(r[1]), num(r[2])
    rows.append([int(r[0]), x, m, round(x - m, 1)])
write("de_steel_mill_products_trade_all_partners_2017_2024.csv", ["year", "exports_mt", "imports_mt", "balance_x_minus_m_mt_approx"], rows)

# base Dataset E: certificate prices
t = table_after(base, r"^## Dataset E")
write("cbam_certificate_prices_2026.csv", ["quarter", "published", "eur_per_tco2e"], [[r[0], r[1], num(r[2])] for r in t[1:]])

# base Dataset F: 2025 macro growth (January 2026 first estimate)
t = table_after(base, r"^## Dataset F")
write("de_macro_growth_2025_first_estimate.csv", ["indicator", "real_growth_2025_pct"], [[r[0], num(r[1])] for r in t[1:]])

# base 1.6: CBAM factor schedule
t = table_after(base, r"^## 1\.6 Free-allocation schedule")
write("cbam_factor_schedule_2026_2034.csv", ["year", "cbam_factor_pct", "complement_pct"], [[int(r[0]), num(r[1]), num(r[2])] for r in t[1:]])
