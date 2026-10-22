# Gephi: company-case network

An evidence map of the dated company cases and public funding used in the deck. It is descriptive, not a causal model: every edge is an announcement, agreement or approval, and `Delivery_status` says whether anything is verified as delivered.

## Files

- `nodes.csv` — 11 nodes (producers, buyers, a hydrogen supplier, one public-funding node).
- `edges.csv` — 7 directed edges. `Source_tag` points to the source library in `sources/text/inter-trade-present-2-revised-research-brief.txt` (U10, U13–U17). `B-funding` means the base workbook section "Funding criteria for German DRI/H2 steel" (`sources/text/inter-trade-present-base.txt`, lines 649–651).

## Build steps (Gephi 0.11.x)

1. File → New project. Data Laboratory → Import Spreadsheet.
2. Import `nodes.csv` as *Nodes table* (separator comma, Id column = `Id`), then `edges.csv` as *Edges table*. Choose "Append to existing workspace" for the edges import.
3. Overview → Layout: ForceAtlas 2 (tick "Prevent overlap"), run, then stop.
4. Appearance: node colour by partition `Role`; edge colour by partition `Status`; node label = `Label`.
5. Preview → Presets "Default Directed", show node labels, then export SVG or PNG for the slide. Save the project as `graphs/gephi/company-cases.gephi`.

## Before presenting

The workbook flags these as time-sensitive; refresh them before 16–18 November: Stegra's capital and delivery status (U16), Salzgitter and Thyssenkrupp milestone dates (U12), and any new agreements.
