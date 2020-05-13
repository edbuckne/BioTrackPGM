import xml.etree.ElementTree as ET
from czifile import CziFile as czi
import czifile
from matplotlib import pyplot as plt
import numpy

# Returns a select metadata in the form of a dictionary from the czi file path specified in path.
def read_metadata(path, print = False):
    cziIn = czi(path)
    md = cziIn.metadata

    root = ET.fromstring(md)

    bitCount = int(root[0][1][2][2].text)
    sizeX = int(root[0][1][2][3].text)
    sizeY = int(root[0][1][2][4].text)
    sizeZ = int(root[0][1][2][5].text)
    # sizeT = int(root[0][1][2][6].text)
    try:
        sizeC = int(root[0][1][2][7].text)
    except:
        sizeC = 0
    try:
        sizeV = int(root[0][1][2][8].text)
    except:
        sizeV = 0

    meta = {'bitCount':bitCount, 'sizeX':sizeX, 'sizeY':sizeY, 'sizeZ':sizeZ, 'sizeC':sizeC, 'sizeV':sizeV}

    if print:
        print('Image Width: ' + str(sizeX))
        print('Image Height: ' + str(sizeY))
        print('Image Depth: ' + str(sizeZ))
        print('Cameras Used: ' + str(sizeC))
        print('Views Used: ' + str(sizeV))

    return meta


# Simply plots an image using the matplotlib library
def view_image(newIm):
    plt.matshow(newIm)
    plt.show()


# Returns the 3 dimensional image data obtained from the czi file pointed to by path
def czi_to_array(path, cm, v = 1, imN = 2):
    md = read_metadata(path)

    if cm == 0:  # If the camera number specified is 0, get both images
        newIm = numpy.empty((md['sizeY'], md['sizeX'], md['sizeZ'], imN), numpy.uint16)
        cziIn = czifile.imread(path)
        for ccm in range(imN):
            for z in range(md['sizeZ']):
                newIm[:, :, z, ccm] = numpy.reshape(cziIn[v - 1, 0, 0, 0, 0, ccm, 0, z, :, :, :],(md['sizeY'], md['sizeX']))
    else:
        newIm = numpy.empty((md['sizeY'], md['sizeX'], md['sizeZ']), numpy.uint16)
        cziIn = czifile.imread(path)
        for z in range(md['sizeZ']):
            newIm[:, :, z] = numpy.reshape(cziIn[v - 1, 0, 0, 0, 0, cm - 1, 0, z, :, :, :], (md['sizeY'], md['sizeX']))

    return newIm


# I = czi_to_array('../data/CYCB11_HEATSHOCK_Fe+-_01_G3(1).czi', 2)
# print(I.shape)
# view_image(I[:, :, 40])
