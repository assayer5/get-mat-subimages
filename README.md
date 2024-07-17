## Project: MAT file Subimage Extraction
### Overview
A tool to cut sub-images from a larger MATLAB image (.mat file)


### Some Details
These scripts are a piece of a larger project using images generated in MATLAB (.mat files). In this project, a single .mat file consisted of a stack of images of plated cells. These scripts identify the cells in each frame and 'cut out' a sub-image of the cell from the larger image.

*parameters.py*
>
>This file allows the setting of parameters such as the image directory and the frames of the mat file to process.

*getsubimages.py*
>
>Running this file after setting parameters will 'cut out' the cell objects identified in the frames of the MAT file. Both version 7.2 and 7.3 mat files are compatible. These images will be saved as .jpg files in the directory set in *parameters.py* with the following file name format: {MATfilename}_f{frame#}_x{xcoordinate}_y{ycoordinate}_.jpg 

*func_subimgs.py*
>
>The functions in this file are used in *getsubimages.py*. They include functions for image normalization, image preprocessing to identify and separate cell objects, determining object coordinates, and extracting the sub-image at a given coordinate. Many preprocessing steps are hardcoded to fit my purpose and would need to be adapted to fit another purpose.


### Language
Python

### Packages Used
cv2, os, h5py, scipy, numpy

### Resources
[OpenCV Python docs](https://docs.opencv.org/4.x/d6/d00/tutorial_py_root.html)

