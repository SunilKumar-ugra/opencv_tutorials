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
import djikstra as djk


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

def get_resources():
	fo = open("resources.txt","r")
	data=fo.read()
	x=ast.literal_eval(data)
	list_of_obj_res=[]
	for i in x:
		list_of_shit=i.split(',')
		elem=resource()
		elem.shape=list_of_shit[0]
		elem.real_point = (int(list_of_shit[1]),int(list_of_shit[2]))
		list_of_obj_res.append(elem)

	list_of_gridpoints,mapd,rmapd = gp.grid(cv2.imread("cropped.png"),9)
	for res in list_of_obj_res:
		d=10000
		for gridp in list_of_gridpoints:
			dist=distance(res.real_point,gridp)
			if dist<d:
				d=dist
				res.nearest_grid=gridp
	return list_of_obj_res


def get_obstacles():
	fo = open("obstacles.txt","r")
	data=fo.read()
	x=ast.literal_eval(data)
	list_of_obj_obs=[]
	for i in x:
		list_of_shit=i.split(',')
		elem=[int(list_of_shit[0]),int(list_of_shit[1]),int(list_of_shit[2]),int(list_of_shit[3])]
		list_of_obj_obs.append(elem)
	fo.close()

	return list_of_obj_obs

def get_start():
	fo = open("start.txt","r")
	data=fo.read().split(',')
	list_of_gridpoints,mapd,rmapd = gp.grid(cv2.imread("cropped.png"),9)
	d=10000
	dat=resource()
	dat.shape="start"
	dat.real_point=(int(data[0]),int(data[1]))
	for gridp in list_of_gridpoints:
		dist=distance(dat.real_point,gridp)
		if dist<d:
			d=dist
			dat.nearest_grid=gridp
	fo.close()

	return dat

def get_stop():
	fo = open("stop.txt","r")
	data=fo.read().split(',')
	list_of_gridpoints,mapd,rmapd = gp.grid(cv2.imread("cropped.png"),9)
	d=10000
	dat=resource()
	dat.shape="stop"
	dat.real_point=(int(data[0]),int(data[1]))
	for gridp in list_of_gridpoints:
		dist=distance(dat.real_point,gridp)
		if dist<d:
			d=dist
			dat.nearest_grid=gridp
	fo.close()

	return dat


def test():

	img =cv2.imread("cropped.png")
	list_of_gridpoints,mapd,rmapd = gp.grid(img,9)
	list_of_obs=[]

	k=5

	o = get_obstacles()
	for obs in o:
		for j in range(obs[1]-k,obs[3]+k):
			for i in range(obs[0]-(k),obs[2]+(k)):
				cv2.circle(img,(i,j),1,(255,120,255),-1)
				list_of_obs.append((i,j))




	i = get_resources()

	for res in i:
		cv2.circle(img,res.real_point,5,(0,110,255),-1)
		cv2.circle(img,res.nearest_grid,5,(0,255,0),-1)
	temp=[]
	for pnt in list_of_gridpoints:
		if pnt in list_of_obs:
			cv2.circle(img,pnt,5,(70,150,25),-1)
			temp.append(pnt)
		else:
			cv2.circle(img,pnt,5,(0,255,255),-1)

	list_of_obs=temp


	start=get_start()
	stop =get_stop()

	cv2.circle(img,start.nearest_grid,5,(0,255,0),-1)
	cv2.circle(img,stop.nearest_grid,5,(0,0,255),-1)

	list_of_obs.append(stop.nearest_grid)
	list_of_obs.append(start.nearest_grid)

	for q,point in zip(range(0,len(list_of_obs)),list_of_obs):
		list_of_obs[q]=mapd[point]



	#stage 1
	#here first take bot center and start , i have started with start center for demo
	d=10000
	for dat in i:
		dist=distance(dat.nearest_grid,start.nearest_grid)
		if dist<d:
			flag=dat
			d=dist


	path=[]
	cv2.line(img,start.real_point,flag.real_point,(255,255,0),2)

	path.append(flag.real_point)

	i.remove(flag)



	#STAGE 2 PATH TO ALL NODES


	while len(i)>0:
		d=1000000
		for res in i:
			if flag.shape== "triangle" and res.shape == "square":
				#djikstra get path points\
				path_points = djk.getPath(mapd[flag.nearest_grid],mapd[res.nearest_grid],9,list_of_obs)

				for j,point in zip(range(0,len(path_points)),path_points):
					path_points[j]=rmapd[point]

				dist = find_distance(path_points)
				if dist<d:
					nxt = res
					d=dist
					temp_path=path_points
			elif res.shape== "triangle" and flag.shape == "square":
				#djikstra get path points\
				path_points = djk.getPath(mapd[flag.nearest_grid],mapd[res.nearest_grid],9,list_of_obs)
				for j,point in zip(range(0,len(path_points)),path_points):
					path_points[j]=rmapd[point]

				dist = find_distance(path_points)
				if dist<d:
					nxt = res
					d=dist
					temp_path=path_points

		for t in range(1,len(temp_path)-1):
			path.append(temp_path[t])

		path.append(nxt.real_point)
		flag=nxt
		i.remove(flag)


	# STAGE 3 MODAFOKA
	path_points = djk.getPath(mapd[flag.nearest_grid],mapd[stop.nearest_grid],9,list_of_obs)
	for j,point in zip(range(0,len(path_points)),path_points):
		path_points[j]=rmapd[point]


	for t in range(1,len(path_points)):
		path.append(path_points[t])


	for i,point in zip(range(0,len(path)-1),path):
		draw_arrow(img,point,path[i+1],(255,255,0),)

	cv2.imshow("sd",img)
	cv2.waitKey(0)

def getThePath():
	img =cv2.imread("cropped.png")
	list_of_gridpoints,mapd,rmapd = gp.grid(img,9)
	list_of_obs=[]

	k=5

	o = get_obstacles()
	for obs in o:
		for j in range(obs[1]-k,obs[3]+k):
			for i in range(obs[0]-(k),obs[2]+(k)):

				list_of_obs.append((i,j))




	i = get_resources()

	temp=[]
	for pnt in list_of_gridpoints:
		if pnt in list_of_obs:
			cv2.circle(img,pnt,5,(70,150,25),-1)
			temp.append(pnt)
		else:
			cv2.circle(img,pnt,5,(0,255,255),-1)

	list_of_obs=temp


	start=get_start()
	stop =get_stop()


	list_of_obs.append(stop.nearest_grid)
	list_of_obs.append(start.nearest_grid)

	for q,point in zip(range(0,len(list_of_obs)),list_of_obs):
		list_of_obs[q]=mapd[point]



	#stage 1
	#here first take bot center and start , i have started with start center for demo
	d=10000
	for dat in i:
		dist=distance(dat.nearest_grid,start.nearest_grid)
		if dist<d:
			flag=dat
			d=dist


	path=[]


	path.append(flag.real_point)

	i.remove(flag)



	#STAGE 2 PATH TO ALL NODES


	while len(i)>0:
		d=1000000
		for res in i:
			if flag.shape== "triangle" and res.shape == "square":
				#djikstra get path points\
				path_points = djk.getPath(mapd[flag.nearest_grid],mapd[res.nearest_grid],9,list_of_obs)

				for j,point in zip(range(0,len(path_points)),path_points):
					path_points[j]=rmapd[point]

				dist = find_distance(path_points)
				if dist<d:
					nxt = res
					d=dist
					temp_path=path_points
			elif res.shape== "triangle" and flag.shape == "square":
				#djikstra get path points\
				path_points = djk.getPath(mapd[flag.nearest_grid],mapd[res.nearest_grid],9,list_of_obs)
				for j,point in zip(range(0,len(path_points)),path_points):
					path_points[j]=rmapd[point]

				dist = find_distance(path_points)
				if dist<d:
					nxt = res
					d=dist
					temp_path=path_points

		for t in range(1,len(temp_path)-1):
			path.append(temp_path[t])

		path.append(nxt.real_point)
		flag=nxt
		i.remove(flag)


	# STAGE 3 MODAFOKA
	path_points = djk.getPath(mapd[flag.nearest_grid],mapd[stop.nearest_grid],9,list_of_obs)
	for j,point in zip(range(0,len(path_points)),path_points):
		path_points[j]=rmapd[point]


	for t in range(1,len(path_points)):
		path.append(path_points[t])

	print path
	return path
test()
