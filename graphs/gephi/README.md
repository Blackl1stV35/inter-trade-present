# Gephi: company-case network

An evidence map of the dated company cases and public funding used in the deck. It is descriptive, not a causal model: every edge is an announcement, agreement or approval, and `Delivery_status` says whether anything is verified as delivered. No edge is a verified delivery.

## Files

- `nodes.csv` — 11 nodes (producers, buyers, a hydrogen supplier, one public-funding node).
- `edges.csv` — 7 directed edges. `Source_tag` points to the source library in `sources/text/inter-trade-present-2-revised-research-brief.txt` (U10, U13–U17). `B-funding` means the base workbook section "Funding criteria for German DRI/H2 steel" (`sources/text/inter-trade-present-base.txt`, lines 649–651).
- `RenderNetwork.java`, `render_network.ps1` — the headless Gephi run that produced the pictures (below).
- `s9_company_network.gephi` — Gephi project of the slide S9 cut (8 nodes: the three cases and the state aid); `a13_company_network_full.gephi` — all 11 nodes (backup A13). Open them in the Gephi window to inspect or edit.
- Exports: `../out/s9_company_network.png|svg` (S9) and `../out/a13_company_network_full.png|svg` (A13).

## How the pictures were made (Gephi Toolkit 0.11.3, no Gephi window)

`powershell -ExecutionPolicy Bypass -File graphs\gephi\render_network.ps1` compiles `RenderNetwork.java` and runs it with the Gephi Toolkit (`tools\gephi-toolkit\gephi-toolkit-0.11.3-all.jar`, Maven Central, SHA-1 `8bfad8f34cf51a42035185ccca8521ab9d375e43`, the same version as the project-local Gephi) on the Java 17 runtime that ships with that Gephi. The Java compiler comes from WSL Ubuntu (any JDK 17 or later works).

1. Import: `nodes.csv` as the nodes table, `edges.csv` as the edges table (Gephi's CSV importer, directed graph).
2. S9 cut: ssab, volvo and outo are removed (they are backup-only in the outline).
3. Layout: positions are set by hand (Gephi's manual layout). ForceAtlas 2 was run first and turned the three disconnected chains into an unreadable cluster; `GEPHI_LAYOUT=scaling,gravity,strong,nodeSize,fa2` still runs it.
4. Appearance: label box colour by `Role` (blue producer, grey buyer, green hydrogen supplier, amber public funder); edge colour by `Status` (amber MoU and state aid, green supply contract, blue supply agreement, grey early application).
5. Preview: labels in TH Sarabun New, directed edges with short edge labels (from `Status` and `Date`; the aid years are the EU decision years in the outline), then export PNG, SVG and the project file.

Display names differ from the CSV for three nodes (Volkswagen, Stegra, State aid (EU-approved)); the CSV keeps the full names.

## Before presenting

The workbook flags these as time-sensitive: Stegra's capital and delivery status (U16), Salzgitter and Thyssenkrupp milestone dates (U12), and any new agreements. If `nodes.csv` or `edges.csv` change, re-run the script.
