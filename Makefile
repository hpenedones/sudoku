# Makefile for Sudoku Solver
# Author: Hugo Penedones

CC = gcc
CFLAGS = -Wall -Wextra -O2
TARGET = solver
SOURCE = sudoku_solver.c
HEADER = sudoku.h

# Shared library settings
LIB_NAME = libsudoku
ifeq ($(OS),Windows_NT)
	SHARED_EXT = .dll
	SHARED_FLAGS = -shared
else
	UNAME_S := $(shell uname -s)
	ifeq ($(UNAME_S),Darwin)
		SHARED_EXT = .dylib
		SHARED_FLAGS = -dynamiclib -install_name @rpath/$(LIB_NAME)$(SHARED_EXT)
	else
		SHARED_EXT = .so
		SHARED_FLAGS = -shared -fPIC
	endif
endif

SHARED_LIB = $(LIB_NAME)$(SHARED_EXT)

.PHONY: all clean test lib

all: $(TARGET) $(SHARED_LIB)

$(TARGET): $(SOURCE) $(HEADER)
	$(CC) $(CFLAGS) $(SOURCE) -o $(TARGET)

$(SHARED_LIB): $(SOURCE) $(HEADER)
	$(CC) $(CFLAGS) $(SHARED_FLAGS) -DSUDOKU_LIB_ONLY=1 $(SOURCE) -o $(SHARED_LIB)

lib: $(SHARED_LIB)

clean:
	rm -f $(TARGET) $(SHARED_LIB)

test: $(TARGET)
	@./test.sh
