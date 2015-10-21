__author__ = 'Administrator'
# coding: utf-8
'''
This use Kalman Filter to remove the gps noise points
'''
from pykalman import KalmanFilter
import numpy as np
import math
from matplotlib import pylab as plt
import  random
import decimal
import copy
import simple_kalman
import  simple_mid_filter
import distance_mean_filter
import simple_mean_filter
def Get_Prime_GpsData(filepath_name):
    Latitude,Longitude=np.loadtxt(filepath_name,dtype=float,delimiter=',',skiprows=1,usecols=(0,1),unpack=True)
    #Longitude=[]
    #Latitude=[]
    #lala=map(lambda x: x * 100000, Latitude)
    #lolo=map(lambda x: x * 100000, Longitude)
    drewgps(Latitude,Longitude)
    drewgps(simple_mean_filter.mean_filter(Latitude,4),simple_mean_filter.mean_filter(Longitude,4))


    drewgps(simple_kalman.Kalman(Latitude),simple_kalman.Kalman(Longitude))


    #drewgps((Latitude),simple_kalman.Kalman(Longitude))
    #drewgps(simple_mid_filter.filter(Latitude,2),Longitude)
    g=distance_mean_filter.DistanceFilter(Latitude,Longitude,3)
    drewgps(g[0],g[1])
    print len(Latitude) ,len(g[0])
    drewgps(simple_mid_filter.filter(Latitude,5),simple_mid_filter.filter(Longitude,5))
    '''
    # chang str to float
    for i in range(0,len(La)):
        print( La[i])
        #lengthLa=len(La[i].split('.')[1])
        #lengthLo=len(Lo[i].split('.')[1])

        Latitude.append(   (decimal.Decimal(La[i]))    )
        Longitude.append( (decimal.Decimal(Lo[i]))    )
    print('-------------')
    #print( Latitude)
    '''
    '''
    gpsData=np.loadtxt(filepath_name,dtype=float,delimiter=',',skiprows=1,usecols=(0,1),unpack=False)
    #Lat=KalmanFilterGPS(Latitude)
    #Long=KalmanFilterGPS(Longitude)
    '''
    #Lat=MediaFilter(Latitude,4)
    #Long=MediaFilter(Longitude,4)
    Lat=KalmanFilterGPS(Latitude)
    Long=KalmanFilterGPS(Longitude)
    #drewgps(Latitude,Long)
    return Longitude,g[1]
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


def drowerror(L1,L2):
    plt.subplot(211)
    plt.plot(L1-L2,c='r',marker='.')
    plt.subplot(212)
    plt.plot(L2,c='b',marker='.')
    plt.show()
if __name__=='__main__':
    #print(__doc__)
    la,laafter=Get_Prime_GpsData(".\\GPS_Get_PreProcesser\\7-12-2015\\locationGPS.txt")
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

