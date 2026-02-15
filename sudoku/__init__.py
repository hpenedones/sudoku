"""
Sudoku Solver Python Package

A Python wrapper for a high-performance C sudoku solver implementation
using constraint propagation and backtracking.

Quick Start:
    >>> import sudoku
    >>> puzzle = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    >>> solution = sudoku.solve(puzzle)
    >>> print(solution)
    534678912672195348198342567859761423426853791713924856961537284287419635345286179

The solve() function accepts puzzles in multiple formats:
- Linear format: 81-character string (use '0', '_', or '.' for empty cells)
- Grid format: Multi-line string with 9 lines of 9 characters each
- List format: 9x9 list of lists
"""

__version__ = "1.0.0"
__author__ = "Hugo Penedones"
__email__ = "hpenedones@gmail.com"

from .sudoku_wrapper import solve

__all__ = ['solve', '__version__']
