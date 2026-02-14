# Makefile for Sudoku Solver
# Author: Hugo Penedones

CC = gcc
CFLAGS = -Wall -Wextra -O2
TARGET = solver
SOURCE = sudoku_solver.c

.PHONY: all clean test

all: $(TARGET)

$(TARGET): $(SOURCE)
	$(CC) $(CFLAGS) $(SOURCE) -o $(TARGET)

clean:
	rm -f $(TARGET)

test: $(TARGET)
	@./test.sh
