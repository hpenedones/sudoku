"""
Python wrapper for the C sudoku solver library using ctypes.

This module provides a clean Python interface to the high-performance C sudoku solver.
"""

import ctypes
import os
import platform
from typing import Optional, Union, List


class SudokuSolver:
    """
    A Python interface to the C sudoku solver library.
    
    This class provides methods to solve sudoku puzzles using a fast C implementation
    with constraint propagation and backtracking.
    
    Examples:
        >>> solver = SudokuSolver()
        
        # Solve with linear format (81 characters)
        >>> puzzle = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
        >>> solution = solver.solve(puzzle)
        >>> print(solution)
        534678912672195348198342567859761423426853791713924856961537284287419635345286179
        
        # Solve with grid format (9x9 list)
        >>> puzzle_grid = [
        ...     ['5', '3', '0', '0', '7', '0', '0', '0', '0'],
        ...     ['6', '0', '0', '1', '9', '5', '0', '0', '0'],
        ...     ['0', '9', '8', '0', '0', '0', '0', '6', '0'],
        ...     ['8', '0', '0', '0', '6', '0', '0', '0', '3'],
        ...     ['4', '0', '0', '8', '0', '3', '0', '0', '1'],
        ...     ['7', '0', '0', '0', '2', '0', '0', '0', '6'],
        ...     ['0', '6', '0', '0', '0', '0', '2', '8', '0'],
        ...     ['0', '0', '0', '4', '1', '9', '0', '0', '5'],
        ...     ['0', '0', '0', '0', '8', '0', '0', '7', '9']
        ... ]
        >>> solution_grid = solver.solve(puzzle_grid, return_format='grid')
        >>> print(solution_grid[0])
        ['5', '3', '4', '6', '7', '8', '9', '1', '2']
    """
    
    def __init__(self, lib_path: Optional[str] = None):
        """
        Initialize the SudokuSolver.
        
        Args:
            lib_path: Optional path to the shared library. If not provided,
                     will search in the current directory and common locations.
        
        Raises:
            OSError: If the shared library cannot be found or loaded.
        """
        if lib_path is None:
            lib_path = self._find_library()
        
        try:
            self._lib = ctypes.CDLL(lib_path)
        except OSError as e:
            raise OSError(f"Failed to load sudoku library from {lib_path}: {e}")
        
        # Configure function signatures
        self._lib.solve_sudoku_from_string.argtypes = [
            ctypes.c_char_p,  # puzzle_str
            ctypes.c_char_p   # solution_str
        ]
        self._lib.solve_sudoku_from_string.restype = ctypes.c_int
    
    def _find_library(self) -> str:
        """
        Find the sudoku shared library.
        
        Returns:
            Path to the shared library.
        
        Raises:
            OSError: If library cannot be found.
        """
        # Determine library extension based on platform
        system = platform.system()
        if system == 'Windows':
            lib_name = 'libsudoku.dll'
        elif system == 'Darwin':
            lib_name = 'libsudoku.dylib'
        else:
            lib_name = 'libsudoku.so'
        
        # Search locations
        search_paths = [
            # Package directory (where this file is)
            os.path.dirname(os.path.abspath(__file__)),
            # Parent directory (repository root for development)
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            # Current working directory
            os.getcwd(),
            # Package lib subdirectory
            os.path.join(os.path.dirname(__file__), 'lib'),
        ]
        
        for path in search_paths:
            lib_path = os.path.join(path, lib_name)
            if os.path.exists(lib_path):
                return lib_path
        
        raise OSError(
            f"Could not find {lib_name} in any of: {search_paths}\n"
            "Please ensure the library is compiled (run 'make lib') and located "
            "in the same directory as this Python module."
        )
    
    def solve(
        self, 
        puzzle: Union[str, List[List[str]]], 
        return_format: str = 'string'
    ) -> Optional[Union[str, List[List[str]]]]:
        """
        Solve a sudoku puzzle.
        
        Args:
            puzzle: The puzzle to solve. Can be either:
                   - A string of 81 characters (linear format) where '0', '_', or '.' 
                     represent empty cells and '1'-'9' represent given numbers.
                   - A 9x9 list of lists (grid format) with the same character rules.
            return_format: Format for the returned solution. Either 'string' or 'grid'.
                          Default is 'string'.
        
        Returns:
            The solved puzzle in the requested format, or None if no solution exists.
            - If return_format='string': returns an 81-character string
            - If return_format='grid': returns a 9x9 list of lists
        
        Raises:
            ValueError: If the puzzle format is invalid.
        
        Examples:
            >>> solver = SudokuSolver()
            >>> puzzle = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
            >>> solution = solver.solve(puzzle)
            >>> print(solution)
            534678912672195348198342567859761423426853791713924856961537284287419635345286179
        """
        # Convert puzzle to linear format if needed
        if isinstance(puzzle, list):
            puzzle_str = self._grid_to_linear(puzzle)
        elif isinstance(puzzle, str):
            puzzle_str = puzzle
        else:
            raise ValueError(f"Puzzle must be a string or 9x9 list, got {type(puzzle)}")
        
        # Validate puzzle string
        if len(puzzle_str) != 81:
            raise ValueError(f"Puzzle must be 81 characters long, got {len(puzzle_str)}")
        
        # Prepare buffers
        puzzle_bytes = puzzle_str.encode('utf-8')
        solution_buffer = ctypes.create_string_buffer(82)  # 81 + null terminator
        
        # Call C function
        result = self._lib.solve_sudoku_from_string(puzzle_bytes, solution_buffer)
        
        if result == 0:
            return None  # No solution found
        elif result == -1:
            raise ValueError("Invalid puzzle format")
        
        # Get solution string
        solution_str = solution_buffer.value.decode('utf-8')
        
        # Return in requested format
        if return_format == 'string':
            return solution_str
        elif return_format == 'grid':
            return self._linear_to_grid(solution_str)
        else:
            raise ValueError(f"return_format must be 'string' or 'grid', got '{return_format}'")
    
    def _grid_to_linear(self, grid: List[List[str]]) -> str:
        """
        Convert a 9x9 grid to an 81-character linear string.
        
        Args:
            grid: A 9x9 list of lists.
        
        Returns:
            An 81-character string.
        
        Raises:
            ValueError: If grid dimensions are invalid.
        """
        if len(grid) != 9:
            raise ValueError(f"Grid must have 9 rows, got {len(grid)}")
        
        result = []
        for i, row in enumerate(grid):
            if len(row) != 9:
                raise ValueError(f"Row {i} must have 9 columns, got {len(row)}")
            for cell in row:
                # Convert empty cell markers to '0'
                # Supports: '_', '.', ' ', '' (empty string), and '0'
                if cell in ('_', '.', ' ', '', '0'):
                    result.append('0')
                else:
                    result.append(cell)
        
        return ''.join(result)
    
    def _linear_to_grid(self, linear: str) -> List[List[str]]:
        """
        Convert an 81-character linear string to a 9x9 grid.
        
        Args:
            linear: An 81-character string.
        
        Returns:
            A 9x9 list of lists.
        
        Raises:
            ValueError: If string length is not 81.
        """
        if len(linear) != 81:
            raise ValueError(f"Linear string must be 81 characters, got {len(linear)}")
        
        grid = []
        for i in range(9):
            row = list(linear[i*9:(i+1)*9])
            grid.append(row)
        
        return grid


def solve_sudoku(
    puzzle: Union[str, List[List[str]]], 
    return_format: str = 'string'
) -> Optional[Union[str, List[List[str]]]]:
    """
    Convenience function to solve a sudoku puzzle without creating a solver instance.
    
    Args:
        puzzle: The puzzle to solve (string or 9x9 grid).
        return_format: Format for the returned solution ('string' or 'grid').
    
    Returns:
        The solved puzzle in the requested format, or None if no solution exists.
    
    Examples:
        >>> solution = solve_sudoku("530070000600195000098000060800060003400803001700020006060000280000419005000080079")
        >>> print(solution)
        534678912672195348198342567859761423426853791713924856961537284287419635345286179
    """
    solver = SudokuSolver()
    return solver.solve(puzzle, return_format)


if __name__ == '__main__':
    # Quick test
    puzzle = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
    print(f"Puzzle: {puzzle}")
    
    solver = SudokuSolver()
    solution = solver.solve(puzzle)
    
    if solution:
        print(f"Solution: {solution}")
        
        # Also test grid format
        grid = solver._linear_to_grid(puzzle)
        solution_grid = solver.solve(grid, return_format='grid')
        print("\nGrid format solution:")
        for row in solution_grid:
            print(' '.join(row))
    else:
        print("No solution found")
