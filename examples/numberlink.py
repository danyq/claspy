#!/usr/bin/env python
#
# Numberlink puzzle solver using claspy.

from claspy import *

# A numberlink puzzle from:
# http://www.nikoli.com/en/puzzles/numberlink/
puzzle = """\
1 ` ` ` ` ` ` ` ` ` ` ` ` ` 3 ` ` `
` ` 2 ` ` ` ` ` ` ` ` 4 ` ` ` ` 9 `
` ` ` ` ` ` 7 ` ` ` ` ` ` 6 ` ` ` `
` ` 3 ` ` ` ` ` ` ` ` ` ` ` ` ` 8 `
` ` ` ` ` ` ` ` ` ` ` ` 7 ` ` ` ` `
` ` ` ` ` ` ` ` 6 ` ` ` ` ` ` ` ` `
` ` ` ` ` ` ` ` ` ` ` ` 5 ` ` ` ` `
` ` 4 ` ` ` ` ` ` ` ` ` ` ` 9 ` ` `
` ` ` ` 5 ` 8 ` ` ` ` ` ` ` ` 2 ` `
` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` ` 1"""

# Convert puzzle to a 2D array.
puzzle = map(lambda line: line.split(' '), puzzle.split('\n'))
height = len(puzzle)
width = len(puzzle[0])

# Get the largest number that occurs in the puzzle.
num_links = max(map(int, filter(lambda x: x != '`', sum(puzzle, []))))

# Create a grid of variables indicating which link number passes
# through each cell. The given endpoints are initialized with that
# number.
grid = [[IntVar(1,num_links) if puzzle[r][c] == '`' else IntVar(int(puzzle[r][c]))
         for c in range(width)] for r in range(height)]

# For every cell, count the number of neighbors that share the same
# grid value. Endpoints should have one, and all other cells should
# have two.
for r in range(height):
    for c in range(width):
        same_neighbors = []
        for r1,c1 in [(r,c-1), (r,c+1), (r-1,c), (r+1,c)]:
            if r1 >= 0 and c1 >= 0 and r1 < height and c1 < width:
                same_neighbors.append(grid[r][c] == grid[r1][c1])
        if puzzle[r][c] == '`':
            require(sum_bools(2, same_neighbors))
        else:
            require(sum_bools(1, same_neighbors))

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
