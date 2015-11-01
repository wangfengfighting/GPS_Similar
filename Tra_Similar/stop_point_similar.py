# coding: utf-8
__author__ = 'WangFeng'
'''
时间：2015-10-30
作用： 读取之前处理好的stop-point 来计算DTW相似度，而不是用原始的数据，因为原始的数据很大，这样n^2的复杂度，就会很麻烦哦

'''
from dtw import dtw
import  numpy as np
from Find_stop_points.stop_points import *
def testdtw(tra1,tra2):

    dist, cost, path = dtw(tra1, tra2)
    #print 'Minimum distance found:', dist,math.log(dist,0.4),math.atan(dist)*2/math.pi
    return dist
def Get_Prime_GpsData(filepath_name1,filepath_name2):
    trajectory1=np.loadtxt(filepath_name1,dtype=float,delimiter=',',skiprows=1,usecols=(0,1),unpack=False)
    tra1=trajectory1.tolist()
    trajectory2=np.loadtxt(filepath_name2,dtype=float,delimiter=',',skiprows=1,usecols=(0,1),unpack=False)
    tra2=trajectory2.tolist()
    return tra1,tra2
def caculate_stoppoint_DTW(fullpath):
    for temppath_index in range(0,len(fullpath)):
        for tt in range(temppath_index+1,len(fullpath)-temppath_index):
            print fullpath[temppath_index],fullpath[tt]
            tra1,tra2=Get_Prime_GpsData(fullpath[temppath_index],fullpath[tt])
            re=testdtw(tra1,tra2)
            #print  re,temppath_index,tt
            writeans([temppath_index,tt,re])
            print('-----------------------我是分割线-----------------------------')

def writeans(out):
    output=open('network_stoppoint.txt','a+')
    output.write(str(out[0]))
    output.write(',')
    output.write(str(out[1]))
    output.write(',')
    output.write(str(out[2]))
    output.write('\n')
    output.close()

if __name__=='__main__':
    Fulldirlist=[]
    dirlist=getfullfilepath()
    for dir in dirlist:
        #print(dir)
        Fulldirlist.append(dir.replace("locationGPS","stoppoint"))
    print(Fulldirlist)


    '''
    fullpath=stop_points.getfullfilepath()

    tra1,tra2=Get_Prime_GpsData(".\\GPS_Get_PreProcesser\\10-21-2015\\locationGPS.txt",".\\GPS_Get_PreProcesser\\10-20-2015\\locationGPS.txt")
    testdtw(tra1,tra2)

    tra3,tra4=Get_Prime_GpsData(".\\GPS_Get_PreProcesser\\7-1-2015\\locationGPS.txt",".\\GPS_Get_PreProcesser\\10-20-2015\\locationGPS.txt")
    testdtw(tra3,tra4)
    '''
    #tra1,tra2=Get_Prime_GpsData(".\\GPS_Get_PreProcesser\\10-01-2015\\locationGPS.txt",".\\GPS_Get_PreProcesser\\10-02-2015\\locationGPS.txt")
    #print  testdtw(tra1,tra2)
    print('-----------------------我是分割线1-----------------------------')
    caculate_stoppoint_DTW(Fulldirlist)