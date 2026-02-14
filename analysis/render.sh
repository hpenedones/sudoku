#!/bin/bash
# Render Sudoku puzzles using Python instead of ImageMagick
set -e  # Exit on error
set -u  # Treat unset variables as errors

i=1
while read line; do
    python3 render_sudoku.py "$line" "hardest_sudoku_$i.png" "blank_grid.gif"
    i=$((i + 1))
done < top10.txt

