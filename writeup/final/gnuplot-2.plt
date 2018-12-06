set terminal epslatex color
set out 'plot_2.tex'

set border 3
set xtics border nomirror out
set ytics border nomirror out
set xlabel "time (weeks)" 
set ylabel "weighted ILL percentage" offset 1
set xtics ("2015" 40, "41" 41, "42" 42, "43" 43, \
"44" 44, "46" 46, "47" 47, "51" 51 , "2016" 55,  " 4" 56)


plot "figure2.txt" using 2: 4 title "real" w lp lt 1 pt 2 lc 1,\
"figure2.txt" using 2: 3 title "predict" w lp lt 2 pt 3 lc 2

set output