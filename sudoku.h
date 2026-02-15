/* 
   Sudoku Solver Public API Header
   
   Author: Hugo Penedones
   Email: hpenedones@gmail.com
*/

#ifndef SUDOKU_H
#define SUDOKU_H

#define SQRT_N 3
#define N (SQRT_N * SQRT_N)

/* Opaque structure for sudoku puzzle state */
typedef struct {
    int constraints[N][N][N];
    int inserted[N][N];
    int ninserted;
    int nbacktracks;
} sudoku;

/* Initialize a new sudoku puzzle */
void new_sudoku(sudoku *s);

/* 
   Solve a sudoku puzzle from a string input
   
   Parameters:
     puzzle_str: Input string (81 characters, '0', '_', or '.' for empty cells, '1'-'9' for given numbers)
     solution_str: Output buffer for solution (should be at least 82 chars for null terminator)
   
   Returns: 1 if solved successfully, 0 if no solution exists, -1 if input is invalid
*/
int solve_sudoku_from_string(const char *puzzle_str, char *solution_str);

/* 
   Get the solution from a solved sudoku as a string
   
   Parameters:
     s: Pointer to sudoku structure
     output: Output buffer (should be at least 82 chars for null terminator)
*/
void get_solution_string(sudoku *s, char *output);

/* 
   Solve a sudoku puzzle (internal function)
   
   Parameters:
     s: Pointer to sudoku structure
   
   Returns: 1 if solved, 0 if no solution exists
*/
int solve(sudoku *s);

/* 
   Insert a number at a specific position
   
   Parameters:
     s: Pointer to sudoku structure
     row: Row index (0-8)
     col: Column index (0-8)
     number: Number to insert (0-8, representing 1-9)
*/
void insert_number_at(sudoku *s, int row, int col, int number);

#endif /* SUDOKU_H */
