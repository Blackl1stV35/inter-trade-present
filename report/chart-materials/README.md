# Chart scripts and sample data for the report figures

| Report figure | Chart script | Sample data |
| --- | --- | --- |
| Fig. 2.1 Negative production externality | Workbook image (no script in repository); the numbers are invented (demand 120 - Q, PMC 20 + Q, external cost 20) | none (illustrative) |
| Fig. 2.2 Carbon-related import cost | Workbook image (no script in repository); illustrative, invented values | none (illustrative) |
| Fig. 2.3 German manufacturing real GVA and production | `scripts/s6_manufacturing.gp` | Destatis and Eurostat manufacturing series (`data/workbook/de_manufacturing_1995_2025.csv` in the repository) |
| Fig. 2.4 Crude steel and rolled market supply | Workbook image; WV Stahl Daten und Fakten 2026 values | WV Stahl figures (`data/steel_route/`) |
| Fig. 2.5 Direct extra-EU Chapter 72 exports and imports | `scripts/s7_extra_eu_imports.gp` | `ch72_extra_eu_imports_1999_2025.csv` (Eurostat Comext DS-045409) |
| Fig. 2.6 Chapter 72 trade values and unit value | Workbook image; Eurostat Comext DS-045409 values | `slide_table_2017_2025.csv` and Comext extracts |
| Company network (appendix) | `scripts/RenderNetwork.java`, `scripts/render_network.ps1` (Gephi Toolkit 0.11.3) | `scripts/nodes.csv`, `scripts/edges.csv` |

The headline and note edits to the six report figures were made by `report/scripts/stage_b_figures.py`. Figures 2.1, 2.2, 2.4 and 2.6 come from the workbook images in their original form; their generating code is not in the repository and should be added before publication if the team wants full reproducibility.
