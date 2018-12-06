set terminal epslatex color
set out 'plot_5.tex'

set border 3
set xtics border nomirror out
set ytics border nomirror out
set xtics ("48" 48, "49" 49, "50" 50, "51" 51, "52" 52)
set xlabel "time (weeks)" 
set ylabel "percentage of weighted ILL" offset 1
set key right top

plot "figure5.txt" using 1:4 title "real" w lp lt 1 pt 2 lc 1,\
"figure5.txt" using 1:2:($2-$3):($2+$3) with errorbars title "predict", \
"figure5.txt" using 1:2 title "" w lp lt 2 pt 3 lc 2

set output