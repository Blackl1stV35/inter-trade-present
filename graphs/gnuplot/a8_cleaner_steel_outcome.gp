# Backup A8 / slide 12: has German steel become cleaner per tonne? Production-side indicators only.
# Data: data/steel_route/chart_data_cleaner_steel_indicators.csv (worldsteel / WV Stahl route shares; DEHSt-UBA ETS emissions scope C 2013-2025; WV Stahl specific CO2).
# Run from the repo root:  gnuplot -c graphs/gnuplot/a8_cleaner_steel_outcome.gp
load 'graphs/gnuplot/common.gp'
data = 'data/steel_route/chart_data_cleaner_steel_indicators.csv'
set terminal pngcairo size 1800,950 font fnt
set output 'graphs/out/a8_cleaner_steel_outcome.png'
set datafile separator ','

set multiplot
set label 40 'German steel: electric-arc share and CO2 per tonne of crude steel' at screen 0.5,0.965 center font fntT textcolor rgb dark
set label 41 'Descriptive, production side only: not a policy effect, not trade-adjusted, not CBAM embedded emissions.' at screen 0.06,0.05 textcolor rgb grey font fntS
set label 42 'ETS line: direct emissions of ETS iron and steel installations (scope from 2013) / crude steel. Sources: worldsteel, WV Stahl, DEHSt, UBA.' at screen 0.06,0.02 textcolor rgb grey font fntS

set lmargin at screen 0.07 ; set rmargin at screen 0.47 ; set tmargin at screen 0.85 ; set bmargin at screen 0.16
set label 1 'Electric-arc share of crude steel, 1999-2025 (%)' at screen 0.07,0.895 textcolor rgb dark
set xrange [1999:2025.8] ; set xtics 2000,5,2025 ; set format x '%g'
set yrange [0:60] ; set ytics 10
set label 2 '29.2 (1999)' at 1999.4,24.5 left textcolor rgb dark
set label 3 '30.5 (2025)' at 2025.3,24.5 right textcolor rgb dark
set label 4 '2009: output cut in blast furnaces' at 2009,38.5 center textcolor rgb grey
set label 5 'EU27 2025: 45.8   Italy: 90.1   Spain: 71.7' at 2012.5,56 center textcolor rgb grey
plot data skip 1 using 1:2 w lp lw 4 pt 7 ps 1.1 lc rgb blue

unset label 1 ; unset label 2 ; unset label 3 ; unset label 4 ; unset label 5
set lmargin at screen 0.56 ; set rmargin at screen 0.96
set label 11 't CO2 per t crude steel, 2013-2025' at screen 0.56,0.895 textcolor rgb dark
set xrange [2013:2025.8] ; set xtics 2
set yrange [0:1.7] ; set ytics 0.2 ; set format y '%.1f'
set label 12 'WV Stahl specific CO2 (incl. purchased power)' at 2013.2,1.62 left textcolor rgb green
set label 14 '1.37 (2019) to 1.39 (2025)' at 2013.2,1.53 left textcolor rgb green
set label 13 'ETS-reported / crude steel (derived)' at 2013.2,0.58 left textcolor rgb blue
set label 15 '0.84 (2013) to 0.88 (2025)' at 2013.2,0.49 left textcolor rgb blue
plot data skip 1 using 1:5 w lp lw 4 pt 7 ps 1.1 lc rgb blue, '' skip 1 using 1:($6 > 0 ? $6 : 1/0) w lp lw 4 pt 5 ps 1.1 lc rgb green
unset multiplot
