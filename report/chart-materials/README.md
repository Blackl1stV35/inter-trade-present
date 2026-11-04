# Chart scripts and sample data for the report figures

All nine report figures are drawn with GNUplot 6.0.5 in Times New Roman (the serif font of the report).
The GNUplot scripts are in `gnuplot/`; `gnuplot/render_all.ps1` renders all six into `figures-gnuplot/`.

| Report figure | Script | Sample data |
| --- | --- | --- |
| Fig. 2.1 Negative production externality | `gnuplot/fig21_externality.gp` | none (invented values: demand 120 - Q, PMC 20 + Q, external cost 20) |
| Fig. 2.2 Carbon-related import cost | `gnuplot/fig22_import_cost.gp` | none (invented values) |
| Fig. 2.3 German manufacturing real GVA and production | `gnuplot/fig23_manufacturing.gp` | `workbook/de_manufacturing_1995_2025.csv` |
| Fig. 2.4 Crude steel and rolled market supply | `gnuplot/fig24_steel_output_supply.gp` | `fig24_steel_2012_2025.csv` (in `data/`) |
| Fig. 2.5 Direct extra-EU Chapter 72 exports and imports | `gnuplot/fig25_direct_trade_volume.gp` | `comext_exports/ch72_extra_eu_exports_1999_2025.csv`, `comext_exports/ch72_extra_eu_imports_1999_2025.csv` |
| Fig. 2.6 Chapter 72 trade values and unit value | `gnuplot/fig26_trade_unit_value.gp` | `comext_exports/slide_table_2017_2025.csv`, `comext_exports/ch72_extra_eu_imports_1999_2025.csv` |
| Fig. 2.7 Chapter 72 trade balance by partner group | `gnuplot/fig27_bop_partner_balance.gp` | `comext_exports/ch72_partner_balance_1999_2025.csv` (derived by `scripts/build_bop_eu_gdp_data.py`) |
| Fig. 2.8 Chapter 72 exports by destination group | `gnuplot/fig28_eu_export_destinations.gp` | `comext_exports/ch72_export_destinations_1999_2025.csv` (derived by `scripts/build_bop_eu_gdp_data.py`) |
| Fig. 2.9 German real GDP index and annual growth | `gnuplot/fig29_gdp_timeline.gp` | `eurostat_macro/tidy/de_real_gdp_1995_2025.csv` (derived from `eurostat_macro/raw/nama_10_gdp_DE_B1GQ_*_1995_2025.json`) |

The Python versions in `scripts/` are earlier rebuilds and are not used in the report.
