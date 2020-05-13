from scipy import io
import numpy as np
from findTip import findTip as ft
from create_config import create_config
from fun.readCzi import czi_to_array as czi
import matplotlib.pyplot as plt
import cv2

def reset():
    expDataMat = io.loadmat('./mat/expData.mat')  # Load the .mat file that contains the experimental data
    expData = expDataMat['expData']

    configMat = io.loadmat('./mat/config.mat')  # Load configuration data
    expConfig = configMat['expArray']
    saveName = configMat['saveName']
    loadName = configMat['loadName']

    S = expData.shape  # Get the number of specimen and time stamps that have gone by
    t = S[2]-1
    nSpm = S[0]

    newExpData = create_config(reset=True)  # Gather new placement information concerning the reset

    tipData = np.empty((nSpm, 2))  # Will hold the information for the new tip locations
    print('Resetting tip location and growth vector')

    for spm in range(nSpm):  # Find the tip location of each specimen
        expData[spm, 1:8, t] = newExpData[spm, 1:8]  # Replace the experimental data of the last known timestamp to the reset values

        timeString = '_%02d' % t  # Load the image from the czi file
        cziFileName = str(loadName)[2:-2] + '/' + str(saveName)[2:-2] + str(timeString) + '_G' + str(spm + 1) + '.czi'
        print('loading ' + cziFileName)
        I = czi(cziFileName, 0)

        print('Calculating tip location for specimen ' + str(spm))  # Get the tip location from this image
        tipData[spm, 0], tipData[spm, 1] = ft(I[:, :, :, 1], False)
        print('Tip recalibration complete')

    io.savemat('./mat/expData', {'expData': expData})  # Overwrite the existing data to reflect new data
    io.savemat('./mat/tipData', {'tipData': tipData})

    return t


def display_annotations(conf, I, spm, t, xy, z):
    expDataMat = io.loadmat(conf.path + '/expData.mat')  # Load the data from the mat folder
    expData = expDataMat['expData']
    # configMat = io.loadmat('./mat/config.mat')
    # configExp = configMat['expArray']
    configExp = conf.expConfig
    tipDataMat = io.loadmat(conf.path + '/tipData.mat')
    tipData = tipDataMat['tipData']

    Ic1 = I[:, :, :, 0]
    Ic1max = np.max(Ic1, axis=0)
    Ic1maxsqueeze = np.transpose(Ic1max)
    Ic2 = I[:, :, :, 1]
    Ic2max = np.max(Ic2, axis=2)
    sbig = Ic2max.shape
    s = Ic1maxsqueeze.shape
    newHeight = int(s[0]*configExp[0, 7]/configExp[0, 3])
    res = cv2.resize(Ic1maxsqueeze, dsize=(s[1], newHeight), interpolation=cv2.INTER_CUBIC)/0.01

    Icat = np.concatenate((Ic2max, res))

    if t == 0:
        if len(expData.shape) == 3:
            GVx = expData[spm, 5, t+1]
            GVy = expData[spm, 6, t+1]
        else:
            GVx = expData[spm, 5]
            GVy = expData[spm, 6]
    else:
        GVx = expData[spm, 5, t+1]
        GVy = expData[spm, 6, t+1]
    resXY = configExp[0, 3]

    x = np.linspace(1, s[1])
    y1mag = sbig[0] + z[spm, 0] * configExp[0, 7] / configExp[0, 3]
    y1 = np.ones((50)) * y1mag
    y2mag = sbig[0] + z[spm, 1] * configExp[0, 7] / configExp[0, 3]
    y2 = np.ones((50)) * y2mag

    textSpace = 75
    textOrigin = [0, 0]
    marginSpacing = [20, 20]

    plt.imshow(Icat)
    plt.scatter(tipData[spm, 0], tipData[spm, 1], c=[[0, 0, 0]])
    plt.scatter(xy[spm, 0], xy[spm, 1], c=[[1, 0, 0]])

    plt.text(textOrigin[0] + marginSpacing[0], textOrigin[1] + marginSpacing[1] + 1 * textSpace, 'Nominal Tip Location, X:' + str(tipData[spm, 0]) + ' Y:' + str(tipData[spm, 1]))
    plt.arrow(xy[spm, 0], xy[spm, 1], GVx/resXY, GVy/resXY, head_width=20, head_length=20, length_includes_head=True)
    xError = (tipData[spm, 0] - xy[spm, 0])
    yError = (tipData[spm, 1] - xy[spm, 1])
    if (xError==0) and (yError==0):
        print('Perfect Prediction')
    else:
        plt.arrow(xy[spm, 0], xy[spm, 1], (tipData[spm, 0] - xy[spm, 0]), (tipData[spm, 1] - xy[spm, 1]), head_width=20, head_length=20, length_includes_head=True)
    plt.text(textOrigin[0] + marginSpacing[0], textOrigin[1] + marginSpacing[1] + 2 * textSpace, 'Current Tip Location, X:' + str(xy[spm, 0]) + ' Y:' + str(xy[spm, 1]))
    plt.text(textOrigin[0] + marginSpacing[0], textOrigin[1] + marginSpacing[1] + 3 * textSpace, 'Growth vector, dX:' + str(round(GVx)) + ' dY:' + str(round(GVy)))
    plt.text(textOrigin[0] + marginSpacing[0], textOrigin[1] + marginSpacing[1] + 5 * textSpace, 'Current Mic Position')
    plt.text(textOrigin[0] + marginSpacing[0], textOrigin[1] + marginSpacing[1] + 6 * textSpace, 'X:' + str(expData[spm, 1, t]))
    plt.text(textOrigin[0] + marginSpacing[0], textOrigin[1] + marginSpacing[1] + 7 * textSpace, 'Y:' + str(expData[spm, 2, t]))
    plt.text(textOrigin[0] + marginSpacing[0], textOrigin[1] + marginSpacing[1] + 9 * textSpace, 't+1 Mic Position')
    plt.text(textOrigin[0] + marginSpacing[0], textOrigin[1] + marginSpacing[1] + 10 * textSpace, 'X:' + str(expData[spm, 1, t+1]))
    plt.text(textOrigin[0] + marginSpacing[0], textOrigin[1] + marginSpacing[1] + 11 * textSpace, 'Y:' + str(expData[spm, 2, t+1]))
    plt.plot(x, y1, 'r')
    plt.plot(x, y2, 'r')
    plt.show()


