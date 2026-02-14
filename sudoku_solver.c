/* 
	Yet another Sudoku solver
   
	Author: Hugo Penedones
   	Email: hpenedones@gmail.com
	Date: 15 April 2010

	Compilation:
	$ gcc sudoku_solver.c -o solver
	
	Usage:
	$ ./solver < puzzle.txt
	
	Format of puzzle input data:
	
	1. Grid format:
	
	53__7____
	6__195___
	_98____6_
	8___6___3
	4__8_3__1
	7___2___6
	_6____28_
	___419__5
	____8__79
	
	2. Linear format:
	
	530070000600195000098000060800060003400803001700020006060000280000419005000080079
	
*/	

#include <assert.h>
#include <stdio.h>
#include <stdlib.h>

#define SQRT_N 3
#define N (SQRT_N * SQRT_N) 

// Data Types

typedef struct {
	int constraints[N][N][N];
	int inserted[N][N];
	int ninserted;
	int nbacktracks;
} sudoku;

enum print_mode { HYPOTHESIS_COUNT, VALUE, ALL_HYPOTHESIS };
enum input_type { LINEAR_INPUT=1, GRID_INPUT};


void new_sudoku(sudoku * s)
{
	int i,j,n;
	for(i = 0; i < N; i++)
		for(j = 0; j < N; j++)
		{
			s->inserted[i][j] = 0;
			for(n = 0; n < N; n++)
				s->constraints[i][j][n] = 0;
		}
	s->ninserted = 0;
	s->nbacktracks = 0;
}


/*
	This method can be used for both insertions and removals, depending on the parameter "type".
	It takes care of propagating restrictions according to the operation that was done.
	You should not call it directly, but instead use insert_number_at and remove_number_at procedures.
*/
void change_state_at(sudoku * s, int row, int col, int number, int type)
{
	assert(type == -1 || type == 1);
	assert(number >=0 && number < N);
	assert(s->constraints[row][col][number] == 0); 

	if (type == -1)
		s->inserted[row][col] = 0;
	else
		s->inserted[row][col] = 1;
	
	int shift = type;  // just for readability (weird to add "type")	
	int a;
	for(a=0; a<N; a++)
		{
			s->constraints[row][a][number]+= shift;
			s->constraints[a][col][number]+= shift;
			s->constraints[row][col][a]+= shift;
		}

	int sq_row = row / SQRT_N;
	int sq_col = col / SQRT_N;

	int i, j;
	for(i=0; i<SQRT_N; i++)
		for(j=0; j<SQRT_N; j++)
			{
				s->constraints[SQRT_N*sq_row + i][SQRT_N*sq_col + j][number]+= shift;
			}
	// alternatively I could put "if"s to prevent changing the constrainsts over the "number" position
	assert(s->constraints[row][col][number] == shift*4); 
	s->constraints[row][col][number] = 0;	
	s->ninserted+=shift;
}


void insert_number_at(sudoku * s, int row, int col, int number)
{
//	printf("Inserting %d at (%d, %d)\n", number+1, row+1, col+1);
	change_state_at(s, row, col, number, +1);
}

void remove_number_at(sudoku * s, int row, int col, int number)
{
//	printf("Removing %d from (%d, %d)\n", number+1, row+1, col+1);
	change_state_at(s, row, col, number, -1);
}


void get_possibilities_at(sudoku * s, int row, int col, int ** possibilities, int *poss_counter)
{
	(*poss_counter) = 0;
	int n;
	for(n = 0; n < N; n++)
		{
			if (s->constraints[row][col][n] == 0)  // no active restriction
				{
				(*possibilities)[(*poss_counter)] = n;
				(*poss_counter)++;	
				}
		}
		
}

void get_most_constrained_cell(sudoku *s, int *row, int *col, int ** possibilities, int *poss_count)
{
	int i,j, min = N+1;
	
	for(i = 0; i < N; i++)
		for(j = 0; j < N; j++)
		{
			if(!s->inserted[i][j])
				{
				get_possibilities_at(s, i, j, possibilities, poss_count);
				if (*poss_count < min)
					{
						min = *poss_count;
						*row = i;
						*col = j;
					}
				}
		}
	get_possibilities_at(s, *row, *col, possibilities, poss_count);
}


/*
Prints the sudoku board in one of 3 visualization modes
*/
void print(sudoku * s, enum print_mode mode)
{
	int * possibilities = malloc(N *sizeof(int));
	
	if (possibilities == NULL)
		{
			fprintf(stderr, "Error: Memory allocation failed in print()\n");
			exit(1);
		}
	
	int poss_count;
	
	int i,j,n;
	for(i = 0; i < N; i++)
	{
		for(j = 0; j < N; j++)
		{
			get_possibilities_at(s, i, j, &possibilities, &poss_count);
			
			switch(mode)
			{
			 case HYPOTHESIS_COUNT:		// shows how many open hypothesis are there in this cell
				putchar(poss_count + '0');
				break;
			 case VALUE:  		// if cell value is known, print it. Otherwise show wildcard character.
				if (poss_count == 1)
					putchar(possibilities[0] + '1');
				else
					putchar('*');
				break;
			case ALL_HYPOTHESIS:			// show all open possibilites
				putchar('[');
				for(n=0; n<N; n++)
					if (s->constraints[i][j][n] == 0)
						putchar(n+'1');
					else
						putchar(' ');
				putchar(']');
				break;
			default:
				abort();	
			};
		}
		putchar('\n');
	}
	putchar('\n');
	
	free(possibilities);
}



void read_input(sudoku * s, enum input_type intype)
{
	int i,j;
	for(i = 0; i < N; i++)
	{
		for(j = 0; j < N; j++)
		{
			char c = getchar();
			if (c == EOF)
				return;
			if (c >= '1' && c <= '9' )
				insert_number_at(s, i, j, c - '1');
		}
		if (intype ==  GRID_INPUT)
			getchar(); // discards the \n at each line
	}
	if (intype == LINEAR_INPUT)
		getchar(); // discards the \n only at the end
}

/*
 Depth first search with backtracking.
 At each level we follow the most constrained sudoku cell (tree node with less childs). 
*/
int solve(sudoku * s)
{
	if( s->ninserted == N*N )
		return 1;
	
	int row, col, poss_count, found_solution=0;
	int * possibilities = malloc(N *sizeof(int));
	
	if (possibilities == NULL)
		{
			fprintf(stderr, "Error: Memory allocation failed in solve()\n");
			exit(1);
		}
	
	get_most_constrained_cell(s, &row, &col, &possibilities, &poss_count);

	if (poss_count == 0) // should backtrack
		{
			s->nbacktracks++;  // just to collect statistics (not important for algorithm)
			free(possibilities);
			return 0; 
		}
		
	int i;
	for(i=0; i<poss_count; i++)
		{
			insert_number_at(s, row, col, possibilities[i]);
			found_solution = solve(s);
			if (found_solution)
				break;
			remove_number_at(s, row, col, possibilities[i]);
			
		}
	free(possibilities);
	return found_solution;
	
}

int main (int argc, char const *argv[])
{
	sudoku s;
	
	if (argc != 2)
		{
			fprintf(stderr, "Usage: %s <input_format>\n", argv[0]);
			fprintf(stderr, "  input_format:\n");
			fprintf(stderr, "    1 = linear format (81 characters, '0' for empty)\n");
			fprintf(stderr, "    2 = grid format (9x9 grid, '_' for empty)\n");
			fprintf(stderr, "\nExample:\n");
			fprintf(stderr, "  %s 1 < examples/example_linear.txt\n", argv[0]);
			fprintf(stderr, "  %s 2 < examples/example_grid.txt\n", argv[0]);
			exit(1);
		}
		
	char *endptr;
	int intype = strtol(argv[1], &endptr, 10);
	if (*endptr != '\0' || intype < 1 || intype > 2)
		{
			fprintf(stderr, "Error: Invalid input format '%s'\n", argv[1]);
			fprintf(stderr, "Must be either 1 (linear) or 2 (grid)\n");
			exit(1);
		}
	
	while(!feof(stdin))
		{
			new_sudoku(&s);
		
			read_input(&s, intype);
			
			// Check if we read a complete puzzle
			if (s.ninserted == 0)
				break;
			
			solve(&s);
	
			print(&s, 1);					   // prints the solution
			// printf("%d\n", s.nbacktracks);  // prints how many times it had to backtrack
		}
		
	return 0;
}