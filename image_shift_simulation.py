import scipy.io as io
import pyautogui as mc
import sys
from fun import dataHandle
from fun.readCzi import czi_to_array as czi
from findTip import findTip as ft
from findTip import new_GV
import numpy
import os.path
import time
import simulations


# Loads the .mat file that holds the screen locations of buttons and input boxes
def load_screen_positions():
    try:
        clickRegions = io.loadmat('./mat/screenPositions.mat')
    except:
        print('Error: no screen positions have been calibrated, try running save_click_regions.py')
    return clickRegions


# Goes to a specified point and enters the specified text
def text_insert(val, CR, mouseTime = 1.0):
    mc.moveTo(CR[0], CR[1], mouseTime)
    mc.click(clicks=3)
    mc.typewrite(str(val))
    mc.press('enter')


# Goes to a specified point and clicks at that location
def click_button(CR, mouseTime = 1.0):  # Moves the mouse there and clicks
    mc.moveTo(CR[0], CR[1], mouseTime)
    mc.click(clicks=1)


# Simply presses the start imaging button in zen
def launch_imaging(mouseTime = 1.0):
    clickRegions = load_screen_positions()
    click_button(clickRegions['sbPos'][0], mouseTime)


# Takes in all 4 values that specify a microscope location and adds it to the list
def insert_xyzfzl(x, y, zf, zl, ang, mouseTime = 1, clickAdd = True):
    clickRegions = load_screen_positions()

    text_insert('%.2f' % x, clickRegions['xPos'][0], mouseTime)
    text_insert('%.2f' % y, clickRegions['yPos'][0], mouseTime)
    text_insert('%.2f' % zf, clickRegions['zPos'][0], mouseTime)
    text_insert('%.2f' % ang, clickRegions['angPos'][0], mouseTime)
    click_button(clickRegions['zfPos'][0], mouseTime)
    text_insert('%.2f' % zl, clickRegions['zPos'][0], mouseTime)
    click_button(clickRegions['zlPos'][0], mouseTime)
    if clickAdd:
        click_button(clickRegions['addPos'][0], mouseTime)


# Takes in the spm number and time and inserts that specimen location into the zen software by reading the file at
# location [DIR]/mat/expData.mat
def insert_specimen_location(spm, t = 0, mouseTime = 0.2):
    expDataMat = io.loadmat('./mat/expData.mat')
    expData = expDataMat['expData']
    s = expData.shape

    if t == 0:
        insert_xyzfzl(expData[spm - 1, 1], expData[spm - 1, 2], expData[spm - 1, 3], expData[spm - 1, 4], expData[spm-1, 7], mouseTime)
    else:
        insert_xyzfzl(expData[spm - 1, 1, t], expData[spm - 1, 2, t], expData[spm - 1, 3, t], expData[spm - 1, 4, t], expData[spm-1, 7, t], mouseTime)


# Inserts all of the specimen in the current experiment into the imaging list for the time stamp (t)
def insert_all_specimen_location(t = 0, mouseTime = 0.2):
    try:  # Load the configuration file if it exists
        configMat = io.loadmat('./mat/config.mat')
        expConfig = configMat['expArray']
    except ValueError:
        print('Error loading config.mat. Make sure you have created a config file by running create_config.py')

    spmN = int(expConfig[0][0])  # Number of specimen ran in this experiment

    for spm in range(spmN):
        insert_specimen_location(spm + 1, t)  # Enter all of the specimen in the


# Goes to the specified remove all button location and clears the specimen list in the zen software
def click_remove_all():
    current_position = mc.position()
    clickRegions = load_screen_positions()

    click_button(clickRegions['raPos'][0], 0.1)
    mc.moveTo(current_position.x, current_position.y)


# Option 1: Calls different functions according to what the user specifies
def manual_control():
    clickRegions = load_screen_positions()

    while True:
        opt = eval(input('Choose an option\n 0. Exit\n 1. Enter X\n 2. Enter Y\n 3. Enter Zf\n 4. Enter Zl\n 5. Add\n 6. Enter Angle\n'))
        if opt == 0:
            break
        val = eval(input('\nWhat value do you want to enter? '))

        if opt == 1:  # Insert X position
            text_insert(val, clickRegions['xPos'][0])
        elif opt == 2:  # Insert Y position
            text_insert(val, clickRegions['yPos'][0])
        elif opt == 3:  # Insert and click Z first value
            text_insert(val, clickRegions['zPos'][0])
            click_button(clickRegions['zfPos'][0])
        elif opt == 4:  # Insert and click Z last value
            text_insert(val, clickRegions['zPos'][0])
            click_button(clickRegions['zlPos'][0])
        elif opt == 5:  # Adds the position to the list
            click_button(clickRegions['addPos'][0])
        elif opt == 6:  # Insert angle position
            text_insert(val, clickRegions['angPos'][0])


# Option 2: Autonomously run the experiment given the initial config.mat setup file
def run_experiment(tStart, v):
    try:  # Load the configuration file if it exists
        configMat = io.loadmat('./mat/config.mat')
        expConfig = configMat['expArray']
        saveName = configMat['saveName']
        loadName = configMat['loadName']
    except ValueError:
        print('Error loading config.mat. Make sure you have created a config file by running create_config.py')

    spmN = int(expConfig[0][0])  # Number of specimen ran in this experiment
    T = int(expConfig[0][4])  # Number of time stamps
    tFreq = expConfig[0][5]  # Number of minutes to wait between imaging
    tFreqSec = int(tFreq*60)  # Number of seconds to wait between imaging
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TEST~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
    # currentShift = numpy.array([[0, 0]])  # Holds the cumlative value of the pixels to shift by
    currentShift = numpy.zeros((spmN, 2))
    testSavePath = input('Enter the path to where you want to save this test: ')
    # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TEST~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

    xy = numpy.empty((spmN, 2))
    z = numpy.empty((spmN, 2))
    GV = numpy.empty((spmN, 2))
    dp = numpy.empty((spmN, 2))

    for t in range(tStart, T):
        tReal = t+1
        if t == 0:
            dataHandle.initialize_expData()
        now = time.time()  # Start a timer
        then = time.time()

        # insert_all_specimen_location(t)
        # launch_imaging(mouseTime=0.2)  # Click the start experiment button in ZEN in 0.2 seconds

        # Wait until ZEN is completed it's imaging

        for spm in range(spmN):
            timeString = '_%02d' % (tReal)
            cziFileName = str(loadName)[2:-2] + '/' + str(saveName)[2:-2] + str(timeString) + '_G' + str(spm+1) + '.czi'  # Path to the czi file to evaluate
            print('Loading czi file for SPM ' + str(spm+1) + ' -- ' + cziFileName)

            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TEST~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
            # I = czi(cziFileName, 0)  # Load the brightfield and fluorescent image from the czi file
            I = czi(cziFileName, 2, v)  # Load the view 2 of the images, just the brightfield
            # print('Shifting image')
            # I = simulations.shift_3d_image(I, currentShift)
            print('Calculating root tip location')
            xy[spm, 0], xy[spm, 1] = ft(I, False)
            xy[spm, :] = xy[spm, :] + currentShift[spm, :]
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TEST~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

            # print('Calculating root tip location')
            # xy[spm, 0], xy[spm, 1] = ft(I[:, :, :, 1], False)  # Get the x and y position of the root tip
            print('Calculated tip position for SPM ' + str(spm + 1) + ' -- X:' + str(xy[spm, 0]) + ' Y:' + str(xy[spm, 1]))
            if t == 0:
                dataHandle.save_tip_data(xy)  # If this is the first time stamp, save the tip data as the nominal values
                dp = dp * 0
            else:
                gvIn, dpIn = new_GV(xy, t, spm)  # Find the new growth vector given the position of the root tip
                GV[spm, 0] = gvIn[0]
                GV[spm, 1] = gvIn[1]
                dp[spm, 0] = dpIn[0]
                dp[spm, 1] = dpIn[1]
                print('Tracking error for SPM ' + str(spm+1) + ' = ' + str(dp[spm, :]))
                print('New Growth Vector: ' + str(GV[spm, :]))

            # z[spm, 0], z[spm, 1] = find_Z_Range(I[:, :, :, 0])  # Get the range of z stacks that are to be imaged according to where the signal is
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TEST~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #
            print('Printing shifted version of image')
            currentShift[spm, :] = simulations.mock_tracking_reposition(t, currentShift, I, dp, testSavePath, spm)  #
            # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TEST~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~ #

        print('Saving new positions into database')
        dataHandle.new_mic_positions(GV, dp, numpy.array([[0, 0]]), t)
        # print('Waiting ....')

        # while (then-now) < tFreqSec:  # Wait until time to take another image
        #     then = time.time()

        # click_remove_all()


# Option 3: Grabs the information from the grid and adds all information there
def add_grid():
    userIn = eval(input('Which specimen do you want to grid? '))

    try:
        gridMat = io.loadmat('./mat/specimen' + str(userIn) + 'Grid.mat')
    except:
        print('Error: This specimen does not exist or a grid has not been created for it')

    try:
        configDataMat = io.loadmat('./mat/config.mat')
        configData = configDataMat['array']
        zf = configData[userIn-1, 3]
        zl = configData[userIn-1, 4]
        ang = configData[userIn-1, 7]
    except:
        print('Error: The configuration file has not yet been created. Try running create_config.py')

    grid = gridMat['grid']
    s = grid.shape

    for row in range(s[0]):
        for col in range(s[1]):
            insert_xyzfzl(grid[row, col, 0], grid[row, col, 1], zf, zl, ang, mouseTime = 0.1)
