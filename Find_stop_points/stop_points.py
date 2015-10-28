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
import distance_mean_filter
import sys
sys.setrecursionlimit(10000)
StopPoint=[]
def getfullfilepath():
    getdir=GetDirName()
    Fulldirlist=[]
    parent_path = os.path.dirname(os.getcwd())
    dirlist=getdir.printPath(parent_path+"\\GPS_Get_PreProcesser")
    for dir in dirlist:
        Fulldirlist.append(parent_path+"\\GPS_Get_PreProcesser"+"\\"+dir+"\\"+'locationGPS.txt')
    #print(Fulldirlist)
    return Fulldirlist
def get_filtered_gps_stop_point(path):
    gpsdata=np.loadtxt(path, dtype={'names': ['Latitude', 'Longitude', 'time','Speed'] ,'formats': ['f18', 'f18', 'f18','f6']},
                       delimiter=',',
                       converters={3:lambda s:float(time.mktime((datetime.datetime.strptime(s,'%m-%d-%Y %H:%M:%S')).timetuple()))},
                       skiprows=1,usecols=(0,1,3,4))
    #gpsdata=np.loadtxt(path, dtype=str,delimiter=',',skiprows=1,usecols=(0,1,3,4))

    gps_stop_point=detecte_stoppoint(gpsdata,0)
    global StopPoint
    StopPoint=[]
    return gps_stop_point
    #调用 发现stoppoint函数，0 是指的开始位置的index

def As_stoppoint(x1,y1,t1,x2,y2,t2):
    avgdis=80
    avgtime=4.0
    if distance_mean_filter.GetDistance(x1,y1,x2,y2)<=avgdis:
        return True
    else:
        return False

def detecte_stoppoint(gpsdata,startindex):
    '''
    global StopPoint
    temp=[]
    if startindex==len(gpsdata):
        print('over----',startindex)
    else:

        if As_stoppoint(float(gpsdata[startindex][0]),float(gpsdata[startindex][1]),float(gpsdata[startindex][2]),
                    float(gpsdata[startindex][0]),float(gpsdata[startindex][1]),float(gpsdata[  startindex][2])):

            temp.append(gpsdata[startindex+1])
            #detecte_stoppoint(gpsdata,startindex+1)
        else:
            break
            #detecte_stoppoint(gpsdata,startindex+1)
    '''
    global StopPoint
    temp=[]
    temp_distance=[]
    index=0
    while index<len(gpsdata)-1:

        temp_distance.append( As_stoppoint(float(gpsdata[index][0]),float(gpsdata[index][1]),float(gpsdata[index][2]),
                    float(gpsdata[index+1][0]),float(gpsdata[index+1][1]),float(gpsdata[index+1][2])))
        index+=1
    #print (temp_distance)


    temp_start=0
    temp_end=0
    for i in range(len(temp_distance)):
        if temp_distance[i]==True:
            temp.append(gpsdata[i])
        else:
            if len(temp)!=0:
                StopPoint.append(temp)
                temp=[]
            else:
                temp=[]


    return StopPoint









    #print('最后都会执行的')




if __name__=='__main__':
    full=getfullfilepath()
    g=get_filtered_gps_stop_point(full[2])
    print('最后结果')
    #print(StopPoint)
    num=0

    print len(g)
    print(g[2])
    for i in g:
        for ii in i:
            num+=1

    print num,'num'


    for i in g:
        print i

