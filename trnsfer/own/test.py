import numpy as np
import cv2
import argparse
import imutils
import urllib2
import sys
import ast
from Resource import resource
import graphing as gp
from math import *
import djkstra as djk

def draw_arrow(image, p, q, color, arrow_magnitude=9, thickness=2, line_type=8, shift=0):
	# adapted from http://mlikihazar.blogspot.com.au/2013/02/draw-arrow-opencv.html

	# draw arrow tail
	cv2.line(image, p, q, color, thickness, line_type, shift)
	# calc angle of the arrow
	angle = np.arctan2(p[1]-q[1], p[0]-q[0])
	# starting point of first line of arrow head
	p = (int(q[0] + arrow_magnitude * np.cos(angle + np.pi/4)),
	int(q[1] + arrow_magnitude * np.sin(angle + np.pi/4)))
	# draw first half of arrow head
	cv2.line(image, p, q, color, thickness, line_type, shift)
	# starting point of second line of arrow head
	p = (int(q[0] + arrow_magnitude * np.cos(angle - np.pi/4)),
	int(q[1] + arrow_magnitude * np.sin(angle - np.pi/4)))
	# draw second half of arrow head
	cv2.line(image, p, q, color, thickness, line_type, shift)

def find_distance(pathpoints):
	totaldist = 0
	length = len(pathpoints)
	if length == 2:
		dist = math.sqrt( (pathpoints[1][0] - pathpoints[0][0])**2 + (pathpoints[1][1] - pathpoints[0][1])**2 )
		return dist
	else:
		for i in range(0,length-1):
			firstpoint = pathpoints[i]
			secondpoint = pathpoints[i+1]
			dist = sqrt( (secondpoint[0] - firstpoint[0])**2 + (secondpoint[1] - firstpoint[1])**2 )
			totaldist = totaldist + dist
		totaldist=totaldist+((length-2)*5)
		return totaldist

def distance(pt1,pt2):
    dist = round(sqrt(((pt1[0]-pt2[0])*(pt1[0]-pt2[0]))+((pt1[1]-pt2[1])*(pt1[1]-pt2[1]))))
    return dist
