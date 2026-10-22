# WV Stahl (Wirtschaftsvereinigung Stahl): German primary data for Dataset A and Dataset B

Retrieved 2026-10-22 (UTC about 03:20 to 03:45) from the live site `https://www.wvstahl.de/` (the old address `stahl-online.de` redirects there). Nothing in this folder is recalled or estimated: every number was read from a WV Stahl document that was opened, by script from the PDF text layer with its colour and position (charts), or typed from the rendered page and asserted against the text layer (a few small tables). A value that is not printed stays empty.

## Result in brief

1. A newer edition exists. The 2026 brochure "Daten und Fakten zur Stahlindustrie in Deutschland" (Stand: September 2026, 48 pages, PDF created 8 Oct 2026, posted 12 Oct 2026) adds 2025 to both series. The workbook cites the 2025 edition as "Fakten zur Stahlindustrie 2025"; the real title is "Daten und Fakten zur Stahlindustrie in Deutschland" (Stand: September 2025, posted 12 Feb 2026). An official English edition of the 2025 brochure exists under the title "Facts and Figures about the Steel Industry in Germany".
2. Dataset A (crude steel 2017 to 2024): all 8 values match the 2025 edition p. 9 and the 2026 edition p. 9. The 2025 value 34.1 Mt is now confirmed by WV Stahl / Statistisches Bundesamt (2026 edition p. 9), not only by worldsteel. Caveat: WV Stahl's later revision (Aug 2026) sums to 34.267 Mt for 2025 and its July 2025 revision to 37.310 Mt for 2024, so 37.2 and 34.1 are the first-estimate vintage.
3. Dataset B (steel mill products, all partners): all 16 workbook values (8 exports, 8 imports) match the 2025 edition p. 30. In the 2026 edition 2018 to 2023 are unchanged, 2017 is no longer shown, and 2024 is revised (exports 22.9 to 23.3 Mt, imports 18.8 to 19.0 Mt). 2025 is new: exports 22.4 Mt, imports 20.5 Mt, printed saldo +1.9 Mt.
4. The workbook's balance column ("derived from rounded values") differs by 0.1 Mt from WV Stahl's own printed Saldo in 5 of 8 years (2018, 2019, 2021, 2022, 2024). WV Stahl prints: -1.2, -1.5, +0.2, +1.4, -0.5, +0.3, +3.0, +4.2, +1.9 for 2017 to 2025. The printed headline for 2024 is +4.2 Mt, not +4.1.
5. The 2025 balance direction reverses: imports rose (19.0 to 20.5 Mt) while exports fell (23.3 to 22.4 Mt), so the all-partner steel balance narrowed from +4.2 to +1.9 Mt. "Imports fell faster than exports" holds only to 2024.
6. WV Stahl publishes a German apparent-demand series, "Marktversorgung Walzstahl" (market supply of rolled steel), 2012 to 2025: 40.8 Mt (2017) to 29.1 Mt (2025), trough 26.9 Mt (2024). This closes the outline's "apparent consumption" gap for rolled steel. The formula in workbook BaseNotes-4 (production + extra-EU imports - extra-EU exports) must not be used (see "Other series extracted" below).
7. Crude steel by process (Oxygenstahl / Elektrostahl) is published by WV Stahl only for 2021 to 2025 (monthly, annual revision PDFs) and 2020 to 2025 (scrap report). Electric-steel share: 30.05, 29.81, 27.74, 29.01, 30.50 percent for 2021 to 2025 (32 percent in 2020, scrap report). 1999 to 2020 is in `data/steel_route/` (worldsteel yearbooks; read-only reference).
8. Employment: WV Stahl gives only rounded or sparse points (179 thousand in 1992, 83 thousand in 2020, 81 thousand in 2021, "rund 80.000" undated in the 2024, 2025 and 2026 editions). No annual series is published on the public pages.

## Documents opened (full list with SHA-256: `sources_manifest.csv`)

PDFs were downloaded only to the session scratch directory, not stored here (copyright). Re-download from the URLs in `sources_manifest.csv`, then run `scripts/build_tables.py`.

| Key | Document | Pages used |
| --- | --- | --- |
| ed2026 | Daten und Fakten zur Stahlindustrie in Deutschland, 2026 edition, Stand Sept 2026 | printed pp. 9, 11, 13, 14, 30, 31, 33, 34 |
| ed2025 | same title, 2025 edition, Stand Sept 2025 | pp. 9, 10, 11, 14, 30, 31, 33, 34 |
| ed2024 | same title, 2024 edition, Stand Nov 2024 | pp. 9, 11, 13, 28, 29, 30 |
| ed2025en | Facts and Figures about the Steel Industry in Germany (English 2025) | pp. 9, 14, 30, 33, 34 (official English labels only) |
| ed2021, ed2022 | Fakten zur Stahlindustrie in Deutschland 2021 and 2022 | PDF p. 10 (employment 1992 / 2020 / 2021) |
| schrott2026 | Statistischer Bericht Stahlschrott 2026 (14 Oct 2026) | pp. 3, 4 |
| rev2021 to rev2025 | Rohstahlerzeugung in Deutschland 20XX, Vollständige Übersicht (revisions Jul 2022, Jul 2023, Jul 2024, Jul 2025, Aug 2026) | 1 page each |
| q1_2026, q2_2026 | Informationen zur Stahlkonjunktur in Deutschland, Q1 and Q2 2026 | pp. 2 to 4 |
| pm2025 | Pressemitteilung Jahresbilanz 2025 (21 Jan 2026) and the Aug 2026 press release (HTML tables) | text, tables |
| jb2025 | Jahresbericht 2024/2025 | p. 7 (employment wording) |

Web pages read: `/stahl-in-zahlen/`, `/konjunkturinformationen/`, `/stahlstandort-deutschland/` ("Wege der Stahlproduktion"), the two press-release pages. Short extracts are in `raw/web_page_extracts_2026-10-22.txt`. The media list of the site was found through `https://www.wvstahl.de/wp-json/wp/v2/media?search=<term>&per_page=100` (public WordPress API). A Wayback CDX query for old `stahl-online.de` pages timed out after 60 s and was not used.

Page numbers: printed page = PDF page in the three brochures (cover is page 1). In the 2021 and 2022 editions the layout is a spread; the employment page is PDF p. 10.

## Verification of Dataset A (crude steel, million tonnes)

Table title: "Rohstahlproduktion" (English edition: "Crude Steel Production"); printed p. 9 in all three editions; source line printed: "Statistisches Bundesamt, WV Stahl". Full numbers: `dataset_a_crude_steel_verification.csv`.

| Year | Workbook | 2025 ed. p. 9 | 2026 ed. p. 9 | WV Stahl revision (kt) | Status |
| --- | --- | --- | --- | --- | --- |
| 2017 | 43.3 | 43.3 | 43.3 | n/a | match |
| 2018 | 42.4 | 42.4 | 42.4 | n/a | match |
| 2019 | 39.6 | 39.6 | 39.6 | n/a | match |
| 2020 | 35.7 | 35.7 | 35.7 | n/a | match |
| 2021 | 40.2 | 40.2 | 40.2 | 40,241 | match |
| 2022 | 36.9 | 36.9 | 36.9 | 36,861 | match (scrap report prints 36.8) |
| 2023 | 35.4 | 35.4 | 35.4 | 35,395 | match |
| 2024 | 37.2 | 37.2 | 37.2 | 37,310 (37.3) | match; revision is 0.1 higher |
| 2025 | 34.1 | not in edition | 34.1 | 34,267 (34.3); preliminary 34,090 | match to 2026 ed.; revision is 0.2 higher |

Crude steel 2025 appears in three WV Stahl vintages: 34.090 Mt (press release 21 Jan 2026, printed as 34.1 in the brochure 2026, the Q1 and Q2 2026 reports, the scrap report of 14 Oct 2026 and by worldsteel) and 34.267 Mt (revision 10 Aug 2026, +0.52 percent). The 2026 brochure and the scrap report were issued after the revision but still print 34.1. Pick one vintage for the whole 2021 to 2025 stretch and say which (see caveat 9).

## Verification of Dataset B (steel mill products, Germany, all partners, million tonnes)

Table title: "Stahlaußenhandel: Deutschland" (English edition: "Steel Foreign Trade: Germany"); printed p. 30 in the 2025 and 2026 editions (p. 28 in 2024); source line: "Amtliche Außenhandelsstatistik, WV Stahl"; unit: "Millionen Tonnen Steel Mill Products". Full numbers: `dataset_b_trade_verification.csv`; extended series: `steel_mill_products_trade_germany_2017_2025_latest_vintage.csv`.

| Year | Workbook X / M | 2025 ed. X / M / Saldo | 2026 ed. X / M / Saldo | Workbook balance (derived) |
| --- | --- | --- | --- | --- |
| 2017 | 27.3 / 28.5 | 27.3 / 28.5 / -1.2 | not shown | -1.2 (equal) |
| 2018 | 26.4 / 28.0 | 26.4 / 28.0 / -1.5 | same | -1.6 (printed -1.5) |
| 2019 | 24.8 / 24.5 | 24.8 / 24.5 / +0.2 | same | +0.3 (printed +0.2) |
| 2020 | 22.1 / 20.7 | 22.1 / 20.7 / +1.4 | same | +1.4 (equal) |
| 2021 | 24.6 / 25.0 | 24.6 / 25.0 / -0.5 | same | -0.4 (printed -0.5) |
| 2022 | 23.2 / 22.8 | 23.2 / 22.8 / +0.3 | same | +0.4 (printed +0.3) |
| 2023 | 23.0 / 20.0 | 23.0 / 20.0 / +3.0 | same | +3.0 (equal) |
| 2024 | 22.9 / 18.8 | 22.9 / 18.8 / +4.2 | 23.3 / 19.0 / +4.2 (revised) | +4.1 (printed +4.2) |
| 2025 | not in workbook | not in edition | 22.4 / 20.5 / +1.9 | n/a |

The 2024 edition printed 19.9 Mt imports and +3.2 Mt saldo for 2023 (revised to 20.0 and +3.0 in the 2025 edition). The workbook used the 2025 edition, so this is only a vintage note.

What the table includes (as printed under the chart): "Steel Mill Products (Walzstahl- und Schmiedeerzeugnisse, Rohre, kaltgewalzte Erzeugnisse)". English edition: "rolled steel and forged products, pipes, cold-rolled products". The workbook's description (rolled/forged products, pipes, cold-rolled products) is correct. The HS or CN list behind this definition is not published in any document opened: unresolved. Scrap, pig iron, ferro-alloys and direct-reduced iron are not named, so they are inferred to be outside; the reconciliation below supports this but does not prove it.

Intra-EU: the p. 30 page does not say "all partners". It is inferred, with high confidence, from p. 33: German steel mill product exports to countries outside the EU were 4.9 Mt in 2023, 4.9 Mt in 2024 and 4.1 Mt in 2025 (`de_steel_mill_product_exports_to_non_eu_by_destination_2023_2025.csv`), against 23.0, 22.9 (2025 ed.) and 22.4 Mt on p. 30. So p. 30 must include trade with other EU states: implied intra-EU exports about 18.3 Mt in 2025. By contrast the EU-27 page (p. 31) is explicitly trade with third countries ("Drittländern"). Units are million tonnes of physical weight; whether net mass is meant is not stated.

## What these WV Stahl numbers measure compared with Eurostat Comext Chapter 72

Read from `data/comext_exports/README.md` and its CSVs (not modified). `reconciliation_wvstahl_vs_comext_ch72_2017_2025.csv` holds the year-by-year arithmetic.

| Point | WV Stahl (brochure) | Comext Chapter 72 (other agent) |
| --- | --- | --- |
| Product scope | Steel mill products: rolled and forged products, pipes, cold-rolled products. Pipes are inferred to sit largely in HS Chapter 73 (the Comext README names 7304 and 7306 as Chapter 73); WV Stahl does not publish the HS list. | HS 72: includes scrap (7204), pig iron, ferro-alloys, direct-reduced iron (7203) and semi-finished products; excludes Chapter 73 pipes. |
| Partners | p. 30 all partners (intra-EU included, inferred); p. 31 EU-27 with third countries; p. 33 Germany to non-EU, by region | Partner aggregates EXT_EU27_2020, INT_EU27_2020, WORLD; fixed 2020 composition (UK counted as extra-EU) |
| Unit and basis | Million tonnes, 1 decimal, rounded; official foreign-trade statistics, aggregated by WV Stahl | Net mass from QUANTITY_IN_100KG, EUR value; exports FOB, imports CIF; extra-EU imports by country of origin, intra-EU by consignment |
| Vintage | 2025 and 2026 editions; 2024 revised in 2026 edition | One pull, 16 Oct 2026; 2023 and 2025 revised slightly against the workbook |
| Not available | No value in EUR; no extra-EU import series for Germany alone; no HS list; no monthly series on the public pages | Not the WV Stahl aggregate; includes scrap and DRI, which WV Stahl reports separately |

Numbers from the reconciliation file:

- All-partner exports: WV Stahl is 76 to 81 percent of Comext Chapter 72 tonnes (2025: 22.4 against 29.2 Mt). All-partner imports: 79 to 85 percent (2025: 20.5 against 24.1 Mt). The gap is mostly scrap: WV Stahl's scrap statistic (separate report) has total exports 7.8 Mt and imports 4.0 Mt in 2025. Chapter 72 minus WV scrap is 21.4 Mt for exports and 20.1 Mt for imports in 2025, against 22.4 and 20.5 Mt steel mill products. Over 2020 to 2025 this difference (Chapter 72 minus WV scrap, minus WV steel mill products) is -1.0 to -2.0 Mt for exports (WV higher) and -0.4 to +0.6 Mt for imports. This is an indicative arithmetic check, not a reconciliation (pipes in, pig iron / ferro-alloys / DRI out, and different cut-offs all matter).
- Scrap tie-out: WV Stahl scrap exports to third countries equal Comext 7204 extra-EU exports within 1 kt in every year 2020 to 2025 (2025: 1,231 against 1,230.8 kt), which shows WV Stahl draws on the same official trade statistics. Scrap imports do not tie: WV Stahl 577 kt against Comext 393.9 kt (2025), and 706 against 534.9 kt (2020). Unreconciled; do not mix the two.
- Extra-EU exports: WV Stahl's 4.9 Mt (2023, 2024) and 4.1 Mt (2025) of steel mill products to non-EU countries compare with Comext Chapter 72 extra-EU exports of 5.04, 5.05 and 4.68 Mt. Both fall in 2025, WV Stahl by 16 percent (4.9 to 4.1, but the 2024 value is from the 2025 edition because the 2026 edition does not print it for 2024) and Comext by 7 percent. The two are not the same universe.
- Direction in 2025 differs by product universe: WV Stahl all-partner balance narrowed to +1.9 Mt; Comext all-partner Chapter 72 balance moved from +5.24 to +5.15 Mt; Comext extra-EU balance widened from +3.09 to +3.22 Mt. Do not subtract one series from another.
- What WV Stahl adds that Comext Chapter 72 does not: the destination split of German non-EU exports (2025: Europe outside EU/CIS 40 percent, USMCA 32, Asia outside Near and Middle East 12, Africa 6, CIS/Ukraine 1, Near and Middle East 3, others 6), the EU-27 third-country trade (imports 44.9 Mt in 2025, exports 20.4 Mt, saldo -24.5 Mt), the indirect trade in steel-containing goods (cars, machinery) converted to rolled-steel weight by a coefficient that is not published (2025: exports 28.7 Mt, imports 25.5 Mt, saldo +3.2 Mt; 5.9 Mt in 2021), and production by process.
- What WV Stahl does not give: euros, HS detail, German extra-EU imports, a series before 2017 on the public pages, or the CBAM base. Neither source is the CBAM-covered product list.

## Other series extracted

| File | Content | Source |
| --- | --- | --- |
| `crude_steel_by_process_2020_2025.csv` | Oxygen and electric steel, pig iron, hot-rolled output (kt), electric share, 2021 to 2025; 2020 only in Mt | revision PDFs; scrap report p. 3 |
| `crude_steel_monthly_by_process_2021_2025.csv` | 60 monthly rows: total, oxygen, electric, pig iron, hot-rolled (kt); month sums checked against the SUMME row | revision PDFs |
| `crude_steel_2025_preliminary_and_2026_ytd.csv` | 2025 preliminary and revised; Jan to Aug 2026 provisional (23,902 kt, electric 31.1 percent) | press releases |
| `crude_steel_brochure_series_by_edition.csv` | crude steel 2010 to 2025 as printed in the 2024, 2025 and 2026 editions | p. 9 |
| `marktversorgung_walzstahl_by_edition_2010_2025.csv` | "Marktversorgung Walzstahl" (market supply of rolled steel; apparent-demand measure), three vintages | p. 13 or 14 |
| `steel_mill_products_trade_germany_2017_2025_latest_vintage.csv` | extended Dataset B with printed Saldo | p. 30 |
| `eu27_steel_mill_products_trade_with_third_countries_2017_2025.csv` | EU-27 trade with third countries | 2026 ed. p. 31 |
| `de_steel_mill_product_exports_to_non_eu_by_destination_2023_2025.csv` | German exports outside the EU by region | pp. 30, 33 |
| `indirect_steel_trade_germany_steel_containing_goods_2020_2025.csv` | trade in steel-containing goods in rolled-steel weight | p. 34 |
| `scrap_trade_germany_2020_2025.csv`, `scrap_third_country_trade_wvstahl_vs_comext_7204.csv` | scrap trade and the Comext 7204 tie-out | scrap report p. 4 |
| `steel_industry_sales_and_employment.csv` | turnover 2012 to 2025 (EUR bn, Statistisches Bundesamt via WV Stahl) and the employment points | 2026 ed. p. 13; others as listed |
| `conjuncture_indicators_wvstahl.csv` | order-intake changes, capacity-utilisation wording, demand wording | Q1, Q2 2026 reports; press release |
| `apparent_consumption_crosscheck_2021_2025.csv` | arithmetic test of three ways to build apparent consumption against WV Stahl's Marktversorgung | derived |
| `reconciliation_wvstahl_vs_comext_ch72_2017_2025.csv` | year-by-year comparison with Comext | derived |

Key readings:

- Marktversorgung Walzstahl (2026 edition, Mt): 38.1, 38.2, 39.6, 39.4, 40.6, 40.8, 39.3, 34.9, 31.5, 35.4, 32.6, 29.1, 26.9, 29.1 for 2012 to 2025. It was revised between editions: 2022 32.5 to 32.6, 2023 29.0 to 29.1, 2024 27.1 to 26.9. The Q1 2026 report says the 2025 uptick rested only on stock building (Lageraufbau), not on real demand growth. The brochure defines no formula; unresolved.
- Cross-check (derived, not a WV Stahl formula): hot-rolled output + imports - exports of steel mill products lands within -0.3 to +1.4 Mt of Marktversorgung in 2021 to 2025. Crude steel + imports - exports overstates it by 3.3 to 6.1 Mt (crude steel is not finished product). The workbook BaseNotes-4 formula (crude steel + extra-EU imports - extra-EU exports, Comext) overstates it by 1.7 to 7.3 Mt.
- Capacity: WV Stahl says 2025 capacity utilisation fell below 70 percent and treats 40 Mt a year of crude steel as the threshold for viable utilisation (press release 21 Jan 2026; Q1 and Q2 2026 reports). No annual utilisation series is published. Order intake for rolled steel changed -12.4, +0.4, -0.4, +2.1 percent in 2022 to 2025 and +7.3 percent in Jan to Jun 2026.
- Turnover of the steel industry (EUR bn): 55.2 (2022), 50.6, 45.3, 42.4 (2025), the third fall in a row.
- Employment: do not combine with Eurostat NACE C24 (basic metals, 245 thousand in the final outline): that group is much wider than WV Stahl's "rund 80.000" direct steel employees.

## Units, conversions, checks

- All tonnages are million tonnes (Mt) as printed, one decimal, or thousand tonnes (kt) where WV Stahl prints "in 1.000 Tonnen". German number format (comma decimal, point thousands) is converted by script. No currency conversion. No value is adjusted.
- Electric share = electric kt / crude kt, from the revision PDFs (2 decimals).
- Checks run by `scripts/build_tables.py` (all passed on 2026-10-22): each brochure chart returns exactly one value per year label; Dataset A and B values compared with the workbook within 0.05; monthly values sum to the SUMME row within 3 kt and oxygen + electric equals total within 2 kt; scrap-report route table adds up within 0.15 Mt; scrap trade rows add up within 2 kt; typed numbers exist in the page text layer; indirect trade saldo = exports - imports within 0.15; pie shares sum to 99 to 101 percent. Chart labels were also compared by eye with rendered pages 9, 13, 14, 30, 31, 33 and 34 of the 2026 edition, pp. 9, 14, 30 and 33 of the 2025 edition, p. 30 of the 2024 edition and pp. 3 and 4 of the scrap report.
- Run: `python -I -X utf8 scripts/build_tables.py --pdf-dir <dir> --comext-dir <repo>/data/comext_exports --out-dir <this folder>`.

## Caveats and unresolved items

1. HS or CN composition of "Steel Mill Products" and the formula of "Marktversorgung Walzstahl" are not given in any document opened. Searches for a public definition (WV Stahl, Eurofer) returned nothing usable.
2. Rounding: 0.1 Mt; printed Saldo is computed by WV Stahl from unrounded values, so it can differ by 0.1 from exports minus imports of the rounded labels.
3. Vintage drift: 2024 trade and 2022 to 2025 Marktversorgung change between editions; crude steel 2024 and 2025 change in the revision PDFs. Never mix vintages inside one series without a footnote.
4. Crude steel by process before 2020 is not on the public WV Stahl pages that were found. 1999 to 2019 is in `data/steel_route/crude_steel_by_route_germany_1999_2025.csv` (worldsteel); its 2021 to 2025 values equal the revision PDFs read here.
5. Scrap imports from third countries differ between WV Stahl and Comext (section above); cause not established.
6. The employment points are rounded text or sparse dates; the Destatis series belongs to another folder.
7. German goods trade statistics here are physical tonnes of steel products. They are not national-accounts NX (goods and services, euros) and not the balance of payments.
8. WV Stahl is an industry association; its text frames the data (import pressure, demand crisis). Only the numbers are used here.
9. A recommendation, not a source claim: choose one crude-steel vintage (brochure 34.1 and 37.2, or revision 34.3 and 37.3) for the whole slide.
