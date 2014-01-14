#!/usr/bin/env python
#
# Fillomino puzzle solver using claspy.

from claspy import *

# Fillomino puzzle from:
# http://en.wikipedia.org/wiki/Fillomino
puzzle = """\
` ` ` 3 ` ` ` ` 5
` ` 8 3 10 ` ` 5 `
` 3 ` ` ` 4 4 ` `
1 3 ` 3 ` ` 2 ` `
` 2 ` ` 3 ` ` 2 `
` ` 2 ` ` 3 ` 1 3
` ` 4 4 ` ` ` 3 `
` 4 ` ` 4 3 3 ` `
6 ` ` ` ` 1 ` ` `"""

# Convert puzzle to a 2D array.
puzzle = map(lambda line: line.split(' '), puzzle.split('\n'))
height = len(puzzle)
width = len(puzzle[0])

# Get the largest number that occurs in the puzzle.
max_val = max(map(int, filter(lambda x: x != '`', sum(puzzle, []))))

# Restrict the number of bits used for IntVar.
set_max_val(width*height)

# Create a grid of IntVars indicating which group each cell belongs to.
grid = [[IntVar(1,max_val) if puzzle[r][c] == '`' else IntVar(int(puzzle[r][c]))
         for c in range(9)] for r in range(9)]

# In order to count the number of cells in each group, create a flow
# field indicating a cardinal direction for each cell. All cells in a
# group will flow towards a single root cell, denoted by a '.'.
flow = [[MultiVar('^','v','>','<','.') for c in range(width)] for r in range(height)]
# flow_c is a grid of Atoms used to ensure that all cells are
# connected along the flow field to a root cell.
flow_c = [[Atom() for c in range(width)] for r in range(height)]
for r in range(height):
    for c in range(width):
        # The root cell is proven.
        flow_c[r][c].prove_if(flow[r][c] == '.')
        # All other cells must be proven by following the flow
        # backwards from the root.
        if r > 0:
            flow_c[r][c].prove_if((flow[r][c] == '^') & flow_c[r-1][c] &
                                  (grid[r][c] == grid[r-1][c]))
        if r < height-1:
            flow_c[r][c].prove_if((flow[r][c] == 'v') & flow_c[r+1][c] &
                                  (grid[r][c] == grid[r+1][c]))
        if c > 0:
            flow_c[r][c].prove_if((flow[r][c] == '<') & flow_c[r][c-1] &
                                  (grid[r][c] == grid[r][c-1]))
        if c < width-1:
            flow_c[r][c].prove_if((flow[r][c] == '>') & flow_c[r][c+1] &
                                  (grid[r][c] == grid[r][c+1]))
        require(flow_c[r][c])

# To count cells in a group, create a grid of IntVars, where each value
# is the sum of the values that flow towards it, plus one.
upstream = [[IntVar(0,max_val) for c in range(width)] for r in range(height)]
for r in range(height):
    for c in range(width):
        upstream_count = IntVar(0)
        if r > 0:        upstream_count += cond(flow[r-1][c] == 'v', upstream[r-1][c], 0)
        if r < height-1: upstream_count += cond(flow[r+1][c] == '^', upstream[r+1][c], 0)
        if c > 0:        upstream_count += cond(flow[r][c-1] == '>', upstream[r][c-1], 0)
        if c < width-1:  upstream_count += cond(flow[r][c+1] == '<', upstream[r][c+1], 0)
        require(upstream[r][c] == upstream_count + 1)
        # If this is a root cell, then the count must match the cell's value.
        require(cond(flow[r][c] == '.', upstream[r][c] == grid[r][c], True))

# Require that no two groups come in contact, by creating a grid of values
# indicating which group each cell belongs to. Each group is identified by
# the index number of the root cell (row*width + col).
group = [[IntVar(0,width*height) for c in range(width)] for r in range(height)]
# Require that vertically adjacent cells with the same grid value have the same group.
for r in range(height-1):
    for c in range(width):
        require(cond(grid[r][c] == grid[r+1][c], group[r][c] == group[r+1][c], True))
# Require that horizontally adjacent cells with the same grid value have the same group.
for r in range(height):
    for c in range(width-1):
        require(cond(grid[r][c] == grid[r][c+1], group[r][c] == group[r][c+1], True))
# Require that root cells have the correct group value.
for r in range(height):
    for c in range(width):
        require(cond(flow[r][c] == '.', group[r][c] == r*width + c, True))

# Loop to find all solutions.
while solve():
    print 'solution:'
    for r in range(height):
        for c in range(width):
            print str(grid[r][c]).rjust(2),
        print
    print
    # Once a solution is found, add a constraint eliminating it.
    x = BoolVar(True)
    for r in range(9):
        for c in range(9):
            x = x & (grid[r][c] == grid[r][c].value())
    require(~x)
