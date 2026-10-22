# build_tables.py: reads raw/evidence/*.pdf (cited pages only) and writes the CSV tables of data/steel_route.
# Requires PyMuPDF (fitz). Run: python -I -X utf8 build_tables.py   (paths below are absolute for this machine)
# Typed values (DEHSt emissions, WV Stahl tables, WV Stahl specific CO2) are asserted against the text of the cited evidence page.
import fitz, re, csv, os, json, sys
R = 'D:/Workspace/inter-trade-present/data/steel_route/'
E = R + 'raw/evidence/'
OUT = R

# ----------------------------------------------------------------------------------
# helpers
# ----------------------------------------------------------------------------------
def words_of(pdf, pg):
    d = fitz.open(E + pdf)
    return d[pg].get_text('words')

def text_of(pdf):
    d = fitz.open(E + pdf)
    return re.sub(r'\s+', ' ', ' '.join(p.get_text() for p in d))

def merge_numbers(row):
    out = []
    i = 0
    toks = [(w[4], w[0], w[2]) for w in row]
    while i < len(toks):
        t, x0, x1 = toks[i]
        if re.fullmatch(r'\d{1,3}', t) and i + 1 < len(toks) and re.fullmatch(r'\d{3}', toks[i + 1][0]) and toks[i + 1][1] - x1 < 6:
            out.append((int(t + toks[i + 1][0]), toks[i + 1][2]))
            i += 2
        elif re.fullmatch(r'\d+(\.\d+)?', t):
            out.append((float(t) if '.' in t else int(t), x1))
            i += 1
        else:
            out.append((t, x1))
            i += 1
    return out

def table_row(pdf, pg, label='Germany', xmax=None):
    w = words_of(pdf, pg)
    cands = [x for x in w if x[4].startswith(label) and (xmax is None or x[0] < xmax)]
    g = cands[0]
    yc = (g[1] + g[3]) / 2
    row = sorted([x for x in w if abs((x[1] + x[3]) / 2 - yc) < 3.5 and x[0] > g[0]], key=lambda x: x[0])
    return merge_numbers(row), w

def year_series(pdf, pg):
    nums, w = table_row(pdf, pg)
    hdr = sorted([x for x in w if re.fullmatch(r'(19|20)\d\d', x[4]) and x[1] < 170], key=lambda x: x[0])
    cols = [(int(h[4]), h[2]) for h in hdr]
    res = {}
    for v, x1 in nums:
        y = min(cols, key=lambda c: abs(c[1] - x1))
        res[y[0]] = v
    return res

def t6(pdf, pg):
    nums, _ = table_row(pdf, pg)
    return [v for v, _ in nums]

def check_in(pdf, strings, txtfile=None):
    t = text_of(pdf)
    if txtfile:
        t = t + ' ' + re.sub(r'\s+', ' ', open(txtfile, encoding='utf-8').read())
    for s in strings:
        assert s in t, f'MISSING {s!r} in {pdf}'

def write_csv(name, header, rows):
    with open(OUT + name, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(header)
        for r in rows:
            w.writerow(['' if v is None else v for v in r])
    print('wrote', name, len(rows), 'rows')

# ----------------------------------------------------------------------------------
# 1. crude steel by process route, Germany
# ----------------------------------------------------------------------------------
yb09 = 'worldsteel_Yearbook-2009_pdfpages_28-30-32-34.pdf'
yb18 = 'worldsteel_Yearbook-2018_pdfpages_23-24-25-27.pdf'
c19f = 'worldsteel_Yearbook-2019-concise_pdfpages_6-8.pdf'
c20f = 'worldsteel_Yearbook-2020-concise_pdfpage_8.pdf'
obc09, obp09, ef09, efp09 = [year_series(yb09, i) for i in range(4)]
obc18, obp18, ef18, efp18 = [year_series(yb18, i) for i in range(4)]
c17 = t6(c19f, 0)
c18 = t6(c19f, 1)
c19 = t6(c20f, 0)
# overlap check 2008
assert obc09[2008] == obc18[2008] and ef09[2008] == ef18[2008]

wsif_pages = {2010: 6, 2011: 6, 2012: 6, 2013: 10, 2014: 6, 2015: 6, 2017: 6, 2018: 6, 2019: 6, 2020: 6, 2021: 10, 2022: 6, 2023: 6, 2024: 6, 2025: 6, 2026: 6}
wsif = {}
for ed, pg in wsif_pages.items():
    nums, _ = table_row(f'worldsteel_WSIF-{ed}-edition_pdfpage_{pg}.pdf', 0)
    vals = [v for v, _ in nums if isinstance(v, (int, float))]
    wsif[ed - 1] = (vals[0], vals[1], vals[2], ed)

# WV Stahl revision tables (SUMME row) - checked against text below
wv = {
    2021: dict(total=40241, oxy=28150, ele=12091, pig=25691, rev='Revision Juli 2022', f='20220731_Rohstahlerzeugung_Deutschland_2021.pdf'),
    2022: dict(total=36861, oxy=25873, ele=10987, pig=23856, rev='Revision Juli 2023', f='20230802_Rohstahlerzeugung_Deutschland_2022.pdf'),
    2023: dict(total=35395, oxy=25578, ele=9817, pig=23635, rev='Revision Juli 2024', f='20240807_Rohstahlerzeugung_Deutschland_2023.pdf'),
    2024: dict(total=37310, oxy=26487, ele=10823, pig=24327, rev='Revision Juli 2025', f='20250804_Rohstahlerzeugung_Deutschland_2024.pdf'),
    2025: dict(total=34267, oxy=23814, ele=10453, pig=21874, rev='Revision August 2026', f='20260810_Rohstahlerzeugung_Deutschland_Revision_2025.pdf'),
}
for y, d in wv.items():
    t = re.sub(r'\s+', ' ', fitz.open(R + 'raw/wvstahl/' + d['f'])[0].get_text())
    s = 'SUMME ' + ' '.join(f"{d[k]:,}".replace(',', '.') for k in ('total', 'oxy', 'ele', 'pig'))
    # text order in the PDF is not guaranteed; check each number individually
    for k in ('total', 'oxy', 'ele', 'pig'):
        assert f"{d[k]:,}".replace(',', '.') in t, (y, k)
    assert abs(d['oxy'] + d['ele'] - d['total']) <= 1

# page locators
yb09_loc = lambda tab: f"worldsteel Steel Statistical Yearbook 2009, Table {tab}"
route_rows = []
for y in range(1999, 2026):
    row = dict(year=y, crude=None, oxy=None, ele=None, pubele=None, pubcrude=None, src='', loc='', note='')
    if 1999 <= y <= 2007:
        row.update(oxy=obc09[y], ele=ef09[y], src='worldsteel Steel Statistical Yearbook 2009',
                   loc='Table 7 (oxygen-blown converters, kt) printed p.26 / PDF p.28; Table 8 (electric furnaces, kt) printed p.30 / PDF p.32; % tables printed pp.28, 32 / PDF pp.30, 34',
                   pubele=efp09[y])
    elif 2008 <= y <= 2017:
        row.update(oxy=obc18[y], ele=ef18[y], src='worldsteel Steel Statistical Yearbook 2018',
                   loc='Table 7 (oxygen-blown converters, kt) printed p.19 / PDF p.23; Table 8 (electric furnaces, kt) printed p.21 / PDF p.25; % tables printed pp.20, 23 / PDF pp.24, 27',
                   pubele=efp18[y])
        if y == 2008:
            row['note'] = 'identical in Yearbook 2009 (Tables 7 and 8, last column)'
        if y == 2017:
            row['note'] = 'WSIF 2018 edition showed an estimate 43.4 Mt, 71.2/28.8; the Yearbook 2018 and concise Yearbook 2019 (final) show 43,297 kt, 70.0/30.0'
    elif y == 2018:
        row.update(oxy=c18[0], ele=c18[1], src='worldsteel Steel Statistical Yearbook 2019 (concise)', loc='Table 6, year 2018, printed p.5 / PDF p.8', pubele=c18[4])
    elif y == 2019:
        row.update(oxy=c19[0], ele=c19[1], src='worldsteel Steel Statistical Yearbook 2020 (concise)', loc='Table 6, year 2019, printed p.5 / PDF p.8', pubele=c19[4])
        row['note'] = 'WSIF 2020 edition printed 39.7 Mt (70.0/30.0); final yearbook 39,627 kt'
    elif y == 2020:
        mt, ox, el, ed = wsif[2020]
        row.update(pubcrude=mt, pubele=el, src='worldsteel World Steel in Figures 2021', loc='Crude steel production by process 2020, printed p.10 / PDF p.10 (Mt and % only; kt not available)',
                   note='kt split not available from an official table I could open; only Mt (1 decimal) and published % shares')
    else:
        d = wv[y]
        row.update(crude=d['total'], oxy=d['oxy'], ele=d['ele'], src='WV Stahl, Rohstahlerzeugung in Deutschland %d, Vollstaendige Uebersicht (%s)' % (y, d['rev']), loc='one-page PDF, SUMME row (Rohstahl gesamt / Oxygenstahl / Elektrostahl)')
        mt, ox, el, ed = wsif[y]
        row.update(pubcrude=mt, pubele=el)
        if y == 2025:
            row['note'] = 'Revision Aug 2026 (34,267 kt). WV Stahl preliminary annual press release 21 Jan 2026: 34,090 / 23,645 / 10,445 kt (electric 30.64%). worldsteel WSIF 2026: 34.1 Mt, 69.4/30.6. Brochure 2026 prints 34.1 Mt.'
        if y == 2024:
            row['note'] = 'Revision Jul 2025 (37,310 kt); WV Stahl brochures and workbook Dataset A print 37.2 Mt (Destatis/WV Stahl, earlier vintage)'
    if row['crude'] is None and row['oxy'] is not None:
        row['crude'] = row['oxy'] + row['ele']
    route_rows.append(row)

# worldsteel published (Mt) cross-check columns from WSIF editions (data year = edition-1)
def wsif_pub(y):
    return wsif.get(y)

hdr = ['year', 'crude_steel_kt', 'oxygen_bof_kt', 'electric_eaf_kt', 'oxygen_share_pct_calc', 'electric_share_pct_calc', 'electric_share_pct_published_by_worldsteel',
       'worldsteel_WSIF_crude_Mt', 'worldsteel_WSIF_oxygen_pct', 'worldsteel_WSIF_electric_pct', 'WSIF_edition_year', 'primary_source', 'locator_table_page', 'note']
rows = []
for r in route_rows:
    y = r['year']
    if r['crude'] is not None and r['oxy'] is not None:
        oc = round(100 * r['oxy'] / r['crude'], 2)
        ec = round(100 * r['ele'] / r['crude'], 2)
    else:
        oc = ec = None
    w = wsif.get(y)
    rows.append([y, r['crude'], r['oxy'], r['ele'], oc, ec, r['pubele'],
                 w[0] if w else None, w[1] if w else None, w[2] if w else None, w[3] if w else None,
                 r['src'], r['loc'], r['note']])
write_csv('crude_steel_by_route_germany_1999_2025.csv', hdr, rows)

# internal checks: calc share vs published share
bad = []
for r in rows:
    y, ecalc, epub = r[0], r[5], r[6]
    if ecalc is not None and epub is not None and abs(ecalc - epub) > 0.06:
        bad.append((y, ecalc, epub))
print('share calc vs published mismatches >0.06pt:', bad)
# WSIF vs yearbook/WV differences
diffs = []
for r in rows:
    y = r[0]
    w = wsif.get(y)
    if w and r[5] is not None and abs(w[2] - r[5]) > 0.15:
        diffs.append((y, 'electric calc', r[5], 'WSIF', w[2]))
print('WSIF vs source electric share differences >0.15pt:', diffs)

# ----------------------------------------------------------------------------------
# 2. EU ETS verified emissions: German iron and steel (DEHSt)
# ----------------------------------------------------------------------------------
# evidence checks (numbers must appear in the cited page text)
check_in('dehst_VET-Bericht-2006_pdfpages_18.pdf', ['2.903.336', '17.625.345', '10.109.960', '3.187.197', '18.747.151', '10.220.811'])
check_in('dehst_VET-Bericht-2008_pdfpages_39.pdf', ['3.279', '1.852', '8.246', '19.680', '3.578', '1.718', '7.888', '19.566', '1.068'])
check_in('dehst_VET-Bericht-2009_pdfpages_36.pdf', ['25.287', '33.819'])
check_in('dehst_VET-Bericht-2010_pdfpages_38.pdf', ['31.804', '25.287'])
check_in('dehst_VET-Bericht-2011_pdfpages_28.pdf', ['32.173', '31.794'])
check_in('dehst_VET-Bericht-2012_pdfpages_31.pdf', ['31.290', '32.095'])
check_in('dehst_VET-Bericht-2013_pdfpages_33-34.pdf', ['35.741', '30.674', '31.290', '21,4 Millionen'])
check_in('dehst_VET-Bericht-2014_pdfpages_27-28.pdf', ['35.650', '36.371', 'Emissionsintensität'])
check_in('dehst_VET-Bericht-2015_pdfpages_35.pdf', ['36.364', '37.081'])
check_in('dehst_VET-Bericht-2016_pdfpages_31.pdf', ['37.125', '36.330'])
check_in('dehst_VET-Bericht-2017_pdfpages_31.pdf', ['36.278', '37.813', 'seit 2005 bis 2017 um rund zwei Prozent'])
check_in('dehst_VET-Bericht-2018_pdfpages_42.pdf', ['37.813', '37.913'])
check_in('dehst_VET-Bericht-2019_pdfpages_43-45-46-49.pdf', ['37.921', '35.577', '31,4 Millionen', '29,7 Millionen', 'um neun Prozent zurückgegangen', '46.223', '129,9', '92,4', '32.867'])
check_in('dehst_VET-Bericht-2020_pdfpages_48-49.pdf', ['31.401', '35.577', '989.000', '26,2 Millionen', '45.167', '143,8', '108,0', '33.898', '16.836'])
check_in('dehst_VET-Bericht-2021_pdfpages_43-45.pdf', ['35.428', '31.473', '1.068.000', '29,6 Millionen', '42.443', '128,2', '83,5', '29.580', '45.422'])
check_in('dehst_VET-Bericht-2022_pdfpages_43-45.pdf', ['33.186', '35.426', '945.000', '28,0 Millionen', '46.551', '140,3', '95,3', '31.621'])
check_in('dehst_VET-Bericht-2023_pdfpages_15-17-18-19.pdf', ['32,5 Mio', '142 Prozent'], E + 'ev_VET2023_pdftotext.txt')
check_in('dehst_VET-Bericht-2024_v5_pdfpages_16-18-22.pdf', ['33,1 Mio', '46.002,99', '33.149,87', '138,8', '94,2', '31.228', '10,2 Prozent'], E + 'ev_VET2024_pdftotext.txt')

ets = [
    # year, first_kt, first_report(pdf page), restated_kt, restated_report(pdf page), segment, n_plants, scope/notes
    (2005, 30638.641, 'VET 2006 report, Tabelle 2-1 (col. VET 2005, Stand 31.03.2006); sum of VII + IXa + IX (3.+6+26 plants); printed p.18 / PDF p.18', None, '', 'A', 35,
     'First trading period scope: Taetigkeit VII Kokereien + IXa integrierte Huettenwerke + IX Roheisen und Stahl (no separate sintering VIII, no IXb processing)'),
    (2006, 32155.159, 'VET 2006 report, Tabelle 2-1 (col. VET 2006, Stand 31.03.2007); sum of VII + IXa + IX; printed p.18 / PDF p.18', None, '', 'A', 35,
     'First trading period scope (same as 2005)'),
    (2007, 33057, 'VET 2008 report, Tabelle 13 (col. Emissionen 2007), sum of VII 3,279 + VIII 1,852 + IX 8,246 + IXa 19,680 + IXb 0 kt; printed p.39 / PDF p.39', None, '', 'A/B transition', 43,
     'Comparison set used by DEHSt in the 2008 report: plants of the 2nd-period scope with their 2007 verified emissions (8 IXb plants and one coke oven had no 2007 value = 0 in the table; sintering VIII listed separately). A VET 2007 report was not found in the archive.'),
    (2008, 33818, 'VET 2008 report, Tabelle 13 (col. VET 2008), sum of VII 3,578 + VIII 1,718 + IX 7,888 + IXa 19,566 + IXb 1,068 kt; printed p.39 / PDF p.39', 33819, 'VET 2009 report, Tabelle 18 (Emissionen 2008); printed p.36 / PDF p.36', 'B', 44,
     'Second trading period scope: Taetigkeiten VII to IXb incl. coke ovens'),
    (2009, 25287, 'VET 2009 report, Tabelle 18 (VET 2009, Stand 31.03.2010); printed p.36 / PDF p.36', 25287, 'VET 2010 report, Tabelle 18 (Emissionen 2009); printed p.38 / PDF p.38', 'B', 44, 'Financial crisis year'),
    (2010, 31804, 'VET 2010 report, Tabelle 18 (Stand 31.03.2011); printed p.38 / PDF p.38', 31794, 'VET 2011 report, Tabelle 18 (Emissionen 2010); printed p.28 / PDF p.28', 'B', 44, ''),
    (2011, 32173, 'VET 2011 report, Tabelle 18 (Stand 31.03.2012); printed p.28 / PDF p.28', 32095, 'VET 2012 report, Tabelle 18 (Emissionen 2011); printed p.31 / PDF p.31', 'B', 46, ''),
    (2012, 31290, 'VET 2012 report, Tabelle 18 (Stand 02.05.2013); printed p.31 / PDF p.31', 31290, 'VET 2013 report, Tabelle 18/19 (Emissionen 2012); printed p.33 / PDF p.33', 'B', 47, 'Last year of the second-period scope'),
    (2013, 35741, 'VET 2013 report, Tabelle 18 (Stand 02.05.2014), 130 plants; printed p.33 / PDF p.33', 35650, 'VET 2014 report, Tabelle 17 (Emissionen 2013), 127 plants; printed p.27 / PDF p.27', 'C', 127,
     'Third trading period scope: Taetigkeiten 8 to 11 and one plant of Taetigkeit 1 (TEHG); about 80 additional plants, mostly Taetigkeit 11 processing. VET 2019 text quotes 35.9 Mt for 2013 (restated incl. plants no longer in ETS)'),
    (2014, 36371, 'VET 2014 report, Tabelle 17 (Stand 04.05.2015); printed p.27 / PDF p.27', 36364, 'VET 2015 report, Tabelle 17 (Emissionen 2014); printed p.35 / PDF p.35', 'C', 127, ''),
    (2015, 37081, 'VET 2015 report, Tabelle 17; printed p.35 / PDF p.35', 37125, 'VET 2016 report, Tabelle 11 (Emissionen 2015); printed p.31 / PDF p.31', 'C', 127, ''),
    (2016, 36330, 'VET 2016 report, Tabelle 11 (Stand 02.05.2017); printed p.31 / PDF p.31', 36278, 'VET 2017 report, Tabelle 9 (Emissionen 2016); printed p.31 / PDF p.31', 'C', 126, ''),
    (2017, 37813, 'VET 2017 report, Tabelle 9 (Stand 02.05.2018); printed p.31 / PDF p.31', 37813, 'VET 2018 report, Tabelle 12 (Emissionen 2017); PDF p.42 (printed p.25)', 'C', 125, ''),
    (2018, 37913, 'VET 2018 report, Tabelle 12 (Stand 02.05.2019); PDF p.42 (printed p.25)', 37921, 'VET 2019 report, Tabelle 9 (Emissionen 2018); PDF p.43 (printed p.25)', 'C', 125, ''),
    (2019, 35577, 'VET 2019 report, Tabelle 9 (Stand 04.05.2020); PDF p.43 (printed p.25)', 35577, 'VET 2020 report, Tabelle 9 (Emissionen 2019); PDF p.48 (printed p.28)', 'C', 125, 'VET 2019 text says 35.5 Mt; its table gives 35,577 kt'),
    (2020, 31401, 'VET 2020 report, Tabelle 9 (Stand 03.05.2021); PDF p.48 (printed p.28)', 31473, 'VET 2021 report, Tabelle 9 (Emissionen 2020); PDF p.43 (printed p.22). UBA table 2026-09-24: 31.5', 'C', 120, 'COVID year; 123 plants in VET 2020, 120 plus 3 no longer in ETS in VET 2021'),
    (2021, 35428, 'VET 2021 report, Tabelle 9 (Stand 02.05.2022); PDF p.43 (printed p.22)', 35426, 'VET 2022 report, Tabelle 9 (Emissionen 2021); PDF p.43 (printed p.22). UBA table 2026-09-24: 35.4', 'C', 120, ''),
    (2022, 33186, 'VET 2022 report, Tabelle 9 (Stand 02.05.2023); PDF p.43 (printed p.22). UBA table 2026-09-24: 33.2', None, '', 'C', 120, ''),
    (2023, 32500, 'VET 2023 report, Abbildung 6: 32.5 Mt CO2-eq (one decimal only); printed p.15 / PDF p.15. UBA table 2026-09-24: 32.5 (118 plants in 2024 table edition)', None, '', 'C', 118, 'Value precision 0.1 Mt'),
    (2024, 33149.87, 'VET 2024 report, Tabelle 3 (Stand 02.05.2025): 33,149.87 kt, 115 plants; PDF p.22 (also Abbildung 6, PDF p.16: 33.1 Mt). UBA table 2026-09-24: 33.1', None, '', 'C', 115, ''),
    (2025, 30000, 'UBA table "Emissionen der Anlagen in Deutschland nach Branchen (EU-ETS-1-Abgrenzung)", dated 2026-09-24, row Eisen und Stahl: 30.0 Mt, 115 plants (source line: DEHSt Treibhausgas-Emissionen 2025, Stand 05/2026); single page', None, '', 'C', 115,
     'Value precision 0.1 Mt; DEHSt VET-Bericht 2025 PDF could not be opened (dehst.de in maintenance on 2026-10-22). UBA press release No. 17/2026 of 2026-07-07 describes steel as one of the sectors with particularly marked decreases, mainly production-driven'),
]
uba = {2020: 31.5, 2021: 35.4, 2022: 33.2, 2023: 32.5, 2024: 33.1, 2025: 30.0}
hdr = ['year', 'emissions_kt_co2e_preferred', 'preferred_basis', 'first_published_kt', 'first_published_source', 'restated_kt', 'restated_source', 'uba_table_2026_09_24_Mt', 'scope_segment', 'n_installations', 'scope_notes']
rows = []
pref = {}
for y, f, fs, rs, rsrc, seg, n, note in ets:
    p = rs if rs is not None else f
    basis = 'restated in following report' if rs is not None else 'first publication (no later restatement opened)'
    if y in (2023, 2025):
        basis = 'first publication, 0.1 Mt precision'
    pref[y] = p
    rows.append([y, p, basis, f, fs, rs, rsrc, uba.get(y), seg, n, note])
write_csv('ets_emissions_german_iron_steel_2005_2025.csv', hdr, rows)

# checks vs UBA table
for y, v in uba.items():
    assert abs(pref[y] / 1000 - v) < 0.06, (y, pref[y], v)
print('UBA 2026 table agrees with preferred values 2020-2025 within 0.06 Mt')
# averages check against UBA table averages
avg08_12 = sum(pref[y] for y in range(2008, 2013)) / 5 / 1000
avg13_20 = sum(pref[y] for y in range(2013, 2021)) / 8 / 1000
print('avg 2008-12 from vintages = %.2f Mt (UBA table 31.1); avg 2013-20 = %.2f Mt (UBA table 36.3)' % (avg08_12, avg13_20))

# ----------------------------------------------------------------------------------
# 3. route-level emissions inside the ETS boundary (DEHSt text) and per tonne
# ----------------------------------------------------------------------------------
route = [
    # year, BF-route Mt (incl coke ovens+sinter), EAF route Mt, tae 11 processing, source
    (2018, 31.4, None, 5.294, 'VET 2019 p.43: Hochofenroute 2018 31.4 Mt; Elektrostahl "etwa 1.2" Mt (approximate, not used); Taetigkeit 11 5,294 kt (Tabelle 9)'),
    (2019, 29.7, 1.029, 4.749, 'VET 2019 p.43 (BF 29.7 Mt, EAF c.1.0 Mt) and VET 2020 p.48 (EAF 1,029,000 t; Taetigkeit 11 4,749 kt)'),
    (2020, 26.2, 0.989, 4.115, 'VET 2020 p.48 (BF 26.2 Mt; EAF 989,000 t; Taetigkeit 11 4,115 kt)'),
    (2021, 29.6, 1.068, 4.354, 'VET 2021 p.43 (BF 29.6 Mt; EAF 1,068,000 t; Taetigkeit 11 4,354 kt)'),
    (2022, 28.0, 0.945, 4.058, 'VET 2022 p.43 (BF 28.0 Mt; EAF 945,000 t; Taetigkeit 11 4,058 kt)'),
]
rrows = []
oxy_kt = {2018: c18[0], 2019: c19[0], 2020: None, 2021: wv[2021]['oxy'], 2022: wv[2022]['oxy']}
ele_kt = {2018: c18[1], 2019: c19[1], 2020: None, 2021: wv[2021]['ele'], 2022: wv[2022]['ele']}
# 2020: kt not available -> derive from WSIF 35.7 Mt x published shares (flagged)
oxy_kt[2020] = round(35700 * 0.677)
ele_kt[2020] = round(35700 * 0.323)
for y, bf, ea, t11, src in route:
    bf_pt = round(bf * 1000 / oxy_kt[y], 3)
    ea_pt = round(ea * 1000 / ele_kt[y], 3) if ea else None
    flag = 'route output derived from 35.7 Mt x published 67.7/32.3 %' if y == 2020 else ''
    rrows.append([y, bf, ea, t11, oxy_kt[y], ele_kt[y], bf_pt, ea_pt, src, flag])
write_csv('ets_route_emissions_and_per_tonne_2018_2022.csv',
          ['year', 'blast_furnace_route_incl_coke_sinter_Mt_CO2e', 'electric_arc_route_direct_Mt_CO2e', 'taetigkeit11_processing_Mt_CO2e', 'oxygen_steel_output_kt', 'electric_steel_output_kt',
           'BF_route_tCO2e_per_t_oxygen_steel', 'EAF_route_tCO2e_per_t_electric_steel', 'source_DEHSt_pdf_pages', 'note'], rrows)

# process-gas forwarding (emissions occur at energy installations, not in the Eisen und Stahl row)
gas = [(2013, 21.4, 'VET 2013 p.33 text: process gases forwarded to the energy sector correspond to 21.4 Mt CO2'),
       (2014, 21.8, 'VET 2014 p.27 text: 21.8 Mt CO2 forwarded to the energy sector'),
       (2019, 19.506, 'VET 2019 p.44 Tabelle 10: forwarded to energy installations 19,506 kt (text: 19.5 Mt vs 20.4 Mt in 2018)'),
       (2020, 16.836, 'VET 2020 p.49 Tabelle 10: 16,836 kt (text 16.8 Mt vs 19.5 Mt in 2019)')]
write_csv('process_gas_forwarded_to_energy_installations.csv', ['year', 'forwarded_to_energy_installations_Mt_CO2', 'source'], [list(g) for g in gas])

# ----------------------------------------------------------------------------------
# 4. emissions per tonne of crude steel (derived) + WV Stahl specific CO2
# ----------------------------------------------------------------------------------
crude = {}
for r in route_rows:
    y = r['year']
    if r['crude'] is not None:
        crude[y] = r['crude']
crude[2020] = 35700  # WSIF 2021 (35.7 Mt, one decimal); WV Stahl brochure 2026 chart also 35.7
wvs = {  # year: (crude steel t CO2/t, hot-rolled t CO2/t, source)
    1990: (1.59, 1.75, 'WV Stahl Daten und Fakten 2025, printed p.20 (PDF p.20) and all editions 2020-2026 (baseline)'),
    2019: (1.37, 1.45, 'WV Stahl Fakten zur Stahlindustrie 2020, printed p.27 (PDF p.27)'),
    2020: (1.38, 1.47, 'WV Stahl Fakten zur Stahlindustrie 2021, printed p.31 (PDF p.31)'),
    2021: (1.40, 1.48, 'WV Stahl Fakten zur Stahlindustrie 2022, printed p.23 (PDF p.23)'),
    2022: (1.41, 1.49, 'WV Stahl Daten und Fakten 2023, printed p.23 (PDF p.23)'),
    2023: (1.43, 1.52, 'WV Stahl Daten und Fakten 2024, printed p.21 (PDF p.21)'),
    2024: (1.40, 1.54, 'WV Stahl Daten und Fakten 2025, printed p.20 (PDF p.20)'),
    2025: (1.39, 1.47, 'WV Stahl Daten und Fakten 2026 (published 2026-10-08), printed p.20 (PDF p.20)'),
}
rows = []
for y, (a, b, s) in wvs.items():
    rows.append([y, a, b, s])
write_csv('wv_stahl_specific_co2_per_tonne.csv',
          ['year', 'crude_steel_tCO2_per_t', 'hot_rolled_and_semis_tCO2_per_t', 'source_edition_page'], rows)
# derived changes
print('WV Stahl crude-steel CO2/t: 2019 %.2f -> 2025 %.2f (%+.1f%%); 1990 -> 2025 %+.1f%%' % (1.37, 1.39, 100 * (1.39 / 1.37 - 1), 100 * (1.39 / 1.59 - 1)))

seg_of = {y: s for y, f, fs, rs, rsrc, s, n, note in ets}
rows = []
inten = {}
for y in range(2005, 2026):
    e = pref[y]
    c = crude[y]
    ratio = round(e / c, 4)
    inten[y] = ratio
    rows.append([y, e, c, ratio, seg_of[y], wvs[y][0] if y in wvs else None, wvs[y][1] if y in wvs else None,
                 'crude steel = OBC+EF (Yearbook)' if y <= 2019 else ('crude steel 35.7 Mt (WSIF 2021, rounded)' if y == 2020 else 'crude steel = WV Stahl revision table')])
write_csv('ets_co2_per_tonne_crude_steel_derived_2005_2025.csv',
          ['year', 'ets_emissions_kt_co2e', 'crude_steel_kt', 'ets_tCO2e_per_t_crude_steel_DERIVED', 'scope_segment', 'wv_stahl_specific_co2_crude_steel_t_per_t', 'wv_stahl_specific_co2_hot_rolled_t_per_t', 'denominator_source'], rows)
print('derived intensity', {y: inten[y] for y in sorted(inten)})
seg_c = [y for y in inten if seg_of[y] == 'C']
print('segment C change 2013->2025: %.4f -> %.4f (%+.1f%%)' % (inten[2013], inten[2025], 100 * (inten[2025] / inten[2013] - 1)))
print('2019->2025: ETS emissions %+.1f%%, crude steel %+.1f%%, ratio %+.1f%%' % (100 * (pref[2025] / pref[2019] - 1), 100 * (crude[2025] / crude[2019] - 1), 100 * (inten[2025] / inten[2019] - 1)))

# ----------------------------------------------------------------------------------
# 5. free allocation context (nominal vs adjusted)
# ----------------------------------------------------------------------------------
alloc = [
    (2019, 46223, 129.9, 32867, 92.4, 'VET 2019 Tabelle 9 and Tabelle 11, PDF pp.43, 45 (printed pp.25, 27)'),
    (2020, 45167, 143.8, 33898, 108.0, 'VET 2020 Tabelle 9 and 11, PDF pp.48, 49 (printed pp.28, 29)'),
    (2021, 45422, 128.2, 29580, 83.5, 'VET 2021 Tabelle 9 and 11, PDF pp.43, 45 (printed pp.22, 24)'),
    (2022, 46551, 140.3, 31621, 95.3, 'VET 2022 Tabelle 9 and 11, PDF pp.43, 45 (printed pp.22, 24)'),
    (2023, None, 142, None, 96.2, 'VET 2023 PDF p.18 (nominal ratio 142 % in text; allocation total not extracted); adjusted 96.2 % from VET 2024 Tabelle 3 column 2023, PDF p.22'),
    (2024, 46003, 138.8, 31228, 94.2, 'VET 2024 Tabelle 3, PDF p.22 (printed p.22)'),
]
write_csv('free_allocation_context_german_iron_steel_2019_2024.csv',
          ['year', 'free_allocation_1000_EUA_nominal', 'nominal_allocation_to_emissions_pct', 'adjusted_allocation_1000_EUA', 'adjusted_allocation_to_emissions_pct', 'source'],
          [list(a) for a in alloc])

# ----------------------------------------------------------------------------------
# 6. EU27 context 2025 (WSIF 2026, printed p.10)
# ----------------------------------------------------------------------------------
eu_labels = ['Austria', 'Belgium', 'Bulgaria', 'Czechia', 'Finland', 'France', 'Germany', 'Greece', 'Italy', 'Luxembourg', 'Netherlands', 'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden', 'European']
wl = words_of('worldsteel_WSIF-2026-edition_pdfpage_6.pdf', 0)
eu_rows2 = []
for lab in eu_labels:
    g = [x for x in wl if x[4].startswith(lab) and x[0] < 100][0]
    yc = (g[1] + g[3]) / 2
    row = sorted([x for x in wl if abs((x[1] + x[3]) / 2 - yc) < 3.5 and g[0] < x[0] < 290 and x[4] not in ('e', 'Union', '(27)', lab)], key=lambda x: x[0])
    toks = [t for t, _ in [(w[4], 0) for w in row]]
    toks = [float(t) if re.fullmatch(r'\d+\.\d+', t) else t for t in toks]
    mt, ox, el = toks[0], toks[1], toks[2]
    name = 'European Union (27)' if lab == 'European' else lab
    eu_rows2.append([name, mt, None if ox == '-' else ox, None if el == '-' else el, 'dash in source; left blank, not zero-filled' if '-' in (ox, el) else ''])
write_csv('eu27_route_share_2025_context.csv', ['country', 'crude_steel_Mt_2025', 'oxygen_pct', 'electric_pct', 'note'], eu_rows2)
print(eu_rows2)

# ----------------------------------------------------------------------------------
# 7. chart data
# ----------------------------------------------------------------------------------
rows = []
for y in range(1999, 2026):
    r = [x for x in route_rows if x['year'] == y][0]
    ele_pct = None
    if r['crude'] is not None and r['ele'] is not None:
        ele_pct = round(100 * r['ele'] / r['crude'], 1)
    elif y == 2020:
        ele_pct = wsif[2020][2]
    rows.append([y, ele_pct,
                 round(pref[y] / 1000, 2) if y >= 2013 else None,
                 round(crude[y] / 1000, 2) if y in crude else None,
                 round(inten[y], 3) if (y >= 2013) else None,
                 wvs[y][0] if y in wvs and y != 1990 else None])
write_csv('chart_data_cleaner_steel_indicators.csv',
          ['year', 'electric_arc_share_of_crude_steel_pct', 'ets_iron_steel_emissions_Mt_CO2e_(scope C only)', 'crude_steel_Mt', 'ets_tCO2e_per_t_crude_steel_(scope C only, derived)', 'wv_stahl_specific_co2_t_per_t_crude_steel_(incl_purchased_power)'], rows)


# ----------------------------------------------------------------------------------
# 8. DEHSt / UBA statements (paraphrased) and source manifest
# ----------------------------------------------------------------------------------
stm = [
    ('VET 2014 report (Stand 04.05.2015)', 'PDF p.28 (printed p.28)', 'Emissions of the iron-and-steel industry 2005-2013 follow the economy (up in period 1, down in period 2); DEHSt states that no clear, significant trend towards lower emission intensity can be derived so far.'),
    ('VET 2017 report (Stand 02.05.2018)', 'PDF p.31 (printed p.31)', 'On a consistent-scope basis (estimated pre-2013 emissions of later-added processing plants and installations no longer in the ETS included) emissions of the iron-and-steel industry were about 2 percent higher in 2017 than in 2005.'),
    ('VET 2019 report (Stand 04.05.2020)', 'PDF p.46 (printed p.28)', 'Emissions rose from 2013 to 2018 (except 2016); 2019 is slightly below 2013; versus 2005 total emissions are 9 percent lower in 2019 (same consistent-scope basis). Text says 35.5 Mt for 2019, the table says 35,577 kt.'),
    ('VET 2019 report (Stand 04.05.2020)', 'PDF p.49 (printed p.31)', 'German iron-and-steel emissions rose to 2018 above 2013 although German crude steel output was flat (42.6 Mt in 2013, 42.4 Mt in 2018) and EU output was flat; DEHSt says production trends give no plausible explanation.'),
    ('VET 2019 report (Stand 04.05.2020)', 'PDF p.43 (printed p.25)', 'Blast-furnace (oxygen steel) route dominates: about 84 percent of the sector emissions for about 70 percent of crude steel; electric steel about 30 percent of output but under 3 percent of the sector emissions (direct emissions only; indirect power emissions are higher for EAF).'),
    ('VET 2023 report (Stand 02.05.2024)', 'PDF p.17 (printed p.17)', '2023: iron-and-steel emissions -2 percent vs 2022; oxygen-steel output -0.9 percent, electric steel -10.8 percent (WV Stahl).'),
    ('VET 2024 report (Stand 02.05.2025)', 'PDF p.18 (printed p.18)', '2024: oxygen-steel output a little over +3 percent, electric steel +10.2 percent (WV Stahl); emissions of the sector about +2 percent.'),
    ('UBA press release No. 17/2026, 2026-07-07', 'web page', '2025: industrial ETS installations -5.5 percent to about 97 Mt; clear decreases in iron and steel among others, mainly production-driven; UBA says ramp-up of direct reduction and related infrastructure is not yet fast enough.'),
]
write_csv('dehst_uba_statements_paraphrased.csv', ['source', 'locator', 'statement_paraphrased'], [list(x) for x in stm])

DEH = 'https://www.dehst.de/SharedDocs/downloads/DE/publikationen/'
man = [
    ['M01', 'UBA: Emissionen der Anlagen in Deutschland nach Branchen (EU-ETS-1-Abgrenzung); source line DEHSt Treibhausgas-Emissionen 2025 (Stand 05/2026)', '2026-09-24', 'https://www.umweltbundesamt.de/system/files/medien/384/bilder/dateien/6_Tab_Emi-Anlagen-nach-Branchen_2026-09-24.pdf', 'live', 'raw/uba_6_tab_2026-09-24.pdf (+ .png, .txt)'],
    ['M02', 'UBA press release No. 17/2026 Europaeischer Emissionshandel: Deutsche Emissionen sinken 2025 um rund 3 Prozent', '2026-07-07', 'https://www.umweltbundesamt.de/presse/pressemitteilungen/europaeischer-emissionshandel-deutsche-emissionen', 'live', 'raw/uba_pm_17_2026_extract.txt'],
]
vet_arch = {
    2006: ('20220321104849', 'VET-Bericht-2006.pdf?__blob=publicationFile&v=6', 'CO2-Emissionen 2006 (VET 2006), Stand 31.03.2007'),
    2008: ('20220321104841', 'VET-Bericht-2008.pdf?__blob=publicationFile&v=6', 'Kohlendioxidemissionen 2008'),
    2009: ('20220321164855', 'VET-Bericht-2009.pdf?__blob=publicationFile&v=6', 'Kohlendioxidemissionen 2009, Stand 31.03.2010'),
    2010: ('20220321104857', 'VET-Bericht-2010.pdf?__blob=publicationFile&v=6', 'Kohlendioxidemissionen 2010, Stand 31.03.2011'),
    2011: ('20220321104908', 'VET-Bericht-2011.pdf?__blob=publicationFile&v=6', 'VET-Bericht 2011, Stand 31.03.2012'),
    2012: ('20220321104859', 'VET-Bericht-2012.pdf?__blob=publicationFile&v=6', 'Kohlendioxidemissionen 2012, Stand 02.05.2013'),
    2013: ('20220308022511', 'VET-Bericht-2013.pdf?__blob=publicationFile&v=5', 'Treibhausgasemissionen 2013, Stand 02.05.2014'),
    2014: ('20220308022514', 'VET-Bericht-2014.pdf?__blob=publicationFile&v=5', 'Treibhausgasemissionen 2014, Stand 04.05.2015'),
    2015: ('20220308022618', 'VET-Bericht-2015.pdf?__blob=publicationFile&v=5', 'Treibhausgasemissionen 2015'),
    2016: ('20220119112943', 'VET-Bericht-2016.pdf?__blob=publicationFile&v=5', 'Treibhausgasemissionen 2016, Stand 02.05.2017'),
    2017: ('20231116002246', 'VET-Bericht-2017.pdf?__blob=publicationFile&v=5', 'Treibhausgasemissionen 2017, Stand 02.05.2018'),
    2018: ('20220120132655', 'VET-Bericht-2018.pdf?__blob=publicationFile&v=5', 'Treibhausgasemissionen 2018, Stand 02.05.2019'),
    2019: ('20210826092128', 'VET-Bericht-2019.pdf?__blob=publicationFile&v=4', 'Treibhausgasemissionen 2019, Stand 04.05.2020'),
    2020: ('20220227153700', 'VET-Bericht-2020.pdf;jsessio-nid=7946FB12AF055EC910CE68DB7948D81A.1_cid292?__blob=publicationFile&v=4', 'Treibhausgasemissionen 2020, Stand 03.05.2021'),
    2021: ('20220619105311', 'VET-Bericht-2021.pdf?__blob=publicationFile&v=3', 'Treibhausgasemissionen 2021, Stand 02.05.2022'),
    2022: ('20240104132806', 'VET-Bericht-2022.pdf?__blob=publicationFile&v=4', 'Treibhausgasemissionen 2022, Stand 02.05.2023'),
    2023: ('20240716201226', 'VET-Bericht-2023.pdf?__blob=publicationFile&v=4', 'Emissionssituation im Europaeischen Emissionshandel 2023, Stand 02.05.2024'),
    2024: ('2025', 'VET-Bericht-2024.pdf?__blob=publicationFile&v=5', 'Emissionssituation 2024 im EU-ETS 1, Stand 02.05.2025'),
}
i = 3
for y, (ts, u, title) in vet_arch.items():
    man.append(['M%02d' % i, 'DEHSt (UBA) VET-Bericht %d: %s' % (y, title), title.split('Stand ')[-1] if 'Stand' in title else '', DEH + u,
                'archived copy: https://web.archive.org/web/%sif_/%s%s (live dehst.de returned a maintenance page on 2026-10-22)' % (ts, DEH, u), 'raw/evidence/dehst_VET-Bericht-%d_*.pdf' % y])
    i += 1
WS = 'https://worldsteel.org/wp-content/uploads/'
man += [
    ['M%02d' % i, 'worldsteel Steel Statistical Yearbook 2009 (data 1999-2008)', '2009', WS + 'Steel-Statistical-Yearbook-2009.pdf', 'live', 'raw/evidence/worldsteel_Yearbook-2009_*.pdf'],
    ['M%02d' % (i + 1), 'worldsteel Steel Statistical Yearbook 2018 (data 2008-2017)', '2018', WS + 'Steel-Statistical-Yearbook-2018.pdf', 'live', 'raw/evidence/worldsteel_Yearbook-2018_*.pdf'],
    ['M%02d' % (i + 2), 'worldsteel Steel Statistical Yearbook 2019 concise (2017, 2018)', '2019', WS + 'Steel-Statistical-Yearbook-2019-concise-version.pdf', 'live', 'raw/evidence/worldsteel_Yearbook-2019-concise_*.pdf'],
    ['M%02d' % (i + 3), 'worldsteel Steel Statistical Yearbook 2020 concise (2018, 2019)', '2020', WS + 'Steel-Statistical-Yearbook-2020-concise-version.pdf', 'live', 'raw/evidence/worldsteel_Yearbook-2020-concise_*.pdf'],
    ['M%02d' % (i + 4), 'worldsteel World Steel in Figures 2010-2015, 2017-2026 editions (table Crude steel production by process, one data year per edition)', '2010-2026', WS + '{2010..2015,2017..2021}-World-Steel-in-Figures.pdf; World-Steel-in-Figures-{2022..2026}.pdf (file names as served by worldsteel.org; the 2026 edition PDF was created 2026-08-31)', 'live', 'raw/evidence/worldsteel_WSIF-*.pdf'],
]
i += 5
WV = 'https://www.wvstahl.de/wp-content/uploads/'
man += [
    ['M%02d' % i, 'WV Stahl: Rohstahlerzeugung in Deutschland 2025, Vollstaendige Uebersicht, Revision Stand August 2026', '2026-08-10', WV + '20260810_Rohstahlerzeugung_Deutschland_Revision_2025.pdf', 'live', 'raw/wvstahl/20260810_Rohstahlerzeugung_Deutschland_Revision_2025.pdf'],
    ['M%02d' % (i + 1), 'WV Stahl: Rohstahlerzeugung in Deutschland 2024, Revision Juli 2025', '2025-08-04', WV + '20250804_Rohstahlerzeugung_Deutschland_2024.pdf', 'live', 'raw/wvstahl/20250804_Rohstahlerzeugung_Deutschland_2024.pdf'],
    ['M%02d' % (i + 2), 'WV Stahl: Rohstahlerzeugung in Deutschland 2023, Revision Juli 2024', '2024-08-07', WV + '20240807_Rohstahlerzeugung_Deutschland_2023.pdf', 'live', 'raw/wvstahl/20240807_Rohstahlerzeugung_Deutschland_2023.pdf'],
    ['M%02d' % (i + 3), 'WV Stahl: Rohstahlerzeugung in Deutschland 2022, Revision Juli 2023', '2023-08-02', WV + '20230802_Rohstahlerzeugung_Deutschland_2022.pdf', 'live', 'raw/wvstahl/20230802_Rohstahlerzeugung_Deutschland_2022.pdf'],
    ['M%02d' % (i + 4), 'WV Stahl: Rohstahlerzeugung in Deutschland 2021, Revision Juli 2022', '2022-07-31', WV + '20220731_Rohstahlerzeugung_Deutschland_2021.pdf', 'live', 'raw/wvstahl/20220731_Rohstahlerzeugung_Deutschland_2021.pdf'],
    ['M%02d' % (i + 5), 'WV Stahl press release: Jahresbilanz der Stahlproduktion 2025 (preliminary: 34,090 / 23,645 / 10,445 kt)', '2026-01-21', 'https://www.wvstahl.de/pressemitteilungen/jahresbilanz-der-stahlproduktion-2025-viertes-krisenjahr-in-folge/', 'live', 'raw/wvstahl/pm_jahresbilanz_2025_table.txt'],
    ['M%02d' % (i + 6), 'WV Stahl: Daten und Fakten zur Stahlindustrie in Deutschland, Ausgabe 2026 (pp.9, 16, 20)', '2026-10-08', WV + '20261008_WV-Stahl_Daten-und-Fakten-2026_RZ_Web.pdf', 'live', 'raw/evidence/wvstahl_20261008_*.pdf'],
    ['M%02d' % (i + 7), 'WV Stahl: Daten und Fakten zur Stahlindustrie in Deutschland, Ausgabe 2025 (pp.9, 20) - the edition used in the workbook (S12)', '2025-09-10', WV + 'WV-Stahl_Daten-und-Fakten-2025_Web.pdf', 'live', 'raw/evidence/wvstahl_WV-Stahl_Daten-und-Fakten-2025_*.pdf'],
    ['M%02d' % (i + 8), 'WV Stahl: Daten und Fakten 2024 (p.21); Fakten 2023 (p.23); Fakten 2022 (p.23); Fakten 2021 (p.31); Fakten 2020 (p.27, archived copy 2024-12-18)', '2020-2024', WV + '{WV-Stahl_Daten-und-Fakten-2024_RZ-Web.pdf; WV-Stahl_Fakten-2023_Web.pdf; WV-Stahl_Fakten-2022_RZ_neu_Web.pdf; WV-Stahl_Fakten-2021_RZ_Web_neu.pdf; WV-Stahl_Fakten-2020_rz_neu_Web1.pdf}', 'live (2020 edition via web.archive.org/web/20241218114834if_/)', 'raw/evidence/wvstahl_WV-Stahl_*.pdf'],
]
write_csv('sources_manifest.csv', ['id', 'document', 'document_date', 'url', 'access', 'evidence_file_in_this_folder'], man)
