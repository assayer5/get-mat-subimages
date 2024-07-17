# -*- coding: utf-8 -*-

import numpy as np
# import matplotlib.pyplot as plt
import cv2 as cv


# convert mat image to uint8 format with pixel values in range 0 to 255
# input: single mat image
# output: normalized image
def preprocessmat(matimage):
    # mat file vales have wide pixel value range, normalize image pixels to 0-255
    normimg = cv.normalize(matimage, None, alpha = 0, beta = 255, norm_type = cv.NORM_MINMAX, dtype = cv.CV_32F)
    # opencv prefers uint8
    outputimg = np.array(normimg, dtype=np.uint8)    
    return outputimg

# process grayscale image to binary image suitible for locating centroids of cells
# input: image - uint8 format, pixelquantile - percentile of pixels where cell objects found (to set threshold)
# output: binary image with 'eroded' cells, binary image after initial thresholding
def processimg(image, pixelquantile=97):
    # smooth out noise
    blur = cv.bilateralFilter(image, d=5, sigmaColor=None, sigmaSpace=8)
    # set threshold to isolate cells based on percentile of pixel values
    threshval = np.percentile(blur.ravel(), q=pixelquantile)
    # binary cutoff at threshold determined by Triangle algorithm
    thresh=threshval
    maxval=255
    ret, thresh1 = cv.threshold(blur, thresh, maxval, cv.THRESH_BINARY+cv.THRESH_TRIANGLE)
    # remove noise
    kernel = np.ones((3,3), np.uint8)
    opening = cv.morphologyEx(thresh1, cv.MORPH_OPEN, kernel, iterations=3)
    # furthur separate cells by eroding edges
    kernel = np.ones((2,2), dtype=np.uint8)
    eroded1 = cv.erode(opening, kernel, iterations=2)
    # remove gaps
    closing = cv.morphologyEx(eroded1, cv.MORPH_CLOSE, kernel, iterations=4)
    # furthur separate cells by eroding edges
    eroded = cv.erode(closing, kernel, iterations=4)

    return eroded, thresh1


# get coordinates of cell centroids from image
# inputs: binaryimg - image after thresholding, erodedimg - processed image (uint8 format)
# outputs: x, y: integer coordinates of cell centroids
def getcentroids(erodedimg, binaryimg=None):
    
    # findcontours alters image so use copy
    imgcopy = erodedimg.copy()
    # keep all contours RETR_TREE, only store necessary points CHAIN_APPROX_SIMPLE
    contours, hierarchy = cv.findContours(imgcopy, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
    
    # find centroids of contours
    cxs = []
    cys = []
    # cir = binaryimg.copy()
    for i, c in enumerate(contours):
        mom = cv.moments(c)
        
        # skip incomplete/missegmented/small contours
        if mom['m00'] <= 15:
            continue
    
        # calculate centroid coordinates from moments
        cx = int(mom['m10']/mom['m00'])
        cy = int(mom['m01']/mom['m00'])
        
        # store x and y coordinates of centroids
        cxs.append(cx)
        cys.append(cy)
    
        # # place circle at centroid coordinate (cx, cy), radius, 'color' 100, thickness filled
        # cv.circle(cir, (cx, cy), 5, 100, -1)
    
    #plt.imshow(cir)
    # return x and y coordinates
    return cxs, cys


# extract subimage at coordinates x, y from larger image
# subimage center given by x aand y coordinates of image
# output subimage size is 2*halfheight x 2*halfwidth
def extractsubimage(image, x, y, halfwidth=64, halfheight=64):
    
    imgshape = image.shape
    
    # if close to top left corner
    if y - halfheight < 0 and x - halfwidth < 0:
        subimg = image[:(y+halfheight), :(x+halfwidth)]
    # if close to top right corner
    elif y - halfheight < 0 and x + halfwidth > imgshape[1]:
        subimg = image[:(y+halfheight), (x-halfwidth):]
    # if close to bottom left corner
    elif y + halfheight > imgshape[0] and x - halfwidth < 0:
        subimg = image[(y-halfheight):, :(x+halfwidth)]
    # if close to bottom right corner
    elif y + halfheight > imgshape[0] and x + halfwidth > imgshape[1]:
        subimg = image[(y-halfheight):, (x-halfwidth):]
        
    # if close to left edge
    elif x - halfwidth < 0:
        subimg = image[(y-halfheight):(y+halfheight), :(x+halfwidth)]
    # if close to top edge
    elif y - halfheight < 0:
        subimg = image[:(y+halfheight), (x-halfwidth):(x+halfwidth)]
    # if close to right edge
    elif x + halfwidth > imgshape[1]:
        subimg = image[(y-halfheight):(y+halfheight), (x-halfwidth):]
    # if close to bottom edge
    elif y + halfheight > imgshape[0]:
        subimg = image[(y-halfheight):, (x-halfwidth):(x+halfwidth)]
        
    # if not near edges
    else:
        subimg = image[(y-halfheight):(y+halfheight), (x-halfwidth):(x+halfwidth)]
        
    # print(subimg.shape)
    # ensure subimage is size 2*halfwidth x 2*halfheight
    if subimg.shape == (2*halfheight, 2*halfwidth):
        return subimg
    
    else:
        # create blank image of proper size
        padded = np.zeros((2*halfheight, 2*halfwidth), dtype=np.uint8)
        # insert undersized subimage
        padded[:subimg.shape[0], :subimg.shape[1]] = subimg
        return padded
        
         
            
    # print(subimg.shape)
    #plt.imshow(subimg)
    #plt.show()
