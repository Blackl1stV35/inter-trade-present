# Slide 8: steel trade, two separate universes side by side (never subtracted from each other).
# Left : all partners incl. intra-EU, 'steel mill products', Mt, 2017-2024 (WV Stahl, Dataset B, rounded).
# Right: direct extra-EU Chapter 72 (incl. scrap), 2017-2025 (Comext DS-045409, vintage 2026-10-16); balance shown in Mt for comparability of units.
# Run from the repo root:  gnuplot -c graphs/gnuplot/s8_steel_trade_balance.gp
load 'graphs/gnuplot/common.gp'
dsb  = 'data/workbook/de_steel_mill_products_trade_all_partners_2017_2024.csv'
ext  = 'data/comext_exports/ch72_extra_eu_balance_1999_2025.csv'
set terminal pngcairo size 1800,950 font fnt
set output 'graphs/out/s8_steel_trade_balance.png'
set datafile separator ','

# balance rows (derived: left from the rounded Dataset B values; right from Comext kt / 1000)
balL = '-1.2 -1.6 +0.3 +1.4 -0.4 +0.4 +3.0 +4.1'
balR = '+2.6 +2.3 +3.0 +2.6 +2.4 +2.5 +3.0 +3.1 +3.2'

set multiplot
set label 40 'Steel trade of Germany: two different universes, shown separately' at screen 0.5,0.965 center font fntT textcolor rgb dark
set label 41 'Not national-accounts NX, not the CBAM base; no competitiveness verdict. Chapter 72 includes scrap, pig iron and DRI.' at screen 0.06,0.052 textcolor rgb grey font fntS
set label 42 'Left: WV Stahl (Fakten zur Stahlindustrie 2025, p. 30), rounded. Right: Eurostat Comext DS-045409, vintage 2026-10-16.' at screen 0.06,0.022 textcolor rgb grey font fntS

# ---- left panel
set lmargin at screen 0.07 ; set rmargin at screen 0.47 ; set tmargin at screen 0.85 ; set bmargin at screen 0.27
set label 1 'All partners incl. intra-EU, steel mill products (million tonnes)' at screen 0.07,0.895 textcolor rgb dark
set xrange [2016.6:2024.9] ; set xtics 1 ; set format x '%g'
set yrange [14:30] ; set ytics 2 ; set format y '%g'
set label 2 'Exports' at 2024.1,23.4 left textcolor rgb blue
set label 3 'Imports' at 2024.1,18.3 left textcolor rgb green
set label 4 'X - M, million tonnes (approx.)' at screen 0.07,0.135 textcolor rgb dark
do for [i=1:8] { set label 100+i word(balL,i) at first (2016+i), screen 0.095 center textcolor rgb dark }
plot dsb skip 1 using 1:2 w lp lw 4 pt 7 ps 1.2 lc rgb blue, '' skip 1 using 1:3 w lp lw 4 pt 7 ps 1.2 lc rgb green

# ---- right panel
unset label 1 ; unset label 2 ; unset label 3 ; unset label 4
do for [i=1:8] { unset label 100+i }
set lmargin at screen 0.56 ; set rmargin at screen 0.96
set label 11 'Direct extra-EU, HS Chapter 72 (thousand tonnes)' at screen 0.56,0.895 textcolor rgb dark
set xrange [2016.6:2025.9] ; set xtics 1
set yrange [0:8000] ; set ytics 1000
set label 12 'Exports' at 2025.15,4900 left textcolor rgb blue
set label 13 'Imports' at 2025.15,1300 left textcolor rgb green
set label 14 'X - M, million tonnes (positive every year since 1999)' at screen 0.56,0.135 textcolor rgb dark
do for [i=1:9] { set label 200+i word(balR,i) at first (2016+i), screen 0.095 center textcolor rgb dark }
plot ext skip 1 using 1:($1>=2017 ? $5 : 1/0) w lp lw 4 pt 7 ps 1.2 lc rgb blue, '' skip 1 using 1:($1>=2017 ? $6 : 1/0) w lp lw 4 pt 7 ps 1.2 lc rgb green
unset multiplot
