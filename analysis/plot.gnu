set xlabel '#backtracks to solve (log-scale)';
set ylabel 'Frequency';
set output 'histogram.png'
set terminal png
set logscale x;
plot 'histogram.txt' u 2:1 w boxes t 'Sudoku 17-puzzles' ;
