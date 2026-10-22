# steel_route: did German steel become cleaner? Outcome series

Retrieved 2026-10-22 (all live downloads and archive copies on that date). Task: find verifiable annual outcome series for German iron and steel (production route, EU ETS emissions, emissions per tonne of crude steel) for the 15-minute deck on EU ETS and CBAM. Nothing in this folder estimates, interpolates or recalls a number: every figure was read from a document that was opened, and the cited page text was re-checked by script (see "Checks").

## Result in one paragraph

Route mix: the electric-arc (scrap-based) share of German crude steel was 29.2 percent in 1999 and 30.5 percent in 2025 (WV Stahl revision; worldsteel prints 30.6), inside a range of 27.7 to 34.7 percent with no trend; the blast-furnace/oxygen route still makes about 70 percent. ETS: verified emissions of German iron and steel installations (DEHSt sector "Eisen und Stahl") are available for every year 2005-2025 but in three different installation scopes. In the current scope (2013-2025) they went from 35.65 Mt CO2e (2013) to 30.0 Mt (2025), while crude steel went from 42.6 Mt to 34.3 Mt, so emissions per tonne of crude steel (derived) were 0.84 t in 2013 and 0.88 t in 2025 (range 0.84 to 0.92): no measured fall per tonne. WV Stahl's own specific CO2 (incl. purchased power, excl. coke ovens) is 1.59 t per t crude steel in 1990, 1.37 in 2019 and 1.39 in 2025 (minus 12.6 percent since 1990, plus 1.5 percent since 2019). So the data show lower absolute emissions because output fell, and no visible outcome improvement per tonne yet; they cannot show a policy effect.

## Files

| File | Content |
| --- | --- |
| `crude_steel_by_route_germany_1999_2025.csv` | Crude steel, oxygen (BOF) and electric (EAF) output in kt and shares, 1999-2025, with source, table and page for each row. 2020 kt is missing (only Mt and published % exist in a table I could open). |
| `ets_emissions_german_iron_steel_2005_2025.csv` | Verified emissions, DEHSt sector Eisen und Stahl, 2005-2025: preferred value, first publication, later restatement, scope segment (A, B, C), number of installations, report and page. |
| `ets_co2_per_tonne_crude_steel_derived_2005_2025.csv` | DERIVED ratio ETS emissions / crude steel, with scope segment and the WV Stahl specific CO2 series for 2019-2025. Only compare within a segment. |
| `ets_route_emissions_and_per_tonne_2018_2022.csv` | DEHSt route emissions (blast-furnace route incl. coke ovens and sinter; electric-arc route, direct only) and derived t CO2e per t of route output, 2018-2022. |
| `process_gas_forwarded_to_energy_installations.csv` | Emissions from iron-and-steel process gases that are released at energy installations and therefore are not in the Eisen und Stahl row (2013, 2014, 2019, 2020). |
| `wv_stahl_specific_co2_per_tonne.csv` | WV Stahl specific primary-energy-related CO2 per tonne of crude steel and of hot-rolled products: 1990 and 2019-2025, by brochure edition and page. |
| `free_allocation_context_german_iron_steel_2019_2024.csv` | Free allocation to iron and steel installations vs emissions (nominal and adjusted for forwarded gases), 2019-2024. |
| `eu27_route_share_2025_context.csv` | Oxygen and electric shares 2025 for EU27 member states in the worldsteel table. |
| `dehst_uba_statements_paraphrased.csv` | Paraphrased DEHSt and UBA statements with locators. |
| `chart_data_cleaner_steel_indicators.csv`, `chart_proposal_cleaner_steel.png` | Data and preview of the recommended two-panel chart. |
| `sources_manifest.csv` | Every document used: title, date, URL, access route, evidence file. |
| `scripts/build_tables.py`, `scripts/make_chart.py` | Code that reads `raw/evidence/` and writes the CSVs and the chart. Run with `python -I -X utf8`. |
| `raw/evidence/` | One small PDF per source with only the pages cited (about 6 MB in all), plus two `pdftotext` extracts used by the checks. |
| `raw/uba_6_tab_2026-09-24.*`, `raw/uba_pm_17_2026_extract.txt` | UBA sector table (PDF, PNG, text) and a text extract of the UBA press release. |
| `raw/wvstahl/` | The five WV Stahl annual crude-steel tables by route (2021-2025, one page each) and the text of the 2025 annual press release table. |

## Units, definitions, conversions

- Crude steel and route output: thousand tonnes (kt); Mt = kt / 1,000. worldsteel tables are in thousand metric tonnes; WV Stahl tables are "in 1.000 Tonnen". Oxygen = blast furnace plus oxygen converter (BOF); electric = electric furnaces (arc and induction; for Germany essentially arc). Open-hearth and other routes are nil for Germany in all tables read.
- Emissions: kt or Mt CO2-equivalent as printed by DEHSt ("kt CO2-Äq"). Preferred value for a year is the number in the following year's report if DEHSt restated it, otherwise the first publication. 2007 is derived as the sum of the comparison-set rows in the 2008 report; 2005 and 2006 are sums of three activity rows (the arithmetic is written in the source column).
- Share of electric steel = electric kt / (oxygen kt + electric kt), 2 decimals; worldsteel's printed share is kept in a separate column.
- Derived intensity = emissions kt / crude steel kt = t CO2e per t crude steel. Crude steel for 2005-2019 is oxygen plus electric kt from the worldsteel yearbooks (this equals the printed total where checked, e.g. 43,297 kt for 2017); 2020 is 35,700 kt (35.7 Mt, one decimal, worldsteel World Steel in Figures 2021; also printed in the WV Stahl 2026 brochure chart); 2021-2025 are the WV Stahl revision totals.
- No currency or 100-kg conversions are used in this folder.

## Exact retrieval

1. UBA sector table, live: `https://www.umweltbundesamt.de/system/files/medien/384/bilder/dateien/6_Tab_Emi-Anlagen-nach-Branchen_2026-09-24.pdf` (one page; row "Eisen und Stahl": 31.1 average 2008-2012, 36.3 average 2013-2020, then 31.5 / 35.4 / 33.2 / 32.5 / 33.1 / 30.0 Mt for 2020-2025, 115 installations in 2025; source line DEHSt Treibhausgas-Emissionen 2025, Stand 05/2026). Older editions at `.../sites/default/files/medien/384/bilder/dateien/6_tab_emi-anlagen-nach-branchen_2025-10-01.pdf` and `..._2024-08-27.pdf` returned HTTP 404 when requested.
2. UBA press release No. 17/2026 of 2026-07-07, live: `https://www.umweltbundesamt.de/presse/pressemitteilungen/europaeischer-emissionshandel-deutsche-emissionen`.
3. DEHSt VET reports ("Treibhausgasemissionen 20XX", from 2023 "Emissionssituation ..."). The live DEHSt server (`https://www.dehst.de/SharedDocs/downloads/DE/publikationen/VET-Bericht-YYYY.pdf?__blob=publicationFile&v=N`) returned a maintenance page (188 bytes) for every request on 2026-10-22, also via WebFetch. The PDFs were therefore taken from the Internet Archive as `https://web.archive.org/web/<timestamp>if_/<original DEHSt URL>`; timestamps and file names per report are in `sources_manifest.csv` (reports 2006, 2008-2024; no 2007 report and no 2025 report was available). The Wayback availability API (`https://archive.org/wayback/available?url=...`) and the CDX endpoint (`https://web.archive.org/cdx/search/cdx?url=dehst.de/SharedDocs/downloads/DE/publikationen/VET-Bericht&matchType=prefix&filter=mimetype:application/pdf`) were used to find the copies.
4. worldsteel, live: `https://worldsteel.org/wp-content/uploads/Steel-Statistical-Yearbook-2009.pdf`, `...-2018.pdf`, `...-2019-concise-version.pdf`, `...-2020-concise-version.pdf`; World Steel in Figures `https://worldsteel.org/wp-content/uploads/World-Steel-in-Figures-2026.pdf` (and the 2010-2025 editions under the names listed in the manifest). Yearbooks for 2021 onward were not found under the same file-name pattern (HTTP 404), so 2020 onward rests on World Steel in Figures and the WV Stahl tables.
5. WV Stahl, live: `https://www.wvstahl.de/konjunkturinformationen/` lists the annual "Rohstahlproduktion in Deutschland 20XX, Gesamtuebersicht" PDFs (2021-2025) under `https://www.wvstahl.de/wp-content/uploads/`; the brochure `https://www.wvstahl.de/wp-content/uploads/20261008_WV-Stahl_Daten-und-Fakten-2026_RZ_Web.pdf` (published 2026-10-08) and earlier editions (names in the manifest). The 2020 edition was fetched as an archive copy (`20241218114834`). Annual press release 2025: `https://www.wvstahl.de/pressemitteilungen/jahresbilanz-der-stahlproduktion-2025-viertes-krisenjahr-in-folge/`.
6. EEA "EU ETS data from the Union Registry" (2005-2025, edition 25 Sep 2026, record `https://sdi.eea.europa.eu/catalogue/srv/api/records/9eee3fc9-3060-4e3f-bc8d-e22e7c3f6bda`): the download endpoints (`https://sdi.eea.europa.eu/data/9eee3fc9-3060-4e3f-bc8d-e22e7c3f6bda` and the datastore path) failed on 2026-10-22 (HTTP 400 "Failed communicate with Nextcloud" and HTTP 503). That installation-level file is the best way to build a scope-consistent series by activity code; it is NOT used here. Retry later.

## Checks performed

- Every number typed in the build script was asserted to appear in the text of the evidence page it cites (script stops otherwise); worldsteel and WSIF rows were parsed from the PDFs by coordinates, not typed.
- Yearbook values were checked visually on rendered crops for the Germany rows of Tables 7 and 8 (2009 and 2018 yearbooks) and on rendered pages for WSIF 2025/2026 and for all WV Stahl CO2 pages.
- Overlap 2008 is identical in the 2009 and 2018 yearbooks; the 2017 values are identical in the 2018 yearbook and the 2019 concise yearbook.
- Route totals: oxygen plus electric equals the printed total for 2007 and 2017 (checked), and for each WV Stahl table (within 1 kt).
- Share cross-check: worldsteel printed share vs share from kt differs by at most 0.15 percentage points except 2017 where WSIF 2018 showed a first estimate (28.8 percent electric) later replaced by the final yearbook figure (30.0).
- Cross-source check of route change rates: DEHSt (from WV Stahl) says oxygen steel minus 0.9 and electric minus 10.8 percent in 2023, plus about 3 and plus 10.2 percent in 2024; the revision kt tables give minus 1.1 / minus 10.7 percent (2023) and plus 3.6 / plus 10.3 percent (2024), and for 2025 minus 10.1 / minus 3.4 percent against the preliminary release's minus 10.7 / minus 3.5 percent (vintage differences between preliminary and revised monthly data).
- UBA 2026 table vs DEHSt report values: agree within 0.06 Mt for 2020-2025. Averages recomputed from the report vintages: 2008-2012 = 30.86 Mt (UBA table 31.1) and 2013-2020 = 36.03 Mt (UBA table 36.3); the 0.2-0.3 Mt gap is a vintage and scope effect (the UBA table includes installations no longer in the ETS), below 1 percent.
- Triangulation of the per-tonne result: DEHSt-based ratio (0.836 to 0.876 in 2013-2025, scope C) and the independent WV Stahl series (1.37 in 2019, 1.39 in 2025) both show no fall.
- WV Stahl brochure 2026 p.16 (Stahl 46 Mt CO2 of 144 Mt industry in 2025) is about 16 Mt above the ETS row (30.0 Mt), consistent with process gases burned at power plants (16.8 Mt in 2020).

## Caveats (what the numbers cannot do)

1. Scope breaks. DEHSt changed the installation scope in 2008 (second trading period: coke ovens, sintering, integrated works, processing) and in 2013 (third period: activities 8 to 11, about 80 more mostly small processing plants). Levels are comparable only within segment A (2005-06, 2007 transitional), B (2008-2012) and C (2013-2025). The jump in the derived ratio from 0.73 (2012) to 0.84 (2013) is the scope change. DEHSt itself publishes a scope-adjusted series only as an unlabelled bar chart (VET 2014 Abbildung 9, VET 2019 Abbildung 20); its text says emissions were 2 percent higher in 2017 than in 2005 and 9 percent lower in 2019.
2. Boundary of the sector row. Process gases from coke ovens, blast furnaces and converters are sent to power plants and burned there; those emissions (16.8 to 21.8 Mt in the years read: 2013, 2014, 2019, 2020) are counted under energy installations, not under Eisen und Stahl. The row also contains coke ovens, sintering and processing (rolling) plants. Direct emissions only; electricity purchased by electric-arc plants is not included.
3. Utilisation effect. Blast-furnace emissions are largely fixed; in low-output years the ratio rises (2023: 0.92 with output 35.4 Mt). Capacity utilisation was below 70 percent in 2025 (WV Stahl).
4. Route share is a proxy: the electric share depends on scrap supply, relative demand for long and flat products and plant closures, and the 2009 peak (34.7 percent) is a recession artefact. A scrap-based electric-arc route is cleaner per tonne but does not itself show hydrogen-based direct reduction, which has not started in Germany (the workbook's company cases, outline S9, place first direct-reduction output at 2027 or later).
5. Precision. 2023 and 2025 ETS values are published to 0.1 Mt only; 2020 crude steel is 35.7 Mt (one decimal); revisions of 0.1-0.4 Mt between vintages exist. Crude steel 2024 and 2025 have two vintages (see discrepancies).
6. Not causal. No series here identifies an effect of the ETS or CBAM; CBAM payments begin in 2027, and exports, imports and steel consumption are not netted out (these are production-side indicators).
7. Free allocation: nominal ratios of 128-144 percent of emissions are inflated by allowances that are passed on for forwarded process gases; DEHSt's adjusted ratio is 83.5-108 percent (94.2 percent in 2024). No 2025 allocation figure was obtained.

## Recommended chart (slide 10 Q row link, appendix A8)

Two panels, descriptive title "Has German steel become cleaner? Outcome indicators". Panel 1: line, electric-arc share of German crude steel in percent, 1999-2025 (27 points; y-axis from 0 to 60 so that flatness is not exaggerated; label 2009 as a recession artefact; optional reference text: EU27 45.8 percent in 2025). Panel 2: two lines in t CO2 per t crude steel, 2013-2025: ETS-reported emissions of iron and steel installations divided by crude steel (0.84 to 0.92) and WV Stahl specific CO2 including purchased power (2019-2025: 1.37 to 1.43), with the note that the boundaries differ and that only trends are comparable. Footer: sources and "does not show a policy effect; process gases burned at power plants are excluded from the ETS line". Data: `chart_data_cleaner_steel_indicators.csv`; preview: `chart_proposal_cleaner_steel.png`.

## Discrepancies against the workbook (Dataset A and S22 text)

- 2017-2023 crude steel (43.3, 42.4, 39.6, 35.7, 40.2, 36.9, 35.4 Mt) agree with the yearbook and WV Stahl revision tables after rounding.
- 2024: workbook 37.2 Mt (WV Stahl brochures, Destatis); the WV Stahl revision table of July 2025 gives 37,310 kt (37.3 Mt). Difference 0.11 Mt (0.3 percent).
- 2025: workbook 34.1 Mt (worldsteel; WV Stahl preliminary 34,090 kt; also printed in the 2026 brochure); the WV Stahl revision of August 2026 gives 34,267 kt (34.3 Mt). Difference 0.18 Mt (0.5 percent). Route split: 69.4 / 30.6 percent (worldsteel, confirmed on the Germany row of the table) vs 69.5 / 30.5 percent in the revision table.
- The workbook figure 69.4 percent oxygen is correct for Germany; the world average of oxygen steel in the same publication is also 69.4 percent (coincidence; page 4 of WSIF 2026), so keep the labels apart.

## Not obtained

EEA/EUTL installation-level emissions (endpoint down); DEHSt VET report 2025 and 2007 (not reachable or not archived); DEHSt route emissions after 2022; free allocation 2025; WV Stahl specific CO2 before 2019 and for 2023-vintage restatements; German route data 2020 in kt.
