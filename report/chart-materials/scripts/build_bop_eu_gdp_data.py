"""Chart data for Figures 2.7 to 2.9 (report section 2.4.3, section 2.4.5 and section 2.6).

Derives three CSV files from the downloaded sources in data/:
  data/comext_exports/ch72_partner_balance_1999_2025.csv      balances by partner group, EUR million
  data/comext_exports/ch72_export_destinations_1999_2025.csv  export tonnes and unit values by destination group
  data/eurostat_macro/tidy/de_real_gdp_1995_2025.csv          German real GDP level, index and growth

Sources: Eurostat Comext DS-045409 (reporter DE, Chapter 72); Eurostat nama_10_gdp (DE, B1GQ), downloaded 3 Nov 2026
into data/eurostat_macro/raw/.
Run from the repository root:  python -I -X utf8 report/chart-materials/scripts/build_bop_eu_gdp_data.py
"""
import csv
import json
import os

ROOT = '.'
COMEXT = os.path.join(ROOT, 'data', 'comext_exports')
RAW = os.path.join(ROOT, 'data', 'eurostat_macro', 'raw')
TIDY = os.path.join(ROOT, 'data', 'eurostat_macro', 'tidy')


def partner_balance():
    rows = csv.DictReader(open(os.path.join(COMEXT, 'ch72_balance_by_partner_group_1999_2025.csv'), encoding='utf-8'))
    out = os.path.join(COMEXT, 'ch72_partner_balance_1999_2025.csv')
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['year', 'extra_eu_balance_eur_m', 'intra_eu_balance_eur_m', 'all_partner_balance_eur_m'])
        for r in rows:
            w.writerow([r['year'],
                        round(float(r['extra_eu_balance_value_eur_million']), 1),
                        round(float(r['intra_eu_balance_value_eur_million']), 1),
                        round(float(r['world_balance_value_eur_million']), 1)])
    return out


def export_destinations():
    rows = csv.DictReader(open(os.path.join(COMEXT, 'ch72_trade_by_partner_group_long.csv'), encoding='utf-8'))
    exp = {}
    for r in rows:
        if r['flow'] == 'export':
            exp.setdefault(r['year'], {})[r['partner']] = (float(r['value_eur_million']), float(r['net_mass_thousand_t']))
    out = os.path.join(COMEXT, 'ch72_export_destinations_1999_2025.csv')
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['year', 'extra_eu_export_kt', 'intra_eu_export_kt', 'extra_eu_export_eur_m', 'intra_eu_export_eur_m',
                    'extra_eu_unit_value_eur_t', 'intra_eu_unit_value_eur_t', 'extra_eu_mass_share_pct'])
        for y in sorted(exp, key=int):
            ev, em = exp[y]['EXT_EU27_2020']
            iv, im = exp[y]['INT_EU27_2020']
            w.writerow([y, round(em, 1), round(im, 1), round(ev, 1), round(iv, 1),
                        round(ev / em * 1000, 1), round(iv / im * 1000, 1), round(100 * em / (em + im), 1)])
    return out


def german_gdp():
    def series(fn):
        j = json.load(open(os.path.join(RAW, fn), encoding='utf-8'))
        time = j['dimension']['time']['category']['index']
        pos = {int(v): k for k, v in time.items()}
        status = j.get('status', {})
        return {int(pos[int(i)]): (float(v), status.get(i, '')) for i, v in j['value'].items()}
    lvl = series('nama_10_gdp_DE_B1GQ_CLV20_MEUR_1995_2025.json')
    gro = series('nama_10_gdp_DE_B1GQ_CLV_PCH_PRE_1995_2025.json')
    base = lvl[2020][0]
    out = os.path.join(TIDY, 'de_real_gdp_1995_2025.csv')
    with open(out, 'w', newline='', encoding='utf-8') as f:
        w = csv.writer(f)
        w.writerow(['year', 'real_gdp_eur_m_2020_prices', 'real_growth_pct', 'real_gdp_index_2020_100', 'flag'])
        for y in sorted(set(lvl) & set(gro)):
            w.writerow([y, round(lvl[y][0], 1), gro[y][0], round(100 * lvl[y][0] / base, 2),
                        (lvl[y][1] + ' ' + gro[y][1]).strip()])
    return out


if __name__ == '__main__':
    for path in (partner_balance(), export_destinations(), german_gdp()):
        print('written', path)
