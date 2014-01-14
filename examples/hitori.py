#!/usr/bin/env python
#
# Hitori puzzle solver using claspy.

from claspy import *

# A very large hitori puzzle from:
# http://www.nikoli.com/en/puzzles/hitori/
puzzle = """\
1 6 6 3 2 4 7 8 16 11 9 10 16 12 5 13 5
2 3 4 9 1 17 6 10 16 10 5 7 11 17 8 14 12
8 2 5 4 8 1 17 7 16 3 6 9 10 11 5 12 5
3 9 8 5 4 9 17 10 1 7 11 7 6 13 2 14 15
8 4 13 6 5 2 17 1 8 12 13 11 8 14 7 9 13
4 1 3 9 6 9 8 2 5 2 10 7 12 15 11 15 14
8 5 7 11 15 12 1 4 2 13 6 14 16 9 3 10 17
5 7 2 12 9 13 3 15 10 2 1 2 14 16 4 2 6
17 16 10 14 5 6 13 13 13 4 3 12 7 16 7 11 9
17 16 9 8 7 13 2 15 3 8 12 8 5 16 6 8 4
6 8 17 13 15 5 15 11 7 14 2 4 16 10 7 3 9
7 1 17 1 11 3 9 3 12 1 8 1 15 3 13 14 10
9 10 17 7 5 8 5 12 6 15 2 16 1 1 1 4 3
12 12 11 10 10 10 14 15 17 9 7 3 13 3 16 2 2
11 11 12 15 13 7 5 14 6 9 6 17 2 2 10 1 1
10 13 1 2 3 11 12 5 14 9 15 7 4 6 17 16 8
12 14 1 2 3 15 4 6 4 5 4 13 16 7 17 16 11"""

# Convert puzzle to a 2D array of ints.
puzzle = map(lambda line: map(int, line.split(' ')),
             puzzle.split('\n'))

# Create a grid of BoolVars indicating which cells are filled.
width = len(puzzle)
height = len(puzzle[0])
fill_grid = [[BoolVar() for x in range(width)] for y in range(height)]

# Require unique unfilled numbers in each row.
for r in range(height):
    for x in range(width+1):  # Go through each possible number.
        # Find numbers which are repeated in this row.
        if sum_vars([puzzle[r][c] == x for c in range(width)]) > 1:
            # Require at most one unfilled cell among those numbers.
            cs = [c for c in range(width) if puzzle[r][c] == x]
            require(at_most(1, [~fill_grid[r][c] for c in cs]))

# Require unique unfilled numbers in each column.
for c in range(width):
    for x in range(height+1):
        if sum_vars([puzzle[r][c] == x for r in range(height)]) > 1:
            rs = [r for r in range(height) if puzzle[r][c] == x]
            require(at_most(1, [~fill_grid[r][c] for r in rs]))

# Vertically adjacent cells cannot be filled.
for r in range(height-1):
    for c in range(width):
        require(~(fill_grid[r][c] & fill_grid[r+1][c]))

# Horizontally adjacent cells cannot be filled.
for r in range(height):
    for c in range(width-1):
        require(~(fill_grid[r][c] & fill_grid[r][c+1]))

# Require connectivity of unfilled cells using a grid of Atoms.
conn_grid = [[Atom() for c in range(width)] for r in range(height)]
# Prove the first two cells to start (one might be filled in).
conn_grid[0][0].prove_if(True)
conn_grid[0][1].prove_if(True)
# All other cells must be proven through a connection to one of those
# two along a path of unfilled cells.
for r in range(height):
    for c in range(width):
        for r1,c1 in [(r,c-1),(r,c+1),(r-1,c),(r+1,c)]:
            if r1 >= 0 and r1 < height and c1 >= 0 and c1 < width:
                conn_grid[r][c].prove_if(conn_grid[r1][c1] & ~fill_grid[r1][c1])
        require(conn_grid[r][c])

# Loop to find all solutions.
while solve():
    print 'solution:'
    for r in range(height):
        for c in range(width):
            if fill_grid[r][c].value():
                print '##',
            else:
                print str(puzzle[r][c]).rjust(2),
        print
    print
    # Once a solution is found, add a constraint eliminating it.
    x = BoolVar(True)
    for r in range(9):
        for c in range(9):
            x = x & (fill_grid[r][c] == fill_grid[r][c].value())
    require(~x)
