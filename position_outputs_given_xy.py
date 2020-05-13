import scipy.io as io
import numpy as np
import fun.gridPositions as grid
import sys


#  This function takes in the specimen number, loads the configuration data from [ROOT]/mat/config.mat and
#  decides the NxN grid to place the specimen for calibration.
#  Note: create_config.py must be called before this function
def position_outputs_given_xy(spm = 1):

    try:
        matFile = io.loadmat("./mat/config.mat")  # Load the config.mat file that holds the experimental setup metadata
    except:
        print('Seems as if you have not created a config.mat file. Try running create_config.py')

    configData = matFile['array']  # 'array' string holds the dictionary key for the configData table
    exp_matrix = matFile['expArray']
    spmNumber = configData.shape[0]  # Get the number of specimen from the configData array size (# of rows = # of specimen)

    h = exp_matrix[0, 1]
    w = exp_matrix[0, 2]
    res = exp_matrix[0, 3]
    N = eval(input("How many positions is the specimen to be moved? "))

    print("Calculating grid .... \n")

    g = grid.calcGrid(configData[spm-1, 1], configData[spm-1, 2], h, w, res, N)  # This function creates the grid to use
    print('Grid for specimen ' + str(spm))
    grid.printGrid(g)
    print('\n')
    io.savemat("./mat/specimen" + str(spm) + "Grid.mat", {'grid':g})


#  This function takes in the x, y position of the specimen (in microns), the height (h) and width (w) of the
#  digital image to be taken (in pixels), the lateral resolution (res) of each pixel (in microns), and the number
#  of grid elements to split the image space.
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


# if len(sys.argv) == 1:
#     position_outputs_given_xy()
# elif len(sys.argv) == 2:
#     position_outputs_given_xy(int(sys.argv[1]))
