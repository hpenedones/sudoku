Sudoku solver
======

This sudoku solver finds the most constrained cell, choses a feasible number, and proceeds recursively.
At some point in the future it might have to backtrack and try another path. 
My goal was to use the solver to identify the hardest puzzles. The measure of difficulty for a puzzle was how many times my algorithm had to backtrack on it. 

At the bottom of this page I show the hardest sudoku puzzles I found. Here is how you can reproduce the experiments by yourself:

Requirements
------

To run the solver you just need a C compiler, such as gcc. 
To do the full analysis you will also need gnuplot and ImageMagick convert tool, and some sort of Unix/Linux shell.

Compilation
------

> gcc solver.c -o solver
 
Usage
------


The input is assumed to come from the standard input, and the program will print to the standard output.
There is one command line argument, which defines the format of the input. 


        Supported input formats:
 
 1. Grid:
 
 53__7____
 6__195___
 _98____6_
 8___6___3
 4__8_3__1
 7___2___6
 _6____28_
 ___419__5
 ____8__79
 
 2. Linear:
 
 530070000600195000098000060800060003400803001700020006060000280000419005000080079

Example:

> ./solver 2 < puzzle.txt


Finding hard Sudoku puzzles
======

Instead of outputting the puzzle solution, we can instead output the number of backtrackings that the algorithm had to perform to achieve that solution. This gives an estimate on how hard the puzzle is.
I didn't put a command line option for this, but you can just (un)comment the appropriate lines in the main routine:

```C
print(&s, 1);    // prints the solution
// printf("%d\n", s.nbacktracks);  // prints how many times it had to backtrack
```

I downloaded a file with about 50000 puzzles (with 17 given numbers, out of the 81):

> wget http://school.maths.uwa.edu.au/~gordon/sudoku17 -O puzzles.txt

Then I computed the number of backtracks per puzzle for all of them (which takes a few hours!):

> ./solve 1 < puzzles.txt > nbacktracks.txt

And generated an histogram with gnuplot. I have a script called make_histograms.sh containing this:

> cat nbacktracks.txt | sort -n | awk -F" " '{print exp(int(log($1))) }' | uniq -c > histogram.txt

> echo "set xlabel '#backtracks to solve (log-scale)';"               > plot.gnu

> echo "set ylabel 'Frequency';"                             >> plot.gnu

> echo "set output 'histogram.png'"                     >> plot.gnu

> echo "set term png"                                        >> plot.gnu

> echo "set logscale x;"                        >> plot.gnu

> echo "plot 'histogram.txt' u 2:1 w boxes t 'Sudoku 17-puzzles' ;"  >> plot.gnu


You can then run: 
 
> ./make_histograms.sh

> gnuplot plot.gnu

![ScreenShot](https://raw.github.com/hpenedones/sudoku/master/analysis/histogram.png)


It's curious that with a logscale x-axis the distribution looks like a Gaussian. I don't have an explanation for this, however. And it's quite impressive to see that some puzzles need about 1 million backtrackings!
I decided to locate the hardest and share them here. Let me know if you also found them hard to solve!


> paste nbacktracks.txt puzzles.txt | sort -nr | head -n 10

1165175 200500080001020000000000000070008000003000020000070600600200001040000700000300000
937856 004036000100000500000000000062000000000050700000800200000002004700000030050700000
669800 000870600200000000000100000060054000000000021400000000070000050000200300500001000
583255 000100038200005000000000000050000400400030000000700006001000050000060200060004000
452647 010050300000800000070000000020400700600280000300000100900000020000001000000000080
448038 200500070060030000000000000000040501004008000050000020100700000003000400000200000
436722 010050300000200000080000000020400800700620000300000100500000020000001000000000060
429469 010050300000600000080000000060400800700260000300000100900000020000001000000000060
427221 010600420000800000000050000005000030700400000000001000200030700000000504040000000
419682 200100600004000500000000000030040000800000009000050700050700010000800030007000000

Ok, so now we need to render this sudoku puzzles in a human-friendly fashion. So we proceed as follows:

We store the top 10 sudoku in a file (drop the backtrack counts):

> paste nbacktracks.txt puzzles.txt | sort -nr | head -n 10 | cut -f 2 > top10.txt

Download an empty sudoku board image from somewhere in the web (searched google images with "sudoku empty"):

> wget http://www.scouk.net/entertainment/sudoku/blank_grid.gif

And now we are ready for some awesomeness! 

Rendering Sudoku puzzles
------

We use ImageMagick convert tool to do the full rendering in one line:

> i=1; cat top10.txt | while read line;  do echo $line | fold -w 9 | tr 0 " " | head -c 89 | convert  -pointsize 100 -font Courier -size 531x721 label:@- puzzle.png ; convert puzzle.png -border 10x10 -splice 0x10 -resize 328x328\! puzzle.png; convert blank_grid.gif puzzle.png -average hardest_sudoku_$i.png; i=`expr $i + 1`; done

Done!

We can now display the top 10 hardest sudoku puzzles (according to my solver): 

![ScreenShot](https://raw.github.com/hpenedones/sudoku/master/analysis/hardest_sudoku_1.png)

![ScreenShot](https://raw.github.com/hpenedones/sudoku/master/analysis/hardest_sudoku_2.png)

![ScreenShot](https://raw.github.com/hpenedones/sudoku/master/analysis/hardest_sudoku_3.png)

![ScreenShot](https://raw.github.com/hpenedones/sudoku/master/analysis/hardest_sudoku_4.png)

![ScreenShot](https://raw.github.com/hpenedones/sudoku/master/analysis/hardest_sudoku_5.png)

![ScreenShot](https://raw.github.com/hpenedones/sudoku/master/analysis/hardest_sudoku_6.png)

![ScreenShot](https://raw.github.com/hpenedones/sudoku/master/analysis/hardest_sudoku_7.png)

![ScreenShot](https://raw.github.com/hpenedones/sudoku/master/analysis/hardest_sudoku_8.png)

![ScreenShot](https://raw.github.com/hpenedones/sudoku/master/analysis/hardest_sudoku_9.png)

![ScreenShot](https://raw.github.com/hpenedones/sudoku/master/analysis/hardest_sudoku_10.png)
