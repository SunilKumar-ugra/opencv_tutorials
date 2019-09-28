import graphing as grph
import djikstra
import ast
from math import *
from rdp import rdp

def get_front():

    fil=open("front.txt","r")
    data=ast.literal_eval(fil.read())
    fil.close()
    return data[7][0][1]

def distance(pt1,pt2):
    dist = round(sqrt(((pt1[0]-pt2[0])*(pt1[0]-pt2[0]))+((pt1[1]-pt2[1])*(pt1[1]-pt2[1]))))
    return dist

def mapped_nearest(point,list_of_gridpoints):
    d=100000
    for gridp in list_of_gridpoints:

        dist=distance(point,gridp)
        if dist<d:
            d=dist
            nearest_grid=gridp
    return nearest_grid

def get_path(matches,obstacles,img,color):
    print matches
    list_of_obs=[]
    k=15
    o = obstacles
    for obs in o:
        for j in range(obs[2][1]-k,obs[2][1]+obs[2][3]+k):
            for i in range(obs[2][0]-k,obs[2][0]+obs[2][2]+k):
                list_of_obs.append((i,j))
    list_of_gridpoints,map_dict,rmapd=grph.grid(img,20)
    temp=[]
    for pnt in list_of_gridpoints:
        if pnt in list_of_obs:
            temp.append(pnt)
    list_of_obs=temp
    list_of_mapped_obs=[]
    for o in list_of_obs:
            list_of_mapped_obs.append(map_dict[o])



    path=[]
    listres=[]
    print map_dict,color,matches
    mapped_get_front = map_dict[mapped_nearest(get_front(),list_of_gridpoints)]
    mapped = map_dict[mapped_nearest(matches[color[0]][1],list_of_gridpoints)]
    path = rdp(djikstra.getPath(mapped_get_front,mapped,20,list_of_mapped_obs))
    path.append(mapped)
    listres.append(mapped)
    for i in range(1,len(color)):
        if type(matches[color[i]]) is not type(9):
            mapped2 =  map_dict[mapped_nearest(matches[color[i]][1],list_of_gridpoints)]
            path=path+ rdp(djikstra.getPath(mapped,mapped2,20,list_of_mapped_obs))
            path.append(mapped2)
            listres.append(mapped2)
            mapped=mapped2

    print path

    for j,point in zip(range(0,len(path)),path):
        path[j]=rmapd[(point[0],point[1])]

    print path
    for j,point in zip(range(0,len(listres)),listres):
        listres[j]=rmapd[(point[0],point[1])]
    return listres,path



