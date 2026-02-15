# Sudoku Solver

[![CI](https://github.com/hpenedones/sudoku/actions/workflows/ci.yml/badge.svg)](https://github.com/hpenedones/sudoku/actions/workflows/ci.yml)

A fast and efficient sudoku solver using constraint propagation and backtracking with depth-first search.

Available as both a C command-line tool and a Python library.

## Quick Start

### Command Line (C)

```bash
make
./solver 1 < examples/example_linear.txt
```

### Python

```bash
# Install
pip install -e .

# Use in Python
python3
>>> from sudoku_wrapper import SudokuSolver
>>> solver = SudokuSolver()
>>> puzzle = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
>>> solution = solver.solve(puzzle)
>>> print(solution)
534678912672195348198342567859761423426853791713924856961537284287419635345286179
```

## Overview

This sudoku solver finds the most constrained cell, chooses a feasible number, and proceeds recursively.
At some point in the future it might have to backtrack and try another path. 

The goal was to use the solver to identify the hardest puzzles. The measure of difficulty for a puzzle is how many times the algorithm has to backtrack on it. 

## Features

- **Two input formats**: Grid (9x9) and Linear (81 characters)
- **Efficient algorithm**: Constraint propagation with backtracking
- **Python wrapper**: Easy-to-use Python interface via ctypes
- **Cross-platform**: Works on Linux, macOS, and Windows
- **Difficulty analysis**: Tracks the number of backtracks per puzzle
- **Comprehensive examples**: Sample puzzles included in the `examples/` directory

At the bottom of this page are the hardest sudoku puzzles found. Here is how you can reproduce the experiments:

Requirements
------

**Basic C usage:**
- A C compiler (e.g., gcc)
- Make (optional, but recommended)

**Python usage:**
- Python 3.6 or later
- A C compiler (to build the shared library)

**For full analysis:**
- Python 3 with matplotlib and Pillow (install with `pip install -r analysis/requirements.txt`)
- Unix/Linux shell with standard utilities (wget, awk, sort, etc.)

Compilation
------

Using Makefile (recommended):
```bash
make
```

Or manually with gcc:
```bash
gcc sudoku_solver.c -o solver
```

## Testing

### C Tests

Run the C test suite:
```bash
make test
```

This will run all tests including:
- Grid format parsing
- Linear format parsing  
- Hard puzzle solving
- Error handling

### Python Tests

Run the Python test suite:
```bash
python3 test_sudoku_wrapper.py
```

This will run comprehensive tests for the Python wrapper including:
- Linear and grid format inputs
- Various empty cell markers (0, _, .)
- Error handling and validation
- Solution correctness

## Performance

Run a performance benchmark:
```bash
./benchmark.sh
```

The solver is very fast for typical puzzles (< 1ms) but can take several seconds for extremely difficult puzzles that require extensive backtracking.

## C Command-Line Usage

The input is assumed to come from the standard input, and the program will print to the standard output.
There is one command line argument, which defines the format of the input: 

 1. Grid:

``` 
 53__7____
 6__195___
 _98____6_
 8___6___3
 4__8_3__1
 7___2___6
 _6____28_
 ___419__5
 ____8__79
```

 2. Linear:

``` 
 530070000600195000098000060800060003400803001700020006060000280000419005000080079
```

Example with grid format:
```bash
./solver 2 < examples/example_grid.txt
```

Example with linear format:
```bash
./solver 1 < examples/example_linear.txt
```

## Python Usage

### Installation

Install the package in development mode:
```bash
pip install -e .
```

Or install directly:
```bash
make lib  # Build the shared library
pip install .
```

### Basic Usage

```python
from sudoku_wrapper import SudokuSolver, solve_sudoku

# Method 1: Using the convenience function
puzzle = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
solution = solve_sudoku(puzzle)
print(solution)
# Output: 534678912672195348198342567859761423426853791713924856961537284287419635345286179

# Method 2: Using the SudokuSolver class
solver = SudokuSolver()
solution = solver.solve(puzzle)
```

### Input Formats

The Python wrapper supports multiple input formats:

**1. Linear format (81-character string):**
```python
puzzle = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
solution = solver.solve(puzzle)
```

Empty cells can be represented with `0`, `_`, or `.`:
```python
puzzle = "53__7____6__195____98____6_8___6___34__8_3__17___2___6_6____28____419__5____8__79"
solution = solver.solve(puzzle)
```

**2. Grid format (9x9 list of lists):**
```python
puzzle = [
    ['5', '3', '0', '0', '7', '0', '0', '0', '0'],
    ['6', '0', '0', '1', '9', '5', '0', '0', '0'],
    ['0', '9', '8', '0', '0', '0', '0', '6', '0'],
    ['8', '0', '0', '0', '6', '0', '0', '0', '3'],
    ['4', '0', '0', '8', '0', '3', '0', '0', '1'],
    ['7', '0', '0', '0', '2', '0', '0', '0', '6'],
    ['0', '6', '0', '0', '0', '0', '2', '8', '0'],
    ['0', '0', '0', '4', '1', '9', '0', '0', '5'],
    ['0', '0', '0', '0', '8', '0', '0', '7', '9']
]

# Return as string
solution = solver.solve(puzzle, return_format='string')

# Or return as grid
solution_grid = solver.solve(puzzle, return_format='grid')
for row in solution_grid:
    print(' '.join(row))
```

### Error Handling

The wrapper provides helpful error messages:

```python
try:
    # Invalid length
    solver.solve("12345")
except ValueError as e:
    print(f"Error: {e}")
    # Error: Puzzle must be 81 characters long, got 5

try:
    # Invalid puzzle with duplicates
    invalid = "110070000600195000098000060800060003400803001700020006060000280000419005000080079"
    solver.solve(invalid)
except ValueError as e:
    print(f"Error: {e}")
    # Error: Invalid puzzle format
```

### Examples

See `examples/python_usage.py` for comprehensive examples:
```bash
python3 examples/python_usage.py
```

This demonstrates:
- Linear and grid format inputs
- Different empty cell markers
- Return format options
- Error handling
- Solving hard puzzles


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

And generated a histogram with Python matplotlib. I have a script called make_histogram.sh containing this:

> cat nbacktracks.txt | sort -n | awk -F" " '{print exp(int(log($1))) }' | uniq -c > histogram.txt

> python3 plot_histogram.py histogram.txt histogram.png

You can then run: 
 
> ./make_histogram.sh

![ScreenShot](https://raw.github.com/hpenedones/sudoku/master/analysis/histogram.png)


It's curious that with a logscale x-axis the distribution looks like a Gaussian. I don't have an explanation for this, however. And it's quite impressive to see that some puzzles need about 1 million backtrackings!
I decided to locate the hardest and share them here. Let me know if you also found them hard to solve!


> paste nbacktracks.txt puzzles.txt | sort -nr | head -n 10

```
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
```
Ok, so now we need to render this sudoku puzzles in a human-friendly fashion. So we proceed as follows:

We store the top 10 sudoku in a file (drop the backtrack counts):

> paste nbacktracks.txt puzzles.txt | sort -nr | head -n 10 | cut -f 2 > top10.txt

Download an empty sudoku board image from somewhere in the web (searched google images with "sudoku empty"):

> wget http://www.scouk.net/entertainment/sudoku/blank_grid.gif

And now we are ready for some awesomeness! 

Rendering Sudoku puzzles
------

We use Python with PIL/Pillow to render the Sudoku puzzles:

> ./render.sh

Or manually for a single puzzle:

> python3 render_sudoku.py "200500080001020000000000000070008000003000020000070600600200001040000700000300000" output.png blank_grid.gif

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

## Contributing

Contributions are welcome! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## Code of Conduct

This project follows a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Hugo Penedones - [hpenedones@gmail.com](mailto:hpenedones@gmail.com)
