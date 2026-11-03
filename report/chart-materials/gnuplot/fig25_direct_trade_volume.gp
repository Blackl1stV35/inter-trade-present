# Figure 2.5: direct extra-EU Chapter 72 exports and imports, 1999 to 2025 (net mass, million tonnes).
# Sample data: ch72_extra_eu_exports_1999_2025.csv and ch72_extra_eu_imports_1999_2025.csv (Comext DS-045409),
# net mass in column 5 (thousand tonnes). Not the CBAM liability base.
# Run:  gnuplot -c fig25_direct_trade_volume.gp <EXPORTS_FILE> <IMPORTS_FILE> <OUT_DIR>
if (ARGC >= 1) EXP_FILE = ARG1; else EXP_FILE = 'ch72_extra_eu_exports_1999_2025.csv'
if (ARGC >= 2) IMP_FILE = ARG2; else IMP_FILE = 'ch72_extra_eu_imports_1999_2025.csv'
if (ARGC >= 3) OUT_DIR = ARG3; else OUT_DIR = 'figures-rebuilt'

set terminal pngcairo size 2048,1173 enhanced font 'Times New Roman,26'
set output OUT_DIR.'/fig25_direct_trade_volume.png'
DARK = '#263444'; BLUE = '#2B5C98'; TEAL = '#167A67'; AMBER = '#B26A00'; GREY = '#78828C'
set datafile separator ','

set label 1 'Direct extra-EU Chapter 72 exports and imports, 1999 to 2025' at screen 0.5,0.96 center font 'Times New Roman:Bold,34' textcolor rgb DARK
set tmargin screen 0.87
set bmargin screen 0.14
set label 2 'Source: Eurostat Comext DS-045409. Germany, fixed extra-EU27_2020, HS72. Not the CBAM liability base.' at screen 0.07,0.02 left font 'Times New Roman,20' textcolor rgb GREY noenhanced
set xrange [1999:2025]
set yrange [0:9]
set xtics 1999,4,2025
set ytics 0,1,9
set grid ytics lc rgb '#e6e6e6'
set xlabel 'Year'
set ylabel 'Net mass (million tonnes)'
set key top right Right spacing 1.4 font 'Times New Roman,24'
set arrow 1 from 2005,0 to 2005,9 nohead dt 2 lw 2 lc rgb AMBER
set arrow 2 from 2023,0 to 2023,9 nohead dt 2 lw 2 lc rgb AMBER
set label 3 '4.681 Mt' at 2019.5,7.7 left textcolor rgb BLUE
set arrow 3 from 2024,4.8 to 2025,4.681 nohead lw 1.5 lc rgb BLUE
set label 4 '1.464 Mt' at 2019.5,0.9 left textcolor rgb TEAL
set arrow 4 from 2024,1.6 to 2025,1.464 nohead lw 1.5 lc rgb TEAL

plot EXP_FILE using 1:($5/1000) every ::1 with lines lc rgb BLUE lw 3 title 'Exports', \
     IMP_FILE using 1:($5/1000) every ::1 with lines lc rgb TEAL lw 3 title 'Direct extra-EU imports'
