# Figure 2.9: Germany, real GDP index and annual real growth, 1995 to 2025.
# Panel A: real GDP index (2020 = 100). Panel B: annual real growth (%). 2023 to 2025 are provisional.
# Sample data: de_real_gdp_1995_2025.csv (columns: year, real GDP EUR million at 2020 prices, real growth %,
# index 2020 = 100, flag).
# Run:  gnuplot -c fig29_gdp_timeline.gp <DATA_FILE> <OUT_DIR>
if (ARGC >= 1) DATA_FILE = ARG1; else DATA_FILE = 'de_real_gdp_1995_2025.csv'
if (ARGC >= 2) OUT_DIR = ARG2; else OUT_DIR = 'figures-rebuilt'

set terminal pngcairo size 2600,2200 enhanced font 'Times New Roman,70'
set output OUT_DIR.'/fig29_gdp_timeline.png'
DARK = '#263444'; BLUE = '#2B5C98'; TEAL = '#167A67'; AMBER = '#B26A00'; GREY = '#78828C'
set datafile separator ','

set multiplot layout 2,1 margins 0.17,0.94,0.09,0.95 spacing 0,0.07
set xrange [1995:2025]
set grid ytics lc rgb '#e6e6e6'
set xtics 1995,5,2025

set yrange [70:110]
set ytics 70,10,110
set ylabel 'Real GDP (2020 = 100)'
set xtics format ''
set arrow 1 from 2005,70 to 2005,110 nohead dt 2 lw 7 lc rgb AMBER
set arrow 2 from 2023,70 to 2023,110 nohead dt 2 lw 7 lc rgb AMBER
set label 3 'ETS launch' at 2005.4,107 left textcolor rgb AMBER
set label 4 'CBAM reporting' at 2022.6,107 right textcolor rgb AMBER
plot DATA_FILE using 1:4 every ::1 with lines lc rgb BLUE lw 11 notitle

set yrange [-7:5]
set ytics -6,2,4
set ylabel 'Real growth (%)'
set xlabel 'Year'
set xtics 1995,5,2025 format '%.0f'
set xzeroaxis lt 1 lw 6 lc rgb DARK
set arrow 1 from 2005,-7 to 2005,5 nohead dt 2 lw 7 lc rgb AMBER
set arrow 2 from 2023,-7 to 2023,5 nohead dt 2 lw 7 lc rgb AMBER
set label 3 'Financial crisis' at 2009.3,-6.4 left textcolor rgb DARK
set label 4 'Pandemic' at 2020.9,-2.6 left textcolor rgb DARK
set label 5 'provisional' at 2025,4.6 right textcolor rgb GREY
set boxwidth 0.7 relative
plot DATA_FILE using 1:3 every ::1 with boxes fs solid 0.9 lc rgb BLUE notitle
unset multiplot
