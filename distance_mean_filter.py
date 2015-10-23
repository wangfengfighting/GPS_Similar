__author__ = 'WanfFeng'
'''
canculate the two location point's distance, and use mean filter to remove the outline
'''
# coding: utf-8
import math
import copy
global EARTH_RADIUS
EARTH_RADIUS = 6371.004  #6378.137
def rad(d):
    return d*math.pi/180.0

def GetDistance( lat1, lng1,  lat2,  lng2):
    radLat1 = rad(lat1)
    radLat2 = rad(lat2)
    a = radLat1 - radLat2
    b = rad(lng1) - rad(lng2)

    s = 2 * math.asin(math.sqrt(math.pow(math.sin(a/2),2) +math.cos(radLat1)*math.cos(radLat2)*math.pow(math.sin(b/2),2)))
    s = s * EARTH_RADIUS
    s = (s * 1000)
    return s

def DistanceFilter(La,Lon,winsize):
    LA=[]
    LONG=[]
    for section in range(0,len(La)/winsize):
        templa=La[section*winsize:(section+1)*winsize]
        templong=Lon[section*winsize:(section+1)*winsize]
        #tempdistane=map(GetDistance(templa[i],templong[i],templa[i+1],templong[i+1])for i in range(0,winsize))
        tempdistane=[]
        for i in range(0,winsize-1):
            tempdistane.append(GetDistance(templa[i],templong[i],templa[i+1],templong[i+1]))
        temp_mean_distance=sum(tempdistane)/len(tempdistane)
        for i in range(0,len(tempdistane)-1):
            if tempdistane[i]>temp_mean_distance or tempdistane[i+1]>temp_mean_distance:
                #i+1 is outline point
                TEMPLA=((templa).tolist())
                TEMPLONG=(templong).tolist()
                TEMPLA.pop(i+1)
                TEMPLONG.pop(i+1)

        LA.extend(TEMPLA)
        LONG.extend(TEMPLONG)
    return LA,LONG

