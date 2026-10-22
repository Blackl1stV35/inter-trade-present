# Refresh runbook: 13–14 November 2026

Purpose: the proposal's 2026 numbers are provisional and several status items move before the 16–18 November presentations. This runbook says what to re-run, what to re-check, which text to update and how to publish. It is written so that a fresh session (human or Claude) can follow it without this conversation.

Why these dates: Eurostat releases September data and revisions on **13 Nov 2026** (about 11:00 CET, 17:00 in Thailand); the Bundestag budget committee meets 12 Nov; WV Stahl publishes September crude steel in the days around then; the team's final confirm is due 14 Nov.

Rules for the run: never invent or estimate numbers; mark anything unverifiable as unresolved; keep the wording rules of the outline ("consistent with", no causal verbs, evidence label per slide); do not put personal data into the repo (member names, student IDs, the Google Doc link and personal emails were redacted on 2026-10-22; never put the requester's email into request headers); do not change the repository's visibility; push only with `scripts/save.ps1`.

## A. Re-run the deterministic pulls

```powershell
powershell -ExecutionPolicy Bypass -File scripts\refresh_data.ps1
```

It re-pulls Comext (monthly and annual), rebuilds the tables, re-renders the five charts and logs to `notes/refresh-log.txt`. Then read `data/trade_2026/tables/ytd_comparison.csv` (Jan–Sep 2026 against Jan–Sep 2025 once September is in) and `data/comext_exports/README.md` (vintage stamp, years that moved).

## B. Re-check by hand or web (record each result with date and URL in the relevant `data/` folder)

| Item | Where to look | Slides affected |
| --- | --- | --- |
| Eurostat Comext update (should say 13 Nov 2026) and restated Jan–Aug | `data/trade_2026/raw/manifest.json` | S5, S7, S8, A6, A7 |
| Destatis Chapter 72 trade by origin (monthly, GENESIS 51000-0007/-0008) and producer price index (61241-0004) | `data/german_sources/destatis/pull_destatis.py` (about 15 minutes; stdlib only) | S5, S7, S8, S10 |
| WV Stahl crude steel for September and the route split | wvstahl.de press releases; `data/trade_2026/scripts/04_wvstahl_crude_steel.py` | S1, S10, S12 |
| SMARD industrial electricity price file (add October; state the vintage) | `data/german_sources/smard_electricity/reproduce.py` and the SMARD data file | S5, A10 |
| Eurostat provisional flags and 2025 national accounts (GVA, employment, growth) | `data/eurostat_macro/scripts/` (flag_audit.py, jsonstat_tidy.py) and the Eurostat API | S1, S6, S10 |
| Stegra: 1 Nov chief executive, financing, start date, deliveries to Mercedes-Benz or BMW | stegra.com newsroom, news.cision.com/stegra, SVT Norrbotten | S9, S11, A13 |
| Downstream CBAM extension: outcome of the 20 Oct trilogue, next dates | OEIL 2025/0419(COD), Council and Commission pages | S13 |
| ETS review (COM(2026) 616): Council position expected in December; Parliament | OEIL, Council | S4, S13 |
| Carbon contracts round 2 awards (Nov–Dec) and the industrial power price | Projektträger Jülich, BMWE (blocked for bots; use trade press with a note) | S9, S11, A11 |
| Bundestag: budget committee 12 Nov, vote 27 Nov (EUR 2.7 bn diversion from the climate fund) | dserver.bundestag.de | S13, A6 |
| CBAM price page: Q4 2026 is due 4 Jan 2027 and must stay empty | taxation-customs.ec.europa.eu price-cbam-certificates | S5, A3 |
| Latest EUA auction price (context only) | EEX auction report | A3 |

## C. Update the text and the figures

1. Replace stale numbers in `outline/final-outline-proposal.md` (S4, S5, S7, S8, S10, S12, S13, section 6, A3, A6, A7) and note the new vintage dates. Keep "provisional" wording for 2026 data. If September is available, compare Jan–Sep 2026 with Jan–Sep 2025, never partial 2026 with full-year 2025.
2. If a headline changes sign or size by more than a few points, re-read the surrounding sentence; the headline depends on the cutoff (+6.1% at July, +7.7% at August in the 22 Oct pull).
3. Update hard-coded numbers inside the chart scripts only where they are typed labels (`graphs/gnuplot/*.gp`: balance rows in `s8_steel_trade_balance.gp`, annotation texts in `s7_extra_eu_imports.gp`, 2025 tags in `a8_cleaner_steel_outcome.gp`); the curves read the CSV files.
4. Add a short entry to `notes/refresh-log.txt` summarising what moved and what did not.

## D. Rebuild, check, publish

```powershell
. scripts\env.ps1
python -I -X utf8 scripts\build_pdf.py outline\final-outline-proposal.md outline\final-outline-proposal.pdf
powershell -ExecutionPolicy Bypass -File scripts\save.ps1 -Message "Refresh 13-14 Nov 2026: <what changed>" -Paths '.'
```

Open the PDF pages that contain changed figures and check text is not clipped. Report to the requester: what changed, what is still unresolved, and anything that contradicts a slide message.

## E. Known limits

- Eurostat restates earlier months; the +7.7% / −0.7% / −16.3% figures of the 22 Oct pull will change.
- BMWE and EUR-Lex pages block automated access; do not bypass, use secondary sources and label them.
- The Q4 certificate price (due 4 Jan 2027) will not exist; never insert an estimate.
