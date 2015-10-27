# coding: utf-8
__author__ = 'WangFeng'
'''
这个主要是用来做 不同坐标之间的转换的类，gps转googlegps，百度坐标等等
传送的是列表，返回的是列表
'''
import math
a = 6378245.0
ee = 0.00669342162296594323
pi = 3.14159265358979324
#  World Geodetic System ==> Mars Geodetic System
def gps2googlegps(location):
    trans_google_gps=[]
    for puregps in location:
        wgLat=puregps[0]
        wgLon=puregps[1]
        temp_gps=[]
        if (outOfChina(wgLat, wgLon)):
            temp_gps=[wgLat,wgLon]
            trans_google_gps.append(temp_gps)
        else:
            dLat = transformLat(wgLon - 105.0, wgLat - 35.0)
            dLon = transformLon(wgLon - 105.0, wgLat - 35.0)
            radLat = wgLat / 180.0 * pi
            magic = math.sin(radLat)
            magic = 1 - ee * magic * magic
            sqrtMagic = math.sqrt(magic)
            dLat = (dLat * 180.0) / ((a * (1 - ee)) / (magic * sqrtMagic) * pi)
            dLon = (dLon * 180.0) / (a / sqrtMagic * math.cos(radLat) * pi)
            mgLat = wgLat + dLat
            mgLon = wgLon + dLon
            temp_gps=[mgLat,mgLon]
            trans_google_gps.append(temp_gps)
    return trans_google_gps

def transformLat(x, y):

    ret = -100.0 + 2.0 * x + 3.0 * y + 0.2 * y * y + 0.1 * x * y + 0.2 * math.sqrt(math.fabs(x))
    ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(y * pi) + 40.0 * math.sin(y / 3.0 * pi)) * 2.0 / 3.0
    ret += (160.0 * math.sin(y / 12.0 * pi) + 320 * math.sin(y * pi / 30.0)) * 2.0 / 3.0
    return ret
def  transformLon( x,  y):

    ret = 300.0 + x + 2.0 * y + 0.1 * x * x + 0.1 * x * y + 0.1 * math.sqrt(math.fabs(x))
    ret += (20.0 * math.sin(6.0 * x * pi) + 20.0 * math.sin(2.0 * x * pi)) * 2.0 / 3.0
    ret += (20.0 * math.sin(x * pi) + 40.0 * math.sin(x / 3.0 * pi)) * 2.0 / 3.0
    ret += (150.0 * math.sin(x / 12.0 * pi) + 300.0 * math.sin(x / 30.0 * pi)) * 2.0 / 3.0
    return ret

def outOfChina( lat,  lon) :

    if (lon < 72.004 or lon > 137.8347):
        return True
    if (lat < 0.8293 or  lat > 55.8271):
        return True
    return False



if __name__=='__main__':
    b=[28.229943516870982,112.99379868255038]
    x=[]
    x.append(b)
    print(gps2googlegps(x))
