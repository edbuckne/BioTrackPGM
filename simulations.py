from scipy import io
import numpy as np
import cv2

def mock_tracking_reposition(t, currentShift, I, dp, savePath, spm):
    GV = np.empty((1, 2))  # Growth vector variable

    expDataMat = io.loadmat('./mat/expData.mat')  # Load the tracking data
    expData = expDataMat['expData']
    configMat = io.loadmat('./mat/config.mat')  # Load configuration data
    expConfig = configMat['expArray']

    res = expConfig[0, 3]  # Resolution of lateral pixels in microns
    if t == 0:
        GV[0, 0] = expData[spm, 5]  # Growth vector from this times estimated growth vector
        GV[0, 1] = expData[spm, 6]
    else:
        GV[0, 0] = expData[spm, 5, t]  # Growth vector from this times estimated growth vector
        GV[0, 1] = expData[spm, 6, t]
    Imax = np.amax(I, axis=2)

    GVPixels = GV/res  # We want to shift the image by pixels not microns
    dpPixels = dp[spm, :]/res
    thisShift = GVPixels + dpPixels

    if t==2:
        a = 0

    ITranslate = cv2.warpAffine(Imax, np.float32([[1, 0, currentShift[spm, 0]], [0, 1, currentShift[spm, 1]]]), Imax.shape)
    cv2.imwrite(savePath + '/lattracksimspm' + str(spm) + 't' + str(t) + '.png', ITranslate)

    newShift = currentShift[spm, :] - thisShift[0, :]
    return newShift

def shift_3d_image(I, currentShift):
    S = I.shape

    for z in range(S[2]):
        I[:, :, z] = cv2.warpAffine(I[:, :, z], np.float32([[1, 0, currentShift[0, 0]], [0, 1, currentShift[0, 1]]]), (S[0], S[1]))

    return I

def cut_image(I, t):
    expDataMat = io.loadmat('./mat/expData.mat')  # Load the tracking data
    expData = expDataMat['expData']
    configMat = io.loadmat('./mat/config.mat')  # Load configuration data
    expConfig = configMat['expArray']

    axRes = expConfig[0, 7]  # Resolution of lateral pixels in microns

    zf = expData[0, 3, t]
    zl = expData[0, 4, t]

    zft0 = expData[0, 3, 0]
    # zlt0 = expData[0, 4, 0]

    zfInd = int((zf-zft0)/axRes)
    zlInd = int((zl-zft0)/axRes)

    return I[:, :, zfInd:zlInd]