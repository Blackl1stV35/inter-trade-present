"""Audit observation status flags per series from the tidy CSVs.
Usage: python -I -X utf8 flag_audit.py TIDY_DIR
Writes TIDY_DIR/provisional_flag_audit.csv: one row per series with first/last year, years flagged, flag codes, latest value, dataset update stamp.
"""
import csv, sys, collections
T = sys.argv[1]
src = [
    ("gva_de_c_tidy.csv", ("unit",), "nama_10_a64 DE, Section C, B1G"),
    ("prod_de_c_tidy.csv", ("unit",), "sts_inpr_a DE, Section C, PRD NSA"),
    ("emp_de_subind_tidy.csv", ("nace_r2", "na_item"), "nama_10_a64_e DE, THS_PER"),
    ("gva_share_eu27_de_tidy.csv", ("geo",), "nama_10_a64 PC_TOT, Section C, B1G"),
    ("gva_levels_eu27_de_tidy.csv", ("geo", "nace_r2"), "nama_10_a64 CP_MEUR, B1G"),
    ("nama_10_gdp_DE_tidy.csv", ("unit", "na_item"), "nama_10_gdp DE annual"),
    ("namq_10_gdp_DE_tidy.csv", ("unit", "s_adj", "na_item"), "namq_10_gdp DE quarterly"),
]
out = []
for f, keys, label in src:
    rows = list(csv.DictReader(open(f"{T}/{f}", encoding="utf-8")))
    g = collections.defaultdict(list)
    for r in rows:
        g[tuple(r[k] for k in keys)].append(r)
    for k, rs in sorted(g.items()):
        rs.sort(key=lambda r: r["time"])
        fl = collections.OrderedDict((r["time"], r["flag"]) for r in rs if r["flag"])
        vals = [r for r in rs if r["value"] != ""]
        out.append([label, f, "|".join(f"{a}={b}" for a, b in zip(keys, k)), rs[0]["time"], vals[-1]["time"],
                    ";".join(fl.keys()) or "none", ";".join(sorted(set(fl.values()))) or "none",
                    vals[-1]["value"], rs[0]["UPDATE_DATA"]])
with open(f"{T}/provisional_flag_audit.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["dataset_and_scope", "tidy_file", "series_key", "first_period_returned", "last_period_with_value",
                "periods_flagged", "flag_codes", "value_in_last_period", "dataset_UPDATE_DATA_stamp"])
    w.writerows(out)
print(len(out), "series audited")
