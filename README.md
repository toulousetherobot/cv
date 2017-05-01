# cv
Python OpenCV algorithm for line decompositoin

Usage:
python process.py [input image file] [output name] [interactive]

Example:
python process.py image1.jpg output1 no

This will generate output1.jpg and output1.crv, without interactively adjusting parameters (using those in params.txt).

Notes: 
Interactive mode is likely not supported on the Pi, so this will usually be "no"
The input must be specified with extension but only a name is needed for output, because the program generates both a .crv file to draw and a  .jpg visualizing the result
