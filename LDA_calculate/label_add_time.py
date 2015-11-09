# coding: utf-8
__author__ = 'WangFeng'
'''
这个文件要做的主要是 找到在一个label停留的时间，开始时间，结束时间等
'''
from getDir import GetDirName
import os
import numpy as np
import time
import datetime
def GetSemanticGPSpath():
    getdir=GetDirName()
    Fulldirlist=[]
    parent_path = os.path.dirname(os.getcwd())
    dirlist=getdir.printPath(parent_path+"\\GPS_Get_PreProcesser")
    for dir in dirlist:
        Fulldirlist.append(parent_path+"\\GPS_Get_PreProcesser"+"\\"+dir+"\\"+'semanticGPS.txt')  #semanticGPS.txt是处理后的gps 加时间， 加label的文件信息
    return Fulldirlist

def Add_timestamp(path):
    tempdata=np.loadtxt(path, dtype={'names': ['Latitude', 'Longitude', 'time','label'] ,'formats': ['f18', 'f18', 'f18','S16']},
                       delimiter=',',
                       converters={3:lambda s:float(time.mktime((datetime.datetime.strptime(s,'%m-%d-%Y %H:%M:%S')).timetuple()))},
                       usecols=(0,1,3,5))
    print tempdata
    

if __name__=='__main__':
    for i in GetSemanticGPSpath():
        Add_timestamp(i)
        break