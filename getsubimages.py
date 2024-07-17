# -*- coding: utf-8 -*-

import os, sys
import numpy as np
import scipy.io
import cv2 as cv
import h5py
from tqdm import tqdm

import parameters as p
from func_subimgs import preprocessmat, processimg, getcentroids, extractsubimage


# path to mat files to be processed
imagefilepath = p.matpath
# path to save subimage files
savefilepath = p.savepath

if not os.path.exists(imagefilepath):
    print(f'Image file path does not exist: {imagefilepath}')
    sys.exit()

# display directories
print(f'Processing files from location:\n{imagefilepath}')
print(f'Save files to location:\n{savefilepath}')

# make directory if doesn't exist
if not os.path.exists(savefilepath):
    os.mkdir(savefilepath)

# get list of files to extract subimages from
filelist = os.listdir(imagefilepath) # list of all files in directory
# frames of file to process
frames = p.frames


# extract subimages from files
for f in filelist:
    
    # show file name to be processed
    print(f'\n{f}')
    # load mat file
    try:
        # for version 7.2 or below matfiles
        matfile = scipy.io.loadmat(os.path.join(imagefilepath, f))
        imgstack = matfile['D_stored']

    except NotImplementedError:
        # for version 7.3 matfiles
        matfile = h5py.File(os.path.join(imagefilepath, f), 'r')
        # reorder dimensions to match version 7.2 files
        imgstack = np.moveaxis(matfile['D_stored'], [0, 1, 2], [2, 1, 0])
        
    except:
        print(' Unable to properly read file. Moving to next file.')
        continue

    # get total number of frames in image stack
    totalframes = imgstack.shape[2]    
    
    for frame in tqdm(frames):
        
        # skip frame number if larger than number of frames in mat file 
        if frame > totalframes:
            print(f'\nframe {frame} beyond number of frames in file')
            continue
        
        # get frame
        img = imgstack[:, :, frame]
        
        # preprocess mat image to standard format
        img = preprocessmat(img)
        # process image for finding centroid coordinates
        processedimg, _ = processimg(img, pixelquantile=p.pixelq)
        # get centroid coordinates from frame
        x_coords, y_coords = getcentroids(processedimg)
        
        # extract subimages at coordinates
        # n = 0
        for x, y in zip(x_coords, y_coords):
            subimg = extractsubimage(img, x, y, halfwidth=p.halfwidth, halfheight=p.halfheight)
            # save image with filename 'filename_frame#xcoordycoord_.jpg'
            cv.imwrite(os.path.join(savefilepath, f'{f[:-4]}_f{frame}x{x}y{y}_.jpg'), subimg)
            
            # n += 1
            # if n >= 5:
            #     break
