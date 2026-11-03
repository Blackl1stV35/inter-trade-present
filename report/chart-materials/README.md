# Chart scripts and sample data for the report figures

| Report figure | Chart script | Sample data |
| --- | --- | --- |
| Fig. 2.1 Negative production externality | `scripts/fig21_externality.py` (invented values: demand 120 - Q, PMC 20 + Q, external cost 20) | none (illustrative) |
| Fig. 2.2 Carbon-related import cost | `scripts/fig22_import_cost.py` (invented values) | none (illustrative) |
| Fig. 2.3 German manufacturing real GVA and production | `scripts/fig23_manufacturing.py` | `workbook/de_manufacturing_1995_2025.csv` |
| Fig. 2.4 Crude steel and rolled market supply | `scripts/fig24_steel_output_supply.py` | steel-route indicator file and WV Stahl market-supply file |
| Fig. 2.5 Direct extra-EU Chapter 72 exports and imports | `scripts/fig25_direct_trade_volume.py` | `ch72_extra_eu_exports_1999_2025.csv`, `ch72_extra_eu_imports_1999_2025.csv` (Eurostat Comext DS-045409) |
| Fig. 2.6 Chapter 72 trade values and unit value | `scripts/fig26_trade_unit_value.py` | `slide_table_2017_2025.csv`, `ch72_extra_eu_imports_1999_2025.csv` |
| Company network (appendix) | `scripts/RenderNetwork.java`, `scripts/render_network.ps1` (Gephi Toolkit 0.11.3) | `scripts/nodes.csv`, `scripts/edges.csv` |

All six figures are reproduced by the scripts above with the report's styling and headlines. The figure-rebuild and report-assembly steps are in `report/scripts/`.
