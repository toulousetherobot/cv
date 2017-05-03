import cv2
import numpy as np
import math
import os, shutil

y_paper_max = 792
x_paper_max = 1224

y_paper_bottom = 250
y_paper_top = 700

x_paper_left = 0
x_paper_right = 0

xMax = 0
xMin = 0
yMax = 0
yMin = 0

writeFrames = False

def sort(lines):
	first = alignLeft(lines[0])
	lines[0] = first

	for index in range(len(lines)):
		
		if first[0] > alignLeft(lines[index])[0]:
			first = alignLeft(lines[index])
			lines[index] = first
	lines.remove(first)
	newLines = [first]

	while len(lines) > 0:
		point = p2(newLines[len(newLines) - 1])
		candidate = lines[0]
		minDistance = 0
		if distance(point, p1(candidate)) < distance(point, p2(candidate)):
			minDistance = distance(point, p1(candidate))
		else:
			minDistance = distance(point, p2(candidate))
			candidate = swap(candidate)
			lines[0] = candidate

		for index in range(len(lines)):
			line = lines[index]
			if distance(point, p1(line)) < minDistance:
				candidate = line
				minDistance = distance(point, p1(line))
			if distance(point, p2(line)) < minDistance:
				candidate = swap(line)
				minDistance = distance(point, p2(line))
				lines[index] = candidate

		lines.remove(candidate)
		newLines.append(candidate)
	return newLines

def connect(lines, joinDistance):
	newLines = []
	for index in range(len(lines)):
		line = lines[index]
		newLines.append(line)
		if index != len(lines) - 1:
			nextLine = lines[index + 1]
			if distance(p2(line), p1(nextLine)) <= joinDistance:
				newLines.append([line[2], line[3], nextLine[0], nextLine[1]])
	return newLines


def p1(line):
	return [line[0], line[1]]

def p2(line):
	return [line[2], line[3]]

def swap(line):
	return [line[2], line[3], line[0], line[1]]

def alignLeft(line):
	if line[2] < line[0]:
		return [line[2], line[3], line[0], line[1]]
	return line

def alignDown(line):
	if line[3] < line[1]:
		return [line[2], line[3], line[0], line[1]]
	return line

def distance(p1, p2):
	return math.sqrt((p1[0] - p2[0])*(p1[0] - p2[0]) + (p1[1] - p2[1])*(p1[1] - p2[1]))

def x_transform(x):
	ratio = 1.0-(float(x) / (xMax - xMin))
	return int(x_paper_right + ratio * (x_paper_left - x_paper_right))

def y_transform(y):
	ratio = 1.0-(float(y) / (yMax - yMin))
	return int(y_paper_bottom + ratio * (y_paper_top - y_paper_bottom))

def process(joinDistance, lines_in, coords_out, interactive, img_out):
	global x_paper_right, x_paper_left, xMax, xMin, yMax, yMin
	tossedFirst = False

	f = open(lines_in, 'r')
	lines = []
	for line in f:
		if not tossedFirst:
			tossedFirst = True
			continue
		splitline = line.split(" ")
		lines.append(map(int, splitline))
	f.close()
	lines = sort(lines)
	xMax = lines[0][0]
	xMin = xMax
	yMin = lines[0][1]
	yMax = yMin
	for line in lines:
		xMax = max(xMax, line[0], line[2])
		xMin = min(xMin, line[0], line[2])
		yMax = max(yMax, line[1], line[3])
		yMin = min(yMin, line[1], line[3])

	aspect_ratio = float(yMax - yMin) / float(xMax - xMin)
	x_paper_width = (y_paper_top - y_paper_bottom) / aspect_ratio
	x_paper_right = x_paper_max/2 - x_paper_width/2
	x_paper_left = x_paper_right + x_paper_width

	thickness = 2

	img = np.zeros((yMax - yMin,xMax - xMin), np.uint8)
	for line in lines:
		cv2.line(img, (line[0] - xMin, line[1] - yMin), (line[2] - xMin, line[3] - yMin), (255, 255, 255), thickness)

	if interactive:
		cv2.imshow("Result", img)
		cv2.waitKey(0)

	lines = sort(lines)
	lines = connect(lines, joinDistance)
	img = np.zeros((yMax - yMin,xMax - xMin), np.uint8)
	count = 0
	if os.path.isdir("./frames"):
		shutil.rmtree("./frames")
	os.mkdir("./frames")

	f = open(coords_out, 'w')
	
	for line in lines:
		cv2.line(img, (line[0] - xMin, line[1] - yMin), (line[2] - xMin, line[3] - yMin), (255, 255, 255), thickness)
		if interactive:
			cv2.imshow("Result", img)
			cv2.waitKey(0)
		if writeFrames:
			cv2.imwrite("./frames/frame%s.jpg" % str(count).zfill(4), img)
		count += 1
		f.write("1; %s, %s, %s, %s\n" % (x_transform(line[0] - xMin), y_transform(line[1] - yMin), x_transform(line[2] - xMin), y_transform(line[3] - yMin)))
	cv2.imwrite("./%s" % img_out, img)
	print("Plotted %s lines." % count)
	cv2.destroyAllWindows()

if __name__ == "__main__":

	lines_in = 'output.txt'
	coords_out = 'coords.txt'
	interactive = True
	joinDistance = 10
	if len(sys.argv) > 1:
		lines_in = sys.argv[1]
	if len(sys.argv) > 2:
		coords_out = sys.argv[2]
	if len(sys.argv) > 3:
		s = sys.argv[3].lower()
		if s == '0' or s == 'no' or s == 'false':
			interactive = False
	if len(sys.argv) > 4:
		joinDistance = int(sys.argv[3])

	process(joinDistance, lines_in, coords_out, interactive, "out.jpg")

