# Figure 2.4: German crude-steel production and rolled-steel market supply, 2012 to 2025 (two panels).
# Sample data: fig24_steel_2012_2025.csv (year, crude steel Mt, rolled market supply Mt). The two series are different
# product measures and must not be subtracted.
# Run:  gnuplot -c fig24_steel_output_supply.gp <DATA_FILE> <OUT_DIR>
if (ARGC >= 1) DATA_FILE = ARG1; else DATA_FILE = 'fig24_steel_2012_2025.csv'
if (ARGC >= 2) OUT_DIR = ARG2; else OUT_DIR = 'figures-rebuilt'

set terminal pngcairo size 2600,2200 enhanced font 'Times New Roman,70'
set output OUT_DIR.'/fig24_steel_output_supply.png'
DARK = '#263444'; BLUE = '#2B5C98'; TEAL = '#167A67'; AMBER = '#B26A00'
set datafile separator ','

set multiplot layout 2,1 margins 0.13,0.97,0.09,0.95 spacing 0,0.06

set xrange [2012:2025]
set yrange [20:46]
set ytics 25,5,45
set grid ytics lc rgb '#e6e6e6'
set arrow 1 from 2023,20 to 2023,46 nohead dt 2 lw 7 lc rgb AMBER

set ylabel 'Crude steel (Mt)'
set xtics format ''
set label 2 '34.1' at 2024.7,35.4 left textcolor rgb BLUE
plot DATA_FILE using 1:2 every ::1 with lines lc rgb BLUE lw 11 notitle
unset label 2

set ylabel 'Rolled market supply (Mt)'
set label 3 '29.1' at 2024.7,30.4 left textcolor rgb TEAL
set xtics 2012,3,2025 format '%.0f'
set xtics add ('2023' 2023)
set xlabel 'Year'
plot DATA_FILE using 1:3 every ::1 with lines lc rgb TEAL lw 11 notitle
unset multiplot
