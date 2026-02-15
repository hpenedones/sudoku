"""
Python wrapper for the C sudoku solver library using ctypes.

This module provides a stateless function-based interface to the high-performance 
C sudoku solver using constraint propagation and backtracking.
"""

import ctypes
import os
import platform
from typing import Optional, Union, List


# Global variable to cache the library instance
_lib = None


def _get_library():
    """
    Get or initialize the sudoku shared library.
    
    Returns:
        The loaded ctypes library.
    
    Raises:
        OSError: If library cannot be found or loaded.
    """
    global _lib
    
    if _lib is not None:
        return _lib
    
    lib_path = _find_library()
    
    try:
        _lib = ctypes.CDLL(lib_path)
    except OSError as e:
        raise OSError(f"Failed to load sudoku library from {lib_path}: {e}")
    
    # Configure function signatures
    _lib.solve_sudoku_from_string.argtypes = [
        ctypes.c_char_p,  # puzzle_str
        ctypes.c_char_p   # solution_str
    ]
    _lib.solve_sudoku_from_string.restype = ctypes.c_int
    
    return _lib


def _find_library() -> str:
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


def _grid_to_linear(grid: List[List[str]]) -> str:
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


def _linear_to_grid(linear: str) -> List[List[str]]:
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


def _parse_grid_format(grid_str: str) -> str:
    """
    Parse a multi-line grid format string into linear format.
    
    Args:
        grid_str: A string with newlines representing a 9x9 grid.
    
    Returns:
        An 81-character linear string.
    
    Raises:
        ValueError: If the grid format is invalid.
    """
    lines = [line.strip() for line in grid_str.strip().split('\n') if line.strip()]
    
    if len(lines) != 9:
        raise ValueError(f"Grid format must have 9 lines, got {len(lines)}")
    
    result = []
    for i, line in enumerate(lines):
        # Remove spaces and other separators
        clean_line = ''.join(c for c in line if c in '0123456789._')
        
        if len(clean_line) != 9:
            raise ValueError(f"Line {i+1} must have 9 cells, got {len(clean_line)}")
        
        # Convert to use '0' for empty cells
        for c in clean_line:
            if c in ('_', '.'):
                result.append('0')
            else:
                result.append(c)
    
    return ''.join(result)


def solve(puzzle: Union[str, List[List[str]]]) -> Optional[str]:
    """
    Solve a sudoku puzzle.
    
    This is a stateless function that solves sudoku puzzles using a fast C 
    implementation with constraint propagation and backtracking.
    
    Args:
        puzzle: The puzzle to solve. Can be either:
               - A string of 81 characters (linear format) where '0', '_', or '.' 
                 represent empty cells and '1'-'9' represent given numbers.
               - A multi-line string with newlines (grid format).
               - A 9x9 list of lists (grid format) with the same character rules.
    
    Returns:
        The solved puzzle as an 81-character string, or None if no solution exists.
        The solution uses '1'-'9' for all cells.
    
    Raises:
        ValueError: If the puzzle format is invalid.
    
    Examples:
        >>> import sudoku
        >>> 
        >>> # Linear format
        >>> puzzle = "530070000600195000098000060800060003400803001700020006060000280000419005000080079"
        >>> solution = sudoku.solve(puzzle)
        >>> print(solution)
        534678912672195348198342567859761423426853791713924856961537284287419635345286179
        >>> 
        >>> # Grid format (multi-line string)
        >>> puzzle_grid = '''53__7____
        ... 6__195___
        ... _98____6_
        ... 8___6___3
        ... 4__8_3__1
        ... 7___2___6
        ... _6____28_
        ... ___419__5
        ... ____8__79'''
        >>> solution = sudoku.solve(puzzle_grid)
        >>> print(solution)
        534678912672195348198342567859761423426853791713924856961537284287419635345286179
        >>> 
        >>> # Grid format (9x9 list)
        >>> puzzle_list = [
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
        >>> solution = sudoku.solve(puzzle_list)
        >>> print(solution)
        534678912672195348198342567859761423426853791713924856961537284287419635345286179
    """
    # Convert puzzle to linear format if needed
    if isinstance(puzzle, list):
        puzzle_str = _grid_to_linear(puzzle)
    elif isinstance(puzzle, str):
        # Check if it's a multi-line grid format
        if '\n' in puzzle:
            puzzle_str = _parse_grid_format(puzzle)
        else:
            puzzle_str = puzzle
    else:
        raise ValueError(f"Puzzle must be a string or 9x9 list, got {type(puzzle)}")
    
    # Validate puzzle string
    if len(puzzle_str) != 81:
        raise ValueError(f"Puzzle must be 81 characters long, got {len(puzzle_str)}")
    
    # Get the library
    lib = _get_library()
    
    # Prepare buffers
    puzzle_bytes = puzzle_str.encode('utf-8')
    solution_buffer = ctypes.create_string_buffer(82)  # 81 + null terminator
    
    # Call C function
    result = lib.solve_sudoku_from_string(puzzle_bytes, solution_buffer)
    
    if result == 0:
        return None  # No solution found
    elif result == -1:
        raise ValueError("Invalid puzzle format")
    
    # Get solution string
    solution_str = solution_buffer.value.decode('utf-8')
    
    return solution_str
