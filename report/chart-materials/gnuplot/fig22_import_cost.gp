# Figure 2.2: carbon-related import cost with partial pass-through (illustrative).
# Invented values, not German data. Demand P = 120 - Q; S: P = 20 + Q; S': P = 30 + Q.
# Delivered price P0 = 40 before the carbon cost; full pass-through benchmark 60 (not assumed); P1 = 50 after partial pass-through.
# Run:  gnuplot -c fig22_import_cost.gp <OUT_DIR>
if (ARGC >= 1) OUT_DIR = ARG1; else OUT_DIR = 'figures-rebuilt'

set terminal pngcairo size 2600,1800 enhanced font 'Times New Roman,70'
set output OUT_DIR.'/fig22_import_cost.png'
DARK = '#263444'; BLUE = '#2B5C98'; TEAL = '#167A67'; GREY = '#78828C'

set tmargin screen 0.95
set bmargin screen 0.27
set lmargin screen 0.21
set rmargin screen 0.97
set xrange [0:100]
set yrange [0:190]
set xtics ("0" 0, "Q_{S0} = Q_{S1}\n20" 20, "Q_{D1}\n70" 70, "Q_{D0}\n80" 80, "100" 100)
set ytics ("0" 0, "P_0 = 40" 40, "P_1 = 50" 50, "P_0 + c = 60" 60, "100" 100, "135" 135)
set xlabel 'Quantity of steel (illustrative units)'
set ylabel 'Price / marginal cost (index)' offset 1,0
set key top left Left reverse maxcols 1 samplen 3 spacing 1.2 font 'Times New Roman,70'
set arrow 1 from 20,0 to 20,40 nohead dt 3 lw 7 lc rgb BLUE
set arrow 2 from 80,0 to 80,40 nohead dt 3 lw 7 lc rgb BLUE
set arrow 3 from 20,0 to 20,50 nohead dt 3 lw 7 lc rgb TEAL
set arrow 4 from 70,0 to 70,50 nohead dt 3 lw 7 lc rgb TEAL
set arrow 5 from 20,33 to 70,33 heads size 1.6,20 lw 9 lc rgb TEAL
set arrow 6 from 20,22 to 80,22 heads size 1.6,20 lw 9 lc rgb BLUE
set label 2 'Imports after = 50' at 45,36 center textcolor rgb TEAL
set label 3 'Imports before = 60' at 50,25 center textcolor rgb BLUE

plot 120-x lc rgb DARK lw 11 title 'D: demand', \
     20+x lc rgb BLUE lw 11 dt 1 title 'S: initial supply', \
     30+x lc rgb TEAL lw 11 dt 2 title "S': domestic cost +10", \
     60 lc rgb GREY lw 7 dt 3 title 'Full pass-through benchmark (not assumed)', \
     40 lc rgb BLUE lw 9 notitle, \
     50 lc rgb TEAL lw 9 notitle, \
     '-' using 1:2 with points pt 7 ps 3.5 lc rgb BLUE notitle
20 40
80 40
e
