# Slide 8: steel trade, two separate universes side by side (never subtracted from each other).
# Left : all partners incl. intra-EU, 'steel mill products', Mt, 2017-2025 (WV Stahl, Daten und Fakten p. 30: 2017 from the 2025 edition, 2018-2025 from the 2026 edition; printed Saldo).
# Right: HS Chapter 72 to / from outside the EU, 2017-2025: exports (Comext = Destatis by destination), imports direct (Comext) and imports by origin (Destatis).
# Run from the repo root:  gnuplot -c graphs/gnuplot/s8_steel_trade_balance.gp
load 'graphs/gnuplot/common.gp'
wv   = 'data/german_sources/wv_stahl/steel_mill_products_trade_germany_2017_2025_latest_vintage.csv'
ext  = 'data/comext_exports/ch72_extra_eu_balance_1999_2025.csv'
ori  = 'data/german_sources/destatis/trade_ch72_eu27_vs_noneu_annual_2008_2025.csv'
set terminal pngcairo size 1800,1050 font fnt
set output 'graphs/out/s8_steel_trade_balance.png'
set datafile separator ','

balL = '-1.2 -1.5 +0.2 +1.4 -0.5 +0.3 +3.0 +4.2 +1.9'
balD = '+2.6 +2.3 +3.0 +2.6 +2.4 +2.5 +3.0 +3.1 +3.2'
balO = '+0.3 +0.4 +1.3 +1.4 +0.4 +0.5 +1.2 +0.9 +0.8'

set multiplot
set label 40 'Steel trade of Germany: two different universes, shown separately' at screen 0.5,0.97 center font fntT textcolor rgb dark
set label 41 'Not national-accounts NX, not the CBAM base; no verdict. Chapter 72 includes scrap, pig iron and DRI; steel mill products include pipes.' at screen 0.06,0.06 textcolor rgb grey font fntS
set label 42 'Left: WV Stahl p. 30 (2025 ed. for 2017, 2026 ed. for 2018-25). Right: Eurostat Comext (vintage 2026-10-16), Destatis 51000-0007.' at screen 0.06,0.03 textcolor rgb grey font fntS

# ---- left panel
set lmargin at screen 0.07 ; set rmargin at screen 0.47 ; set tmargin at screen 0.86 ; set bmargin at screen 0.34
set label 1 'All partners incl. intra-EU, steel mill products (million tonnes)' at screen 0.07,0.905 textcolor rgb dark
set xrange [2016.6:2025.9] ; set xtics 1 ; set format x '%g'
set yrange [14:30] ; set ytics 2 ; set format y '%g'
set label 2 'Exports' at 2025.15,22.9 left textcolor rgb blue
set label 3 'Imports' at 2025.15,20.0 left textcolor rgb green
set label 4 'X - M, Mt (printed Saldo)' at screen 0.07,0.2 textcolor rgb dark
do for [i=1:9] { set label 100+i word(balL,i) at first (2016+i), screen 0.165 center textcolor rgb dark }
plot wv skip 1 using 1:2 w lp lw 4 pt 7 ps 1.2 lc rgb blue, '' skip 1 using 1:3 w lp lw 4 pt 7 ps 1.2 lc rgb green

# ---- right panel
unset label 1 ; unset label 2 ; unset label 3 ; unset label 4
do for [i=1:9] { unset label 100+i }
set lmargin at screen 0.56 ; set rmargin at screen 0.89
set label 11 'Chapter 72, outside the EU (thousand tonnes)' at screen 0.56,0.905 textcolor rgb dark
set yrange [0:8000] ; set ytics 1000
set label 12 'Exports' at 2025.15,5100 left textcolor rgb blue
set label 13 'By origin' at 2025.15,3500 left textcolor rgb amber
set label 14 'Direct' at 2025.15,1100 left textcolor rgb green
set xtics 2017,2,2025
set label 16 'direct = cleared at German customs; by origin = all channels' at screen 0.56,0.245 textcolor rgb grey font fntS
set label 15 'X - M, Mt (green: direct imports; amber: by origin)' at screen 0.56,0.2 textcolor rgb dark
do for [i=1:9] { set label 200+i word(balD,i) at first (2016+i), screen 0.165 center textcolor rgb green }
do for [i=1:9] { set label 300+i word(balO,i) at first (2016+i), screen 0.125 center textcolor rgb amber }
plot ext skip 1 using 1:($1>=2017 ? $5 : 1/0) w lp lw 4 pt 7 ps 1.2 lc rgb blue, \
     '' skip 1 using 1:($1>=2017 ? $6 : 1/0) w lp lw 4 pt 7 ps 1.2 lc rgb green, \
     ori skip 1 using 1:($1>=2017 ? $5 : 1/0) w lp lw 4 dt 2 pt 9 ps 1.2 lc rgb amber
unset multiplot
