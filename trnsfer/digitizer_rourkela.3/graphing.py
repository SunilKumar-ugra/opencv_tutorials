import numpy as np
import cv2
import argparse
import imutils
import math


def map(value, in_min, in_max, out_min, out_max):
    return int((value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min)

def grid(img,k):

	x=img.shape[1]
	y=img.shape[0]

	list_of_gridpoints=[]
	map_dict={}
	rev_map_dict={}

	for j in range(x/(2*k),x,x/k):
		for i in range(x/(2*k),x,x/k):


			iN=map(i,x/(2*k),x,0,k)
			jN=map(j,x/(2*k),x,0,k)


			map_dict[(i,j)]=(jN,iN)
			rev_map_dict[(jN,iN)]=(i,j)

			list_of_gridpoints.append((i,j))

	return list_of_gridpoints,map_dict,rev_map_dict




