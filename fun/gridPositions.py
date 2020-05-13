import numpy as np

# Calculates the positions the specimen needs to be in for a NXN grid
def calcGrid(x, y, h, w, res, N):
    grid = np.empty([N, N, 2], dtype=float)

    resh = res * h  # Convert the pixel height and width to microns
    resw = res * w

    boxh = resh / N
    boxw = resw / N

    top = y - (resh / 2)
    left = x - (resw / 2)

    dynh = boxh / 2
    dynw = boxw / 2

    for gridRow in range(N):
        for gridCol in range(N):
            grid[gridRow, gridCol, 0] = left + dynw + (gridCol * boxw)
            grid[gridRow, gridCol, 1] = top + dynh + (gridRow * boxh)


    return grid

# Prints the grid that was created by calcGrid
def printGrid(grid):
    s = grid.shape

    for row in range(s[0]):
        for col in range(s[1]):
            print('x: ' + '{0:12.2f}'.format(grid[row, col, 0]) + ', y: ' + '{0:12.2f}'.format(grid[row, col, 1]))
