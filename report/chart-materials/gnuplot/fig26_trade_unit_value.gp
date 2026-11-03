# Figure 2.6: direct extra-EU Chapter 72 nominal trade values and import unit value, 2017 to 2025 (two panels).
# Sample data: slide_table_2017_2025.csv (columns 5 and 6: exports and imports, EUR million) and
# ch72_extra_eu_imports_1999_2025.csv (column 6: unit value, EUR per net tonne; 2017 to 2025 used).
# Unit value is total import euros divided by net tonnes; it reflects product mix, not a fixed-product price index.
# Run:  gnuplot -c fig26_trade_unit_value.gp <TRADE_FILE> <UNIT_FILE> <OUT_DIR>
if (ARGC >= 1) TRADE_FILE = ARG1; else TRADE_FILE = 'slide_table_2017_2025.csv'
if (ARGC >= 2) UNIT_FILE = ARG2; else UNIT_FILE = 'ch72_extra_eu_imports_1999_2025.csv'
if (ARGC >= 3) OUT_DIR = ARG3; else OUT_DIR = 'figures-rebuilt'

set terminal pngcairo size 2600,2200 enhanced font 'Times New Roman,70'
set output OUT_DIR.'/fig26_trade_unit_value.png'
DARK = '#263444'; BLUE = '#2B5C98'; TEAL = '#167A67'; AMBER = '#B26A00'
set datafile separator ','
set datafile missing 'NaN'

set multiplot layout 2,1 margins 0.17,0.94,0.09,0.95 spacing 0,0.06
set xrange [2017:2025]
set xtics 2017,1,2025
set arrow 1 from 2023,0 to 2023,9 nohead dt 2 lw 7 lc rgb AMBER

set yrange [0:9]
set ytics 0,2,8
set grid ytics lc rgb '#e6e6e6'
set ylabel 'Trade value (EUR billion)'
set key top left Left reverse box samplen 4 spacing 1.4 font 'Times New Roman,70'
set xtics format ''
plot TRADE_FILE using 1:($5/1000) every ::1::9 with lines lc rgb BLUE lw 11 title 'Exports', \
     TRADE_FILE using 1:($6/1000) every ::1::9 with lines lc rgb TEAL lw 11 dt 2 title 'Imports'

set arrow 1 from 2023,400 to 2023,1500 nohead dt 2 lw 7 lc rgb AMBER
set yrange [400:1500]
set ytics 400,200,1400
set ylabel 'Import unit value (EUR/t)'
set xlabel 'Year'
set xtics 2017,1,2025 format '%.0f'
unset key
plot UNIT_FILE using (($1>=2017)?$1:NaN):6 with linespoints lc rgb TEAL lw 11 pt 7 ps 1.2 notitle
unset multiplot
