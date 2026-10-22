# CBAM certificate price item (policy_status / cbam_price)

Retrieved on 2026-10-22 (local time about 09:30-09:45, UTC+7; server `Date` header of the EEX download 2026-10-22 02:37 GMT). Nothing in this folder is an estimate of a Q4 2026 certificate price. No Q4 2026 price exists on the retrieval date.

## Bottom line

| Item | Result |
| --- | --- |
| Q1 2026 price | EUR 75.36 per tCO2e, published 7 April 2026 - verified, equals workbook |
| Q2 2026 price | EUR 75.28 per tCO2e, published 6 July 2026 - verified, equals workbook |
| Q3 2026 price | EUR 82.32 per tCO2e, published 5 October 2026 - verified, equals workbook |
| Q4 2026 price | NOT PUBLISHED. The Commission table shows the publication date 4 January 2027 and an empty price cell |
| Can a Q4 price exist before 16-18 Nov 2026? | No. The price is the quarterly average over the whole of Q4 (1 Oct - 31 Dec 2026), calculated during the first calendar week after the quarter (28 Dec 2026 - 3 Jan 2027) and published on the first working day of the following week (Monday 4 Jan 2027). On 16-18 Nov the quarter is still running; the last scheduled 2026 EEX auctions are in mid-December |
| Certificate sales start | 1 February 2027 - verified (Reg 2023/956 Art 20(1)), unchanged |
| First declaration and surrender | 30 September 2027 for the year 2026 - verified (Art 6(1), Art 22(1)), unchanged |
| Latest verifiable EUA auction clearing price | EUR 85.10 per tCO2 on 20 Oct 2026 (EEX common platform, 2,791,500 EUAs); German-platform auction 16 Oct 2026: EUR 85.50 |

## Sources opened (all primary)

1. Commission, "Price of CBAM certificates" - https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/price-cbam-certificates_en (page metadata: datePublished 2026-04-07T10:51:43+02:00, dateModified 2026-10-05T09:30:14+02:00). Raw: `raw/price_cbam_certificates_2026-10-22.html`. The workbook's search path `.../cbam-certificate-prices_en` returns HTTP 404; the live URL is the one above.
2. Commission, "CBAM definitive regime" - https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-definitive-regime_en (dateModified 2026-08-10). Raw: `raw/cbam_definitive_regime_2026-10-22.html`.
3. Commission, "CBAM legislation and guidance" - https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-legislation-and-guidance_en (dateModified 2026-09-24). Raw: `raw/cbam_legislation_2026-10-22.html`.
4. Commission, "CBAM communication and news" - https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-communication-and-news_en (dateModified 2026-10-05). Raw: `raw/cbam_news_2026-10-22.html`. Also the news item of 30 Sep 2026 `raw/news_webinar_followup_2026-09-30.html` (states 30 September 2027 as the first compliance deadline).
5. Commission Implementing Regulation (EU) 2025/2548 of 10 Dec 2025 (OJ L, 22.12.2025) on calculation and publication of the CBAM certificate price - fetched from the Publications Office: `curl -L -H "Accept: application/xhtml+xml" -H "Accept-Language: eng" https://publications.europa.eu/resource/celex/32025R2548`. Raw: `raw/ir2025_2548_cellar.xhtml`, text in `raw/ir2025_2548_text.txt`.
6. Regulation (EU) 2025/2083 of 8 Oct 2025 (OJ L, 17.10.2025; in force on the third day after publication, i.e. 20 Oct 2025): `https://publications.europa.eu/resource/celex/32025R2083` (same headers). Raw: `raw/reg2025_2083_cellar.xhtml`, `raw/reg2025_2083_text.txt`.
7. Consolidated Regulation (EU) 2023/956 as at 20.10.2025 (documentation tool, no legal effect; the Commission legislation page links this as the consolidated version after 2025/2083): `https://publications.europa.eu/resource/celex/02023R0956-20251020` (same headers). Raw: `raw/reg2023_956_consolidated_20251020.xhtml`, `raw/reg2023_956_consolidated_text.txt`.
8. EEX primary-market auction report 2026 (all EUA auctions on the common platform CAP3, Germany, Poland and the Northern Ireland auction): `https://public.eex-group.com/eex/eua-auction-report/emission-spot-primary-market-auction-report-2026-data.xlsx` (HTTP Last-Modified 2026-10-20 09:02:01 GMT; covers auctions 2026-01-07 to 2026-10-20). Raw: `raw/eex_emission_spot_primary_market_auction_report_2026.xlsx`, headers in `raw/eex_headers.txt`.
9. EEX press release 30 Jul 2026 (revised 2026 calendar, Q4 volumes) `raw/eex_pr_20260730_auction_calendar_update.pdf`; EEX press release 28 Jul 2025 (auction day pattern and last 2026 auction dates) `raw/eex_pr_20250728_auction_calendar.pdf`; EEX customer information 11 Dec 2025 `raw/eex_auction_calendar_2026_20251211.pdf`. Text extracts are the `*_text.txt` files.

SHA-256 of each raw file can be recomputed with `sha256sum raw/*`.

## Legal rule for the 2026 quarterly prices (exact wording, abbreviated)

- Reg 2023/956 Art 21(1a): for emissions declared for 2026 the price is "the quarterly average of the closing prices of EU ETS allowances on the auction platform ... of the quarter of importation of the goods". Art 21(1): from 2027 the price is the average per calendar week.
- IR 2025/2548 Art 1(1)-(2): quarterly average of auction clearing prices; "The Commission shall calculate the price of a quarter during the first calendar week of the following quarter."
- IR 2025/2548 Art 1(3)-(4): all auctions on the common platform and the opt-out platforms since the last calculation, cancelled auctions excluded, each clearing price weighted by auctioned volume; Art 1(5): euro, rounded to the nearest cent; Art 1(6): the quarterly price applies to certificates for the embedded emissions of goods imported in that quarter.
- IR 2025/2548 Art 4(1): published on the Commission website "on the first working day ... of the calendar week following the week of calculation". Art 4(2): quarterly prices are available in the CBAM registry from Q3 2026.
- IR 2025/2548 Arts 5 and 8: from 1 January 2027 a weekly price, published on the first working day of the calendar week following the relevant auctions.
- Reg 2023/956 Art 20(1): "From 1 February 2027, a Member State shall sell CBAM certificates on a common central platform". Art 6(1) and Art 22(1): declaration and surrender "By 30 September of each year, and for the first time in 2027 for the year 2026". Art 22(2): from 2027 declarants must hold certificates for at least 50 percent of the embedded emissions of goods imported since 1 January of the year at each quarter end (by its wording a rule for goods imported from 2027).

Date arithmetic (`publication_timing_check.csv`, produced by `scripts/build_tables.py`): the reading "first calendar week of the following quarter = Monday-Sunday week containing the first day of that quarter; publication on the first working day of the next week" reproduces all three published dates (Q1: week 30 Mar - 5 Apr, next Monday 6 Apr is Easter Monday, published Tuesday 7 Apr; Q2: Monday 6 Jul; Q3: Monday 5 Oct) and gives Monday 4 January 2027 for Q4, which is the date the Commission table shows. The Easter Monday explanation for 7 April is my inference; the Commission page itself lists 7 April.

## Independent reproduction of the published prices (method check)

`eex_quarterly_weighted_check.csv`: volume-weighted average of the clearing prices of all EEX auctions (CAP3 + Germany + Poland + Northern Ireland) in each calendar quarter, as IR 2025/2548 Art 1 prescribes, rounded to 2 decimals:

| Quarter | EEX recomputed | Commission published |
| --- | --- | --- |
| Q1 2026 (54 auctions) | 75.3641 -> 75.36 | 75.36 |
| Q2 2026 (53 auctions) | 75.2766 -> 75.28 | 75.28 |
| Q3 2026 (59 auctions) | 82.3185 -> 82.32 | 82.32 |

All three match to the cent. Using CAP3-only auctions or an unweighted mean does not match (for example Q1 CAP3-only 75.23; unweighted 75.47), which confirms that the Commission uses all platforms and volume weights. This is a consistency check on the EEX file, not a substitute for the Commission table.

## EUA auction context for October 2026 (not a CBAM price)

`eua_auctions_october_2026.csv` lists the 14 auctions of 1-20 Oct 2026. Latest: 20 Oct 2026, EUR 85.10/tCO2 (CAP3). October CAP3 range so far: 82.60 (5 Oct) to 87.04 (13 Oct). German platform: 85.31 (2 Oct), 86.11 (9 Oct), 85.50 (16 Oct). Poland 87.02 (14 Oct). Northern Ireland 83.83 (7 Oct).

For information only, the volume-weighted average of these 14 October auctions is 85.28 (32,296,500 allowances). It is a partial-quarter figure, NOT the Q4 2026 CBAM certificate price, which is a whole-quarter average that will include auctions through the last scheduled 2026 auctions (CAP3 until 14 Dec, Germany until 11 Dec, Poland until 9 Dec 2026 per the EEX calendar of July 2025; the July 2026 revision says other auction details are unchanged). Do not show 85.28 on a slide as Q4. If the deck needs a market reference, quote the single latest auction clearing price with its date and label it "EU ETS auction, context".

## Units and conversions

EUR per tonne of CO2 (equivalent), as in the workbook. EEX columns: `Auction Price EUR/tCO2` and `Auction Volume tCO2` (number of allowances, 1 allowance = 1 tCO2). No unit conversion applied. Derived percentage changes are arithmetic on the published numbers: Q3 vs Q1 +9.2 percent (82.32/75.36), Q3 vs Q2 +9.3 percent (82.32/75.28).

## Checks performed

1. Commission price table read directly from the live page (HTML saved) - Q1-Q3 and dates equal the workbook; Q4 row has date but no price.
2. Page metadata dateModified 2026-10-05 equals the Q3 publication date, so nothing has been added since.
3. Legal text read from the Official Journal versions (2025/2548, 2025/2083, consolidated 2023/956).
4. Reproduction of Q1-Q3 prices from EEX auction data (above); revenue = price x volume holds for all 180 auctions.
5. Cross-check of EEX auction volumes with the EEX release of 30 Jul 2026 (CAP3 2,791,500; DE 1,548,000; PL 1,945,000; Northern Ireland 584,000 per auction) - the October rows carry exactly these volumes.
6. Commission legislation page lists no act after Reg 2025/2083 that changes the dates (latest listed act: Implementing Reg 2026/1740, default-values correction, July 2026).
7. Trade press found by web search (alcircle, Andersen, GMK, Eurometal) was used only to locate leads, never as the source of a figure. GMK's "6 June" for Q2 is a slip; the Commission says 6 July 2026.

## Caveats

- Direct EUR-Lex URLs return an empty HTTP 202 response to scripted clients (bot challenge). I did not try to bypass it; the legal texts come from the Publications Office (Cellar) endpoint, which serves the Official Journal XHTML of the same acts. The consolidated version is a documentation tool without legal effect; the amending act 2025/2083 itself was read for Arts 6, 20, 21, 22.
- The 30 Sep 2026 Commission factsheet "How CBAM certificates work" redirects to a DOI link that did not resolve for me; it was not used. The webinar follow-up news item (same date) was used for 30 September 2027.
- The 4 January 2027 date is the Commission's published schedule, supported by the legal timing rule; the Commission could in principle change a published schedule, but nothing indicates this.
- The last-auction dates (14/11/9 Dec 2026) come from the EEX press release of 28 Jul 2025; I did not open the full dated EEX calendar after the 2026 revisions.
- The EEX file contains only EEX-run auctions; the Commission calculation states it covers all auctions on the common platform and opt-out platforms. Because Q1-Q3 reproduce to the cent, no other platform appears to carry material 2026 volume.
- Art 22(2) quarterly holding rule: reading that it concerns goods imported from 2027 is my reading of the wording.
