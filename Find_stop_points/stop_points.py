# coding: utf-8
'''
时间2015/10/21
py作用，主要是通过一天的gps 路径，找出stay-point，返回的是一个列表
列表样式[[stop-point1],[2],....[n]]
stop-point=[gps1,gps2,gps3.....]

'''
__author__ = 'WangFeng'
import os
import numpy as np
from getDir import GetDirName
import datetime
import time
def getfullfilepath():
    getdir=GetDirName()

    Fulldirlist=[]
    parent_path = os.path.dirname(os.getcwd())
    dirlist=getdir.printPath(parent_path+"\\GPS_Get_PreProcesser")
    for dir in dirlist:
        Fulldirlist.append(parent_path+"\\GPS_Get_PreProcesser"+"\\"+dir+"\\"+'locationGPS.txt')
    print(Fulldirlist)
    return Fulldirlist
def get_filtered_gps(path):
    gpsdata=np.loadtxt(path, dtype={'names': ['Latitude', 'Longitude', 'time','Speed'] ,'formats': ['f18', 'f18', 'f18','f6']},
                       delimiter=',',
                       converters={3:lambda s:float(time.mktime((datetime.datetime.strptime(s,'%m-%d-%Y %H:%M:%S')).timetuple()))},
                       skiprows=1,usecols=(0,1,3,4))
    #gpsdata=np.loadtxt(path, dtype=[('f0',float),('f1',float),('s3',str),('f4',float)],delimiter=',',skiprows=1,usecols=(0,1,3,4))
    print(gpsdata)


if __name__=='__main__':
    full=getfullfilepath()
    g=get_filtered_gps(full[0])
    print(g)