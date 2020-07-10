import scipy.io as io
import pyautogui as mc
import tkinter as tk
import sys
from fun import dataHandle
from fun.readCzi import czi_to_array as czi
from fun.dataHandle import imwrite3d
from findTip import findTip as ft
from findTip import find_Z_Range
from findTip import new_GV
import numpy
import os.path
import time
import scipy.misc
import cv2
import simulations
import image_shift_simulation
import axial_selection_simulation
from create_config import create_config
from position_outputs_given_xy import position_outputs_given_xy
from fun.mockExperimentFun import reset
from save_click_regions import collect_click_regions
from fun.mockExperimentFun import display_annotations
from box_class import App
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QPushButton, QAction, QLineEdit, QMessageBox
from config_class import config
from sequence_class import sequence
from setting_class import settings

# import pywinauto as win
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
def launch_imaging(conf, mouseTime = 1.0):
    # clickRegions = load_screen_positions()
    click_button(conf.click_regions['sbPos'][0], mouseTime)


# Takes in all 4 values that specify a microscope location and adds it to the list
def insert_xyzfzl(conf, x, y, zf, zl, ang, mouseTime = 1, clickAdd = True):
    clickRegions = conf.click_regions

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
def insert_specimen_location(conf, spm, t = 0, mouseTime = 0.2):
    expDataMat = io.loadmat(conf.path + '/expData.mat')
    expData = expDataMat['expData']
    s = expData.shape

    if len(expData.shape) == 2:
        conf.sequence[spm - 1].run_sequence(expData[spm - 1, 1], expData[spm - 1, 2], expData[spm - 1, 3], expData[spm - 1, 4])
        # insert_xyzfzl(conf, expData[spm - 1, 1], expData[spm - 1, 2], expData[spm - 1, 3], expData[spm - 1, 4], expData[spm-1, 7], mouseTime)
    else:
        conf.sequence[spm - 1].run_sequence(expData[spm - 1, 1, t], expData[spm - 1, 2, t], expData[spm - 1, 3, t], expData[spm - 1, 4, t])
        # insert_xyzfzl(conf, expData[spm - 1, 1, t], expData[spm - 1, 2, t], expData[spm - 1, 3, t], expData[spm - 1, 4, t], expData[spm-1, 7, t], mouseTime)


# Inserts all of the specimen in the current experiment into the imaging list for the time stamp (t)
def insert_all_specimen_location(conf, t = 0, mouseTime = 0.2):
    try:  # Load the configuration file if it exists
        configMat = io.loadmat('./mat/config.mat')
        expConfig = configMat['expArray']
    except ValueError:
        print('Error loading config.mat. Make sure you have created a config file by running create_config.py')
    # expConfig = conf.expConfig

    spmN = int(conf.expConfig[0])  # Number of specimen ran in this experiment

    for spm in range(spmN):
        insert_specimen_location(conf, spm + 1, t)  # Enter all of the specimen in the


# Goes to the specified remove all button location and clears the specimen list in the zen software
def click_remove_all(conf):
    # current_position = mc.position()
    # clickRegions = load_screen_positions()
    # clickRegions = conf.click_regions
    click_button(conf.click_regions['raPos'][0], 0.1)


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
def run_experiment(conf, tStart, wait = False, simulation = False):
    save_wait_time = 4  # Wait
    image_wait_time = 20
    saveName = conf.saveName
    loadName = conf.path
    spmN = int(conf.expConfig[0])  # Number of specimen ran in this experiment
    T = int(conf.expConfig[4])  # Number of time stamps
    tFreq = conf.expConfig[5]  # Number of minutes to wait between imaging
    tFreqSec = int(tFreq*60)  # Number of seconds to wait between imaging

    xy = numpy.empty((spmN, 2))  # Create variables to hold information during the experiment
    z = numpy.empty((spmN, 2))
    zMic = numpy.empty((spmN, 2))
    GV = numpy.empty((spmN, 2))
    dp = numpy.empty((spmN, 2))

    for t in range(tStart, T):  # Go through each time stamp
        tReal = t+1
        if t == 0:
            dataHandle.initialize_expData(conf)
        now = time.time()  # Start a timer
        then = time.time()

        if not simulation:
            insert_all_specimen_location(conf, t)  # Plug in information through the sequence

        timeString = '_%02d' % (tReal)

        if not simulation:
            nowtmp = time.time()  # Wait until ZEN has pulled up the save image file
            while time.time() < nowtmp + save_wait_time:
                tmp = 0
            mc.typewrite(saveName + str(timeString))
            mc.press('enter')

            print('Waiting for imaging to complete .... ')
            nowtmp = time.time()  # Wait until ZEN is completed it's imaging
            while time.time() < nowtmp + image_wait_time:
                tmp = 0
        else:
            # ==========================================SIMULATION========================================== #
            print('Save name: ' + conf.return_convention_name(t, 0, conf.sett.MICROSCOPE_SAVE_CONFIGURATION))
            # ==========================================SIMULATION========================================== #


        for spm in range(spmN):
            ch = int(conf.registration[spm].channel) - 1  # Determine the image to use for registration

            print('Loading: ' + conf.return_convention_name(t, spm, conf.sett.MICROSCOPE_LOAD_CONFIGURATION))
            # Here we need to design a way for loading the images from different file sources

            image_file_path = loadName + '/' + conf.return_convention_name(t, spm, conf.sett.MICROSCOPE_LOAD_CONFIGURATION) + '.czi'  # Load the image file into memory
            print('Loading czi file for SPM ' + str(spm+1) + ' -- ' + image_file_path)
            I = czi(image_file_path, 0)  # Load the brightfield and fluorescent image from the czi file

            if t > 0 and (conf.registration[spm].method == 'PMIR' or conf.registration[spm].method == 'PCIR'):  # Load the previous image as well if feature matching image registration is used
                image_file_path_previous = loadName + '/' + conf.return_convention_name(t-1, spm, conf.sett.MICROSCOPE_LOAD_CONFIGURATION) + '.czi'
                print('Loading czi file for SPM ' + str(spm + 1) + ' -- ' + image_file_path_previous)
                Imin = czi(image_file_path_previous, 0)
                Im1 = Imin[:, :, :, ch]
            else:
                Im1 = 0
                image_file_path_previous = 'None'

            if conf.simulation and conf.sett.SIMULATION_IMAGE_PRINT:  # Print the simulated image if necessary
                num_rows, num_cols = I.shape[:2]
                translation_matrix = numpy.float32([[1, 0, -conf.registration[spm].cumshift[0]], [0, 1, -conf.registration[spm].cumshift[1]]])
                imtranslate = cv2.warpAffine(I[:, :, :, ch], translation_matrix, (num_cols, num_rows))
                scipy.misc.imsave('./Results/Sim/' + conf.return_convention_name(t, spm, conf.sett.MICROSCOPE_LOAD_CONFIGURATION) + '.png', numpy.max(imtranslate, axis=2))

            conf.registration[spm].register_movement(conf, I[:, :, :, ch], t, spm, Im1)  # Calculates the shift in position for the XY lateral plane

            print('Calculating new z range for fluorescent image')

            z[spm, 0], z[spm, 1] = find_Z_Range(conf, I[:, :, :, 0])  # Get the range of z stacks that are to be imaged according to where the signal is

        print('Saving new positions into database')
        dataHandle.new_mic_positions(conf, z, t)

        # ==========================================SIMULATION========================================== #
        # if simulation:
        #     display_annotations(conf, I, 1, t, xy, z)
        # ==========================================SIMULATION========================================== #

        print('Waiting ....')
        # =============================================TEST============================================= #
        if wait:
            dumby = 0
            # tmp = input('Press Enter when you are ready to proceed: ')
        # =============================================TEST============================================= #
        else:
            while (then-now) < tFreqSec:  # Wait until time to take another image
                then = time.time()


# Option 3: Grabs the information from the grid and adds all information there
def add_grid():
    userIn = eval(input('Which specimen do you want to grid? '))
    position_outputs_given_xy(spm=userIn)

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

    # for row in range(s[0]):
    #     for col in range(s[1]):
    #         insert_xyzfzl(grid[row, col, 0], grid[row, col, 1], zf, zl, ang, mouseTime = 0.1)


def simulation_menu(conf):
    opt = eval(input('\n\n =========================================================================================== \n'
                     'Choose an option\n 1. Lateral Tracking Simulation\n 2. Axial Tracking Simulation\n '
                     '3. Microscope Simulation\n 4. Return \n\n Option: '))
    if opt == 1:
        tStart = eval(input('At what time stamp would you like to start? '))
        v = eval(input('Enter which view to evaluate: '))
        image_shift_simulation.run_experiment(tStart, v)
    elif opt == 2:
        tStart = eval(input('At what time stamp would you like to start? '))
        v = eval(input('Enter which view to evaluate: '))
        axial_selection_simulation.run_experiment(tStart, v)
    elif opt == 3:
        tStart = eval(input('At what time stamp would you like to start? '))
        run_experiment(conf, tStart, wait=True, simulation=True)
    elif opt == 4:
        print('\n\n =========================================================================================== \n')
        return


def calibration_menu():
    opt = eval(input('\n\n =========================================================================================== '
                     '\nChoose an option\n 1. Calibrate Vignetting\n 2. Calibrate Click Regions \n 3. Return \n\n Option: '))
    if opt == 1:
        add_grid()
    elif opt == 2:
        collect_click_regions(5)
    elif opt == 3:
        print('\n\n =========================================================================================== \n')
        return

def setup_exp_menu(sett):
    loop = True
    while loop:
        loop = False
        opt = eval(input('\n\n =========================================================================================== '
                         '\nChoose an option\n 1. Load Configuration\n 2. Create Configuration\n 3. Return '
                         '\n\n Option: '))
        if opt == 1:
            conf = config(sett, True, True)
            return conf
        elif opt == 2:
            conf = config(sett, True, False)  # Create a new configuration class object
            return conf
        elif opt == 3:
            print('\n\n =========================================================================================== \n')
            return

def sequence_menu():

    loop = True
    while loop:
        opt = eval(input('\n\n =========================================================================================== '
                         '\nChoose an option\n 1. Create new sequence\n 2. Load a sequence\n 3. Run a sequence\n '
                         '4. Create new sequence from existing\n 5. Return'
                         '\n Option: '))
        loop = False
        if opt == 1:
            seq = sequence(new=True)
        elif opt == 2:
            seq = sequence(new=False)
        elif opt == 3:
            seq = sequence(new=False, ret=True)
            seq.run_sequence()
        elif opt == 4:
            seq = sequence(new=False, preexisting=True)
        elif opt == 5:
            return

def print_some_stuff():
    print('This is a test')

# Main interface with the user
def ZEN_AI(optArg = 0):
    if not os.path.exists('./mat/settings/settings.pkl'):
        sett = settings(create=True)
    else:
        sett = settings(create=False)
    opt = optArg
    while opt != -1:
        if optArg == 0:
            opt = eval(input('\n\nChoose an option\n 1. Run Experiment\n 2. Setup Experiment \n 3. Sequence Menu \n '
                             '4. Run Simulation\n 5. Settings \n -1: Exit\n\n Option: '))
        else:
            opt = optArg
        if opt == 1:
            try:
                run_experiment(conf, 0)
            except:
                print('You must setup the experiment before you can run it')
        elif opt == 2:
            conf = setup_exp_menu(sett)
        elif opt == 3:
            sequence_menu()
        elif opt == 4:
            conf.simulation = True
            run_experiment(conf, 0, wait=True, simulation=True)
            conf.simulation = False
        elif opt == 5:
            sett.settings_menu(0)
        elif opt == -1:
            continue
        else:
            print('\nInvalid option')


        # elif opt == 6:
        #     tStart = eval(input('At what time stamp would you like to start? '))
        #     run_experiment(tStart, wait=True)

        # elif opt == 8:
        #     t = reset()
        #     run_experiment(t, wait=True)

            # manual_control()

# if len(sys.argv) >= 2:
#     if sys.argv[1] == 'run':
#         ZEN_AI()

ZEN_AI()
