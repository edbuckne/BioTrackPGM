#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# """
# Created on Tue Jun 26 12:18:41 2018
#
# @author: crichar9
# """

import numpy as np
import skimage
from skimage import io, color, transform
import cv2
from scipy.io import loadmat
from fun import readCzi
import matplotlib.pyplot as plt


# This function loads the data found in the av.mat file which contains the data required to detect root tips. It returns
# the data as an array.
def load_av():
    y = loadmat('./mat/av.mat')
    av = y['av']
    return av


#  This function takes in the array that represents an image and converts it to a double 0-1.
def make_image_double(Ib):
    if Ib.dtype == 'uint16':  # Make the file a double
        Ib2 = Ib/(2**16)
    elif Ib.dtype == 'uint8':
        Ib2 = Ib/(2**8)
    else:
        Ib2 = Ib

    return Ib2


#  This function takes in the path to an image, loads it, and converts to a double if prompted. It returns the resulting
#  image as an array.
def load_image(I_path, makeDouble = True):
    Ib = io.imread(I_path)  # Load the image into memory
    if makeDouble:
        Ib = make_image_double(Ib)

    return Ib


def find_Z_Range(conf, I):
    # configDataMat = loadmat('./mat/config.mat')  # Load the experimental data to get the threshold value
    # configData = configDataMat['expArray']
    configData = conf.expConfig
    TH = configData[6]

    z1 = 0
    z2 = I.shape[2]

    blur = cv2.GaussianBlur(I, (11, 11), 0)
    Ibw = blur > TH

    for z in range(I.shape[2]):  # Find the first z stack to contain signal
        zSum = np.sum(Ibw[:, :, z])
        if zSum > 0:
            z1 = z  # Indexing format
            break

    for z in range(I.shape[2]):  # Find the las z stack to contain signal
        zind = I.shape[2]-1-z
        zSum = np.sum(Ibw[:, :, zind])
        if zSum > 0:
            z2 = zind  # Indexing format
            break

    if z1 > z2:
        print('WARNING: Calculation for Zf or Zl was incorrect')

    return z1, z2

def findTip(I, path = True):
    if path:
        Ib = load_image(I, True)  # Grab the image to evaluate
    else:
        Ib = make_image_double(I)
    av = load_av()  # Grab the av matrix
    
    for z in range(0,np.size(Ib, axis=0)): # blur and find gradient of each slice
        tempimg = cv2.GaussianBlur(Ib[z],(5,5),0)  # gaussian blur on slice
        sX = cv2.Scharr(tempimg, cv2.CV_64F,1, 0)  # horizontal gradient
        sY = cv2.Scharr(tempimg, cv2.CV_64F,0, 1)  # vertical gradient
        Ib[z] = cv2.addWeighted(sX, 0.5, sY, 0.5, 0)  # add two gradient pictures

    # Imax = np.amax(Ib, axis = 0); #create Max. Proj. image
    Imax = np.amax(Ib, axis=2)
    Imax = skimage.transform.resize(Imax, [480,480]); #resize MP image
    Imaxsmooth = Imax;
    # readCzi.view_image(Imaxsmooth)
        
    Sfilt = av.shape  # find dimensions of av file in avPath
    Sim = Imax.shape  # find dimensions of Imax resized img (480,480)

    L = (Sfilt[0]-1)/2; #subtract 1 from # rows in av, divide by 2 to create pad size
    L = int(L);
    Imaxpad = np.pad(Imaxsmooth, ((L,L),(L,L)), mode='constant',constant_values=0); #pad MP image with 0
    Ifilt = np.zeros(Sim); #create zeros matrix with dimensions of MP image
    
    for row in range(0,Sim[0]): #iterate across rows of MP image
        for col in range(0,Sim[1]): #iterate across columns
            Ismall = Imaxpad[row:(row+Sfilt[0]), col:(col+Sfilt[1])]; #crop a section of padded image
            
            isAV = np.mean(Ismall); #find mean of cropped img for normalization
            isStd = np.std(Ismall); #find std dev. of cropped image for normalization
            Ismall = (Ismall-isAV)/isStd; #takes diff. btwn cropped img values and mean, then divides by std dev.
            
            Ifilt[row,col] = abs(Ismall-av).sum(axis=0).sum(axis=0); #least difference squared of normalized cropped img & trained img
    
    
    Ifilt = Ifilt[L:Ifilt.shape[1]-L, L:Ifilt.shape[1]-L]; #crop out padded zone
    newS = Ifilt.shape; #store dim of image
    p = np.argmin(Ifilt); #returns flattened array index of min. value in Ifilt 
    [row, col] = np.unravel_index([p], newS); #returns row, col. index of p (flattened array index)
    
    x = (col+L)*4; #to adjust for inaccuracy of root tip coord. from padding
    y = (row+L)*4; 
    
    #plot x,y on image and display
# =============================================================================
#     implot = plt.imshow(Ib[int(np.size(I, axis=0)/2)]);
#     plt.scatter([x],[y], c='r', s=40);
#     plt.show()
# =============================================================================

    
    return x, y
            

def new_GV(conf, xy, t, spm):
    # io.savemat('./mat/tipData.mat', {'tipData':tipData})
    tipLocMat = loadmat(conf.path + '/tipData.mat')  # Load matlab file with nominal tip locations
    nomTip = tipLocMat['tipData']
    expDataMat = loadmat(conf.path + '/expData.mat')
    expData = expDataMat['expData']

    configData = conf.expConfig  # Load the experimental data to get the pixel resolution

    if t == 0:
        gvOld = expData[spm, 5:7]

    else:
        gvOld = expData[spm, 5:7, t]

    pixRes = configData[3]  # Grab the pixel resolution from the config data

    dp = xy[spm, :]-nomTip[spm, :]  # Calculate the error vector from the estimated growth vector
    dpMicrons = dp*pixRes  # Convert the error vector into terms of physical distance (microns)

    gvNew = dpMicrons + gvOld

    return gvNew, dpMicrons
