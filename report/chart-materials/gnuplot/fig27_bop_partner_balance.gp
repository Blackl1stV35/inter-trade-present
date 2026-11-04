# Figure 2.7: Germany, Chapter 72 trade balance by partner group, 1999 to 2025 (value, EUR billion).
# Sample data: ch72_partner_balance_1999_2025.csv (columns: year, extra-EU balance, intra-EU balance, all-partner balance; EUR million).
# Run:  gnuplot -c fig27_bop_partner_balance.gp <DATA_FILE> <OUT_DIR>
if (ARGC >= 1) DATA_FILE = ARG1; else DATA_FILE = 'ch72_partner_balance_1999_2025.csv'
if (ARGC >= 2) OUT_DIR = ARG2; else OUT_DIR = 'figures-rebuilt'

set terminal pngcairo size 2600,1600 enhanced font 'Times New Roman,70'
set output OUT_DIR.'/fig27_bop_partner_balance.png'
DARK = '#263444'; BLUE = '#2B5C98'; TEAL = '#167A67'; AMBER = '#B26A00'; GREY = '#78828C'
set datafile separator ','

set tmargin screen 0.95
set bmargin screen 0.14
set rmargin screen 0.94
set xrange [1998.4:2025.6]
set yrange [-7:6]
set ytics -7,1,6
set grid ytics lc rgb '#e6e6e6'
set xzeroaxis lt 1 lw 6 lc rgb DARK
set xtics 1999,4,2025
set boxwidth 0.36 absolute
set xlabel 'Year'
set ylabel 'Balance (EUR billion)'
set key bottom left Left box spacing 1.2 font 'Times New Roman,56'
set arrow 1 from 2005,-7 to 2005,6 nohead dt 2 lw 7 lc rgb AMBER
set arrow 2 from 2023,-7 to 2023,6 nohead dt 2 lw 7 lc rgb AMBER
set label 3 'ETS launch' at 2005.4,5.5 left textcolor rgb AMBER
set label 4 'CBAM reporting' at 2022.6,5.5 right textcolor rgb AMBER

plot DATA_FILE using ($1-0.2):($2/1000) every ::1 with boxes fs solid 0.9 lc rgb BLUE title 'Extra-EU partners', \
     DATA_FILE using ($1+0.2):($3/1000) every ::1 with boxes fs solid 0.9 lc rgb GREY title 'Intra-EU partners', \
     DATA_FILE using 1:($4/1000) every ::1 with linespoints lc rgb DARK lw 9 pt 7 ps 3 title 'All partners'
