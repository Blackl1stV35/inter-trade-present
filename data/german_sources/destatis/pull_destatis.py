#!/usr/bin/env python
"""
Destatis (Statistisches Bundesamt) pull for the Germany iron-and-steel / EU ETS + CBAM deck.

Run:   python -I -X utf8 pull_destatis.py [--out DIR] [--cache DIR] [--repo DIR]

What it does
  * Reads GENESIS-Online tables through the public JSON endpoints that the GENESIS-Online web app itself
    calls (https://genesis.destatis.de/genesis/api/rest/...).  No login, no credentials, no token, no
    bot-challenge handling.  (The documented genesisWS API needs a login and is NOT used.)
  * Writes extracted tables as CSV (UTF-8, comma separated, missing values left empty) plus manifest.json.
  * Never fills a missing observation: GENESIS flags such cells with "..." / "." / "x" / "/" and a
    placeholder value 0.0 - these become EMPTY cells here.  Flag "-" means "nothing / exactly zero".
  * Raw cubes are cached in --cache (default: system temp) and are NOT written to the repo.

Units (GENESIS): foreign-trade mass in tonnes (t), foreign-trade value in EUR 1,000;
                 national accounts in bn EUR (nominal / chain-linked volume) or chain index 2020=100;
                 production index 2021=100; producer price index 2021=100.
"""
import argparse, collections, copy, csv, datetime, hashlib, json, os, re, sys, tempfile, time
import urllib.error, urllib.request

BASE = "https://genesis.destatis.de/genesis/api/rest"
UA = "Mozilla/5.0 (university coursework data pull)"
MISSING = {"...", ".", "x", "/"}          # value unknown / later / secret  -> keep EMPTY
RETRIEVED = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

# EU27 (2020 composition, fixed over time) minus Germany = 26 partner codes in the GENESIS country list
EU26 = ["STLAH017", "STLAH068", "STLAH008", "STLAH053", "STLAH014", "STLAH001", "STLAH009", "STLAH007",
        "STLAH005", "STLAH092", "STLAH054", "STLAH055", "STLAH018", "STLAH046", "STLAH003", "STLAH015",
        "STLAH060", "STLAH010", "STLAH066", "STLAH013", "STLAH063", "STLAH091", "STLAH011", "STLAH061",
        "STLAH064", "STLAH600"]
EU_ALL = EU26 + ["STLAH959"]              # 959 = "countries not specified (intra-Community trade)"


# --------------------------------------------------------------------------------------------- client
class Client:
    def __init__(self, cache_dir):
        self.cache = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
        self.manifest = []

    @staticmethod
    def _http(url, body=None, timeout=600):
        data = None
        headers = {"User-Agent": UA, "Accept": "application/json"}
        if body is not None:
            data = json.dumps(body, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
            headers["Content-Type"] = "application/json"
        last = None
        for attempt in range(3):
            try:
                req = urllib.request.Request(url, data=data, headers=headers)
                with urllib.request.urlopen(req, timeout=timeout) as resp:
                    return resp.read()
            except urllib.error.HTTPError as e:
                if e.code in (413, 400, 404):
                    raise
                last = e
            except Exception as e:                      # transient network error
                last = e
            time.sleep(5 * (attempt + 1))
        raise last

    def get_json(self, path):
        return json.loads(self._http(f"{BASE}/{path}"))

    def structure(self, code):
        p = os.path.join(self.cache, f"struct_{code}.json")
        if not os.path.exists(p):
            open(p, "wb").write(self._http(f"{BASE}/tables/{code}/structure"))
        return json.load(open(p, encoding="utf-8"))

    @staticmethod
    def _attr(a):
        return {"attribute": a, "childVariable": None, "childAttributes": [], "isHidden": False, "isDocumentary": False}

    def cube(self, code, swap=None, select=None, note=""):
        """Raw cube JSON for a table. swap: replace the innermost row classification by this main variable.
        select: {mainVariable: [codes]} (the server honours it only for large tables, limit ~40,000 cells)."""
        tag = hashlib.sha1(json.dumps([swap, select], sort_keys=True).encode()).hexdigest()[:12]
        p = os.path.join(self.cache, f"cube_{code}_{tag}.json")
        st = self.structure(code)
        if not os.path.exists(p):
            state = copy.deepcopy(st["initialState"])
            if swap:
                vb = state["variableBlocks"]
                tcode = [k for k, v in vb.items() if v["mainVariable"] == swap][0]

                def walk(nodes):
                    for n in nodes:
                        if tcode in n.get("possibleBlocks", []):
                            n["blockCode"] = tcode
                            return True
                        if walk(n.get("childBlocks", [])):
                            return True
                    return False
                ts = state["tableStructure"]
                assert walk(ts["rowTitle"]) or walk(ts["colTitle"]), swap
            if select:
                for bv in state["variableBlocks"].values():
                    if bv["mainVariable"] in select:
                        bv["mainAttributes"] = [self._attr(a) for a in select[bv["mainVariable"]]]
                used = set()

                def walk2(nodes):
                    for n in nodes:
                        used.add(n["blockCode"])
                        walk2(n.get("childBlocks", []))
                for k in ("filter", "colTitle", "rowTitle"):
                    walk2(state["tableStructure"][k])
                for bk, bv in state["variableBlocks"].items():
                    if bk not in used:                   # keep request body small
                        bv["mainAttributes"] = bv["mainAttributes"][:1]
            t0 = time.time()
            raw = self._http(f"{BASE}/tables/{code}/data", body=state)
            open(p, "wb").write(raw)
            secs = round(time.time() - t0)
            fetched_at = RETRIEVED
        else:
            raw = open(p, "rb").read()
            secs = 0
            # cache hit: the file's modification time is the time the response was downloaded
            fetched_at = datetime.datetime.fromtimestamp(os.path.getmtime(p), datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
        d = json.loads(raw)
        blk = d["data"][0]
        self.manifest.append({
            "table": code, "table_label_de": " ".join(st["table"]["label"]["de"].split()),
            "table_lastChange_utc": st["table"]["lastChange"], "row_swap": swap,
            "selection": ({k: (v if len(v) <= 6 else f"{len(v)} codes: {v[0]}..{v[-1]}") for k, v in select.items()} if select else None),
            "dimensions": dict(zip(blk["id"], blk["size"])), "response_bytes": len(raw),
            "response_sha256": hashlib.sha256(raw).hexdigest(), "fetch_seconds": secs,
            "retrieved_utc": fetched_at, "note": note,
            "request": f"POST {BASE}/tables/{code}/data (body = table initialState from GET .../structure, modified as listed)"})
        return d


def decode(d, keep=None):
    """Yield dict rows {dim: code, 'measure':..., 'value':..., 'status':...} from a GENESIS cube."""
    blk = d["data"][0]
    ids, size, dim = blk["id"], blk["size"], blk["dimension"]
    values, status = blk["value"], blk.get("status")
    inv = {n: {i: c for c, i in dim[n]["category"]["index"].items()} for n in ids}
    strides, s = [], 1
    for sz in reversed(size):
        strides.append(s)
        s *= sz
    strides.reverse()
    sel = []
    for n, sz in zip(ids, size):
        idxs = list(range(sz))
        if keep and n in keep:
            idxs = [i for i in idxs if inv[n][i] in keep[n]]
        sel.append(idxs)
    import itertools
    for combo in itertools.product(*sel):
        flat = sum(i * st for i, st in zip(combo, strides))
        row = {n: inv[n][i] for n, i in zip(ids, combo)}
        stt = status[flat] if status else None
        row["status"] = stt
        row["value"] = None if (stt in MISSING or values[flat] is None) else values[flat]
        c = row.get("content", "")
        row["measure"] = c.split("$")[0]
        row["func"] = c.split("$")[1] if "$" in c else ""
        yield row


def labels(st, var):
    vv = st["variableValues"]
    out = {}
    for c in st["variables"][var]["variableValues"]:
        l = vv[c]["label"]
        out[c] = (" ".join((l.get("de") or "").split()), " ".join((l.get("en") or l.get("de") or "").split()))
    return out


def write_csv(path, header, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(["" if v is None else v for v in r])
    print(f"  wrote {os.path.basename(path)} ({len(rows)} rows)")


def r1(x, n=1):
    return None if x is None else round(x, n)


def div(a, b, n=1):
    return None if a is None or b is None else round(a / b, n)


def ym(y, m):
    return f"{y}-{m[-2:]}"


# ------------------------------------------------------------------------------------------- section 1
def trade_annual(cl, out):
    """51000-0005 (annual, commodity systems): chapter 72 'Eisen und Stahl', 73, headings 72xx/73xx, groupings."""
    st = cl.structure("51000-0005")
    # --- chapters 72 and 73 (WAM2)
    d = cl.cube("51000-0005", note="WAM2 chapters, all partners, 2008-2025")
    T = collections.defaultdict(dict)
    S = {}
    for r in decode(d, keep={"WAM2": {"WA72", "WA73"}}):
        T[(r["WAM2"], r["JAHR"])][r["measure"]] = r["value"]
        S[(r["WAM2"], r["JAHR"], r["measure"])] = r["status"]
    rows = []
    for (code, y) in sorted(T, key=lambda k: (k[0], k[1])):
        t = T[(code, y)]
        xkt, mkt = t["GEWA"] / 1e3, t["GEWE"] / 1e3
        xe, me = t["WERTA"] / 1e3, t["WERTE"] / 1e3
        sts = {S[(code, y, m)] for m in ("GEWA", "GEWE", "WERTA", "WERTE")}
        rows.append([code, "Eisen und Stahl (Ch. 72)" if code == "WA72" else "Waren aus Eisen oder Stahl (Ch. 73)", y,
                     r1(t["GEWA"], 1), r1(t["GEWE"], 1), r1(xkt, 1), r1(mkt, 1), r1(t["WERTA"], 0), r1(t["WERTE"], 0),
                     r1(xe, 1), r1(me, 1), r1(xkt - mkt, 1), r1(xe - me, 1), r1(xe * 1e6 / (xkt * 1e3), 1), r1(me * 1e6 / (mkt * 1e3), 1),
                     "+".join(sorted(sts))])
    write_csv(os.path.join(out, "trade_ch72_ch73_annual_2008_2025.csv"),
              ["wv_code", "label", "year", "exports_t", "imports_t", "exports_kt", "imports_kt", "exports_eur_thousand", "imports_eur_thousand",
               "exports_eur_m", "imports_eur_m", "balance_kt", "balance_eur_m", "export_unit_value_eur_per_t", "import_unit_value_eur_per_t", "status(e=final,p=provisional)"], rows)
    ch72 = {y: T[("WA72", y)] for (c, y) in T if c == "WA72"}

    # --- headings WAM4 (all partners) ---------------------------------------------------------
    d4 = cl.cube("51000-0005", swap="WAM4", note="WAM4 4-digit headings, all partners")
    lab4 = labels(st, "WAM4")
    H = {}
    HS = {}
    for r in decode(d4):
        h = r["WAM4"]
        if h.startswith("WA72") or h.startswith("WA73"):
            H[(h, r["JAHR"], r["measure"])] = r["value"]
            HS[(h, r["JAHR"])] = r["status"]
    heads72 = sorted({k[0] for k in H if k[0].startswith("WA72")})
    # check headings add up to chapter total
    for y in ("2017", "2024", "2025"):
        for m in ("GEWA", "GEWE", "WERTA", "WERTE"):
            tot = sum(H[(h, y, m)] or 0 for h in heads72)
            # published headings are rounded individually (0.1 t / EUR 1,000) -> allow 0.001 % relative slack
            assert abs(tot - ch72[y][m]) <= max(5.0, 1e-5 * ch72[y][m]), ("headings do not add to chapter 72", y, m, tot, ch72[y][m])

    # --- steel groupings -----------------------------------------------------------------------
    G = []

    def grp(swap, var, codes, system):
        dd = cl.cube("51000-0005", swap=swap, note=f"{var} grouping, all partners")
        lab = labels(cl.structure("51000-0005"), var)
        tt = collections.defaultdict(dict)
        ss = {}
        for r in decode(dd, keep={var: set(codes)}):
            tt[(r[var], r["JAHR"])][r["measure"]] = r["value"]
            ss[(r[var], r["JAHR"])] = r["status"]
        for (c, y) in sorted(tt):
            t = tt[(c, y)]
            G.append([system, c, lab[c][0], lab[c][1], y, r1(t["GEWA"] / 1e3, 1), r1(t["GEWE"] / 1e3, 1),
                      r1(t["WERTA"] / 1e3, 1), r1(t["WERTE"] / 1e3, 1), ss[(c, y)]])
    grp("SITC2A", "SITC2A", ["SITC-67"], "SITC rev.4 2-digit")
    grp("GP19B4", "GP19B4", ["GP19-2410", "GP19-2420", "GP19-2431", "GP19-2432", "GP19-2433", "GP19-2434"], "GP2019 4-digit")
    grp("GP19B2", "GP19B2", ["GP19-24", "GP19-25"], "GP2019 2-digit")
    grp("EGW3", "EGW3", ["EGW641", "EGW642", "EGW643", "EGW644", "EGW751", "EGW753", "EGW755", "EGW757", "EGW759"], "EGW 2002 3-digit")
    # derived 'steel-mill-product-like' aggregate (NOT a Destatis aggregate): HS 7207-7229 + 7304-7306
    comp = [h for h in heads72 if "WA7207" <= h <= "WA7229"] + ["WA7304", "WA7305", "WA7306"]
    for y in sorted({k[1] for k in H}):
        if any(H.get((h, y, "GEWA")) is None for h in comp):
            continue
        s = {m: sum(H[(h, y, m)] for h in comp) for m in ("GEWA", "GEWE", "WERTA", "WERTE")}
        G.append(["DERIVED (team construction, not a Destatis aggregate)", "HS7207-7229+7304-7306",
                  "Semi-finished, flat, long, wire products of iron/steel incl. stainless & alloy (7207-7229) plus tubes 7304-7306",
                  "Semi-finished, flat, long, wire products of iron/steel incl. stainless & alloy (7207-7229) plus tubes 7304-7306",
                  y, r1(s["GEWA"] / 1e3, 1), r1(s["GEWE"] / 1e3, 1), r1(s["WERTA"] / 1e3, 1), r1(s["WERTE"] / 1e3, 1), HS[("WA7207", y)]])
    for code in ("WA72", "WA73"):
        for y in sorted(k[1] for k in T if k[0] == code):
            t = T[(code, y)]
            G.append(["Warenverzeichnis 2-digit", code, "Eisen und Stahl" if code == "WA72" else "Waren aus Eisen oder Stahl",
                      "Iron and steel" if code == "WA72" else "Articles of iron or steel", y, r1(t["GEWA"] / 1e3, 1), r1(t["GEWE"] / 1e3, 1),
                      r1(t["WERTA"] / 1e3, 1), r1(t["WERTE"] / 1e3, 1), S[(code, y, "GEWA")]])
    write_csv(os.path.join(out, "trade_steel_groupings_annual_2008_2025.csv"),
              ["classification", "code", "label_de", "label_en", "year", "exports_kt", "imports_kt", "exports_eur_m", "imports_eur_m", "status"], G)
    return ch72, H, HS, heads72, lab4


def trade_eu_split(cl, out, ch72):
    """51000-0007: chapter 72 by country -> EU27(2020) partners vs non-EU. Imports by ORIGIN, exports by DESTINATION."""
    d = cl.cube("51000-0007", note="WAM2 x STLAH, all partners (country detail); keep WA72")
    A = collections.defaultdict(float)
    n_dash = collections.Counter()
    for r in decode(d, keep={"WAM2": {"WA72"}}):
        if r["value"] is None:
            raise SystemExit(f"unexpected missing country cell {r}")
        g = "EU27" if r["STLAH"] in EU_ALL else "NON_EU"
        A[(r["JAHR"], r["measure"], g)] += r["value"]
        A[(r["JAHR"], r["measure"], "ALL")] += r["value"]
        if r["status"] == "-":
            n_dash[r["JAHR"]] += 1
    rows = []
    split = {}
    for y in sorted({k[0] for k in A}):
        for m in ("GEWA", "GEWE", "WERTA", "WERTE"):
            assert abs(A[(y, m, "ALL")] - ch72[y][m]) <= max(20.0, 1e-5 * ch72[y][m]), ("country sum != chapter total", y, m, A[(y, m, "ALL")], ch72[y][m])
        v = lambda m, g: A[(y, m, g)]
        split[y] = {"xe": v("GEWA", "EU27") / 1e3, "xn": v("GEWA", "NON_EU") / 1e3, "me": v("GEWE", "EU27") / 1e3, "mn": v("GEWE", "NON_EU") / 1e3,
                    "xeV": v("WERTA", "EU27") / 1e3, "xnV": v("WERTA", "NON_EU") / 1e3, "meV": v("WERTE", "EU27") / 1e3, "mnV": v("WERTE", "NON_EU") / 1e3}
        s = split[y]
        rows.append([y, r1(s["xe"]), r1(s["xn"]), r1(s["me"]), r1(s["mn"]), r1(s["xeV"]), r1(s["xnV"]), r1(s["meV"]), r1(s["mnV"]),
                     div(100 * s["xn"], s["xe"] + s["xn"]), div(100 * s["mn"], s["me"] + s["mn"]),
                     r1(s["xn"] - s["mn"]), r1(s["xnV"] - s["mnV"]), r1(s["xe"] - s["me"]), r1(s["xeV"] - s["meV"])])
    write_csv(os.path.join(out, "trade_ch72_eu27_vs_noneu_annual_2008_2025.csv"),
              ["year", "exports_to_EU27_kt", "exports_to_nonEU_kt", "imports_EU27_origin_kt", "imports_nonEU_origin_kt",
               "exports_to_EU27_eur_m", "exports_to_nonEU_eur_m", "imports_EU27_origin_eur_m", "imports_nonEU_origin_eur_m",
               "nonEU_share_of_exports_pct_mass", "nonEU_share_of_imports_pct_mass",
               "nonEU_balance_kt(exports-imports)", "nonEU_balance_eur_m", "EU27_balance_kt", "EU27_balance_eur_m"], rows)
    return split


def trade_headings(cl, out, H, HS, heads72, lab4):
    """EU27 vs non-EU by 4-digit heading, 2017-2025: all-partner (0005) minus EU27 partners (0009, 27 codes)."""
    st9 = cl.structure("51000-0009")
    yrs = [str(y) for y in range(2017, 2026)]
    wam4 = [c for c in st9["variables"]["WAM4"]["variableValues"] if c.startswith("WA72")]
    E = collections.defaultdict(float)
    for chunk in (wam4[:17], wam4[17:]):
        d = cl.cube("51000-0009", select={"JAHR": yrs, "WAM4": chunk, "STLAH": EU_ALL},
                    note="chapter-72 headings x EU27 partner countries (cells < 40,000 limit)")
        for r in decode(d):
            if r["value"] is not None:
                E[(r["WAM4"], r["JAHR"], r["measure"])] += r["value"]
    rows = []
    for h in heads72:
        if h in ("WA7296", "WA7297", "WA7298", "WA7299"):
            continue                                              # estimation positions, no country allocation
        for y in yrs:
            for flow, mq, mv in (("export", "GEWA", "WERTA"), ("import", "GEWE", "WERTE")):
                aq, av = H[(h, y, mq)], H[(h, y, mv)]
                eq, ev = E[(h, y, mq)], E[(h, y, mv)]
                rows.append([h, lab4[h][0], lab4[h][1], y, flow, r1(aq / 1e3), r1(eq / 1e3), r1((aq - eq) / 1e3), r1(av / 1e3), r1(ev / 1e3), r1((av - ev) / 1e3), HS[(h, y)]])
    write_csv(os.path.join(out, "trade_ch72_headings_eu27_vs_noneu_2017_2025.csv"),
              ["wv_heading", "label_de", "label_en", "year", "flow", "all_partners_kt", "EU27_kt", "nonEU_kt(derived=all-EU27; imports=origin, exports=destination)",
               "all_partners_eur_m", "EU27_eur_m", "nonEU_eur_m(derived)", "status"], rows)
    return E


def trade_monthly(cl, out):
    """51000-0006 monthly chapters 72/73 (all partners) and 51000-0008 monthly by country (EU/non-EU)."""
    d = cl.cube("51000-0006", note="monthly WAM2, all partners; keep WA72, WA73")
    M = collections.defaultdict(dict)
    S = {}
    for r in decode(d, keep={"WAM2": {"WA72", "WA73"}}):
        M[(r["WAM2"], r["JAHR"], r["MONAT"])][r["measure"]] = r["value"]
        S[(r["WAM2"], r["JAHR"], r["MONAT"])] = r["status"]
    rows = []
    for (c, y, m) in sorted(M):
        t = M[(c, y, m)]
        f = lambda k, dv: None if t[k] is None else r1(t[k] / dv, 1)
        rows.append([c, ym(y, m), y, int(m[-2:]), f("GEWA", 1e3), f("GEWE", 1e3), f("WERTA", 1e3), f("WERTE", 1e3),
                     None if t["GEWA"] is None else r1((t["GEWA"] - t["GEWE"]) / 1e3, 1),
                     None if t["WERTA"] is None else r1((t["WERTA"] - t["WERTE"]) / 1e3, 1), S[(c, y, m)] if t["GEWA"] is not None else "missing(...)"])
    write_csv(os.path.join(out, "trade_ch72_ch73_monthly_2008_2026.csv"),
              ["wv_code", "month", "year", "month_no", "exports_kt", "imports_kt", "exports_eur_m", "imports_eur_m", "balance_kt", "balance_eur_m", "status"], rows)
    # year-to-date comparison on common months
    last = max((y, m) for (c, y, m), t in M.items() if c == "WA72" and t["GEWA"] is not None)
    ly, lm = last
    n = int(lm[-2:])
    mname = ['', 'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'][n]
    ytd = []
    ytdv = {}
    for code in ("WA72", "WA73", "WA72+WA73"):
        parts = ["WA72", "WA73"] if code == "WA72+WA73" else [code]
        for y in range(2019, int(ly) + 1):
            ms = [f"MONAT{i:02d}" for i in range(1, n + 1)]
            if any(M[(pc, str(y), m)]["GEWA"] is None for pc in parts for m in ms):
                continue
            tot = {k: sum(M[(pc, str(y), m)][k] for pc in parts for m in ms) for k in ("GEWA", "GEWE", "WERTA", "WERTE")}
            ytdv[(code, y)] = tot
            ytd.append([code, y, f"Jan-{mname}", r1(tot["GEWA"] / 1e3), r1(tot["GEWE"] / 1e3), r1(tot["WERTA"] / 1e3), r1(tot["WERTE"] / 1e3)])
    write_csv(os.path.join(out, "trade_ytd_by_year.csv"),
              ["wv_code", "year", "months", "exports_kt", "imports_kt", "exports_eur_m", "imports_eur_m"], ytd)
    # validation against Destatis' own press release PD25_380_51 (20 Oct 2025): 'Eisen und Stahl' = chapters 72+73, Jan-Aug 2025
    if ("WA72+WA73", 2025) in ytdv and ("WA72+WA73", 2024) in ytdv and n == 8:
        a, b = ytdv[("WA72+WA73", 2025)], ytdv[("WA72+WA73", 2024)]
        chk = [["exports Jan-Aug 2025, EUR bn", 39.9, r1(a["WERTA"] / 1e6, 2)],
               ["imports Jan-Aug 2025, EUR bn", 34.0, r1(a["WERTE"] / 1e6, 2)],
               ["exports change vs Jan-Aug 2024, %", -4.8, r1(100 * (a["WERTA"] / b["WERTA"] - 1), 2)],
               ["imports change vs Jan-Aug 2024, %", -2.7, r1(100 * (a["WERTE"] / b["WERTE"] - 1), 2)]]
        write_csv(os.path.join(out, "check_destatis_press_release_PD25_380_51_vs_genesis.csv"),
                  ["quantity (chapters 72+73, Jan-Aug)", "published in PD25_380_51 (20 Oct 2025)", "recomputed from GENESIS 51000-0006 (current vintage)"], chk)

    # monthly by country (EU / non-EU) for 2023..2026
    rows2 = []
    A = collections.defaultdict(float)
    miss = collections.Counter()
    for yr in ("2023", "2024", "2025"):
        dd = cl.cube("51000-0008", select={"JAHR": [yr], "WAM2": ["WA72"]}, note=f"monthly WAM2=WA72 x STLAH, {yr}")
        for r in decode(dd):
            if r["value"] is None:
                miss[(r["JAHR"], r["MONAT"])] += 1
                continue
            g = "EU27" if r["STLAH"] in EU_ALL else "NON_EU"
            A[(r["JAHR"], r["MONAT"], r["measure"], g)] += r["value"]
    dd = cl.cube("51000-0008", note="monthly default state = year 2026, all WAM2, all countries; keep WA72")
    for r in decode(dd, keep={"WAM2": {"WA72"}}):
        if r["value"] is None:
            miss[(r["JAHR"], r["MONAT"])] += 1
            continue
        g = "EU27" if r["STLAH"] in EU_ALL else "NON_EU"
        A[(r["JAHR"], r["MONAT"], r["measure"], g)] += r["value"]
    months = sorted({(k[0], k[1]) for k in A} | set(miss))
    for (y, m) in months:
        if miss[(y, m)]:
            rows2.append([ym(y, m), y, int(m[-2:])] + [None] * 8 + ["missing(...)"])
            continue
        v = lambda me, g: A[(y, m, me, g)] / 1e3
        rows2.append([ym(y, m), y, int(m[-2:]), r1(v("GEWA", "EU27")), r1(v("GEWA", "NON_EU")), r1(v("GEWE", "EU27")), r1(v("GEWE", "NON_EU")),
                      r1(v("WERTA", "EU27")), r1(v("WERTA", "NON_EU")), r1(v("WERTE", "EU27")), r1(v("WERTE", "NON_EU")), "p/e as published"])
    write_csv(os.path.join(out, "trade_ch72_monthly_eu27_vs_noneu_2023_2026.csv"),
              ["month", "year", "month_no", "exports_to_EU27_kt", "exports_to_nonEU_kt", "imports_EU27_origin_kt", "imports_nonEU_origin_kt",
               "exports_to_EU27_eur_m", "exports_to_nonEU_eur_m", "imports_EU27_origin_eur_m", "imports_nonEU_origin_eur_m", "status"], rows2)
    # YTD non-EU, last common month
    have = [(y, m) for (y, m) in months if not miss[(y, m)] and y == "2026"]
    n2 = max(int(m[-2:]) for (y, m) in have)
    ytd2 = []
    for y in ("2023", "2024", "2025", "2026"):
        ms = [f"MONAT{i:02d}" for i in range(1, n2 + 1)]
        g = lambda me, grp: sum(A[(y, m, me, grp)] for m in ms) / 1e3
        ytd2.append([y, f"Jan-{n2:02d}", r1(g("GEWA", "EU27")), r1(g("GEWA", "NON_EU")), r1(g("GEWE", "EU27")), r1(g("GEWE", "NON_EU")),
                     r1(g("WERTA", "NON_EU")), r1(g("WERTE", "NON_EU"))])
    write_csv(os.path.join(out, "trade_ch72_ytd_eu27_vs_noneu.csv"),
              ["year", "months(1..n)", "exports_to_EU27_kt", "exports_to_nonEU_kt", "imports_EU27_origin_kt", "imports_nonEU_origin_kt",
               "exports_to_nonEU_eur_m", "imports_nonEU_origin_eur_m"], ytd2)


def trade_total(cl, out):
    d = cl.cube("51000-0001", note="total foreign trade, annual 1950-2025")
    T = collections.defaultdict(dict)
    S = {}
    for r in decode(d):
        T[r["JAHR"]][r["measure"]] = r["value"]
        S[r["JAHR"]] = r["status"]
    rows = []
    for y in sorted(T):
        if int(y) < 2000:
            continue
        t = T[y]
        if any(t[k] is None for k in ("WERTA", "WERTE")):
            continue
        rows.append([y, r1(t["WERTA"] / 1e6, 1), r1(t["WERTE"] / 1e6, 1), r1((t["WERTA"] - t["WERTE"]) / 1e6, 1),
                     r1(t["GEWA"] / 1e6, 2), r1(t["GEWE"] / 1e6, 2), S[y]])
    write_csv(os.path.join(out, "trade_total_goods_annual_2000_2025.csv"),
              ["year", "exports_eur_bn", "imports_eur_bn", "balance_eur_bn", "exports_mass_mt", "imports_mass_mt", "status"], rows)
    return T


def crosscheck_comext_world(out, ch72, repo):
    """All-partner chapter 72 totals: Destatis vs Eurostat Comext 'WORLD' (read-only repo file)."""
    p = os.path.join(repo, "data", "comext_exports", "slide_table_2017_2025.csv")
    if not os.path.exists(p):
        return
    rows = []
    for r in csv.DictReader(open(p, encoding="utf-8")):
        y = r["year"]
        if y not in ch72:
            continue
        cx, cm = float(r["comext_ch72_world_exports_mt"]) * 1e3, float(r["comext_ch72_world_imports_mt"]) * 1e3
        dx, dm = ch72[y]["GEWA"] / 1e3, ch72[y]["GEWE"] / 1e3
        rows.append([y, r1(dx), r1(cx), r1(dx - cx), div(100 * (dx - cx), cx, 3), r1(dm), r1(cm), r1(dm - cm), div(100 * (dm - cm), cm, 3)])
    write_csv(os.path.join(out, "crosscheck_destatis_vs_comext_world_ch72.csv"),
              ["year", "destatis_exports_kt", "comext_WORLD_exports_kt", "diff_kt", "diff_pct", "destatis_imports_kt", "comext_WORLD_imports_kt", "diff_kt", "diff_pct"], rows)


def crosscheck_comext(out, split, repo):
    """Compare Destatis non-EU split with the Eurostat Comext direct extra-EU series already in the repo (read-only)."""
    cdir = os.path.join(repo, "data", "comext_exports")
    fx, fm = os.path.join(cdir, "ch72_extra_eu_exports_1999_2025.csv"), os.path.join(cdir, "ch72_extra_eu_imports_1999_2025.csv")
    if not (os.path.exists(fx) and os.path.exists(fm)):
        print("  (Comext files not found - cross-check skipped)")
        return
    rd = lambda p: {r["year"]: r for r in csv.DictReader(open(p, encoding="utf-8"))}
    cx, cm = rd(fx), rd(fm)
    rows = []
    for y in sorted(split):
        if y not in cx or y not in cm:
            continue
        s = split[y]
        cxq, cmq = float(cx[y]["net_mass_thousand_t"]), float(cm[y]["net_mass_thousand_t"])
        cxv, cmv = float(cx[y]["value_eur_million"]), float(cm[y]["value_eur_million"])
        rows.append([y, r1(s["xn"]), r1(cxq), r1(s["xn"] - cxq), div(100 * (s["xn"] - cxq), cxq, 2),
                     r1(s["xnV"]), r1(cxv), r1(s["xnV"] - cxv),
                     r1(s["mn"]), r1(cmq), r1(s["mn"] - cmq), div(100 * cmq, s["mn"], 1),
                     r1(s["mnV"]), r1(cmv), div(100 * cmv, s["mnV"], 1)])
    write_csv(os.path.join(out, "crosscheck_destatis_vs_comext_extraEU_ch72.csv"),
              ["year", "destatis_exports_to_nonEU_kt", "comext_EXT_EU27_exports_kt", "diff_kt", "diff_pct",
               "destatis_exports_to_nonEU_eur_m", "comext_EXT_EU27_exports_eur_m", "diff_eur_m",
               "destatis_imports_nonEU_ORIGIN_kt", "comext_EXT_EU27_direct_imports_kt", "gap_kt(arrived_via_other_EU_states)", "comext_direct_as_pct_of_destatis_origin_mass",
               "destatis_imports_nonEU_ORIGIN_eur_m", "comext_EXT_EU27_direct_imports_eur_m", "comext_direct_as_pct_of_destatis_origin_value"], rows)


# ------------------------------------------------------------------------------------------- section 2
def production(cl, out):
    """42153-0001 (C total) and 42153-0002 (WZ 2/3-digit): monthly index 2021=100; annual = mean of 12 unadjusted months."""
    sel = [("42153-0001", None, "WZ08V1", ["WZ08-C"]), ("42153-0002", None, "WZ08V2", ["WZ08-24", "WZ08-25"]),
           ("42153-0002", "WZ08V3", "WZ08V3", ["WZ08-241"])]
    lab = {"WZ08-C": ("Verarbeitendes Gewerbe", "Manufacturing"), "WZ08-24": ("Metallerzeugung und -bearbeitung", "Manufacture of basic metals"),
           "WZ08-25": ("Herstellung von Metallerzeugnissen", "Manufacture of fabricated metal products"),
           "WZ08-241": ("Erzeugung von Roheisen, Stahl und Ferrolegierungen", "Manufacture of basic iron and steel and of ferro-alloys")}
    mon = {}
    for code, swap, var, codes in sel:
        d = cl.cube(code, swap=swap, note=f"production index {var}")
        for r in decode(d, keep={var: set(codes), "WERT03": {"WERTORG", "X13JDKSB"}}):
            mon[(r[var], r["JAHR"], r["MONAT"], r["WERT03"])] = (r["value"], r["status"])
    # monthly file (2024-2026 plus all later for trend)
    rows = []
    for wz in lab:
        for y in range(2019, 2027):
            for m in range(1, 13):
                mk = f"MONAT{m:02d}"
                o = mon.get((wz, str(y), mk, "WERTORG"))
                a = mon.get((wz, str(y), mk, "X13JDKSB"))
                if o is None:
                    continue
                rows.append([wz, lab[wz][1], ym(str(y), mk), r1(o[0], 1), o[1] if o[0] is not None else "missing(...)",
                             r1(a[0], 1) if a else None, (a[1] if a[0] is not None else "missing(...)") if a else None])
    write_csv(os.path.join(out, "production_index_monthly_2019_2026.csv"),
              ["wz08", "label_en", "month", "index_2021=100_unadjusted", "status_unadj(e=final,r=revised,p=provisional)",
               "index_2021=100_calendar_and_seasonally_adjusted_X13", "status_adj"], rows)
    # annual means
    ann = []
    annual = {}
    for wz in lab:
        for y in range(1991, 2026):
            vals = [mon[(wz, str(y), f"MONAT{m:02d}", "WERTORG")] for m in range(1, 13) if (wz, str(y), f"MONAT{m:02d}", "WERTORG") in mon]
            ok = [v for v, s in vals if v is not None]
            if len(ok) == 12:
                mean = sum(ok) / 12
                annual[(wz, y)] = mean
                ann.append([wz, lab[wz][0], lab[wz][1], y, round(mean, 2), r1(mean, 1), 12, "+".join(sorted({s for v, s in vals}))])
    write_csv(os.path.join(out, "production_index_annual_mean_1991_2025.csv"),
              ["wz08", "label_de", "label_en", "year", "annual_mean_of_12_unadjusted_months_2dp", "rounded_1dp", "months_used", "status_set"], ann)
    # YTD 2026 vs 2025
    n = max(m for m in range(1, 13) if mon.get(("WZ08-C", "2026", f"MONAT{m:02d}", "WERTORG"), (None,))[0] is not None)
    ytd = []
    for wz in lab:
        a25 = [mon[(wz, "2025", f"MONAT{m:02d}", "WERTORG")][0] for m in range(1, n + 1)]
        a26 = [mon[(wz, "2026", f"MONAT{m:02d}", "WERTORG")][0] for m in range(1, n + 1)]
        ytd.append([wz, lab[wz][1], f"Jan-{n:02d}", r1(sum(a25) / n, 2), r1(sum(a26) / n, 2), r1(100 * (sum(a26) / sum(a25) - 1), 1)])
    write_csv(os.path.join(out, "production_index_ytd_2026_vs_2025.csv"),
              ["wz08", "label_en", "months", "mean_index_2025_same_months", "mean_index_2026", "change_pct"], ytd)
    return annual, mon


def employment(cl, out):
    """42111 (Monatsbericht, establishments of firms with 50+ employees) and 42271 (annual survey) + VGR 81000-0102/-0123."""
    lab = {"WZ08-C": "Manufacturing (C)", "WZ08-24": "Basic metals (24)", "WZ08-25": "Fabricated metal products (25)", "WZ08-241": "Basic iron and steel, ferro-alloys (24.1)"}
    spec = [("42111-0001", None, "WZ08M1", ["WZ08-C"], {"ERH001": "establishments", "ERW012": "employees", "UMS002": "turnover_eur_thousand", "UMSN3": "foreign_turnover_eur_thousand", "VST003": "gross_wages_eur_thousand", "ARBST1": "hours_thousand"}),
            ("42111-0003", None, "WZ08X2", ["WZ08-24", "WZ08-25"], {"ERH001": "establishments", "ERW012": "employees", "UMS002": "turnover_eur_thousand", "UMSN3": "foreign_turnover_eur_thousand", "VST003": "gross_wages_eur_thousand", "ARBST1": "hours_thousand"}),
            ("42111-0003", "WZ08X3", "WZ08X3", ["WZ08-241"], {"ERH001": "establishments", "ERW012": "employees", "UMS002": "turnover_eur_thousand", "UMSN3": "foreign_turnover_eur_thousand", "VST003": "gross_wages_eur_thousand", "ARBST1": "hours_thousand"}),
            ("42271-0001", None, "WZ08M1", ["WZ08-C"], {"BETR01": "establishments", "ERW012": "employees", "UMS002": "turnover_eur_thousand", "UMSN3": "foreign_turnover_eur_thousand", "VST003": "gross_wages_eur_thousand"}),
            ("42271-0002", None, "WZ08X2", ["WZ08-24", "WZ08-25"], {"BETR01": "establishments", "ERW012": "employees", "UMS002": "turnover_eur_thousand", "UMSN3": "foreign_turnover_eur_thousand", "VST003": "gross_wages_eur_thousand"}),
            ("42271-0002", "WZ08X3", "WZ08X3", ["WZ08-241"], {"BETR01": "establishments", "ERW012": "employees", "UMS002": "turnover_eur_thousand", "UMSN3": "foreign_turnover_eur_thousand", "VST003": "gross_wages_eur_thousand"})]
    R = collections.defaultdict(dict)
    for code, swap, var, codes, meas in spec:
        d = cl.cube(code, swap=swap, note=f"establishment survey {var}")
        for r in decode(d, keep={var: set(codes)}):
            if r["measure"] in meas:
                R[(code[:5], r[var], r["JAHR"])][meas[r["measure"]]] = (r["value"], r["status"])
    cols = ["establishments", "employees", "turnover_eur_thousand", "foreign_turnover_eur_thousand", "gross_wages_eur_thousand", "hours_thousand"]
    rows = []
    for (stat, wz, y) in sorted(R):
        if int(y) < 2008:
            continue
        t = R[(stat, wz, y)]
        sts = "+".join(sorted({s for v, s in t.values()}))
        rows.append([stat, "Monatsbericht (establishments, GENESIS 42111)" if stat == "42111" else "Annual survey (GENESIS 42271)", wz, lab[wz], y] +
                    [(t[c][0] if c in t else None) for c in cols] + [sts])
    write_csv(os.path.join(out, "employment_turnover_establishment_surveys_2008_2025.csv"),
              ["genesis_statistic", "survey", "wz08", "label_en", "year"] + cols + ["status(e=final,r=revised)"], rows)

    # VGR: GVA and employment by branch (domestic concept)
    g = cl.cube("81000-0102", note="VGR gross value added by branch")
    e = cl.cube("81000-0123", note="VGR employed persons by branch")
    codes = {"WZ08-C", "WZ08-24", "WZ08-25", "WZ08-24-01", "WZ08-A-02"}
    G = collections.defaultdict(dict)
    for r in decode(g, keep={"WZ08G3": codes}):
        G[(r["WZ08G3"], r["JAHR"])][r["VGRPB5"]] = (r["value"], r["status"])
    E = {}
    for r in decode(e, keep={"WZ08G3": codes}):
        E[(r["WZ08G3"], r["JAHR"])] = (r["value"], r["status"])
    st = cl.structure("81000-0102")
    lbl = labels(st, "WZ08G3")
    rows = []
    for (wz, y) in sorted(G):
        if int(y) < 2008:
            continue
        t = G[(wz, y)]
        tot = G[("WZ08-A-02", y)]["VGRJPM"][0]
        emp = E.get((wz, y), (None, None))
        nom = t["VGRJPM"][0]
        rows.append([wz, lbl[wz][0], lbl[wz][1], y, nom, t["VGRPKM"][0], t["VGRPVK"][0],
                     div(100 * nom, tot, 2) if (nom is not None and tot) else None, emp[0], t["VGRJPM"][1] if nom is not None else "missing(...)"])
    write_csv(os.path.join(out, "national_accounts_branch_gva_employment_2008_2025.csv"),
              ["wz08", "label_de", "label_en", "year", "gva_nominal_bn_eur", "gva_chain_index_2020=100", "gva_chain_linked_volume_bn_eur",
               "share_of_total_gva_pct", "employed_persons_thousand(domestic concept)", "status"], rows)
    return G, E, R


# ------------------------------------------------------------------------------------------- section 3
def yoy_context(out, mon, R):
    """2025 vs 2024 change for manufacturing (C) and basic metals (24, 24.1): production (two bases), turnover, employees."""
    def mean(wz, y, basis):
        v = [mon[(wz, str(y), f"MONAT{m:02d}", basis)][0] for m in range(1, 13)]
        return sum(v) / 12 if all(x is not None for x in v) else None
    rows = []
    for wz, nm in (("WZ08-C", "Manufacturing (C)"), ("WZ08-24", "Basic metals (24)"), ("WZ08-25", "Fabricated metal products (25)"), ("WZ08-241", "Basic iron and steel (24.1)")):
        for basis, lab in (("WERTORG", "production index, unadjusted annual mean (2021=100)"), ("X13JDKSB", "production index, calendar+seasonally adjusted annual mean (2021=100)")):
            a, b = mean(wz, 2025, basis), mean(wz, 2024, basis)
            rows.append([wz, nm, lab, r1(b, 2), r1(a, 2), r1(100 * (a / b - 1), 2)])
        for stat in ("42111", "42271"):
            for meas, lab in (("turnover_eur_thousand", "turnover (nominal), EUR thousand"), ("employees", "employees (Beschaeftigte)")):
                k25, k24 = R.get((stat, wz, "2025"), {}), R.get((stat, wz, "2024"), {})
                if meas in k25 and meas in k24 and k24[meas][0]:
                    a, b = k25[meas][0], k24[meas][0]
                    rows.append([wz, nm, f"GENESIS {stat}: {lab}", b, a, r1(100 * (a / b - 1), 2)])
    write_csv(os.path.join(out, "manufacturing_and_metals_yoy_2025_context.csv"),
              ["wz08", "label_en", "measure", "2024", "2025", "change_pct"], rows)


def ppi(cl, out):
    """61241-0003 (annual) / -0004 (monthly) by GP2019; total from 61241-0001/-0002."""
    sel = [("GP19M2", None, ["GP19-24"]), ("GP19M3", "GP19M3", ["GP19-241", "GP19-242", "GP19-243"]), ("GP19M4", "GP19M4", ["GP19-2410"]),
           ("GP19M5", "GP19M5", ["GP19-24103", "GP19-24104", "GP19-24105", "GP19-24106", "GP19-24107"]),
           ("GP19N1", "GP19N1", ["GP19-241062100"]), ("GP19N2", "GP19N2", ["GP-X007", "GP-X400", "GP-X0052"])]
    st3 = cl.structure("61241-0003")
    A, Mo = {}, {}
    names = {}
    for var, swap, codes in sel:
        lb = labels(st3, var)
        for c in codes:
            names[c] = lb[c]
        d = cl.cube("61241-0003", swap=swap, note=f"annual PPI {var}")
        for r in decode(d, keep={var: set(codes)}):
            A[(r[var], r["JAHR"])] = (r["value"], r["status"])
        d = cl.cube("61241-0004", swap=swap, note=f"monthly PPI {var}")
        for r in decode(d, keep={var: set(codes), "JAHR": {str(y) for y in range(2014, 2027)}}):
            Mo[(r[var], r["JAHR"], r["MONAT"])] = (r["value"], r["status"])
    names["TOTAL"] = ("Gewerbliche Produkte insgesamt", "Industrial products, total")
    d = cl.cube("61241-0001", note="PPI total annual")
    pub_yoy = {}
    for r in decode(d):
        if r["func"] == "QMU":
            A[("TOTAL", r["JAHR"])] = (r["value"], r["status"])
        elif r["func"] == "CH0004":
            pub_yoy[r["JAHR"]] = r["value"]
    d = cl.cube("61241-0002", note="PPI total monthly")
    pub_m = {}
    for r in decode(d, keep={"JAHR": {str(y) for y in range(2014, 2027)}}):
        if r["func"] == "QMU":
            Mo[("TOTAL", r["JAHR"], r["MONAT"])] = (r["value"], r["status"])
        elif r["func"] == "CH0005":
            pub_m[(r["JAHR"], r["MONAT"])] = r["value"]
    rows = []
    for c in names:
        for y in range(2015, 2026):
            v, s = A[(c, str(y))]
            pv = A.get((c, str(y - 1)), (None,))[0]
            rows.append([c, names[c][0], names[c][1], y, v, r1(100 * (v / pv - 1), 1) if (v is not None and pv) else None, s])
    write_csv(os.path.join(out, "ppi_annual_2015_2025.csv"),
              ["gp2019_code", "label_de", "label_en", "year", "index_2021=100", "change_vs_prior_year_pct(computed from index)", "status(e=final)"], rows)
    # check computed y/y vs published for total
    for y in range(2016, 2026):
        v, pv = A[("TOTAL", str(y))][0], A[("TOTAL", str(y - 1))][0]
        assert abs(100 * (v / pv - 1) - pub_yoy[str(y)]) < 0.15, ("PPI total yoy mismatch", y)
    rows = []
    for c in names:
        for y in range(2024, 2027):
            for m in range(1, 13):
                mk = f"MONAT{m:02d}"
                if (c, str(y), mk) not in Mo:
                    continue
                v, s = Mo[(c, str(y), mk)]
                pv = Mo.get((c, str(y - 1), mk), (None,))[0]
                rows.append([c, names[c][1], ym(str(y), mk), v, r1(100 * (v / pv - 1), 1) if (v is not None and pv) else None,
                             pub_m.get((str(y), mk)) if (c == "TOTAL" and v is not None) else None, s if v is not None else "missing(...)"])
    write_csv(os.path.join(out, "ppi_monthly_2024_2026.csv"),
              ["gp2019_code", "label_en", "month", "index_2021=100", "yoy_pct(computed)", "yoy_pct(published, total only)", "status"], rows)
    return A, Mo


# ------------------------------------------------------------------------------------------- section 4
def national_accounts(cl, out):
    items = [("VGR014", "Bruttoinlandsprodukt", "GDP", "81000-0019"),
             ("VGR026", "Konsumausgaben der privaten Haushalte", "Household final consumption", "81000-0019"),
             ("VGR035", "Private Konsumausgaben (Haushalte + priv. Organisationen o.E.)", "Private final consumption (households + NPISH)", "81000-0019"),
             ("VGR015", "Konsumausgaben des Staates", "Government final consumption", "81000-0019"),
             ("VGR041", "Bruttoanlageinvestitionen", "Gross fixed capital formation", "81000-0019"),
             ("VGR008", "Ausrüstungsinvestitionen", "GFCF machinery & equipment", "81000-0023"),
             ("VGR009", "Bauinvestitionen", "GFCF construction", "81000-0023"),
             ("VGR042", "Sonstige Anlageinvestitionen", "GFCF other products", "81000-0023"),
             ("VGR034", "Vorratsveränderungen u. Nettozugang Wertsachen", "Changes in inventories & valuables", "81000-0019"),
             ("VGR038", "Inländische Verwendung", "Domestic use", "81000-0019"),
             ("EXP001", "Exporte", "Exports of goods and services", "81000-0019"),
             ("EXP002", "Exporte von Waren", "Exports of goods", "81000-0027"),
             ("EXP003", "Exporte von Dienstleistungen", "Exports of services", "81000-0027"),
             ("IMP001", "Importe", "Imports of goods and services", "81000-0019"),
             ("IMP002", "Importe von Waren", "Imports of goods", "81000-0027"),
             ("IMP003", "Importe von Dienstleistungen", "Imports of services", "81000-0027"),
             ("VGR022", "Außenbeitrag", "Net exports (exports - imports)", "81000-0019")]
    cubes = {}
    for code in ("81000-0019", "81000-0023", "81000-0027"):
        d = cl.cube(code, note="national accounts (VGR) annual")
        T = collections.defaultdict(dict)
        for r in decode(d):
            T[(r["measure"], r["VGRPB5"], r["JAHR"])] = (r["value"], r["status"])
        cubes[code] = T
    rows = []
    GR = {}
    for code, de, en, tab in items:
        T = cubes[tab]
        for y in range(2019, 2026):
            ys = str(y)
            nom, sn = T[(code, "VGRJPM", ys)]
            idx, si = T[(code, "VGRPKM", ys)]
            vol, sv = T[(code, "VGRPVK", ys)]
            pvol = T[(code, "VGRPVK", str(y - 1))][0]
            pnom = T[(code, "VGRJPM", str(y - 1))][0]
            real_ok = (sv != "-" and vol and pvol and code not in ("VGR022", "VGR034"))
            g = 100 * (vol / pvol - 1) if real_ok else None
            gn = 100 * (nom / pnom - 1) if (nom is not None and pnom and code != "VGR022") else None
            GR[(code, y)] = g
            rows.append([code, de, en, y, nom, (idx if si != "-" else None), (vol if sv != "-" else None), r1(g, 2), r1(gn, 2), sn])
    write_csv(os.path.join(out, "national_accounts_expenditure_side_2019_2025.csv"),
              ["item_code", "label_de", "label_en", "year", "nominal_bn_eur", "chain_index_2020=100", "chain_linked_volume_bn_eur(2020 prices)",
               "real_growth_pct(COMPUTED from chain-linked volumes)", "nominal_growth_pct(computed)", "status(p=provisional)"], rows)
    # published GDP growth rate (81000-0001)
    d = cl.cube("81000-0001", note="GDP and value added, annual")
    pub = {}
    for r in decode(d):
        if r["measure"] == "BIP005":
            pub[(r["VGRPB5"], r["JAHR"])] = r["value"]
    # contributions (81000-0029)
    d = cl.cube("81000-0029", note="growth contributions to real GDP")
    st = cl.structure("81000-0029")
    lb = labels(st, "VGRVWA")
    rows = []
    for r in decode(d, keep={"JAHR": {"2023", "2024", "2025"}}):
        rows.append([r["VGRVWA"], lb[r["VGRVWA"]][0], lb[r["VGRVWA"]][1], r["JAHR"], r["value"], r["status"]])
    write_csv(os.path.join(out, "national_accounts_growth_contributions_2023_2025.csv"),
              ["item_code", "label_de", "label_en", "year", "contribution_to_real_gdp_growth_pp(published)", "status"], sorted(rows, key=lambda x: (x[3], x[0])))
    return GR, pub


def national_accounts_vintages(out, GR, pub):
    """2025 real growth, three vintages. Published values are typed in from the Destatis pages named in the
    'source' columns (opened 2026-10-22); the GENESIS column is computed from the current database."""
    JAN = "Destatis press release no. 017 of 15 Jan 2026 (PD26_017_811, first annual estimate)"
    REV = "Destatis page 'Sommerueberarbeitung 2026 der VGR' (Stand 25 Aug 2026, updated 30 Sep 2026): columns 'Alt' (before) and 'Neu' (after)"
    g = lambda k: r1(GR[(k, 2025)], 2)
    rows = [
        ["GDP, price-adjusted % change 2025", 0.2, 0.2, 0.2, g("VGR014"), 0.2, "GENESIS 81000-0001 BIP005 (published) = %s" % pub.get(("VGRPKM", "2025"))],
        ["Private consumption (households + NPISH), price-adjusted % 2025", 1.4, 1.3, 1.3, g("VGR035"), 1.4,
         "Jan release calls it 'Private Konsumausgaben'; workbook Dataset F labels the same 1.4 'Household consumption'"],
        ["Household consumption only, price-adjusted % 2025", None, None, None, g("VGR026"), 1.4, "computed only; no published rate opened"],
        ["Government consumption, price-adjusted % 2025", 1.5, 1.5, 1.7, g("VGR015"), 1.5, "revised up 0.2 pp in the summer revision"],
        ["Gross fixed capital formation, price-adjusted % 2025", -0.5, -0.2, -0.6, g("VGR041"), -0.5, "Jan -0.5 -> pre-revision -0.2 -> now -0.6"],
        ["  of which machinery & equipment investment", -2.3, None, None, g("VGR008"), None, "Jan release: Ausruestungsinvestitionen -2.3; now computed from 81000-0023"],
        ["  of which construction investment", -0.9, None, None, g("VGR009"), None, "Jan release: Bauinvestitionen -0.9; now computed from 81000-0023"],
        ["Exports of goods and services, price-adjusted % 2025", -0.3, None, None, g("EXP001"), -0.3,
         "no published current rate found; computed -0.95 rounds to -0.9 or -1.0 depending on unrounded levels"],
        ["  of which goods", -0.7, None, None, g("EXP002"), None, "computed from 81000-0027 chain-linked volumes"],
        ["  of which services", 1.1, None, None, g("EXP003"), None, "computed from 81000-0027 chain-linked volumes"],
        ["Imports of goods and services, price-adjusted % 2025", 3.6, None, None, g("IMP001"), 3.6, "no published current rate found; computed"],
        ["  of which goods", 5.1, None, None, g("IMP002"), None, "computed"],
        ["  of which services", 0.2, None, None, g("IMP003"), None, "computed"],
        ["Net exports, contribution to real GDP growth 2025 (pp)", None, -1.5, -1.5, -1.5, None, "81000-0029 VGR-VWA-02 (published) = -1.5; exports -0.4, imports -1.1"],
        ["GDP nominal 2025 (bn EUR)", None, 4469.81, 4529.71, 4529.71, None, "revision page: old 4 469,810 -> new 4 529,710; Jan release gives no nominal level"],
    ]
    write_csv(os.path.join(out, "national_accounts_2025_vintage_comparison.csv"),
              ["indicator", "jan2026_first_estimate", "pre_revision_vintage('Alt')", "post_revision_published('Neu')", "genesis_current_computed_or_published",
               "workbook_DatasetF_value", "comment"], rows)
    with open(os.path.join(out, "national_accounts_2025_vintage_comparison.sources.txt"), "w", encoding="utf-8") as f:
        f.write("jan2026_first_estimate: " + JAN + "\npre_revision / post_revision: " + REV +
                "\ngenesis column: GENESIS-Online 81000-0019 / -0023 / -0027 / -0029 / -0001, table lastChange 2026-09-21 (see manifest.json); "
                "growth rates marked 'computed' = 100*(chain-linked volume_t / volume_t-1 - 1) from the published volumes, not a published rate.\n")


# -------------------------------------------------------------------------------------------- checks
def check_workbook(out, repo, annual_prod, G, E, T_total):
    base = os.path.join(repo, "sources", "text", "inter-trade-present-base.txt")
    if not os.path.exists(base):
        print("  (workbook text not found - check skipped)")
        return
    wb = {}
    in41 = False
    for line in open(base, encoding="utf-8"):
        s = line.strip()
        if s.startswith("## 4.1 Germany manufacturing"):
            in41 = True
            continue
        if in41 and s.startswith("[/TABLE]"):
            break
        m = re.match(r"^(\d{4}) \| ([\d.]+) \| ([\d.]+) \| ([\d.]+)$", s)
        if in41 and m and 1995 <= int(m.group(1)) <= 2025:
            wb[int(m.group(1))] = (float(m.group(2)), float(m.group(3)), float(m.group(4)))
    assert len(wb) == 31, ("workbook table 4.1 not parsed", len(wb))
    rows = []
    for y in sorted(wb):
        gva_w, prod_w, sh_w = wb[y]
        pd = annual_prod.get(("WZ08-C", y))
        gva_d = G.get(("WZ08-C", str(y)), {}).get("VGRPKM", (None,))[0]
        nom_c = G.get(("WZ08-C", str(y)), {}).get("VGRJPM", (None,))[0]
        nom_t = G.get(("WZ08-A-02", str(y)), {}).get("VGRJPM", (None,))[0]
        sh_d = 100 * nom_c / nom_t if (nom_c is not None and nom_t) else None
        rows.append([y, prod_w, r1(pd, 2), None if pd is None else r1(pd - prod_w, 2), gva_w, gva_d, None if gva_d is None else r1(gva_d - gva_w, 2),
                     sh_w, r1(sh_d, 2), None if sh_d is None else r1(sh_d - sh_w, 2),
                     "match" if (pd is not None and abs(round(pd, 1) - prod_w) < 0.051) else ("n/a" if pd is None else "DIFF")])
    write_csv(os.path.join(out, "check_workbook_table_4_1_vs_destatis.csv"),
              ["year", "workbook_production_2021=100(Eurostat sts_inpr_a)", "destatis_42153_annual_mean", "diff",
               "workbook_real_GVA_2020=100(Eurostat nama_10_a64)", "destatis_81000-0102_chain_index", "diff",
               "workbook_GVA_share_pct", "destatis_81000-0102_share_pct(computed)", "diff", "production_check(1dp)"], rows)


# ------------------------------------------------------------------------------------------------ main
def main():
    ap = argparse.ArgumentParser()
    here = os.path.dirname(os.path.abspath(__file__))
    ap.add_argument("--out", default=here)
    ap.add_argument("--cache", default=os.path.join(tempfile.gettempdir(), "destatis_genesis_cache"))
    ap.add_argument("--repo", default=os.path.abspath(os.path.join(here, "..", "..", "..")))
    a = ap.parse_args()
    out = a.out
    cl = Client(a.cache)
    print("Destatis pull, retrieved", RETRIEVED)
    print("[1] foreign trade")
    ch72, H, HS, heads72, lab4 = trade_annual(cl, out)
    split = trade_eu_split(cl, out, ch72)
    trade_headings(cl, out, H, HS, heads72, lab4)
    trade_monthly(cl, out)
    T_total = trade_total(cl, out)
    crosscheck_comext(out, split, a.repo)
    crosscheck_comext_world(out, ch72, a.repo)
    print("[2] production index and employment")
    annual_prod, mon = production(cl, out)
    G, E, R = employment(cl, out)
    yoy_context(out, mon, R)
    print("[3] producer prices")
    ppi(cl, out)
    print("[4] national accounts")
    GR, pub = national_accounts(cl, out)
    national_accounts_vintages(out, GR, pub)
    check_workbook(out, a.repo, annual_prod, G, E, T_total)
    with open(os.path.join(out, "manifest.json"), "w", encoding="utf-8") as f:
        json.dump({"retrieved_utc": RETRIEVED, "base_url": BASE, "note": "Raw cubes are not stored in the repo; sha256 identifies each API response.",
                   "requests": cl.manifest}, f, ensure_ascii=False, indent=1)
    print("done;", len(cl.manifest), "API responses used")


if __name__ == "__main__":
    main()
