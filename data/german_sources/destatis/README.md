# Destatis primary data - Germany, iron and steel (EU ETS + CBAM deck)

Retrieved 2026-10-22 (UTC 04:13-04:24) from Statistisches Bundesamt (Destatis) GENESIS-Online, plus Destatis press-release and table pages and one Bundesbank article that were opened and read.
Everything below comes from responses in `manifest.json` (SHA-256 per response) or from the pages named in the text. Nothing is recalled from memory; cells GENESIS flags as "later / unknown / secret" (`...`, `.`, `x`, `/`) are left EMPTY, never zero.
Reproduce: `python -I -X utf8 pull_destatis.py` (about 15 minutes cold, stdlib only; raw cubes are cached outside the repo and are not stored here).

## How the data was reached (access note)

* GENESIS-Online (https://www-genesis.destatis.de/datenbank/online/table/<code>) is a JavaScript app. It reads public JSON endpoints under `https://genesis.destatis.de/genesis/api/rest/` (`/tables/<code>/structure`, `/tables/<code>/data`, `/statistics/<code>/tables`). The script uses only those, with no login, no credentials, no token and no bot-challenge handling.
* The documented `genesisWS` API and the table-download (CSV/XLSX) endpoint were not used (the first needs a login; the download call returned HTTP 502 in a test). So nothing was bypassed.
* Server behaviour observed in my tests (not documented): for tables with moderate size the server returned the whole cube whatever selection was posted (the script filters locally); for the very large country tables a custom selection was accepted only up to roughly 40,000 cells (larger requests returned HTTP 413; 18,900 cells worked, 52,000 did not), so heading-level country data is pulled in two chunks (27 EU codes x 9 years x 17/16 headings x 6 measures).
* Quality flags used by GENESIS: `e` final, `p` provisional, `r` revised, `-` nothing/exactly zero, `...` figure follows later. 2025 foreign-trade and national-accounts data are still `p`.

## Table codes, dimensions, units (all Germany total)

| Topic | GENESIS table (lastChange UTC) | Dimensions used | Unit as published | Converted to |
| --- | --- | --- | --- | --- |
| Trade, chapters, annual | 51000-0005 (2026-09-24) | JAHR 2008-2025 x WAM2 (98 WV chapters) x 6 measures; row swaps WAM4 (1,626 headings), SITC2A, GP19B2/B4, EGW3 | mass t; value EUR 1,000 (GEWA/GEWE, WERTA/WERTE; export/import) | kt = t/1,000; EUR m = EUR 1,000/1,000 |
| Trade by country, annual | 51000-0007 (2026-09-24) | JAHR x WAM2 x STLAH (262 countries) | same | EU27 / non-EU sums |
| Trade, heading x country | 51000-0009 (2026-09-24) | JAHR 2017-2025 x WAM4 72xx x STLAH (26 EU partners + code 959) | same | same |
| Trade, monthly | 51000-0006 (2026-10-20); by country 51000-0008 (2026-10-20) | JAHR 2008-2026 x MONAT x WAM2; 0008 adds STLAH | same | same |
| Trade, total goods | 51000-0001 (2026-09-24) | JAHR 1950-2025 | same | EUR bn, Mt |
| Production index | 42153-0001 (C) and -0002 (WZ08 2/3/4-digit), lastChange 2026-10-09 | JAHR 1991-2026 x MONAT x WERT03 (WERTORG unadjusted; X13JDKSB calendar+seasonally adjusted) | index 2021=100 | annual = mean of 12 unadjusted months |
| Employment, establishments | 42111-0001/-0003 (2026-09-21/22), 42271-0001/-0002 (2026-09-21) | JAHR 2005/2008-2025 x WZ08 | persons; EUR 1,000 | none |
| Employment and GVA, national accounts | 81000-0123 (employed persons, 1,000) and 81000-0102 (GVA) (2026-09-21) | JAHR 1991-2025 x WZ08G3 x price base | 1,000 persons; bn EUR; chain index 2020=100 | share of total GVA computed |
| Producer prices | 61241-0003 annual (2026-09-21), -0004 monthly (2026-10-20), -0001/-0002 total | GP2019 2/3/4/5/9-digit and special positions x JAHR (x MONAT) | index 2021=100 | y/y computed |
| National accounts, use side | 81000-0019, -0023, -0027, -0029, -0001 (2026-09-21) | JAHR 1991-2025 x VGRPB5 (current prices bn EUR; chain index 2020=100; chain-linked volume bn EUR) | as stated | growth computed |

Country grouping (my construction, same as Eurostat's `EXT_EU27_2020`): EU27 (2020 composition) = the 26 partner countries listed first in the GENESIS country list (every EU member except Germany) plus code 959 "countries not specified (intra-Community)"; non-EU = every other code, including the United Kingdom in all years. Per the GENESIS definition text, imports are assigned by country of ORIGIN and exports by country of DESTINATION.
Check: the country sums reproduce the all-partner chapter totals within rounding for every year 2008-2025, and the 33 chapter-72 headings add up to the chapter total (<= 0.001 %).

## Files

| File | Content |
| --- | --- |
| `trade_ch72_ch73_annual_2008_2025.csv` | Chapters 72 (iron and steel) and 73 (articles of iron/steel): kt, EUR m, balances, unit values, status |
| `trade_ch72_eu27_vs_noneu_annual_2008_2025.csv` | Chapter 72 split EU27 / non-EU (exports by destination, imports by origin), kt and EUR m, non-EU balances |
| `trade_ch72_headings_eu27_vs_noneu_2017_2025.csv` | HS headings 7201-7229: all partners, EU27, non-EU (derived = all - EU27), English labels |
| `trade_steel_groupings_annual_2008_2025.csv` | SITC-67, GP2019 24.10 / 24.20 / 24.31-24.34 / 24 / 25, EGW steel groups, WV 72 and 73, plus my derived "steel-mill-like" aggregate (HS 7207-7229 + 7304-7306; NOT a Destatis aggregate) |
| `trade_ch72_ch73_monthly_2008_2026.csv`, `trade_ytd_by_year.csv` | Monthly all-partner series (to Aug 2026) and year-to-date comparisons on identical months |
| `trade_ch72_monthly_eu27_vs_noneu_2023_2026.csv`, `trade_ch72_ytd_eu27_vs_noneu.csv` | Monthly EU27 / non-EU split (to Jul 2026) and Jan-Jul comparisons |
| `trade_total_goods_annual_2000_2025.csv` | Total goods exports/imports/balance |
| `crosscheck_destatis_vs_comext_extraEU_ch72.csv`, `crosscheck_destatis_vs_comext_world_ch72.csv` | Destatis vs the Eurostat Comext series already in `data/comext_exports/` (read only) |
| `check_destatis_press_release_PD25_380_51_vs_genesis.csv` | Recomputation of Destatis' own iron-and-steel press release |
| `production_index_*.csv` | Annual mean 1991-2025, monthly 2019-2026, YTD 2026 vs 2025 for WZ08 C, 24, 25, 24.1 |
| `employment_turnover_establishment_surveys_2008_2025.csv` | 42111 and 42271: establishments, employees, turnover, wages for C, 24, 25, 24.1 |
| `national_accounts_branch_gva_employment_2008_2025.csv` | Manufacturing and basic-metals GVA (nominal, index, share) and employed persons |
| `manufacturing_and_metals_yoy_2025_context.csv` | 2025 vs 2024 for production (two bases), turnover and employees |
| `check_workbook_table_4_1_vs_destatis.csv` | Workbook table 4.1 (Eurostat) against Destatis, 1995-2025 |
| `ppi_annual_2015_2025.csv`, `ppi_monthly_2024_2026.csv` | Producer price index: total, metals, steel positions, intermediate goods, energy |
| `national_accounts_expenditure_side_2019_2025.csv`, `national_accounts_growth_contributions_2023_2025.csv`, `national_accounts_2025_vintage_comparison.csv` (+ `.sources.txt`) | GDP use side, growth contributions, three vintages for 2025 |
| `manifest.json`, `pull_destatis.py` | Request log with hashes; replication script |

## Findings (numbers are from the CSVs above)

### 1. Iron and steel foreign trade (WV chapter 72, all partners)

| | 2017 | 2019 | 2024 | 2025 (p) |
| --- | --- | --- | --- | --- |
| Exports, kt / EUR m | 33,518.8 / 23,266.8 | 31,500.2 / 22,798.1 | 29,257.7 / 28,397.2 | 29,178.5 / 26,262.7 |
| Imports, kt / EUR m | 34,424.6 / 25,609.5 | 29,312.6 / 24,411.5 | 24,021.3 / 25,850.7 | 24,043.6 / 24,101.3 |
| Balance, kt / EUR m | -905.8 / -2,342.7 | +2,187.6 / -1,613.4 | +5,236.4 / +2,546.5 | +5,134.9 / +2,161.4 |

* Chapter 72 includes scrap (heading 7204: exports 7,782.5 kt and imports 3,978.7 kt in 2025, about 27 % and 17 % of chapter mass) and ferro-alloys, pig iron and ores-in-lumps; it is wider than the German Steel Federation's "steel mill products" (Dataset B).
* Split by partner group (imports by origin): non-EU exports 7,224.6 kt (2017) -> 4,680.6 kt (2025), -35.2 %; non-EU-origin imports 6,932.7 -> 5,049.6 (2019) -> 4,156.0 (2024) -> 3,918.6 kt (2025), -22.4 % since 2019. Non-EU exports minus non-EU-origin imports: +291.8 kt (2017), +762.0 kt (2025); EUR +1,332.6 m and +1,673.8 m.
* Cross-check against Eurostat Comext (already in the repo): Destatis non-EU exports equal Comext `EXT_EU27_2020` flow-2 exports within 0.1 % in every year 2017-2025 (2025: 4,680.6 vs 4,681.2 kt; EUR 5,425.1 vs 5,427.9 m). All-partner chapter totals equal Comext `WORLD` within 0.01 % up to 2022 and 0.1 % in 2023-2025 (vintage).
* Key reconciliation for slide 7: the Comext direct extra-EU import series is NOT the same concept as Destatis non-EU-origin imports. Comext assigns extra-EU imports by origin but intra-EU arrivals by consignment, so non-EU steel cleared in another member state counts there as intra-EU; Destatis assigns every import by origin. Because the totals agree, the difference is exactly the non-EU-origin steel that reached Germany via other EU states: 2,455 kt in 2025 (3,918.6 - 1,463.6). The direct series was 66.2 % of Destatis non-EU-origin mass in 2019 and 37.3 % in 2025 (value: 59.4 % -> 42.4 %). Direct extra-EU imports fell 56.2 % over 2019-2025 while non-EU-origin imports fell 22.4 %.
* Concept check for slide 8: the extra-EU balance is +0.76 Mt (2025) with Destatis origin-based imports but +3.22 Mt with Comext direct imports (4,681.2 - 1,463.6); the two must never be mixed.
* Steel-mill-like proxy (derived from published headings, HS 7207-7229 + 7304-7306): exports 26.8 / 22.8 / 22.1 Mt and imports 27.4 / 18.0 / 19.8 Mt in 2017 / 2024 / 2025p; balance -0.65 / +4.83 / +2.23 Mt. Imports +10.3 % and exports -3.3 % in 2025, so the 2017-2024 swing to a surplus partly reversed in 2025. It tracks Dataset B (balance -1.2 -> +4.1 Mt, 2017 -> 2024) in direction with a stable offset (exports 0.4-2.3 % and imports 3.8-5.1 % below Dataset B in every year 2017-2024), so it is a bridge, not a replacement.
* 2026 year to date (Jan-Aug, chapter 72, GENESIS 51000-0006): exports 20,814.6 kt (+4.7 % on Jan-Aug 2025's 19,887.6), imports 16,592.4 kt (+2.2 % on 16,233.8); value exports EUR 18,939.0 m (+4.1 %), imports 17,010.1 m (+3.5 %); all `p`. Split to July (51000-0008, August not yet published): exports to non-EU 2,513.0 vs 3,013.3 kt (-16.6 %), exports to EU27 +9.3 %, non-EU-origin imports 2,362.4 vs 2,225.8 kt (+6.1 %). For 2023-2025 the by-country monthly totals equal the commodity table; for 2026 they differ in single months by up to 1.1 % (exports) and 2.0 % (imports, June 2026), so the 2026 split is indicative.
* Total goods 2025 (51000-0001, p): exports EUR 1,564.2 bn, imports 1,361.9 bn, surplus 202.3 bn (chapter 72 = 1.7 % / 1.8 %). Destatis releases: 6 Feb 2026 1,562.9 / 1,362.5 / 200.4 (as quoted in the workbook; that page not opened); press release no. 056 of 20 Feb 2026 1,563.0 / 1,362.5 / 200.5. Jan-Aug 2026 (press release no. 356, 8 Oct 2026): exports EUR 1,092.7 bn and imports 946.7 bn, +4.4 % each, calendar and seasonally adjusted.

### 2. Production index and employment

* Eurostat's annual manufacturing series in workbook table 4.1 is Destatis data: all 31 years 1995-2025 agree (production index |diff| <= 0.05 on the annual mean of 12 unadjusted months; real GVA index diff 0.00; GVA share |diff| <= 0.05 pp). 2025 = 92.75 -> 92.8.
* WZ08-24 basic metals (2021=100): 110.0 (2015), 104.6 (2019), 91.0 (2020), 96.0 (2022), 90.0 (2024), 88.1 (2025). WZ08-24.1 basic iron and steel: 91.73 (2024) -> 86.58 (2025), -5.6 %. WZ08-25 fabricated metals 88.0 -> 85.8. 2026 Jan-Aug mean vs same months of 2025: C -1.9 %, 24 +1.0 %, 24.1 +9.0 %, 25 -1.3 % (Jan-Jul revised, Aug provisional; Sep-Dec empty).
* 2025 vs 2024 for manufacturing: production -1.16 % unadjusted and -0.93 % calendar and seasonally adjusted; turnover -1.41 % (42111; EUR 2,119.4 bn vs 2,149.7 bn); employees -1.93 %.
* Employment: national accounts (domestic concept) manufacturing 7,490 / 7,415 / 7,262 thousand (2023 / 2024 / 2025p), range 7,262-7,773 over 2015-2025 (peak 2019); basic metals 245 thousand (2024; 2025 not yet published); manufacturing GVA share 19.93 % (2024), 19.42 % (2025p). Establishment surveys: 42111 (Monatsbericht, press release: establishments with 50+ employees) manufacturing 5,566,649 / 5,540,101 / 5,433,048 (2023-2025, annual figures, final); basic metals 227,406 -> 215,640 (-5.2 %); steel 24.1 70,458 -> 68,993 (-2.1 %); turnover of 24.1 EUR 38.8 bn -> 36.2 bn (-6.6 %). 42271 (annual survey, larger coverage, threshold not verified): manufacturing 6,215,663 -> 6,086,878.
* Destatis press release no. 127 of 2 Apr 2025 (read): about 5.5 million persons worked in manufacturing establishments with 50+ employees at the end of 2024, metal production and processing 225,000; this is the "5.5 million" in the chat, a different universe from the 7.4 million national-accounts figure.
* Destatis' own crude-steel series (42311-0001, "Erzeugung von Roheisen, Rohstahl, Walzstahl, Stahlrohren") ends in 2009, so Dataset A (34.1 Mt) cannot be replaced from Destatis.

### 3. Producer prices (domestic sales, 2021 = 100)

| Position | 2015 | 2019 | 2022 | 2024 | 2025 | Sep 2026 (y/y) |
| --- | --- | --- | --- | --- | --- | --- |
| GP 24.10 / 24.1 Pig iron, steel, ferro-alloys | 69.8 | 78.9 | 135.2 | 108.0 | 101.2 | 107.9 (+8.4 %) |
| GP19-24103 hot-rolled flat | 70.7 | 80.2 | 142.6 | 114.1 | 106.8 | 117.0 (+11.5 %) |
| GP19-24104 cold-rolled flat (>=600 mm) | 62.7 | 71.5 | 128.5 | 93.7 | 85.4 | 97.0 (+14.4 %) |
| Reinforcing bars (GP19-241062100) | 59.0 | 71.6 | 133.7 | 88.3 | 87.0 | 91.8 (+7.0 %) |
| GP 24 Metals | 77.9 | 83.8 | 126.2 | 114.3 | 114.3 | 128.9 (+14.0 %) |
| Industrial products, total | 87.9 | 92.1 | 129.8 | 127.7 | 126.2 | 133.7 (+6.7 %) |

Latest month is September 2026 (released 20 Oct 2026); Oct-Dec 2026 are empty. Cross-check: Destatis press release no. 373 (20 Oct 2026, via search result; page not opened) reports total +6.7 %, pig iron/steel/ferro-alloys +8.4 % and reinforcing steel +7.0 %, which equal the recomputed values. This is the domestic steel price series the audit found missing; it is a price index of domestic sales, not an import price.

### 4. National accounts, 2025 (GDP use side)

Vintages of 2025 real growth (`national_accounts_2025_vintage_comparison.csv`): first estimate 15 Jan 2026 (press release no. 017: GDP +0.2, private consumption +1.4, government +1.5, GFCF -0.5, exports -0.3, imports +3.6) -> Destatis summer revision page (Stand 25 Aug 2026, updated 30 Sep 2026; revised 2022-2025, and 2011-2021 outside the usual schedule): GDP +0.2, private consumption +1.3, government +1.7 (was 1.5), GFCF -0.6 (was -0.2 before the revision). The page lists no export/import rates; computed from the chain-linked volumes in GENESIS 81000-0019/-0027 (current vintage): exports -0.95 % (goods -1.40 %, services +0.43 %), imports +2.86 % (goods +3.83 %, services +0.72 %), households-only consumption +1.35 %, equipment investment -1.30 %, construction -0.98 %. Net exports contribute -1.5 pp (exports -0.4, imports -1.1; published). Nominal GDP EUR 4,529.710 bn (previously 4,469.810 bn). Nominal exports/imports (national accounts concept) EUR 1,816.0 bn / 1,715.7 bn, net exports EUR 100.3 bn (156.7 bn in 2024). GDP 2024 is now 0.0 % and 2023 -1.0 %.
Bundesbank (not Destatis): current account 2025 about EUR 203 bn (Monatsbericht March 2026 article "Die deutsche Zahlungsbilanz fuer das Jahr 2025", published 26 Mar 2026; down 52 bn, about 4.5 % of GDP; goods surplus in the balance-of-payments concept 184.2 bn).

## Caveats and unresolved

* Growth rates marked "computed" are 100 x (volume_t / volume_t-1 - 1) from published chain-linked volumes (bn EUR, 3 decimals); they are not published rates. The export figure -0.950 % sits exactly on the rounding boundary between -0.9 and -1.0; the published rate was not found.
* 2025 foreign-trade and national-accounts data are provisional (`p`). Jan-Aug 2025 chapters 72+73 recomputed from the current database give exports EUR 39.74 bn (-5.19 %) and imports 33.68 bn (-4.02 %); Destatis' press release no. 380 of 20 Oct 2025 gave 39.9 bn (-4.8 %) and 34.0 bn (-2.7 %). The gap (0.4 % and 1.0 % in level, 1.3 pp in the import change) is consistent with revision of the provisional data but was not reconciled.
* Not obtained: monthly EU/non-EU split for August 2026 (the by-country table ends in July); 2025 basic-metals GVA and employment in the national accounts (flag `...`); published current export/import growth rates; Destatis crude steel after 2009; PRODCOM steel quantities were not extracted.
* The Jan 2026 and August 2026 national-accounts figures were read from Destatis pages and are typed into the vintage CSV; the three-vintage comparison is therefore only as good as those pages. The "Alt" GFCF value (-0.2) is as shown on the revision page and was not independently checked.
* Production-index annual values are my annual means of the 12 unadjusted monthly values (Destatis' table gives monthly values only); they reproduce Eurostat's annual series, which supports the method.
* 42271 coverage (establishment size) was not found in the table metadata; the larger employee counts imply it includes smaller establishments than 42111.
* The derived steel-mill-like aggregate is a team construction from published headings, not a Destatis or German Steel Federation definition.
