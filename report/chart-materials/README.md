# Chart scripts and sample data for the report figures

All six report figures are drawn with GNUplot 6.0.5 in Times New Roman (the serif font of the report).
The GNUplot scripts are in `gnuplot/`; `gnuplot/render_all.ps1` renders all six into `figures-gnuplot/`.

| Report figure | Script | Sample data |
| --- | --- | --- |
| Fig. 2.1 Negative production externality | `gnuplot/fig21_externality.gp` | none (invented values: demand 120 - Q, PMC 20 + Q, external cost 20) |
| Fig. 2.2 Carbon-related import cost | `gnuplot/fig22_import_cost.gp` | none (invented values) |
| Fig. 2.3 German manufacturing real GVA and production | `gnuplot/fig23_manufacturing.gp` | `workbook/de_manufacturing_1995_2025.csv` |
| Fig. 2.4 Crude steel and rolled market supply | `gnuplot/fig24_steel_output_supply.gp` | `fig24_steel_2012_2025.csv` (in `data/`) |
| Fig. 2.5 Direct extra-EU Chapter 72 exports and imports | `gnuplot/fig25_direct_trade_volume.gp` | `comext_exports/ch72_extra_eu_exports_1999_2025.csv`, `comext_exports/ch72_extra_eu_imports_1999_2025.csv` |
| Fig. 2.6 Chapter 72 trade values and unit value | `gnuplot/fig26_trade_unit_value.gp` | `comext_exports/slide_table_2017_2025.csv`, `comext_exports/ch72_extra_eu_imports_1999_2025.csv` |

The Python versions in `scripts/` are earlier rebuilds and are not used in the report.
