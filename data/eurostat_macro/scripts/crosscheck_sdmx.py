"""Cross-check JSON-stat values/flags against SDMX-CSV (second Eurostat endpoint).
Usage: python -I -X utf8 crosscheck_sdmx.py RAW_DIR TIDY_DIR
Prints, per series: rows compared, value mismatches, flag mismatches, LAST UPDATE stamp from SDMX-CSV.
"""
import csv, sys
RAW, TIDY = sys.argv[1:3]
pairs = [
    ("sdmxcsv_nama_10_a64_CLV_I20_DE_C.csv", "gva_de_c_tidy.csv", {"unit": "CLV_I20"}),
    ("sdmxcsv_nama_10_a64_PC_TOT_DE_C.csv", "gva_de_c_tidy.csv", {"unit": "PC_TOT"}),
    ("sdmxcsv_sts_inpr_a_PRD_NSA_I21_DE_C.csv", "prod_de_c_tidy.csv", {}),
    ("sdmxcsv_nama_10_a64_e_EMP_DC_THS_PER_DE_C.csv", "emp_de_c_tidy.csv", {}),
]
for sd, js, filt in pairs:
    a = {r["TIME_PERIOD"]: (float(r["OBS_VALUE"]), r["OBS_FLAG"]) for r in csv.DictReader(open(f"{RAW}/{sd}", encoding="utf-8"))}
    upd = {r["LAST UPDATE"] for r in csv.DictReader(open(f"{RAW}/{sd}", encoding="utf-8"))}
    b = {}
    for r in csv.DictReader(open(f"{TIDY}/{js}", encoding="utf-8")):
        if all(r[k] == v for k, v in filt.items()):
            b[r["time"]] = (float(r["value"]), r["flag"])
    vm = [y for y in a if y not in b or abs(a[y][0] - b[y][0]) > 0.0006]
    fm = [y for y in a if y in b and a[y][1] != b[y][1]]
    print(sd, "n_sdmx", len(a), "n_json", len(b), "value_mismatch", vm, "flag_mismatch", fm, "LAST UPDATE", sorted(upd))
