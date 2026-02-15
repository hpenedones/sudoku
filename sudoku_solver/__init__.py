"""
Sudoku Solver Python Package

A Python wrapper for a high-performance C sudoku solver implementation
using constraint propagation and backtracking.

Quick Start:
    >>> from sudoku_solver import SudokuSolver
    >>> solver = SudokuSolver()
    >>> puzzle = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    >>> solution = solver.solve(puzzle)
    >>> print(solution)
    534678912672195348198342567859761423426853791713924856961537284287419635345286179

Or use the convenience function:
    >>> from sudoku_solver import solve_sudoku
    >>> solution = solve_sudoku(puzzle)
"""

__version__ = "1.0.0"
__author__ = "Hugo Penedones"
__email__ = "hpenedones@gmail.com"

from .sudoku_wrapper import SudokuSolver, solve_sudoku

__all__ = ['SudokuSolver', 'solve_sudoku', '__version__']
