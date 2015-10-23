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
StopPoint=[]
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
    #gpsdata=np.loadtxt(path, dtype=str,delimiter=',',skiprows=1,usecols=(0,1,3,4))
    print(len(gpsdata))
    detecte_stoppoint(gpsdata,0)

def detecte_stoppoint(gpsdata,startindex):
    avgdis=80
    avgtime=20
    tempstoppoint=[]

    for index in range(startindex,len(gpsdata)-1):
        #print distance_mean_filter.GetDistance(gpsdata[index][0],gpsdata[index][1],gpsdata[index+1][0],gpsdata[index+1][1]),'-------'

        if distance_mean_filter.GetDistance(gpsdata[index][0],gpsdata[index][1],gpsdata[index+1][0],gpsdata[index+1][1])<avgdis:
            if  gpsdata[index+1][2]-gpsdata[index][2]>avgtime:
                tempstoppoint.append(list(gpsdata[index]))
                #print(index)
                StopPoint.append(tempstoppoint)
            else:
                detecte_stoppoint(gpsdata,index+1)
                break
        else:
            detecte_stoppoint(gpsdata,index+1)
            break
        #break

    #print('最后都会执行的')




if __name__=='__main__':
    full=getfullfilepath()
    get_filtered_gps(full[2])
    print('最后结果')
    print(StopPoint)
    num=0
    print len(StopPoint)
    for i in StopPoint:
        for ii in i:
            num=num+1

    print num,'num'
