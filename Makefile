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
	@echo "Testing with sample puzzle..."
	@echo "530070000600195000098000060800060003400803001700020006060000280000419005000080079" | ./$(TARGET) 1
