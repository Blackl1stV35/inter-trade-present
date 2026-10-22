"""Compare the workbook table (update tab 4.1) with the live Eurostat pull.

Usage:
    python -I -X utf8 compare_workbook.py WORKBOOK_TXT TIDY_DIR OUT_DIR

Reads
    WORKBOOK_TXT                 sources/text/inter-trade-present-2-revised-research-brief.txt
    TIDY_DIR/gva_de_c_tidy.csv   nama_10_a64 (CLV_I20 and PC_TOT)
    TIDY_DIR/prod_de_c_tidy.csv  sts_inpr_a
    TIDY_DIR/emp_de_c_tidy.csv   nama_10_a64_e (EMP_DC, THS_PER, Section C)
Writes
    OUT_DIR/workbook_table_4_1.csv           the workbook table, parsed
    OUT_DIR/de_manufacturing_1995_2025_live.csv   live values + flags, one row per year
    OUT_DIR/revision_check_vs_workbook.csv   year, series, workbook value, live value, diff, flag
"""
import csv
import sys


def parse_workbook(path):
    rows = {}
    with open(path, encoding="utf-8") as fh:
        lines = [ln.rstrip("\n") for ln in fh]
    # find the table that starts with the header "Year | Real GVA"
    start = None
    for i, ln in enumerate(lines):
        if ln.startswith("Year | Real GVA / 2020 = 100"):
            start = i
            break
    if start is None:
        raise SystemExit("workbook table header not found")
    for ln in lines[start + 1:]:
        if ln.startswith("[/TABLE]"):
            break
        parts = [p.strip() for p in ln.split("|")]
        if len(parts) != 4 or not parts[0].isdigit():
            continue
        rows[int(parts[0])] = (float(parts[1]), float(parts[2]), float(parts[3]))
    return rows


def read_tidy(path):
    with open(path, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def main():
    wb_path, tidy_dir, out_dir = sys.argv[1:4]
    wb = parse_workbook(wb_path)
    gva = read_tidy(f"{tidy_dir}/gva_de_c_tidy.csv")
    prod = read_tidy(f"{tidy_dir}/prod_de_c_tidy.csv")
    emp = read_tidy(f"{tidy_dir}/emp_de_c_tidy.csv")
    live = {}
    for r in gva:
        y = int(r["time"])
        key = "gva_clv_i20" if r["unit"] == "CLV_I20" else "gva_share_pc_tot"
        live.setdefault(y, {})[key] = (float(r["value"]), r["flag"])
    for r in prod:
        y = int(r["time"])
        live.setdefault(y, {})["prod_i21"] = (float(r["value"]), r["flag"])
    for r in emp:
        y = int(r["time"])
        live.setdefault(y, {})["emp_c_ths"] = (float(r["value"]), r["flag"])

    with open(f"{out_dir}/workbook_table_4_1.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["year", "wb_real_gva_2020_100", "wb_production_2021_100", "wb_mfg_share_total_gva_pct"])
        for y in sorted(wb):
            w.writerow([y, *wb[y]])

    cols = ["gva_clv_i20", "prod_i21", "gva_share_pc_tot", "emp_c_ths"]
    with open(f"{out_dir}/de_manufacturing_1995_2025_live.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["year", "real_gva_clv_i20_2020_100", "flag_gva_clv", "production_i21_2021_100", "flag_prod",
                    "mfg_share_of_total_gva_pct", "flag_share", "employment_C_ths_persons_EMP_DC", "flag_emp"])
        for y in sorted(live):
            d = live[y]
            row = [y]
            for c in cols:
                v, f = d.get(c, ("", ""))
                row += [v, f]
            w.writerow(row)

    n_cmp = 0
    n_diff = 0
    diffs = []
    with open(f"{out_dir}/revision_check_vs_workbook.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["year", "series", "workbook_value", "live_value", "difference_live_minus_workbook",
                    "live_flag", "status"])
        for y in sorted(wb):
            for name, idx, key in (("real GVA CLV_I20 (2020=100)", 0, "gva_clv_i20"),
                                   ("production I21 (2021=100)", 1, "prod_i21"),
                                   ("mfg share of total GVA PC_TOT (%)", 2, "gva_share_pc_tot")):
                old = wb[y][idx]
                if key not in live.get(y, {}):
                    w.writerow([y, name, old, "", "", "", "MISSING_IN_LIVE"])
                    continue
                new, flag = live[y][key]
                diff = round(new - old, 6)
                n_cmp += 1
                status = "unchanged" if abs(diff) < 1e-9 else "REVISED"
                if status == "REVISED":
                    n_diff += 1
                    diffs.append((y, name, old, new))
                w.writerow([y, name, old, new, diff, flag, status])
        # years in live but not in workbook
        for y in sorted(live):
            if y not in wb:
                w.writerow([y, "(year not in workbook table)", "", "", "", "", "NEW_YEAR_IN_LIVE"])
    print(f"compared {n_cmp} values; revised: {n_diff}")
    for d in diffs:
        print("REVISED", d)
    # employment workbook values (U28)
    emp_wb = {2023: 7490.0, 2024: 7415.0, 2025: 7262.0}
    for y, old in emp_wb.items():
        new, flag = live[y]["emp_c_ths"]
        print("EMP", y, "workbook", old, "live", new, "flag", flag, "UNCHANGED" if abs(new - old) < 1e-9 else "REVISED")


if __name__ == "__main__":
    main()
