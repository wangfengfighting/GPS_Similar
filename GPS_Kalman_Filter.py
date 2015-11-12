__author__ = 'WangFeng'
# coding: utf-8
'''
This use Kalman Filter to remove the gps noise points
'''
from pykalman import KalmanFilter
import scipy.signal as signal
import numpy as np
import math
from matplotlib import pylab as plt
import  random
import decimal
import copy
import simple_kalman
import  simple_mid_filter
import simple_mean_filter
from Find_stop_points import  multiple_cluster
from Find_stop_points.multiple_cluster import *
def Get_Prime_GpsData(filepath_name):
    Latitude,Longitude=np.loadtxt(filepath_name,dtype=float,delimiter=',',skiprows=1,usecols=(0,1),unpack=True)
    data=np.loadtxt(filepath_name,dtype=float,delimiter=',',skiprows=1,usecols=(0,1),unpack=False)
    drewgps(Latitude,Longitude)
    gpsdata=RS_Kalman(Latitude,Longitude,3,3)
    labels,centers=multiple_cluster.science_cluster(gpsdata,num=5,cutoff_distance=0.000087,experience=0.000045)
    print len(centers)
    labels1,centers1=multiple_cluster.science_cluster(data,num=10,cutoff_distance=0.000087,experience=0.000045)
    print len(centers1)
    #gpsdata=RS_Kalman(data,3,3)
    print gpsdata
    Lat=KalmanFilterGPS(Latitude)
    Long=KalmanFilterGPS(Longitude)
    #drewgps(Latitude,Long)
    t=[gpsdata[i][1] for i in range(len(gpsdata))]
    return Longitude,t

def Kalman(Z):
    n_iter = len(Z)
    sz = (n_iter,)
    Q = 1e-5
    xhat=np.zeros(sz)      # a posteri estimate of x
    P=np.zeros(sz)         # a posteri error estimate
    xhatminus=np.zeros(sz) # a priori estimate of x
    Pminus=np.zeros(sz)    # a priori error estimate
    K=np.zeros(sz)         # gain or blending factor
#    R = 0.1**2
#    R = numpy.std(numpy.array(Z)) * 1
    R = 1
#    print R

    xhat[0] = Z[0]
    P[0] = 0.5

    for k in range(1,n_iter):
        # time update
        xhatminus[k] = xhat[k-1]
        Pminus[k] = P[k-1]+Q

        # measurement update
        K[k] = Pminus[k]/( Pminus[k]+R )
        xhat[k] = xhatminus[k]+K[k]*(Z[k]-xhatminus[k])
        P[k] = (1-K[k])*Pminus[k]
    return xhat

def RS_Kalman(lat,lng,l_size=5 ,g_size=5):
    Lat=signal.medfilt(lat,l_size)
    Lng=signal.medfilt(lng,g_size)
    drewgps(Lat,Lng)
    Lat=KalmanByGroup(Lat)
    Lng=KalmanByGroup(Lng)
    drewgps(Lat,Lng)
    gps_data = [[Lat[i],Lng[i]] for i in range(len(Lat))]
    return gps_data

# def RS_Kalman(data,l_size=5 ,g_size=5):
#     Lat=signal.medfilt(lat,l_size)
#     Lng=signal.medfilt(lng,g_size)
#     drewgps(Lat,Lng)
#     Lat=KalmanByGroup(Lat)
#     Lng=KalmanByGroup(Lng)
#     drewgps(Lat,Lng)
#     gps_data = [[Lat[i],Lng[i]] for i in range(len(Lat))]
#     return gps_data

def calDistance(data):
    ind = np.array(data).argsort()
    left = data[ind[0]]
    right = data[ind[-1]]
    return abs(left - right)
def KalmanByGroup(dataGroup):
    i = 0
    data = []
    while True:
        for j in range(i + 1,len(dataGroup) - 1,1):
            if calDistance(dataGroup[i:j + 1]) > 0.0015:
                if j - i > 10:
                    data.extend(Kalman(dataGroup[i:j]))
                else:
                    data.extend(dataGroup[i:j])
                i = j
                break
            elif i != j and j == len(dataGroup) - 2:
                data.extend(Kalman(dataGroup[i:j]))
                i = j
        if i == len(dataGroup) - 2:
            data.extend(dataGroup[-2:])
            break
    return data

def KalmanFilterGPS(gpsData):
    kf = KalmanFilter(initial_state_mean=0.44, n_dim_obs=1)
    afteremGps=kf.filter(gpsData)[0]
    #print(afteremGps)
    return afteremGps
    #for i in range(0,len(afteremGps)):
        #print afteremGps[i]-gpsData[i]

def MediaFilter(gpsListprime,windows_size):
    gpsList=copy.deepcopy(gpsListprime)
    for index in range(windows_size,len(gpsList)-windows_size-1):
        tempmedia=[]
        tempmedia.extend(gpsList[index-windows_size:index+windows_size])
        #tempmedia.extend(gpsList[index:index+windows_size])
        #tempmedia.sort()
        #print(tempmedia)
        gpsList[index]=tempmedia[windows_size]
    return gpsList

def drawKalmanPic(PrimegpsData,Lat,Long):
    print('---')
    print len(Long)
    print len(Lat)
    #plt.subplot(211)
    plt.scatter(Long,Lat,c='r',marker='.')
    #plt.subplot(212)
    #plt.scatter(PrimegpsData[::][0],PrimegpsData[::][1],c='b',marker='o')
    plt.show()


def drewgps(weidu,jindu):

    plt.scatter(jindu,weidu,c='r',marker='.')
    #plt.savefig('.\\GPS_pic\\'+date+'.png',dpi=800)
    plt.show()
    plt.hold()


def drowerror(L1,L2):
    plt.subplot(211)
    plt.plot(L1-L2,c='r',marker='.')
    plt.subplot(212)
    plt.plot(L2,c='b',marker='.')
    plt.show()
if __name__=='__main__':
    #print(__doc__)
    la,laafter=Get_Prime_GpsData(".\\GPS_Get_PreProcesser\\10-04-2015\\locationGPS.txt")
    #KalmanFilterGPS()

    err=[]
    erraf=[]
    for i in range(1,len(la)):
        err.append(la[i]-la[i-1])
        #erraf.append(laafter[i]-laafter[i-1])
    for i in range(1,len(laafter)):

        erraf.append(laafter[i]-laafter[i-1])
    plt.subplot(211)
    plt.plot(err)
    plt.subplot(212)
    plt.plot(erraf)
    plt.show()

