import numpy as np
import scipy.io

def create_config(reset=False):
    specimen = eval(input("What is the number of specimen?"))  # input reads integers
    n_time_stamps = eval(input("What is the number of time stamps? "))
    capture_frequency = eval(input("What is the capture frequency of the experiment? "))
    h, w = input("Enter the size of the digital image in pixels (H,W): ").split(',')  # Get additional information from the user
    res = eval(input("What is the xy pixel resolution in microns? "))
    axRes = eval(input("What is the z axial resolution in microns? "))
    TH = eval(input("What is the 16 bit threshold value for fluorescence? "))
    saveName = input("Give this experiment a save name: ")
    loadName = input("Specify the path that CZI files will be loaded from: ")

    data_matrix = np.empty([specimen, 8])
    exp_matrix = np.empty([8])

    exp_matrix[0] = specimen  # Number of specimen
    exp_matrix[1] = h  # Height of image in pixels
    exp_matrix[2] = w  # Width of image in pixels
    exp_matrix[3] = res  # Lateral resolution of pixels in microns
    exp_matrix[4] = n_time_stamps  # Number of images to take in the time course
    exp_matrix[5] = capture_frequency  # Frequency in capturing images in minutes
    exp_matrix[6] = TH  # 16-bit threshold value for determining what is GFP signal
    exp_matrix[7] = axRes  # The axial resolutions of z-slices in microns
    i = 0
    while i < specimen:
        # taking in parameters of specimens
        print('Insert the information for specimen ' + str(i+1) + '\n')
        x_start = eval(input("What is the initial x coordinate? "))
        y_start = eval(input("What is the initial y coordinate? "))
        z1_start = eval(input("What is the z1 coordinate? "))
        z2_start = eval(input("What is the z2 coordinate? "))
        delta_x = eval(input("What is delta x? "))
        delta_y = eval(input("What is delta y? "))
        ang = eval(input("What is the angle? "))
        # storing the values in the config data matrix
        data_matrix[i][0] = i
        data_matrix[i][1] = x_start
        data_matrix[i][2] = y_start
        data_matrix[i][3] = z1_start
        data_matrix[i][4] = z2_start
        data_matrix[i][5] = delta_x
        data_matrix[i][6] = delta_y
        data_matrix[i][7] = ang

        i = i+1
    # put the data of the array into list form
    if reset:
        return data_matrix
    else:
        matDict = {"array": data_matrix, 'expArray': exp_matrix, 'saveName': saveName, 'loadName': loadName}
        scipy.io.savemat("./mat/config.mat", matDict)
        print(data_matrix)
    return matDict