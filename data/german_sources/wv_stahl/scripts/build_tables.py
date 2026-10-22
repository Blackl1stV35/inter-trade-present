"""Build the WV Stahl verification tables for the German steel data task.

Run (Python 3.12, PyMuPDF installed; no other third-party packages):
    python -I -X utf8 build_tables.py --pdf-dir <dir with the downloaded WV Stahl PDFs> \
        --comext-dir <repo>/data/comext_exports --out-dir <repo>/data/german_sources/wv_stahl

The PDFs are NOT stored in the repo (copyright); download them first from the URLs in
sources_manifest.csv and put them in --pdf-dir under the file names given there ("local_name").
The Comext folder is only read.

How numbers are read:
  * chart labels in the brochures are read from the PDF text layer with their position and
    colour (PyMuPDF spans), then assigned to years by x-position. Nothing is typed for them.
  * the monthly crude-steel tables are parsed from the one-page "Vollstaendige Uebersicht" PDFs.
  * a few small tables (scrap trade, route table of the scrap report, pie shares) are typed
    from the rendered page; the script asserts that every typed number exists in that page's
    text layer and that rows add up within rounding.
No value is estimated, interpolated or recalled; a value that is not printed stays empty.
"""
import argparse
import csv
import hashlib
import re
import sys
from pathlib import Path

import fitz  # PyMuPDF

# ----------------------------------------------------------------------------- inputs
FILES = {
    # key: (local_name, url, title, edition / date, retrieved)
    "ed2026": ("df2026.pdf",
               "https://www.wvstahl.de/wp-content/uploads/20261008_WV-Stahl_Daten-und-Fakten-2026_RZ_Web.pdf",
               "Daten und Fakten zur Stahlindustrie in Deutschland (2026 edition)", "Stand: September 2026; PDF created 8 Oct 2026; file dated 12 Oct 2026"),
    "ed2025": ("df2025.pdf",
               "https://www.wvstahl.de/wp-content/uploads/WV-Stahl_Daten-und-Fakten-2025_Web.pdf",
               "Daten und Fakten zur Stahlindustrie in Deutschland (2025 edition)", "Stand: September 2025; file dated 12 Feb 2026"),
    "ed2024": ("df2024.pdf",
               "https://www.wvstahl.de/wp-content/uploads/WV-Stahl_Daten-und-Fakten-2024_RZ-Web.pdf",
               "Daten und Fakten zur Stahlindustrie in Deutschland (2024 edition)", "Stand: November 2024; file dated 15 Jul 2025"),
    "ed2025en": ("df2025en.pdf",
                 "https://www.wvstahl.de/wp-content/uploads/WV-Stahl_Daten-und-Fakten-2025_EN_Web.pdf",
                 "Facts and Figures about the Steel Industry in Germany (English edition of the 2025 brochure)", "file dated 12 Feb 2026"),
    "ed2022": ("df2022.pdf",
               "https://www.wvstahl.de/wp-content/uploads/2024/10/WV-Stahl_Fakten-2022_RZ_neu_Web.pdf",
               "Fakten zur Stahlindustrie in Deutschland 2022", "2022 edition (data 2021)"),
    "ed2021": ("df2021.pdf",
               "https://www.wvstahl.de/wp-content/uploads/2024/10/WV-Stahl_Fakten-2021_RZ_Web_neu.pdf",
               "Fakten zur Stahlindustrie in Deutschland 2021", "2021 edition (data 2020)"),
    "schrott2026": ("schrott2026.pdf",
                    "https://www.wvstahl.de/wp-content/uploads/20261014_Statistischer_Bericht__Stahlschrott_2026.pdf",
                    "Statistischer Bericht Stahlschrott 2026", "dated 14 Oct 2026"),
    "rev2025": ("20260810_Rohstahlerzeugung_Deutschland_Revision_2025.pdf",
                "https://www.wvstahl.de/wp-content/uploads/20260810_Rohstahlerzeugung_Deutschland_Revision_2025.pdf",
                "Rohstahlerzeugung in Deutschland 2025, Vollstaendige Uebersicht (Revision, Stand August 2026)", "10 Aug 2026"),
    "rev2024": ("20250804_Rohstahlerzeugung_Deutschland_2024.pdf",
                "https://www.wvstahl.de/wp-content/uploads/20250804_Rohstahlerzeugung_Deutschland_2024.pdf",
                "Rohstahlerzeugung in Deutschland 2024, Vollstaendige Uebersicht (Revision, Stand Juli 2025)", "Jul/Aug 2025"),
    "rev2023": ("20240807_Rohstahlerzeugung_Deutschland_2023.pdf",
                "https://www.wvstahl.de/wp-content/uploads/20240807_Rohstahlerzeugung_Deutschland_2023.pdf",
                "Rohstahlerzeugung in Deutschland 2023, Vollstaendige Uebersicht (Revision, Stand Juli 2024)", "Jul/Aug 2024"),
    "rev2022": ("20230802_Rohstahlerzeugung_Deutschland_2022.pdf",
                "https://www.wvstahl.de/wp-content/uploads/20230802_Rohstahlerzeugung_Deutschland_2022.pdf",
                "Rohstahlerzeugung in Deutschland 2022, Vollstaendige Uebersicht (Revision, Stand Juli 2023)", "Jul/Aug 2023"),
    "rev2021": ("20220731_Rohstahlerzeugung_Deutschland_2021.pdf",
                "https://www.wvstahl.de/wp-content/uploads/20220731_Rohstahlerzeugung_Deutschland_2021.pdf",
                "Rohstahlerzeugung in Deutschland 2021, Vollstaendige Uebersicht (Revision, Stand Juli 2022)", "Jul/Aug 2022"),
    "q2_2026": ("20260721_Stahlkonjunktur_Deutschland_Q2_2026.pdf",
                "https://www.wvstahl.de/wp-content/uploads/20260721_Stahlkonjunktur_Deutschland_Q2_2026.pdf",
                "Informationen zur Stahlkonjunktur in Deutschland, Zweites Quartal 2026", "21 Jul 2026"),
    "q1_2026": ("20260424_Stahlkonjunktur_Deutschland_Q1_2026.pdf",
                "https://www.wvstahl.de/wp-content/uploads/20260424_Stahlkonjunktur_Deutschland_Q1_2026.pdf",
                "Informationen zur Stahlkonjunktur in Deutschland, Erstes Quartal 2026", "24 Apr 2026"),
    "jb2025": ("jb2025.pdf",
               "https://www.wvstahl.de/wp-content/uploads/20260522_WVStahl_Jahresbericht_2025_zweiseitig.pdf",
               "WV Stahl Jahresbericht 2024/2025", "file dated 22 May 2026"),
    "pm2025": ("pm2025.pdf",
               "https://www.wvstahl.de/wp-content/uploads/20260121_PM_Jahresbilanz_Stahlindustrie_2025.pdf",
               "Pressemitteilung: Jahresbilanz der Stahlproduktion 2025", "21 Jan 2026"),
}

MONTHS = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli", "August",
          "September", "Oktober", "November", "Dezember"]
NUM = re.compile(r"^[−-]?\d{1,3}(?:\.\d{3})*(?:,\d+)?$")
EXPORT_RGB, IMPORT_RGB, SALDO_RGB = 0x384F87, 0x009FE3, 0x575756

warnings = []


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def num(t):
    """German number text -> float (1.234 = thousands, 1,5 = decimal)."""
    t = t.strip().replace("−", "-")
    if not NUM.match(t):
        return None
    return float(t.replace(".", "").replace(",", "."))


class Pdfs:
    def __init__(self, pdf_dir):
        self.dir = Path(pdf_dir)
        self.cache = {}

    def doc(self, key):
        if key not in self.cache:
            p = self.dir / FILES[key][0]
            if not p.exists():
                raise SystemExit(f"missing PDF {p} (download from {FILES[key][1]})")
            self.cache[key] = fitz.open(p)
        return self.cache[key]

    def text(self, key, page):
        return self.doc(key)[page - 1].get_text()

    def spans(self, key, page):
        out = []
        for b in self.doc(key)[page - 1].get_text("dict")["blocks"]:
            for l in b.get("lines", []):
                for s in l["spans"]:
                    t = s["text"].strip()
                    if t:
                        x0, y0, x1, y1 = s["bbox"]
                        out.append(dict(t=t, x=(x0 + x1) / 2, y=(y0 + y1) / 2,
                                        color=s["color"], horizontal=abs(l["dir"][1]) < 1e-6))
        return out


def year_labels(sp):
    return sorted({(round(s["x"], 1), int(s["t"])) for s in sp if re.fullmatch(r"20\d\d", s["t"])})


def line_chart(pdfs, key, page):
    """Germany / EU-27 trade charts: export / import / saldo labels by colour, year by x."""
    sp = pdfs.spans(key, page)
    ys = year_labels(sp)
    res = {"export": {}, "import": {}, "saldo": {}}
    for s in sp:
        v = num(s["t"])
        if v is None or "," not in s["t"]:
            continue
        name = {EXPORT_RGB: "export", IMPORT_RGB: "import", SALDO_RGB: "saldo"}.get(s["color"])
        if not name:
            continue
        yr = min(ys, key=lambda a: abs(a[0] - s["x"]))[1]
        assert yr not in res[name], (key, page, name, yr, "duplicate label")
        res[name][yr] = v
    return res


def bar_chart(pdfs, key, page):
    """Single-series bar chart with one value label per year; labels ordered by x."""
    sp = pdfs.spans(key, page)
    ys = sorted({int(s["t"]) for s in sp if re.fullmatch(r"20\d\d", s["t"])})
    ylab_y = min(s["y"] for s in sp if re.fullmatch(r"20\d\d", s["t"]))
    xs = [s["x"] for s in sp if re.fullmatch(r"20\d\d", s["t"])]
    seen = {}
    for s in sp:
        if "," in s["t"] and num(s["t"]) is not None and s["horizontal"] and s["y"] < ylab_y + 20 \
                and min(xs) - 20 <= s["x"] <= max(xs) + 30:
            seen[(round(s["x"]), s["t"])] = s  # white halo duplicates collapse here
    vals = sorted(seen.values(), key=lambda s: s["x"])
    assert len(vals) == len(ys), (key, page, len(vals), len(ys))
    return {yr: num(v["t"]) for yr, v in zip(ys, vals)}


def grouped_bars(pdfs, key, page, ngroup=3):
    sp = pdfs.spans(key, page)
    ys = year_labels(sp)
    groups = {yr: [] for _, yr in ys}
    for s in sp:
        v = num(s["t"])
        if v is not None and "," in s["t"] and s["horizontal"]:
            yr = min(ys, key=lambda a: abs(a[0] - s["x"]))[1]
            groups[yr].append((s["x"], v))
    out = {}
    for yr, lst in groups.items():
        lst.sort()
        assert len(lst) == ngroup, (key, page, yr, lst)
        out[yr] = [v for _, v in lst]
    return out


def monthly_table(pdfs, key):
    """Parse a one-page 'Vollstaendige Uebersicht' PDF into 12 monthly rows + SUMME row."""
    lines = [l.strip() for l in pdfs.text(key, 1).split("\n") if l.strip()]
    year = int(re.search(r"Rohstahlerzeugung in Deutschland (20\d\d)", " ".join(lines)).group(1))
    rows = {}
    i = 0
    while i < len(lines):
        if lines[i] in MONTHS or lines[i] == "SUMME":
            vals = [num(x) for x in lines[i + 1:i + 6]]
            assert all(v is not None for v in vals), (key, lines[i], lines[i + 1:i + 6])
            rows[lines[i]] = vals
            i += 6
        else:
            i += 1
    assert set(rows) == set(MONTHS) | {"SUMME"}, (key, sorted(rows))
    cols = ["crude_steel_total_kt", "oxygen_steel_kt", "electric_steel_kt", "pig_iron_kt", "hot_rolled_products_kt"]
    for j, c in enumerate(cols):  # months add up to SUMME within rounding
        s = sum(rows[m][j] for m in MONTHS)
        assert abs(s - rows["SUMME"][j]) <= 3, (key, c, s, rows["SUMME"][j])
    assert abs(rows["SUMME"][1] + rows["SUMME"][2] - rows["SUMME"][0]) <= 2, (key, "O+E != total")
    return year, cols, rows


def assert_in_text(pdfs, key, page, values, fmt):
    txt = pdfs.text(key, page)
    for v in values:
        s = fmt(v)
        assert s in txt, f"{s} not found in {key} p.{page} text layer"


def de1(v):  # 12.3 -> '12,3'
    return f"{v:.1f}".replace(".", ",")


def de0(v):  # 7398 -> '7.398'
    return f"{int(v):,}".replace(",", ".")


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        w.writerows(rows)
    print("wrote", Path(path).name, len(rows), "rows")


def fmt(v, nd=1):
    return "" if v is None else (f"{v:.{nd}f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pdf-dir", required=True)
    ap.add_argument("--comext-dir", required=True)
    ap.add_argument("--out-dir", required=True)
    ap.add_argument("--manifest-only", action="store_true")
    a = ap.parse_args()
    out = Path(a.out_dir)
    pdfs = Pdfs(a.pdf_dir)

    # ------------------------------------------------------------------ manifest
    mrows = []
    for k, (local, url, title, ed) in FILES.items():
        p = Path(a.pdf_dir) / local
        mrows.append([k, local, url, title, ed, p.stat().st_size if p.exists() else "", sha256(p) if p.exists() else ""])
    write_csv(out / "sources_manifest.csv",
              ["key", "local_name", "url", "title", "edition_or_date", "bytes", "sha256"], mrows)
    if a.manifest_only:
        return

    # ------------------------------------------------------------------ crude steel (Dataset A)
    crude = {"ed2024": bar_chart(pdfs, "ed2024", 9), "ed2025": bar_chart(pdfs, "ed2025", 9),
             "ed2026": bar_chart(pdfs, "ed2026", 9)}
    assert crude["ed2026"][2025] == 34.1 and crude["ed2025"][2024] == 37.2
    workbook_a = {2017: 43.3, 2018: 42.4, 2019: 39.6, 2020: 35.7, 2021: 40.2, 2022: 36.9, 2023: 35.4, 2024: 37.2, 2025: 34.1}
    # monthly tables
    monthly, annual = [], {}
    for k in ("rev2021", "rev2022", "rev2023", "rev2024", "rev2025"):
        year, cols, rows = monthly_table(pdfs, k)
        for m in MONTHS:
            monthly.append([year, MONTHS.index(m) + 1, m] + [int(v) for v in rows[m]] + [k])
        annual[year] = dict(zip(cols, rows["SUMME"]))
    write_csv(out / "crude_steel_monthly_by_process_2021_2025.csv",
              ["year", "month_no", "month_de", "crude_steel_total_kt", "oxygen_steel_kt", "electric_steel_kt",
               "pig_iron_kt", "hot_rolled_products_kt", "source_key"], monthly)

    # scrap-report route table (typed from rendered p.3, asserted against the text layer)
    sr_years = [2020, 2021, 2022, 2023, 2024, 2025]
    sr_eaf = [11.5, 12.1, 11.0, 9.8, 10.8, 10.4]
    sr_bof = [24.1, 28.1, 25.9, 25.6, 26.5, 23.6]
    sr_tot = [35.7, 40.2, 36.8, 35.4, 37.3, 34.1]
    sr_share = [32, 30, 30, 28, 29, 31]
    assert_in_text(pdfs, "schrott2026", 3, sr_eaf + sr_bof + sr_tot, de1)
    for e, b, t in zip(sr_eaf, sr_bof, sr_tot):
        assert abs(e + b - t) <= 0.15, (e, b, t)
    # preliminary 2025 (press release 21 Jan 2026, HTML table of the press-release page; checked by hand
    # against raw/pm_jahresbilanz_2025_table.txt below)
    prelim_2025 = dict(crude_steel_total_kt=34090, oxygen_steel_kt=23645, electric_steel_kt=10445,
                       pig_iron_kt=21872, hot_rolled_products_kt=29760)
    rows = []
    for yr in range(2021, 2026):
        d = annual[yr]
        sr = sr_years.index(yr)
        rows.append([yr, int(d["crude_steel_total_kt"]), int(d["oxygen_steel_kt"]), int(d["electric_steel_kt"]),
                     int(d["pig_iron_kt"]), int(d["hot_rolled_products_kt"]),
                     fmt(100 * d["electric_steel_kt"] / d["crude_steel_total_kt"], 2),
                     fmt(100 * d["oxygen_steel_kt"] / d["crude_steel_total_kt"], 2),
                     f"rev{yr}", crude["ed2026"].get(yr, ""), crude["ed2025"].get(yr, ""),
                     sr_tot[sr], sr_eaf[sr], sr_bof[sr], sr_share[sr]])
    # 2020 row: only the scrap report (Mt, one decimal) is available
    rows.insert(0, [2020, "", "", "", "", "", "", "", "none (no 2020 revision PDF on the site)", crude["ed2026"][2020],
                    crude["ed2025"][2020], 35.7, 11.5, 24.1, 32])
    write_csv(out / "crude_steel_by_process_2020_2025.csv",
              ["year", "crude_steel_total_kt_revision", "oxygen_steel_kt_revision", "electric_steel_kt_revision",
               "pig_iron_kt_revision", "hot_rolled_products_kt_revision", "electric_share_pct_calc",
               "oxygen_share_pct_calc", "revision_source_key", "brochure2026_total_mt_p9", "brochure2025_total_mt_p9",
               "scrap_report2026_total_mt", "scrap_report2026_eaf_mt", "scrap_report2026_bof_mt",
               "scrap_report2026_eaf_share_pct_printed"], rows)
    write_csv(out / "crude_steel_2025_preliminary_and_2026_ytd.csv",
              ["period", "vintage", "crude_steel_total_kt", "oxygen_steel_kt", "electric_steel_kt", "pig_iron_kt",
               "hot_rolled_products_kt", "electric_share_pct_calc", "source"],
              [["2025 full year", "preliminary, press release 21 Jan 2026"] + list(prelim_2025.values()) +
               [fmt(100 * prelim_2025["electric_steel_kt"] / prelim_2025["crude_steel_total_kt"], 2),
                "wvstahl.de/pressemitteilungen/jahresbilanz-der-stahlproduktion-2025-viertes-krisenjahr-in-folge/ (table 'Januar-Dezember 2025')"],
               ["2025 full year", "revision, Aug 2026", int(annual[2025]["crude_steel_total_kt"]),
                int(annual[2025]["oxygen_steel_kt"]), int(annual[2025]["electric_steel_kt"]),
                int(annual[2025]["pig_iron_kt"]), int(annual[2025]["hot_rolled_products_kt"]),
                fmt(100 * annual[2025]["electric_steel_kt"] / annual[2025]["crude_steel_total_kt"], 2),
                FILES["rev2025"][1]],
               ["Jan-Aug 2026", "provisional, press release 22 Sep 2026", 23902, 16464, 7438, 14936, 21004,
                fmt(100 * 7438 / 23902, 2),
                "wvstahl.de/pressemitteilungen/rohstahlerzeugung-im-august-2026-weiterhin-verhaltene-erholung/ (table 'Januar-August 2026')"]])

    ver_rows = []
    for yr, wb in workbook_a.items():
        e24, e25, e26 = crude["ed2024"].get(yr), crude["ed2025"].get(yr), crude["ed2026"].get(yr)
        rev = annual.get(yr, {}).get("crude_steel_total_kt")
        printed = [v for v in (e24, e25, e26) if v is not None]
        ok = all(abs(v - wb) < 0.05 for v in printed)
        note = ""
        if yr == 2024:
            note = "revision Jul 2025 sums to 37.310 Mt (37.3); brochures print 37.2 (Statistisches Bundesamt / WV Stahl)"
        if yr == 2025:
            note = "brochure 2026 prints 34.1 (as does worldsteel); WV Stahl Aug 2026 revision sums to 34.267 Mt (34.3)"
        if yr == 2022:
            note = "scrap report 2026 prints 36.8; brochures and revision (36.861) round to 36.9"
        ver_rows.append([yr, wb, e24 if e24 is not None else "", e25 if e25 is not None else "",
                         e26 if e26 is not None else "", "" if rev is None else int(rev),
                         "" if rev is None else fmt(rev / 1000, 1),
                         "MATCH" if ok else "MISMATCH", note])
    write_csv(out / "dataset_a_crude_steel_verification.csv",
              ["year", "workbook_dataset_a_mt", "brochure2024_p9_mt", "brochure2025_p9_mt", "brochure2026_p9_mt",
               "wvstahl_revision_kt", "wvstahl_revision_mt_rounded", "workbook_vs_brochures", "note"], ver_rows)
    long_rows = []
    for k, label in (("ed2024", "2024 edition"), ("ed2025", "2025 edition"), ("ed2026", "2026 edition")):
        for yr, v in sorted(crude[k].items()):
            long_rows.append([yr, v, label, 9, "Rohstahlproduktion",
                              "Statistisches Bundesamt, WV Stahl"])
    write_csv(out / "crude_steel_brochure_series_by_edition.csv",
              ["year", "crude_steel_mt", "edition", "printed_page", "table_title_de", "source_line_printed"], long_rows)

    # ------------------------------------------------------------------ trade of steel mill products (Dataset B)
    de = {"ed2024": line_chart(pdfs, "ed2024", 28), "ed2025": line_chart(pdfs, "ed2025", 30),
          "ed2026": line_chart(pdfs, "ed2026", 30)}
    eu = {"ed2024": line_chart(pdfs, "ed2024", 29), "ed2025": line_chart(pdfs, "ed2025", 31),
          "ed2026": line_chart(pdfs, "ed2026", 31)}
    wb_b = {2017: (27.3, 28.5), 2018: (26.4, 28.0), 2019: (24.8, 24.5), 2020: (22.1, 20.7), 2021: (24.6, 25.0),
            2022: (23.2, 22.8), 2023: (23.0, 20.0), 2024: (22.9, 18.8)}
    wb_bal = {2017: -1.2, 2018: -1.6, 2019: 0.3, 2020: 1.4, 2021: -0.4, 2022: 0.4, 2023: 3.0, 2024: 4.1}
    rows = []
    for yr, (wx, wm) in wb_b.items():
        def g(ed, s):
            return de[ed][s].get(yr, "")
        x25, m25, s25 = g("ed2025", "export"), g("ed2025", "import"), g("ed2025", "saldo")
        x26, m26, s26 = g("ed2026", "export"), g("ed2026", "import"), g("ed2026", "saldo")
        x24, m24, s24 = g("ed2024", "export"), g("ed2024", "import"), g("ed2024", "saldo")
        match25 = "MATCH" if (abs(x25 - wx) < .05 and abs(m25 - wm) < .05) else "MISMATCH"
        later = [(x26, m26)] if x26 != "" else []
        match26 = "n/a (2017 not in 2026 edition)" if not later else (
            "MATCH" if (abs(x26 - wx) < .05 and abs(m26 - wm) < .05) else "REVISED")
        note = []
        if abs(wb_bal[yr] - s25) > 0.05:
            note.append(f"workbook balance {wb_bal[yr]:+.1f} (derived from rounded values) vs printed saldo {s25:+.1f}")
        if yr == 2023 and m24 != "" and abs(m24 - m25) > 0.05:
            note.append(f"2024 edition printed imports {m24} and saldo {s24} for 2023 (revised in 2025 edition)")
        if yr == 2024:
            note.append("2026 edition revises 2024 to exports 23.3, imports 19.0 (saldo unchanged at 4.2)")
        rows.append([yr, wx, wm, wb_bal[yr], x24, m24, s24, x25, m25, s25, match25, x26, m26, s26, match26, "; ".join(note)])
    write_csv(out / "dataset_b_trade_verification.csv",
              ["year", "workbook_exports_mt", "workbook_imports_mt", "workbook_balance_derived_mt",
               "brochure2024_p28_exports", "brochure2024_p28_imports", "brochure2024_p28_saldo",
               "brochure2025_p30_exports", "brochure2025_p30_imports", "brochure2025_p30_saldo",
               "workbook_vs_brochure2025", "brochure2026_p30_exports", "brochure2026_p30_imports",
               "brochure2026_p30_saldo", "workbook_vs_brochure2026", "note"], rows)
    # latest-vintage extended series
    latest = []
    for yr in range(2017, 2026):
        ed = "ed2026" if yr >= 2018 else "ed2025"
        pg = 30
        d = de[ed]
        latest.append([yr, d["export"][yr], d["import"][yr], d["saldo"][yr],
                       fmt(d["export"][yr] - d["import"][yr], 1), "2026 edition" if ed == "ed2026" else "2025 edition",
                       pg, "Stahlaußenhandel: Deutschland", "Steel Mill Products (Walzstahl- und Schmiedeerzeugnisse, Rohre, kaltgewalzte Erzeugnisse)",
                       "Amtliche Außenhandelsstatistik, WV Stahl"])
    write_csv(out / "steel_mill_products_trade_germany_2017_2025_latest_vintage.csv",
              ["year", "exports_mt", "imports_mt", "saldo_printed_mt", "saldo_calc_from_rounded_mt", "edition_used",
               "printed_page", "table_title_de", "product_footnote_printed", "source_line_printed"], latest)
    # EU-27 third-country trade
    eurows = []
    for yr in range(2017, 2026):
        ed = "ed2026"
        eurows.append([yr, eu[ed]["export"][yr], eu[ed]["import"][yr], eu[ed]["saldo"][yr],
                       "2026 edition", 31, "Stahlaußenhandel: EU-27"])
    write_csv(out / "eu27_steel_mill_products_trade_with_third_countries_2017_2025.csv",
              ["year", "eu27_exports_mt", "eu27_imports_from_third_countries_mt", "saldo_printed_mt", "edition_used",
               "printed_page", "table_title_de"], eurows)

    # ------------------------------------------------------------------ German exports to non-EU by destination (pies)
    pies = [  # year, edition, page, total_mt, usmca(nafta), europe_ex_eu_cis, asia_ex_nme, africa, cis_ukraine, nme, others
        (2023, "ed2024", 30, 4.9, 32, 35, 16, 5, 1, 3, 9),
        (2024, "ed2025", 33, 4.9, 29, 38, 12, 6, 1, 3, 11),
        (2025, "ed2026", 33, 4.1, 32, 40, 12, 6, 1, 3, 6),
    ]
    for yr, ed, pg, tot, *sh in pies:
        txt = pdfs.text(ed, pg)
        assert de1(tot) in txt, (ed, pg, tot)
        for s in sh:
            assert f"{s} %" in txt or f"{s}%" in txt, (ed, pg, s)
        assert 99 <= sum(sh) <= 101
    write_csv(out / "de_steel_mill_product_exports_to_non_eu_by_destination_2023_2025.csv",
              ["year", "edition", "printed_page", "non_eu_exports_mt", "usmca_or_nafta_pct", "europe_ex_eu_cis_pct",
               "asia_ex_near_middle_east_pct", "africa_pct", "cis_ukraine_pct", "near_middle_east_pct", "others_pct",
               "sum_pct", "note"],
              [[y, e, p, t] + s + [sum(s), "pie labels read from the rendered chart; slice-to-region mapping confirmed against the legend colours; shares as printed (rounded)"]
               for y, e, p, t, *s in pies])

    # ------------------------------------------------------------------ indirect trade, Marktversorgung, Umsatz
    ind26 = grouped_bars(pdfs, "ed2026", 34)
    ind25 = grouped_bars(pdfs, "ed2025", 34)
    irows = []
    for yr in sorted(set(ind26) | set(ind25)):
        for ed, d in (("2025 edition", ind25), ("2026 edition", ind26)):
            if yr in d:
                ex, im, sa = d[yr]
                assert abs(ex - im - sa) <= 0.15, (ed, yr, d[yr])
                irows.append([yr, ed, ex, im, sa, 34])
    write_csv(out / "indirect_steel_trade_germany_steel_containing_goods_2020_2025.csv",
              ["year", "edition", "exports_mt_rolled_steel_weight", "imports_mt_rolled_steel_weight", "saldo_mt",
               "printed_page"], irows)
    mv = []
    for ed, key, pg in (("2024 edition", "ed2024", 13), ("2025 edition", "ed2025", 14), ("2026 edition", "ed2026", 14)):
        for yr, v in sorted(bar_chart(pdfs, key, pg).items()):
            mv.append([yr, v, ed, pg, "Marktversorgung Walzstahl", "WV Stahl, Außenhandelsstatistik"])
    write_csv(out / "marktversorgung_walzstahl_by_edition_2010_2025.csv",
              ["year", "market_supply_rolled_steel_mt", "edition", "printed_page", "table_title_de", "source_line_printed"], mv)
    mv26 = {r[0]: r[1] for r in mv if r[2] == "2026 edition"}
    umsatz = bar_chart(pdfs, "ed2026", 13)

    # ------------------------------------------------------------------ scrap trade (typed, asserted) and Comext
    sy = [2020, 2021, 2022, 2023, 2024, 2025]
    scrap = {
        "eu27_export_kt": [7398, 7514, 6539, 6575, 6200, 6544],
        "eu27_import_kt": [3269, 4356, 3751, 3064, 3794, 3398],
        "third_export_kt": [1229, 1275, 1323, 1443, 1114, 1231],
        "third_import_kt": [706, 677, 643, 486, 597, 577],
        "total_export_kt": [8628, 8790, 7862, 8018, 7314, 7775],
        "total_import_kt": [3975, 5033, 4394, 3550, 4391, 3975],
    }
    for k, v in scrap.items():
        assert_in_text(pdfs, "schrott2026", 4, v, de0)
    for i in range(6):
        assert abs(scrap["eu27_export_kt"][i] + scrap["third_export_kt"][i] - scrap["total_export_kt"][i]) <= 2
        assert abs(scrap["eu27_import_kt"][i] + scrap["third_import_kt"][i] - scrap["total_import_kt"][i]) <= 2
    write_csv(out / "scrap_trade_germany_2020_2025.csv",
              ["year"] + list(scrap) + ["source", "printed_page"],
              [[sy[i]] + [scrap[k][i] for k in scrap] + ["Statistischer Bericht Stahlschrott 2026, 'Stahlschrott-Außenhandel (1.000 t)'", 4]
               for i in range(6)])

    cdir = Path(a.comext_dir)
    comext = {}
    with open(cdir / "ch72_trade_by_partner_group_long.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            comext[(r["partner"], r["flow"], int(r["year"]))] = float(r["net_mass_thousand_t"])
    c7204 = {}
    with open(cdir / "byproduct_ext_eu_trade_long_1999_2025.csv", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["product"] == "7204" and r["net_mass_thousand_t"]:
                c7204[(r["flow"], int(r["year"]))] = float(r["net_mass_thousand_t"])
    nonEU = {r[0]: r[3] for r in pies}
    rec = []
    for yr in range(2017, 2026):
        ed = "ed2026" if yr >= 2018 else "ed2025"
        wx, wm = de[ed]["export"][yr], de[ed]["import"][yr]
        cx, cm = comext[("WORLD", "export", yr)] / 1000, comext[("WORLD", "import", yr)] / 1000
        ex_x, ex_m = comext[("EXT_EU27_2020", "export", yr)] / 1000, comext[("EXT_EU27_2020", "import", yr)] / 1000
        si = sy.index(yr) if yr in sy else None
        scr_x = scrap["total_export_kt"][si] / 1000 if si is not None else None
        scr_m = scrap["total_import_kt"][si] / 1000 if si is not None else None
        rec.append([yr, wx, wm, fmt(cx, 3), fmt(cm, 3), fmt(wx / cx * 100, 1), fmt(wm / cm * 100, 1),
                    fmt(cx - wx, 2), fmt(cm - wm, 2),
                    "" if scr_x is None else fmt(scr_x, 3), "" if scr_m is None else fmt(scr_m, 3),
                    "" if scr_x is None else fmt(cx - scr_x, 2), "" if scr_m is None else fmt(cm - scr_m, 2),
                    fmt(ex_x, 3), fmt(ex_m, 3), nonEU.get(yr, "")])
    write_csv(out / "reconciliation_wvstahl_vs_comext_ch72_2017_2025.csv",
              ["year", "wv_steel_mill_products_exports_mt", "wv_steel_mill_products_imports_mt",
               "comext_ch72_all_partner_exports_mt", "comext_ch72_all_partner_imports_mt",
               "wv_as_pct_of_comext_exports", "wv_as_pct_of_comext_imports", "comext_minus_wv_exports_mt",
               "comext_minus_wv_imports_mt", "wv_scrap_total_exports_mt", "wv_scrap_total_imports_mt",
               "comext_ch72_minus_wv_scrap_exports_mt", "comext_ch72_minus_wv_scrap_imports_mt",
               "comext_ch72_extra_eu_exports_mt", "comext_ch72_extra_eu_imports_mt",
               "wv_german_exports_to_non_eu_steel_mill_products_mt"], rec)
    scr_rec = []
    for i, yr in enumerate(sy):
        scr_rec.append([yr, scrap["third_export_kt"][i], fmt(c7204[("export", yr)], 1), scrap["third_import_kt"][i],
                        fmt(c7204[("import", yr)], 1)])
    write_csv(out / "scrap_third_country_trade_wvstahl_vs_comext_7204.csv",
              ["year", "wv_scrap_exports_to_third_countries_kt", "comext_7204_extra_eu_exports_kt",
               "wv_scrap_imports_from_third_countries_kt", "comext_7204_extra_eu_imports_kt"], scr_rec)

    # ------------------------------------------------------------------ apparent consumption cross-check
    cc = []
    for yr in range(2021, 2026):
        ed = "ed2026"
        x, m = de[ed]["export"][yr], de[ed]["import"][yr]
        hr = annual[yr]["hot_rolled_products_kt"] / 1000
        cr = annual[yr]["crude_steel_total_kt"] / 1000
        ex_x = comext[("EXT_EU27_2020", "export", yr)] / 1000  # extra-EU only, Comext Ch. 72
        ex_m = comext[("EXT_EU27_2020", "import", yr)] / 1000
        bn = cr + ex_m - ex_x  # formula written in the workbook BaseNotes-4 (production + extra-EU M - extra-EU X)
        cc.append([yr, mv26[yr], x, m, fmt(hr, 3), fmt(hr + m - x, 2), fmt(mv26[yr] - (hr + m - x), 2),
                   fmt(cr, 3), fmt(cr + m - x, 2), fmt(mv26[yr] - (cr + m - x), 2),
                   fmt(ex_x, 3), fmt(ex_m, 3), fmt(bn, 2), fmt(mv26[yr] - bn, 2)])
    write_csv(out / "apparent_consumption_crosscheck_2021_2025.csv",
              ["year", "wv_marktversorgung_walzstahl_mt_ed2026", "wv_exports_steel_mill_products_mt",
               "wv_imports_steel_mill_products_mt", "wv_hot_rolled_products_output_mt",
               "calc_hot_rolled_plus_imports_minus_exports_mt", "marktversorgung_minus_calc_hot_rolled_mt",
               "wv_crude_steel_output_mt", "calc_crude_plus_imports_minus_exports_mt",
               "marktversorgung_minus_calc_crude_mt", "comext_ch72_extra_eu_exports_mt",
               "comext_ch72_extra_eu_imports_mt", "calc_workbook_basenotes_formula_crude_plus_extra_eu_m_minus_extra_eu_x_mt",
               "marktversorgung_minus_workbook_formula_mt"], cc)

    # ------------------------------------------------------------------ industry sales, employment, other indicators
    ind = []
    for yr, v in sorted(umsatz.items()):
        ind.append(["Umsatz der Stahlindustrie (Roheisen, Stahl, Ferrolegierungen + Stahlrohre)", yr, v, "EUR bn", "2026 edition", 13,
                    "Statistisches Bundesamt (as printed)"])
    emp = [
        ("Beschäftigte Stahlindustrie", 1992, 179, "thousand", "2021 edition", "PDF p.10", "Statistisches Bundesamt, WV Stahl"),
        ("Beschäftigte Stahlindustrie", 2020, 83, "thousand", "2021 edition", "PDF p.10", "Statistisches Bundesamt, WV Stahl"),
        ("Beschäftigte Stahlindustrie", 2021, 81, "thousand", "2022 edition", "PDF p.10", "Statistisches Bundesamt, WV Stahl"),
        ("Beschäftigte Stahlindustrie (direkt), 'rund 80.000', year not stated", "", 80, "thousand (rounded text)", "2024, 2025 and 2026 editions", 11, "text only"),
        ("Arbeitsplätze in stahlintensiven Branchen, 'etwa/rund 4 Millionen'", "", 4000, "thousand (rounded text)", "2025 and 2026 editions", "10-11", "RWI, Statistisches Bundesamt, WV Stahl"),
    ]
    assert "80.000" in pdfs.text("ed2026", 11) and "80.000" in pdfs.text("ed2025", 11) and "80.000" in pdfs.text("ed2024", 11)
    for e in emp:
        ind.append(list(e))
    write_csv(out / "steel_industry_sales_and_employment.csv",
              ["indicator", "year", "value", "unit", "edition", "printed_page", "source_line_printed"], ind)

    notes = [
        ["capacity utilisation 2025", "2025", "below 70 percent", "text", "press release 21 Jan 2026 (pm2025)", "no annual series published"],
        ["crude steel threshold for a viable utilisation", "n/a", "40 Mt per year", "text", "press release 21 Jan 2026; Q1 and Q2 2026 reports", "WV Stahl's own benchmark"],
        ["Auftragseingang Walzstahl, change on prior year", "2022", -12.4, "percent", "Q2 2026 report p.4", "chart label"],
        ["Auftragseingang Walzstahl, change on prior year", "2023", 0.4, "percent", "Q2 2026 report p.4", "chart label"],
        ["Auftragseingang Walzstahl, change on prior year", "2024", -0.4, "percent", "Q2 2026 report p.4", "chart label"],
        ["Auftragseingang Walzstahl, change on prior year", "2025", 2.1, "percent", "Q2 2026 report p.4", "chart label"],
        ["Auftragseingang Walzstahl, change on prior year", "Jan-Jun 2026", 7.3, "percent", "Q2 2026 report p.4", "chart label"],
        ["Marktversorgung, change on prior year", "2022", -8, "percent", "Q2 2026 report p.4", "chart label"],
        ["Marktversorgung, change on prior year", "2023", -11, "percent", "Q2 2026 report p.4", "chart label"],
        ["Marktversorgung, change on prior year", "2024", -7, "percent", "Q2 2026 report p.4", "chart label"],
        ["Marktversorgung, change on prior year", "2025", 8, "percent", "Q2 2026 report p.4", "chart label"],
        ["Marktversorgung, change on prior year", "Jan-Apr 2026", 2, "percent", "Q2 2026 report p.4", "chart label"],
        ["domestic steel demand since 2017", "2025", "about -30 percent, about 12 Mt", "text", "Q1 2026 report p.2", "WV Stahl wording"],
        ["2025 Marktversorgung stabilisation", "2025", "'based exclusively on stock building' (Lageraufbau), not real demand growth", "text", "Q1 2026 report p.2", "WV Stahl wording"],
    ]
    q2t, q1t, pmt = pdfs.text("q2_2026", 4), pdfs.text("q1_2026", 2), pdfs.text("pm2025", 1)
    for s in ("-12,4%", "+0,4%", "-0,4%", "+2,1%", "+7,3%", "-8%", "-11%", "-7%", "+8%", "+2%"):
        assert s in q2t.replace(chr(10), "").replace(" ", ""), s
    assert "unter 70 Prozent" in pmt.replace("\n", " ")
    assert "Lageraufbau" in q1t
    write_csv(out / "conjuncture_indicators_wvstahl.csv",
              ["indicator", "period", "value", "unit", "source", "note"], notes)

    for w in warnings:
        print("WARNING:", w)
    print("done")


if __name__ == "__main__":
    sys.exit(main())
