"""Decode the raw JSON-stat files, build tidy CSVs and the like-for-like YTD comparison.

Run:  python -I -X utf8 02_compute_ytd.py <raw_dir> <out_dir>

Definitions (same as the workbook): tonnes = QUANTITY_IN_100KG / 10; kt = tonnes / 1000;
EUR million = EUR / 1e6; unit value EUR/t = EUR / tonnes. Missing observations stay missing (empty cell).
"""
import csv
import json
import sys
from itertools import product as iproduct
from pathlib import Path

RAW = Path(sys.argv[1])
OUT = Path(sys.argv[2])
OUT.mkdir(parents=True, exist_ok=True)

FLOW_NAME = {"1": "imports", "2": "exports"}


def decode(path):
    """Return dict {(dim values...): value} for a JSON-stat 2.0 file with full dimension decoding."""
    d = json.loads(Path(path).read_text(encoding="utf-8"))
    ids = d["id"]
    sizes = d["size"]
    cats = []
    for dim in ids:
        idx = d["dimension"][dim]["category"]["index"]
        inv = {v: k for k, v in idx.items()}
        cats.append([inv[i] for i in range(len(inv))])
    rows = {}
    n = 1
    for s in sizes:
        n *= s
    # JSON-stat: last dimension varies fastest
    combos = list(iproduct(*[range(s) for s in sizes]))
    assert len(combos) == n
    vals = d["value"]
    for pos, combo in enumerate(combos):
        key = tuple(cats[i][c] for i, c in enumerate(combo))
        v = vals.get(str(pos)) if isinstance(vals, dict) else (vals[pos] if pos < len(vals) else None)
        rows[key] = v
    return d, ids, rows


def conv(eur, q100):
    eur_m = None if eur is None else eur / 1e6
    kt = None if q100 is None else q100 / 10 / 1000
    uv = None if (eur is None or q100 is None or q100 == 0) else eur / (q100 / 10)
    return eur_m, kt, uv


# ---------- monthly long table ----------
monthly = {}  # (product, flow, period) -> dict(eur, q100)
meta = {}
for f in sorted(RAW.glob("monthly_*.json")):
    d, ids, rows = decode(f)
    meta[f.name] = dict(updated=d.get("updated"), no_data=d["extension"].get("positions-with-no-data"))
    for key, v in rows.items():
        k = dict(zip(ids, key))
        mk = (k["product"], k["flow"], k["time"])
        monthly.setdefault(mk, {"eur": None, "q100": None})
        if k["indicators"] == "VALUE_IN_EUROS":
            monthly[mk]["eur"] = v
        elif k["indicators"] == "QUANTITY_IN_100KG":
            monthly[mk]["q100"] = v

all_periods = sorted({k[2] for k in monthly})
# periods that carry at least one observation anywhere in the pull
with_data = sorted({k[2] for k, v in monthly.items() if v["eur"] is not None or v["q100"] is not None})
print("periods requested:", all_periods[0], "->", all_periods[-1], "| periods with any data:", with_data[0], "->", with_data[-1])

with open(OUT / "monthly_series.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["product_cn", "flow_code", "flow", "period", "value_eur", "quantity_100kg",
                "value_eur_million", "mass_thousand_t", "unit_value_eur_per_t"])
    for (p, fl, per), v in sorted(monthly.items(), key=lambda x: (x[0][0], x[0][1], x[0][2])):
        if v["eur"] is None and v["q100"] is None:
            continue  # period with no observation at all: not written, never zero-filled
        eur_m, kt, uv = conv(v["eur"], v["q100"])
        w.writerow([p, fl, FLOW_NAME[fl], per,
                    "" if v["eur"] is None else f"{v['eur']:.2f}",
                    "" if v["q100"] is None else f"{v['q100']:.2f}",
                    "" if eur_m is None else f"{eur_m:.4f}",
                    "" if kt is None else f"{kt:.4f}",
                    "" if uv is None else f"{uv:.2f}"])

# ---------- like-for-like YTD ----------
last_month_by_series = {}
for p in ("72", "7208", "7204"):
    for fl in ("1", "2"):
        months_2026 = sorted(per for (pp, ff, per), v in monthly.items()
                             if pp == p and ff == fl and per.startswith("2026") and v["eur"] is not None and v["q100"] is not None)
        last_month_by_series[(p, fl)] = months_2026

# Common cutoff: the latest month for which ALL six series have 2026 data
common = None
for lst in last_month_by_series.values():
    s = set(lst)
    common = s if common is None else common & s
common_months = sorted(common)
print("common 2026 months across all series:", common_months)


def ytd(p, fl, months26):
    months25 = [m.replace("2026", "2025") for m in months26]
    out = {}
    for yr, ms in (("2025", months25), ("2026", months26)):
        miss = [m for m in ms if monthly.get((p, fl, m), {}).get("eur") is None or monthly[(p, fl, m)]["q100"] is None]
        if miss:
            return None, f"missing observations in {yr}: {miss}"
        eur = sum(monthly[(p, fl, m)]["eur"] for m in ms)
        q = sum(monthly[(p, fl, m)]["q100"] for m in ms)
        out[yr] = conv(eur, q)
    return out, ""


rows = []
for p in ("72", "7208", "7204"):
    for fl in ("1", "2"):
        res, note = ytd(p, fl, common_months)
        if res is None:
            rows.append([p, FLOW_NAME[fl], note] + [""] * 10)
            continue
        v25, m25, u25 = res["2025"]
        v26, m26, u26 = res["2026"]
        pct = lambda a, b: (b / a - 1) * 100
        rows.append([p, FLOW_NAME[fl], f"{common_months[0]}..{common_months[-1]} vs same months 2025",
                     f"{v25:.2f}", f"{v26:.2f}", f"{pct(v25, v26):+.1f}",
                     f"{m25:.2f}", f"{m26:.2f}", f"{pct(m25, m26):+.1f}",
                     f"{u25:.0f}", f"{u26:.0f}", f"{pct(u25, u26):+.1f}"])

with open(OUT / "ytd_comparison.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["product_cn", "flow", "window",
                "value_eur_m_2025", "value_eur_m_2026", "value_pct_change",
                "mass_kt_2025", "mass_kt_2026", "mass_pct_change",
                "unit_value_eur_t_2025", "unit_value_eur_t_2026", "unit_value_pct_change"])
    w.writerows(rows)

# ---------- cumulative YTD for every cutoff month (so any cutoff can be quoted) ----------
with open(OUT / "ytd_by_cutoff.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["product_cn", "flow", "cutoff_2026", "months",
                "value_eur_m_2025", "value_eur_m_2026", "value_pct_change",
                "mass_kt_2025", "mass_kt_2026", "mass_pct_change",
                "unit_value_eur_t_2025", "unit_value_eur_t_2026", "unit_value_pct_change"])
    for p in ("72", "7208", "7204"):
        for fl in ("1", "2"):
            for i in range(1, len(common_months) + 1):
                ms = common_months[:i]
                res, note = ytd(p, fl, ms)
                if res is None:
                    continue
                v25, m25, u25 = res["2025"]
                v26, m26, u26 = res["2026"]
                pct = lambda a, b: (b / a - 1) * 100
                w.writerow([p, FLOW_NAME[fl], ms[-1], i, f"{v25:.2f}", f"{v26:.2f}", f"{pct(v25, v26):+.1f}",
                            f"{m25:.2f}", f"{m26:.2f}", f"{pct(m25, m26):+.1f}",
                            f"{u25:.0f}", f"{u26:.0f}", f"{pct(u25, u26):+.1f}"])

# ---------- monthly YoY table ----------
with open(OUT / "monthly_yoy.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["product_cn", "flow", "month", "value_eur_m_2025", "value_eur_m_2026", "value_pct",
                "mass_kt_2025", "mass_kt_2026", "mass_pct", "uv_eur_t_2025", "uv_eur_t_2026", "uv_pct"])
    for p in ("72", "7208", "7204"):
        for fl in ("1", "2"):
            for m26 in common_months:
                m25 = m26.replace("2026", "2025")
                a = monthly.get((p, fl, m25)); b = monthly.get((p, fl, m26))
                if not a or not b or None in (a["eur"], a["q100"], b["eur"], b["q100"]):
                    continue
                va, ka, ua = conv(a["eur"], a["q100"]); vb, kb, ub = conv(b["eur"], b["q100"])
                w.writerow([p, FLOW_NAME[fl], m26[5:], f"{va:.2f}", f"{vb:.2f}", f"{(vb/va-1)*100:+.1f}",
                            f"{ka:.2f}", f"{kb:.2f}", f"{(kb/ka-1)*100:+.1f}", f"{ua:.0f}", f"{ub:.0f}", f"{(ub/ua-1)*100:+.1f}"])

# ---------- net trade (exports - imports), chapter 72, extra-EU, YTD ----------
with open(OUT / "net_trade_ch72_ytd.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["window", "year", "exports_eur_m", "imports_eur_m", "net_eur_m", "exports_kt", "imports_kt", "net_kt"])
    for yr in ("2025", "2026"):
        ms = [m.replace("2026", yr) for m in common_months]
        ex_e = sum(monthly[("72", "2", m)]["eur"] for m in ms); ex_q = sum(monthly[("72", "2", m)]["q100"] for m in ms)
        im_e = sum(monthly[("72", "1", m)]["eur"] for m in ms); im_q = sum(monthly[("72", "1", m)]["q100"] for m in ms)
        exv, exk, _ = conv(ex_e, ex_q); imv, imk, _ = conv(im_e, im_q)
        w.writerow([f"{ms[0]}..{ms[-1]}", yr, f"{exv:.2f}", f"{imv:.2f}", f"{exv-imv:.2f}", f"{exk:.2f}", f"{imk:.2f}", f"{exk-imk:.2f}"])

# ---------- annual cross-check ----------
annual = {}
for f in sorted(RAW.glob("annual_*.json")):
    d, ids, rows_a = decode(f)
    for key, v in rows_a.items():
        k = dict(zip(ids, key))
        annual.setdefault((k["product"], k["flow"], k["time"]), {})[k["indicators"]] = v

with open(OUT / "annual_crosscheck_2025.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["product_cn", "flow", "year", "annual_value_eur_m", "annual_mass_kt", "sum_of_12_months_value_eur_m",
                "sum_of_12_months_mass_kt", "diff_value_eur_m", "diff_mass_kt"])
    for p in ("72", "7208"):
        for fl in ("1", "2"):
            for yr in ("2025",):
                a = annual.get((p, fl, yr), {})
                ms = [f"{yr}-{i:02d}" for i in range(1, 13)]
                sv = sum(monthly[(p, fl, m)]["eur"] for m in ms)
                sq = sum(monthly[(p, fl, m)]["q100"] for m in ms)
                av, ak, _ = conv(a.get("VALUE_IN_EUROS"), a.get("QUANTITY_IN_100KG"))
                mv, mk, _ = conv(sv, sq)
                w.writerow([p, FLOW_NAME[fl], yr, f"{av:.2f}", f"{ak:.2f}", f"{mv:.2f}", f"{mk:.2f}", f"{mv-av:+.4f}", f"{mk-ak:+.4f}"])

# also write annual values 2024/2025 tidy
with open(OUT / "annual_2024_2025.csv", "w", newline="", encoding="utf-8") as fh:
    w = csv.writer(fh)
    w.writerow(["product_cn", "flow", "year", "value_eur_m", "mass_kt", "unit_value_eur_t"])
    for (p, fl, yr), a in sorted(annual.items()):
        e, k, u = conv(a.get("VALUE_IN_EUROS"), a.get("QUANTITY_IN_100KG"))
        if e is None or k is None:
            continue  # annual 2026 is empty (year not complete): not written, never zero-filled
        w.writerow([p, FLOW_NAME[fl], yr, f"{e:.2f}", f"{k:.2f}", f"{u:.2f}"])

(OUT / "run_meta.json").write_text(json.dumps(dict(common_months=common_months, files=meta), indent=2), encoding="utf-8")
print("done")
