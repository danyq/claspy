#!/usr/bin/env python
#
# Sudoku puzzle solver using claspy.

from claspy import *
import itertools

# Sudoku puzzle from:
# http://www.kristanix.com/sudokuepic/worlds-hardest-sudoku.php
puzzle = """\
1 ` ` ` ` 7 ` 9 `
` 3 ` ` 2 ` ` ` 8
` ` 9 6 ` ` 5 ` `
` ` 5 3 ` ` 9 ` `
` 1 ` ` 8 ` ` ` 2
6 ` ` ` ` 4 ` ` `
3 ` ` ` ` ` ` 1 `
` 4 ` ` ` ` ` ` 7
` ` 7 ` ` ` 3 ` `"""

# Convert puzzle to a 2D array.
puzzle = map(lambda line: line.split(' '), puzzle.split('\n'))

# Create a grid of variables with values 1-9.
# Wherever there is a number in the puzzle,
# the IntVar is initialized with that number.
grid = [[IntVar(1,9) if puzzle[r][c] == '`' else IntVar(int(puzzle[r][c]))
         for c in range(9)] for r in range(9)]

# These are the sudoku constraints.
for r in range(9):
    require_all_diff(grid[r])
for c in range(9):
    require_all_diff([grid[r][c] for r in range(9)])
for r in range(0,9,3):
    for c in range(0,9,3):
        require_all_diff([grid[r+i][c+j] for (i,j) in
                          itertools.product(range(3), range(3))])

# Loop to find all solutions.
while solve():
    print 'solution:'
    print '\n'.join([' '.join(map(str, row)) for row in grid])
    print
    # Once a solution is found, add a constraint eliminating it.
    x = BoolVar(True)
    for r in range(9):
        for c in range(9):
            x = x & (grid[r][c] == grid[r][c].value())
    require(~x)
