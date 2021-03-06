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
    #print(path),'-----------------------------------'
    gpsdata=np.loadtxt(path, dtype={'names': ['Latitude', 'Longitude', 'time','Speed'] ,'formats': ['f18', 'f18', 'f18','f6']},
                       delimiter=',',
                       converters={3:lambda s:float(time.mktime((datetime.datetime.strptime(s,'%m-%d-%Y %H:%M:%S')).timetuple()))},
                       skiprows=1,usecols=(0,1,3,4))
    #gpsdata=np.loadtxt(path, dtype=str,delimiter=',',skiprows=1,usecols=(0,1,3,4))
    print(len(gpsdata)),'premier number of point'
    gps_stop_point=detecte_stoppoint(gpsdata,0)
    global StopPoint
    StopPoint=[]
    print(len(gps_stop_point)),'stoppoint number of point'
    #print('---------------------------我是分割线----------------------------------')
    return gps_stop_point
    #调用 发现stoppoint函数，0 是指的开始位置的index

def As_stoppoint(x1,y1,t1,x2,y2,t2):
    avgdis=50.0
    avgtime=40.0
    if distance_mean_filter.GetDistance(x1,y1,x2,y2)<=avgdis and t2-t1>avgtime:
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
def writeasn(file,data):
    #print(file),'+++++++++++++++++++++++++'
    #if not data:
        #print('+++++++++++===========================')


    file=file.replace("locationGPS","stoppoint")
    stopfile=open(file,'w+')
    for bigstoppoint in data:
        length=len(bigstoppoint)
        lat=0.0
        long=0.0
        intime=bigstoppoint[0][2]
        outtime=bigstoppoint[length-1][2]
        for smallstoppoint in bigstoppoint:
            lat+=smallstoppoint[0]
            long+=smallstoppoint[1]
        avg_lat=lat/float(length)
        avg_long=long/float(length)

        #stopfile.writelines([avg_lat,avg_long,intime,outtime].__str__())
        stopfile.write(avg_lat.__str__())
        stopfile.write(',')
        stopfile.write(avg_long.__str__())
        stopfile.write(',')
        stopfile.write(intime.__str__())
        stopfile.write(',')
        stopfile.write(outtime.__str__())

        stopfile.write('\n')
    stopfile.close()







if __name__=='__main__':
    full=getfullfilepath()

    for path in full:
        point=get_filtered_gps_stop_point(path)
        writeasn(path,point)
    print('运行结束')


    #
    # print(full[2]),'--------------------'
    # g=get_filtered_gps_stop_point(full[2])
    # print((g))
    # print('最后结果')
    # print(StopPoint)
    # num=0
    #
    # print(g[2])
    # for i in g:
    #     for ii in i:
    #         num+=1
    #
    # print num,'num'
    # writeasn(full[2],g)



    # for i in g:
    #     print i

