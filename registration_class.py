import os
import cv2
import numpy as np
from skimage.measure import regionprops
from skimage.feature import register_translation
from findTip import findTip as ft
import matplotlib.pyplot as plt

class registration:
    def __init__(self, reg_method, chan):
        self.rmstrain = 'None'
        self.method = reg_method
        self.channel = chan
        self.recentmove = []  # Holds the x and y values of the last movement calculated by the registration method
        self.initial_position = np.array([0, 0])  # Holds the reference point
        self.previous_image = []  # Holds the image from the previous time stamp
        self.GV = np.array([0, 0])
        self.dp = np.array([0, 0])
        self.cumshift = np.array([0, 0])

    # readtrainedrms reads all trained images in the trainedrms directory to be used as a reference for root mean square
    # calculations.
    def readtrainedrms(self):
        d = os.listdir('./mat/conf/')  # List files in this directory

        count = 1
        for file in d:  # Print out the list of trained images that exist
            print(str(count) + '. ' + file)
            count = count + 1

        opt = eval(input('\n Pick an image: '))

        try:
            imageName = d[opt - 1]
        except:
            print('Error, not an option')
            return

        return imageName


    def configimage(self, im):
        imshape = im.shape  # Get the dimensions of the image
        dimlength = len(imshape)  # Get the number of dimensions in the image (2 = 2D, 3 = 3D)

        if dimlength == 3:  # If the image is 3D, then create a max projection
            im = np.max(im, axis=2)
        elif dimlength == 2:  # If already 2D, don't worry about it
            im = im
        else:
            print('Error: Too many dimensions in the image')
            return
        return im

    def new_GV(self, conf, xy):
        gvOld = self.GV  # Save the old growth vector

        pixRes = conf.expConfig[3]  # Grab the pixel resolution from the config data

        if conf.simulation and conf.sett.SIMULATION_IMAGE_ADJUST:
            dp = xy - self.cumshift - self.initial_position
        else:
            dp = xy - self.initial_position  # Calculate the error vector from the estimated growth vector (This is different if running a simulation)

        dpMicrons = dp * pixRes  # Convert the error vector into terms of physical distance (microns)

        self.GV = dpMicrons + gvOld
        self.dp = dpMicrons


    # comr calculates the center of mass for the region above the threshold value of th. Returns the x and y location in a numpy array
    def comr(self, im1, th):
        im1config = self.configimage(im1)
        im1smooth = cv2.blur(im1config, (10, 10))  # Blur the images
        im1pos = (im1smooth > th).astype(int)  # Create a mask for all fluorescence above the threshold specified by the user
        im1props = regionprops(im1pos, im1smooth)  # Collect the properties concerning the images
        im1centroid = im1props[0].centroid
        return np.array([im1centroid[1], im1centroid[0]])


    # tmir calculates the point in which the template (specified in tmpname) best matches the image
    def tmir(self, im1, tmpname = 'av.mat'):
        return np.array([0, 0])  # Just return 0, 0 as the point until the method is programmed


    # pmir calculates the point matching image registration translation from one image to the next. Returns the tracking error
    def pmir(self, im1, im2):
        return np.array([0, 0])  # Just return 0, 0 as the registered movement until the method is programmed


    # pcir calculates the phase shift image registration translation from one image to the next. Returns the tracking error
    def pcir(self, im1, im2):
        im1config = self.configimage(im1)
        im2config = self.configimage(im2)
        shift, error, diffphase = register_translation(im2config, im1config)
        return np.array([0, 0])  # Just return 0, 0 as the registered movement until the method is programmed


    def register_movement(self, conf, I, t, spm, Im1 = 0):
        if self.method == 'PMIR':  # Point matching image registration
            print('Sorry that method has not been developed yet')
        elif self.method == 'COMR':
            poixy = self.comr(I, conf.expConfig[6])  # Calculate the center of mass of GFP
            if t == 0:
                self.initial_position = poixy
            else:
                self.new_GV(conf, poixy)  # Find the new growth vector given the position of the root tip
                print('Tracking error for SPM ' + str(spm + 1) + ' = ' + str(self.dp))
                print('New Growth Vector: ' + str(self.GV))
        elif self.method == 'TMIR':  # Template matching image registration
            # xy[spm, 0], xy[spm, 1] = ft(I[:, :, :, 1], False)  # Get the x and y position of the root tip
            print('Sorry that method has not been developed yet')
        elif self.method == 'PCIR':  # Phase Correlation Image
            if t == 0:
                self.dp = np.array([0, 0])
            else:
                self.dp = self.pcir(I, Im1)
            print('Sorry that method has not been developed yet')
        else:
            print('Something has gone wrong in selecting an image registration method')

