import cv2
import numpy as np
import sys, os

def nothing(x):
	pass

def update(x):
	#return
	global canny, hough, w, rho, theta, threshold, minLineLength, maxLineGap, lines, img
	rho = rho_min + (float(cv2.getTrackbarPos('rho', 'main'))/100) * (rho_max - rho_min)
	theta = theta_min + (float(cv2.getTrackbarPos('theta', 'main'))/100) * (theta_max - theta_min)
	threshold = int(threshold_min + (float(cv2.getTrackbarPos('threshold', 'main'))/100) * (threshold_max - threshold_min))
	minLineLength = int(minLineLength_min + (float(cv2.getTrackbarPos('minLineLength', 'main'))/100) * (minLineLength_max - minLineLength_min)) 
	maxLineGap = int(maxLineGap_min + (float(cv2.getTrackbarPos('maxLineGap', 'main'))/100) * (maxLineGap_max - maxLineGap_min))  
	ret,hough = cv2.threshold(img,0,0,cv2.THRESH_BINARY)
	lines = cv2.HoughLinesP(canny, rho=rho, theta=theta, threshold = threshold, minLineLength = minLineLength, maxLineGap = maxLineGap)
	if lines is not None:
		for line in lines:
			cv2.line(hough, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (255, 255, 255), thickness)
	cv2.imshow('main', hough)
	#print("update: %s, %s" % (rho, theta))

def updateCanny(x):
	global canny, img, blurSize, threshold_canny
	threshold_canny = int(threshold_canny_min + (float(cv2.getTrackbarPos('threshold_canny', 'canny'))/100) * (threshold_canny_max - threshold_canny_min))
	blurSize = int(blurSize_min + (float(cv2.getTrackbarPos('blurSize', 'canny'))/100) * (blurSize_max - blurSize_min))
	if (blurSize % 2 == 0):
		blurSize += 1
	img_blur = cv2.GaussianBlur(img,(blurSize,blurSize),0)
	canny = cv2.Canny(img_blur, threshold_canny*.4, threshold_canny, True)
	kernel = np.ones((thickness_canny,thickness_canny), np.uint8)
	canny = cv2.dilate(canny, kernel, iterations=1)
	cv2.imshow('canny', canny)

thickness = 3
thickness_canny = 1
PI = 3.1415

blurSize = 7
threshold_canny = 100

blurSize_min = 1
blurSize_max = 21

threshold_canny_min = 10
threshold_canny_max = 300


rho_min = 1
rho_max = 10

theta_min = .1*PI/180
theta_max = 2*PI/180

threshold_min = 1
threshold_max = 300

minLineLength_min = 1
minLineLength_max = 40

maxLineGap_min = 1
maxLineGap_max = 40

rho = 2.26
theta = .00174
threshold = 40
maxLineGap = 11
minLineLength = 5
img = 0

canny = 0
hough = 0

demo = False

def process(image_in, lines_out, interactive):
	global rho, theta, threshold, maxLineGap, minLineLength, img, thickness, thickness_canny, PI, blurSize, blurSize_min, blurSize_max, canny, hough, lines
	
	if interactive:
		cv2.namedWindow('canny')
		cv2.namedWindow('main')

		cv2.createTrackbar('blurSize','canny',0,100,updateCanny)
		cv2.createTrackbar('threshold_canny','canny', 0,100,updateCanny)

		cv2.createTrackbar('rho','main',0,100,update)
		cv2.createTrackbar('theta','main', 0,100,update)
		cv2.createTrackbar('threshold','main', 0,100,update)
		cv2.createTrackbar('minLineLength','main', 0,100,update)
		cv2.createTrackbar('maxLineGap','main', 0,100,update)
	else:
		if os.path.exists('params.txt'):
			readParams()


	img = cv2.imread(image_in)
	if demo:
		cv2.imwrite("demo1.jpg", img)
	img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	if demo:
		cv2.imwrite("demo2.jpg", img)
	img = cv2.resize(img,None,fx=.25, fy=.25, interpolation = cv2.INTER_CUBIC)
	if demo:
		cv2.imwrite("demo3.jpg", img)

	img_blur = cv2.GaussianBlur(img,(blurSize,blurSize),0)
	if demo:
		cv2.imwrite("demo4.jpg", img)

	canny = cv2.Canny(img_blur, threshold_canny*.4, threshold_canny, True)
	if demo:
		cv2.imwrite("demo5.jpg", canny)

	kernel = np.ones((thickness_canny,thickness_canny), np.uint8)

	canny = cv2.dilate(canny, kernel, iterations=1)
	if demo:
		cv2.imwrite("demo6.jpg", canny)

	lines = cv2.HoughLinesP(canny, rho=rho, theta=theta, threshold = threshold, minLineLength = minLineLength, maxLineGap = maxLineGap)

	ret,hough = cv2.threshold(img,0,0,cv2.THRESH_BINARY)

	if lines is not None:
		for line in lines:
			cv2.line(hough, (line[0][0], line[0][1]), (line[0][2], line[0][3]), (255, 255, 255), thickness)
	if interactive:
		cv2.imshow('main', hough)
		cv2.imshow('canny', canny)
		cv2.waitKey(0)
		writeParams()
	if demo:
		cv2.imwrite("demo7.jpg", hough)

	f = open(lines_out, 'w')
	f.write("BlurSize: %s, CannyThreshold: %s, Rho: %s, Theta: %s, HoughThreshold: %s, MaxLineGap: %s, MinLineLength: %s\n" % (blurSize, threshold_canny, rho, theta, threshold, maxLineGap, minLineLength))
	if lines is not None:
		for line in lines:
			f.write("%s %s %s %s\n" % (line[0][0], line[0][1], line[0][2], line[0][3]))
	f.close()
	cv2.destroyAllWindows()

def writeParams():
	f = open('params.txt', 'w')
	f.write("%s\n" % blurSize)
	f.write("%s\n" % threshold_canny)
	f.write("%s\n" % rho)
	f.write("%s\n" % theta)
	f.write("%s\n" % threshold)
	f.write("%s\n" % maxLineGap)
	f.write("%s\n" % minLineLength)
	f.close()

def readParams():
	global blurSize, threshold_canny, rho, theta, threshold, maxLineGap, minLineLength
	f = open('params.txt', 'r')
	blurSize = int(f.readline())
	threshold_canny = int(f.readline())
	rho = float(f.readline())
	theta = float(f.readline())
	threshold = int(f.readline())
	maxLineGap = int(f.readline())
	minLineLength = int(f.readline())

if __name__ == "__main__":
	image_in = 'im1.JPG'
	lines_out = 'output.txt'
	interactive = True
	if len(sys.argv) > 1:
		image_in = sys.argv[1]
	if len(sys.argv) > 2:
		lines_out = sys.argv[2]
	if len(sys.argv) > 3:
		s = sys.argv[3].lower()
		if s == '0' or s == 'no' or s == 'false':
			interactive = False
	process(image_in, lines_out, interactive)


