import scipy.io as io

# Takes in the spm number and time and displays the data collected for that specimen at that time
def read_specimen_data(spm, t = -1, ret = True, pnt = True):
    configDataMat = io.loadmat('./mat/expData.mat')
    configData = configDataMat['expData']

    S = configData.shape

    if len(S) == 3:
        T = S[2]
    else:
        T = 1

    if pnt:
        print('{0:5} {1:5} {2:5} {3:5} {4:5} {5:5} {6:5}'.format(' Time', '    X', '    Y', '   Zf', '   Zl', '  GVx', '  GVy'))
        if t == -1:
            if len(S) == 3:
                for i in range(T):
                    print('{0:5d} {1:5d} {2:5d} {3:5d} {4:5d} {5:5d} {6:5d}'.format(int(i+1), int(configData[spm-1][1][i]), int(configData[spm-1][2][i]),
                          int(configData[spm-1][3][i]), int(configData[spm-1][4][i]), int(configData[spm-1][5][i]), int(configData[spm-1][6][i])))
            else:
                for i in range(T):
                    print('{0:5d} {1:5d} {2:5d} {3:5d} {4:5d} {5:5d} {6:5d}'.format(int(i+1), int(configData[spm-1][1]), int(configData[spm-1][2]),
                          int(configData[spm-1][3]), int(configData[spm-1][4]), int(configData[spm-1][5]), int(configData[spm-1][6])))
        else:
            print('{0:5d} {1:5d} {2:5d} {3:5d} {4:5d} {5:5d} {6:5d}'.format(int(t), int(configData[spm - 1][1][t-1]),
                   int(configData[spm - 1][2][t-1]), int(configData[spm - 1][3][t-1]), int(configData[spm - 1][4][t-1]),
                   int(configData[spm - 1][5][t-1]), int(configData[spm - 1][6][t-1])))
            if ret:
                return configData[spm-1][:][t-1]
        print('\n')

    if ret:
        return configData[spm-1][:][:]