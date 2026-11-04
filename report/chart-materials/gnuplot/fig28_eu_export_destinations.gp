# Figure 2.8: Germany, Chapter 72 exports by destination group, 1999 to 2025.
# Panel A: export net mass as an index (1999 = 100). Panel B: nominal unit value (EUR per tonne).
# Sample data: ch72_export_destinations_1999_2025.csv (columns: year, extra-EU kt, intra-EU kt, extra-EU EUR m,
# intra-EU EUR m, extra-EU EUR/t, intra-EU EUR/t, extra-EU share of mass %).
# Run:  gnuplot -c fig28_eu_export_destinations.gp <DATA_FILE> <OUT_DIR>
if (ARGC >= 1) DATA_FILE = ARG1; else DATA_FILE = 'ch72_export_destinations_1999_2025.csv'
if (ARGC >= 2) OUT_DIR = ARG2; else OUT_DIR = 'figures-rebuilt'

set terminal pngcairo size 2600,2200 enhanced font 'Times New Roman,70'
set output OUT_DIR.'/fig28_eu_export_destinations.png'
DARK = '#263444'; BLUE = '#2B5C98'; TEAL = '#167A67'; AMBER = '#B26A00'; GREY = '#78828C'
set datafile separator ','
stats DATA_FILE using 2 every ::1::1 nooutput
EXT0 = STATS_mean
stats DATA_FILE using 3 every ::1::1 nooutput
INT0 = STATS_mean

set multiplot layout 2,1 margins 0.17,0.94,0.09,0.95 spacing 0,0.07
set xrange [1999:2025]
set grid ytics lc rgb '#e6e6e6'
set xtics 1999,4,2025
set key Right box spacing 1.2 font 'Times New Roman,56'

set yrange [0:150]
set ytics 0,25,150
set ylabel 'Volume (1999 = 100)'
set xtics format ''
set key bottom left
set arrow 1 from 2005,0 to 2005,150 nohead dt 2 lw 7 lc rgb AMBER
set arrow 2 from 2023,0 to 2023,150 nohead dt 2 lw 7 lc rgb AMBER
set label 3 'ETS launch' at 2005.4,143 left textcolor rgb AMBER
set label 4 'CBAM reporting' at 2022.6,143 right textcolor rgb AMBER
plot DATA_FILE using 1:(100*$2/EXT0) every ::1 with lines lc rgb BLUE lw 11 title 'Extra-EU destinations', \
     DATA_FILE using 1:(100*$3/INT0) every ::1 with lines lc rgb GREY lw 11 dt 2 title 'Intra-EU destinations'

set yrange [0:1600]
set ytics 0,400,1600
set ylabel 'Unit value (EUR/t)'
set xlabel 'Year'
set xtics 1999,4,2025 format '%.0f'
set key top left
unset label 3
unset label 4
set arrow 1 from 2005,0 to 2005,1600 nohead dt 2 lw 7 lc rgb AMBER
set arrow 2 from 2023,0 to 2023,1600 nohead dt 2 lw 7 lc rgb AMBER
set label 3 'ETS launch' at 2005.4,120 left textcolor rgb AMBER
set label 4 'CBAM reporting' at 2022.6,120 right textcolor rgb AMBER
plot DATA_FILE using 1:6 every ::1 with lines lc rgb BLUE lw 11 title 'Extra-EU destinations', \
     DATA_FILE using 1:7 every ::1 with lines lc rgb GREY lw 11 dt 2 title 'Intra-EU destinations'
unset multiplot
