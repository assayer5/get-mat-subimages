# -*- coding: utf-8 -*-
# parameters for 'getsubimages.py'

# path to directory of mat files 
matpath = r'C:\directory\imagestoprocess'

# path to directory where subimages will be saved (directory created if not yet existing)
savepath = r'C:\directory\subimagesoutput'

# image frames to process in each mat file
# format should be list of integers, i.e. [0, 5, 37, 61, 100]
frames = [i for i in range(10)]

# percentile of pixel values where cell objects are found
# cell pixels should be in highest percentiles, while background pixels in lowest percentiles
# sets binary threshold to isolate cell objects in image
pixelq = 97

# subimage size will be 2*halfheight x 2*halfwidth
halfheight = 64
halfwidth = 64
