# Policy status refresh (EU ETS + CBAM, iron and steel)

Retrieved: 2026-10-22 (all pages and documents below were fetched live on that date; "as of" dates in the tables are the dates printed on each source).
Scope: legal and policy items the outline flags as "needs refresh": downstream CBAM extension, the steel trade measure that replaced the safeguard, CBAM definitive-regime dates and threshold, and any new ETS/CBAM legal changes in Sep-Oct 2026.
Nothing in this folder was typed from memory. Every number in the tables comes from a document opened during this run (file or URL in `source_log.csv`). Where a figure could not be verified it is marked unresolved.

## Headline results

| Item | Result | Confidence |
| --- | --- | --- |
| Downstream CBAM extension | Commission proposal 17 Dec 2025 (COM(2025) 989; 180 downstream products; start 1 Jan 2028). Council general approach 12 Jun 2026 (keeps 1 Jan 2028 start, adds codes). Parliament plenary position 15 Sep 2026, 464-50-159, file referred back to ENVI for negotiations. Not law. Trilogue: schedule only from a law-firm note (first political trilogue 20 Oct, next 30 Nov provisionally, aim: agreement before end 2026); outcome of 20 Oct not found. | High for dates and votes; medium for trilogue schedule; product totals for Council/Parliament unresolved |
| Steel measure | Regulation (EU) 2026/1384, dated 17 Jun 2026, OJ 24 Jun 2026, applies 1 Jul 2026; Council adoption 8 Jun 2026. Duty-free quota 18 345 922 t a year (18.3 Mt), out-of-quota duty 50% (was 25%), about 47% below 2024 safeguard quotas. | High |
| U7 wording | "18.3 million tonnes annually and a 50% out-of-quota duty" describe the NEW regime, not the 2024 base. | High |
| CBAM dates | 1 Jan 2026 start, 50 t threshold, certificate sales from 1 Feb 2027, first declaration/surrender 30 Sep 2027: all confirmed in the Official Journal text and the Commission Q&A updated 15 Oct 2026. No change since 2026-10-11. | High |
| Threshold assessment | Commission notice of 30 Sep 2026: 50 t would exempt 0.87% of embedded emissions (1 Apr 2025 - 31 Mar 2026), below the 1% limit. Confirmed. | High |
| New legal change not in workbook | Commission ETS-review proposal of 17 Jul 2026 (COM(2026) 616) would stretch the CBAM-sector free-allocation phase-out from 2034 to 2038 (CBAM factor 15% for 2034-2037). Proposal only; Environment Council debated it on 12 Oct 2026 without a decision; Irish Presidency targets a general approach in December. | High that it is a proposal; high on the numbers |

## Files

| File | Content |
| --- | --- |
| `policy_status_items.csv` | One row per item checked: value, status against the workbook, dates, URL, confidence, note |
| `steel_measure_parameters.csv` | Parameter table for Regulation (EU) 2026/1384 (quota, duty, comparison base, dates) |
| `cbam_factor_schedule.csv` | CBAM factor 2026-2038: current law versus the 17 Jul 2026 proposal; checked against the workbook table |
| `downstream_cbam_timeline.csv` | Dated events of the downstream file, marked primary-verified or not |
| `legal_changes_jul_oct_2026.csv` | ETS/CBAM legal events Jul-Oct 2026 with the slides they touch |
| `source_log.csv` | Every source with URL, date, retrieval method, HTTP status, local file; also the blocked sources |
| `raw/` | Saved pages (HTML), text of small documents, excerpts of large documents, `secondary_sources_log.txt`, `sha256_of_downloaded_originals.txt` |

## How the data were retrieved

- Method: `curl -sSL` with a browser-style User-Agent for Commission, Council register, Legislative Observatory and EPRS pages; `Accept: application/xhtml+xml` with `Accept-Language: eng` for Official Journal and Commission proposal texts via `https://publications.europa.eu/resource/celex/<CELEX>` (CELEX 32025R2083, 32023L0959, 32026R1384) and the CELLAR URLs listed in `source_log.csv`. HTML was converted to text with a small script (tags and scripts removed); PDFs with `pdftotext -layout`.
- Large PDFs and texts were not kept in this folder; `raw/excerpt_*.txt` hold the passages used and `raw/sha256_of_downloaded_originals.txt` holds the SHA-256 of every file as downloaded, so a re-download can be compared.
- Procedure files used: `https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference=2025/0419(COD)` (downstream CBAM), `...2025/0726(COD)` (steel regulation), `...2026/0212(COD)` (ETS Directive proposal). The EPRS briefing prints the ETS file as "2025/0212(COD)"; the Observatory and Council documents show 2026/0212(COD), which is used here.
- Sources that could not be opened (not bypassed): Council press releases and meeting pages (HTTP 403 and a browser check page), EUR-Lex HTML pages and the European Parliament document server (a bot-challenge page with no content). Where such a page was the natural source, the date was taken from the Legislative Observatory, the Commission or the Council's PDF register instead; see `B1-B4` in `source_log.csv`.
- Web-search and page-summary tools were used to discover leads. Anything learned only through them is listed in `raw/secondary_sources_log.txt` and flagged `secondary` or "medium/low" confidence.

## Units, conversions and definitions

- Quota volume: tonnes as printed in Annex II (18 345 922 t). Million tonnes = tonnes / 1 000 000 = 18.346 Mt (rounded in the Commission text to 18.3 Mt).
- "About 47%": the Commission's own rounded comparison with 2024 safeguard quotas. The old 2024 total is not stated in any source opened. The implied value 18.346 / (1 - 0.47) = about 34.6 Mt is arithmetic only and is labelled derived; do not quote it as a sourced number.
- CBAM factor = share of the free-allocation benchmark amount still granted to CBAM goods (97.5% in 2026 means 2.5% phased out). "Complement" = 100 minus factor, as in the workbook table.
- Out-of-quota duty is ad valorem and is in addition to other duties (recital 16).
- Threshold: tonnes of net mass per importer per calendar year, summed over all CN codes of iron and steel, aluminium, fertilisers and cement; electricity and hydrogen are outside it (Article 2a(4)).
- No currency conversion and no price data other than the three published CBAM quarterly prices (EUR per tCO2e) quoted as published.

## Checks performed

1. Steel measure numbers checked in three independent documents: the OJ text (Annex II, Article 2(3), Article 14, recitals 16 and 18), the pre-signature Council/EP text PE-CONS 23/26, and the Commission statements (IP/25/2293, Access2Markets 30 Jun 2026, DG TRADE page showing news up to 14 Oct 2026). All agree on 18.3 Mt / 18 345 922 t, 50%, 1 Jul 2026, 30 categories.
2. Steel adoption dates: Legislative Observatory key events (Parliament 19 May, Council 8 Jun, signed 17 Jun, OJ 24 Jun 2026) agree with the OJ header ("of 17 June 2026", 24.6.2026).
3. CBAM dates and threshold: Regulation (EU) 2025/2083 articles checked by article number (Article 2a, Article 6(1), Article 20(1), Article 22(1), Annex VII) and compared with the Commission Q&A of 15 Oct 2026 and the Commission definitive-regime page. All agree.
4. 0.87%: Commission notice text read on the Commission site; legal basis Article 2a(3) read in the OJ text, which says the assessment is due "by 30 April of each calendar year", so the 30 Sep 2026 publication is later than the legal date. The notice does not say whether a delegated act to change the threshold will follow.
5. CBAM factor table: current-law column reproduced from Directive (EU) 2023/959 Article 10a(1a) and matches the workbook table in every year 2026-2033 and 0% from 2034; the proposed column reproduced from the text of COM(2026) 616 and matches the Council Working Party table (WK 13227/2026) and a secondary summary.
6. Parliament vote: 464 / 50 / 159 from the Observatory summary; two secondary sources agree on 464, one search summary printed 264 (treated as a typo).
7. Observatory pages were read on 2026-10-22: the downstream file shows no event after 15 Sep 2026, so any trilogue outcome from 20 Oct is not yet in the official record.

## Caveats and unresolved points

- Trilogue schedule (20 Oct, 30 Nov) comes only from a law-firm note of 7 Oct 2026; I could not find any report of the 20 Oct meeting. The deck must say "negotiations under way, not law" and avoid reporting an outcome.
- Product totals under the Council and Parliament positions disagree across sources (Council: about 200, or 200 added to the Commission's 180, or just over 300 entries; Parliament: 457 or about 453). Only the Commission figure of 180 is confirmed from a primary document. Do not print a Council or Parliament total.
- The Parliament's adopted text (T10-0276/2026) could not be opened; the 5-tonne threshold for aluminium products and the start date in the Parliament text are therefore secondary.
- The outcome of the 12 Oct Environment Council is described from the Council Presidency paper (agenda and purpose, primary) and one secondary summary of the Council press page (outcome wording, medium confidence). The Council's own press page was blocked.
- The Council press release of 8 Jun 2026 was not opened; the 8 Jun date comes from the Legislative Observatory.
- A Commission web page labels the steel regulation "2026/1284" in one link; the Official Journal and other Commission pages say 2026/1384 (typo on that page).
- Anything dated after 2026-10-22 is not covered. The first CBAM Q4 2026 price will appear on 4 Jan 2027; a website's "Q4 estimate" of EUR 84.76 is not an official price and was not used.
