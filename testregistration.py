from skimage import io
import numpy as np
from registration_class import registration
import cv2

def reconfigim(im):
    imageshape = im.shape
    newim = np.empty((imageshape[1], imageshape[2], imageshape[0]))

    for i in range(imageshape[0]):
        newim[:, :, i] = im[i]

    return newim

reg = registration(2)  # Center of mass registration

im1 = reconfigim(io.imread('data/11.tif'))
im2 = reconfigim(io.imread('data/15.tif'))

num_rows, num_cols = im1.shape[:2]
manual_shift = [200, 300]
translation_matrix = np.float32([[1, 0, manual_shift[0]], [0, 1, manual_shift[1]]])
im2 = cv2.warpAffine(im1, translation_matrix, (num_cols, num_rows))

print(reg.comr(im1, im2, 260))