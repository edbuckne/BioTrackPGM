from scipy import io
import numpy as np
import tifffile as tiff

def initialize_expData(conf):
    dataInsert = conf.initConfig
    # configMat = io.loadmat('./mat/config.mat')
    # dataInsert = configMat['array']
    io.savemat(conf.path + '/expData.mat', {'expData':dataInsert})

def save_tip_data(conf, tipData):
    io.savemat(conf.path + '/tipData.mat', {'tipData':tipData})

def new_z_range_microns(conf, z12, zflm):
    # configMat = io.loadmat('./mat/config.mat')
    # expConfig = configMat['expArray']
    # axRes = expConfig[0, 7]
    axRes = conf.expConfig[7]

    z1 = z12[0]
    z2 = z12[1]
    zfm = zflm[0, 0]
    zlm = zflm[0, 1]

    zfmnew = zfm - (z1 - 7) * axRes
    # z1m = zfm + z1 * axRes
    # zfmnew = z1m - 3 * axRes

    zlmnew = zfm - (z2 + 7) * axRes
    # z2m = zfm + z2 * axRes
    # zlmnew = z2m + 3 * axRes

    return zfmnew, zlmnew

def new_mic_positions(conf, z, t, print=True):
    expDataMat = io.loadmat(conf.path + '/expData.mat')
    expData = expDataMat['expData']

    S = expData.shape
    spmN = S[0]

    newData = np.empty((S[0], S[1], 1))
    zflm = np.empty((1, 2))
    if t == 0:
        oldData = expData
    else:
        oldData = expData[:, :, t]

    for spm in range(spmN):
        newData[spm, 0] = oldData[spm, 0]  # Spm number never changes
        newData[spm, 7] = oldData[spm, 7]  # Angle never changes

        if z[0, 0] == 0 and z[0, 1] == 0:  # When z is just zero, the user does not want the z stack range to change
            newData[spm, 3] = oldData[spm, 3]
            newData[spm, 4] = oldData[spm, 4]
        else:
            zflm[0, 0] = oldData[spm, 3]
            zflm[0, 1] = oldData[spm, 4]
            newData[spm, 3], newData[spm, 4] = new_z_range_microns(conf, z[spm, :], zflm)  # Calculate new range for z-stacks to be

        if t == 0:
            newData[spm, 1] = oldData[spm, 1] - oldData[spm, 5]  # Correct for estimated future growth
            newData[spm, 2] = oldData[spm, 2] - oldData[spm, 6]
            newData[spm, 5] = oldData[spm, 5]  # The growth vector between 0 and 1 are the same
            newData[spm, 6] = oldData[spm, 6]
            conf.registration[spm].GV[0] = oldData[spm, 5]
            conf.registration[spm].GV[1] = oldData[spm, 6]
            conf.registration[spm].cumshift[0] = conf.registration[spm].cumshift[0] + oldData[spm, 5]  # Update the cumulative shift with growth vector
            conf.registration[spm].cumshift[1] = conf.registration[spm].cumshift[1] + oldData[spm, 6]
        else:
            newData[spm, 1] = oldData[spm, 1] - conf.registration[spm].dp[0] - conf.registration[spm].GV[0]  # Correct for error and correct for future growth
            newData[spm, 2] = oldData[spm, 2] - conf.registration[spm].dp[1] - conf.registration[spm].GV[1]
            newData[spm, 5] = conf.registration[spm].GV[0]  # Update the growth vector
            newData[spm, 6] = conf.registration[spm].GV[1]
            conf.registration[spm].cumshift[0] = conf.registration[spm].cumshift[0] + conf.registration[spm].dp[0] + conf.registration[spm].GV[0]  # Update the cumulative shift with growth vector and error
            conf.registration[spm].cumshift[1] = conf.registration[spm].cumshift[1] + conf.registration[spm].dp[1] + conf.registration[spm].GV[1]

    if t == 0:
        expDataNew = np.empty((S[0], S[1], 2))
        expDataNew[:, :, 0] = expData
        expDataNew[:, :, 1] = np.reshape(newData, (S[0], S[1]))
    else:
        expDataNew = np.concatenate((expData, newData), axis=2)

    io.savemat(conf.path + '/expData.mat', {'expData': expDataNew})
    print_positions(conf, t+1)

def print_positions(conf, t):
    expDataMat = io.loadmat(conf.path + '/expData.mat')
    expData = expDataMat['expData']

    S = expData.shape
    spmN = S[0]

    if t == 0:
        for spm in range(spmN):
            print('{0:4d} X:{1:10.2f} Y:{2:10.2f} Zf:{3:10.2f} Zl:{4:10.2f}'.format(spm, expData[spm, 1], expData[spm, 2], expData[spm, 3], expData[spm, 4]))
    else:
        for spm in range(spmN):
            print('{0:4d} X:{1:10.2f} Y:{2:10.2f} Zf:{3:10.2f} Zl:{4:10.2f}'.format(spm, expData[spm, 1, t], expData[spm, 2, t], expData[spm, 3, t], expData[spm, 4, t]))

def imwrite3d(I, saveName):
    tiff.imwrite(saveName, bring_z_to_front(I))

def bring_z_to_front(I):
    S = I.shape
    Inew = np.empty((S[2], S[0], S[1]), np.uint16)
    for z in range(S[2]):
        for row in range(S[0]):
            for col in range(S[1]):
                Inew[z, row, col] = I[row, col, z]

    return Inew