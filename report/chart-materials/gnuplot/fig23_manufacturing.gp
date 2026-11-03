# Figure 2.3: German manufacturing real GVA and production, 1995 to 2025 (two panels, different base years).
# Sample data: de_manufacturing_1995_2025.csv (columns: year, real GVA 2020 = 100, production 2021 = 100, share %).
# Run:  gnuplot -c fig23_manufacturing.gp <DATA_FILE> <OUT_DIR>
if (ARGC >= 1) DATA_FILE = ARG1; else DATA_FILE = 'de_manufacturing_1995_2025.csv'
if (ARGC >= 2) OUT_DIR = ARG2; else OUT_DIR = 'figures-rebuilt'

set terminal pngcairo size 2048,1471 enhanced font 'Times New Roman,26'
set output OUT_DIR.'/fig23_manufacturing.png'
DARK = '#263444'; BLUE = '#2B5C98'; TEAL = '#167A67'; AMBER = '#B26A00'; GREY = '#78828C'
set datafile separator ','

set label 1 'German manufacturing: real GVA and production, 1995 to 2025' at screen 0.5,0.97 center font 'Times New Roman:Bold,34' textcolor rgb DARK
set label 2 'Source: Eurostat nama_10_a64 and sts_inpr_a. 2023 to 2025 GVA provisional.' at screen 0.07,0.02 left font 'Times New Roman,20' textcolor rgb GREY noenhanced
set multiplot layout 2,1 margins 0.09,0.98,0.10,0.92 spacing 0,0.06

set xrange [1995:2025]
set yrange [60:120]
set ytics 60,10,120
set grid ytics lc rgb '#e6e6e6'
set arrow 1 from 2005,60 to 2005,120 nohead dt 2 lw 2 lc rgb AMBER
set arrow 2 from 2023,60 to 2023,120 nohead dt 2 lw 2 lc rgb AMBER
set label 3 'ETS launch' at 2005.4,116 left textcolor rgb AMBER
set label 4 'CBAM reporting' at 2022.6,116 right textcolor rgb AMBER

set ylabel 'Real GVA (2020 = 100)'
set xtics format ''
plot DATA_FILE using 1:2 every ::1 with lines lc rgb BLUE lw 3 notitle

set ylabel 'Production (2021 = 100)'
set xtics 1995,5,2025 format '%.0f'
set xlabel 'Year'
plot DATA_FILE using 1:3 every ::1 with lines lc rgb TEAL lw 3 notitle
unset multiplot
