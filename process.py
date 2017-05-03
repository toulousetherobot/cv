import os
import sys
import edge
import plot

if __name__ == "__main__":

	image_in = 'im1.JPG'
	lines_out = 'lines'
	intermediate = 'temp.txt'
	interactive = False
	params = 'params.txt'
	if len(sys.argv) > 1:
		image_in = sys.argv[1]
	if len(sys.argv) > 2:
		lines_out = sys.argv[2]
	if len(sys.argv) > 3:
		s = sys.argv[3].lower()
		if s == '1' or s == 'yes' or s == 'true' or s == 'interactive':
			interactive = True
	if len(sys.argv) > 4:
		params = sys.argv[4]
	params = '/home/pi/image-processing/cv/params.txt'
	lines_out_text = "%s" % lines_out
	lines_out_img = "%s.jpg" % lines_out
	edge.process(image_in, intermediate, interactive, params)
	joinDistance = 20
	plot.process(joinDistance, intermediate, lines_out_text, False, lines_out_img)

# Top right is origin
# (positive X, positive Y)
# Absolute X (0 -> 1224)
# Absolute Y (0 -> 792)
