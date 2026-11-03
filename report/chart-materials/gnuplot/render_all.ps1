# Render the six report figures with GNUplot (Times New Roman through the Windows font folder, see scripts/env.ps1).
#   powershell -ExecutionPolicy Bypass -File render_all.ps1 -Data <folder with the sample data> -Out <output folder>
param([string]$Data = 'data', [string]$Out = 'figures-gnuplot')
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
New-Item -ItemType Directory -Force -Path $Out | Out-Null
$Out = (Resolve-Path $Out).Path
$Data = (Resolve-Path $Data).Path
gnuplot -c (Join-Path $here 'fig21_externality.gp') $Out
gnuplot -c (Join-Path $here 'fig22_import_cost.gp') $Out
gnuplot -c (Join-Path $here 'fig23_manufacturing.gp') (Join-Path $Data 'workbook\de_manufacturing_1995_2025.csv') $Out
gnuplot -c (Join-Path $here 'fig24_steel_output_supply.gp') (Join-Path $Data 'fig24_steel_2012_2025.csv') $Out
gnuplot -c (Join-Path $here 'fig25_direct_trade_volume.gp') (Join-Path $Data 'comext_exports\ch72_extra_eu_exports_1999_2025.csv') (Join-Path $Data 'comext_exports\ch72_extra_eu_imports_1999_2025.csv') $Out
gnuplot -c (Join-Path $here 'fig26_trade_unit_value.gp') (Join-Path $Data 'comext_exports\slide_table_2017_2025.csv') (Join-Path $Data 'comext_exports\ch72_extra_eu_imports_1999_2025.csv') $Out
