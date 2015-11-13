# -*- coding: utf-8 -*-
"""
Created on Sat Jan 24 20:03:24 2015

@author: yangruosong
"""
from distance_mean_filter import GetDistance
import numpy
import pylab
import math
import json
import datetime
import scipy.signal as signal
import cluster
import readdata
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import baidumap
import CalPointDistance

def dwap_map(centers):
    m = Basemap(width=12000000,height=9000000,projection='lcc',
            resolution='c',lat_1=45.,lat_2=55,lat_0=50,lon_0=-107.)
# draw a boundary around the map, fill the background.
# this background will end up being the ocean color, since
# the continents will be drawn on top.
    m.drawmapboundary(fill_color='aqua')
# fill continents, set lake color same as ocean color.
    m.fillcontinents(color='coral',lake_color='aqua')
# draw parallels and meridians.
# label parallels on right and top
# meridians on bottom and left
    parallels = numpy.arange(0.,81,10.)
# labels = [left,right,top,bottom]
    m.drawparallels(parallels,labels=[False,True,True,False])
    meridians = numpy.arange(10.,351.,20.)
    m.drawmeridians(meridians,labels=[True,False,False,True])
# plot blue dot on Boulder, colorado and label it as such.
    for i in range(len(centers)):
        lon = centers[i][0]
        lat = centers[i][1] # Location of Boulder
# convert to map projection coords.
# Note that lon,lat can be scalars, lists or numpy arrays.
        xpt,ypt = m(lon,lat)
# convert back to lat/lon
        lonpt, latpt = m(xpt,ypt,inverse=True)
        m.plot(xpt,ypt,'bo')  # plot a blue dot there
# put some text next to the dot, offset a little bit
# (the offset is in map projection coordinates)
        plt.text(xpt+100000,ypt+100000,'Boulder (%5.1fW,%3.1fN)' % (lonpt,latpt))
    plt.show()
def get_file_gps(fname):
    gps_list = []
    date = []
    f = open(fname,'r')
    lines = f.readlines()
    lines = lines[6:]
    for line in lines:
        line = line[:len(line) - 1]
        data = line.split(',')
        time_date = data[5]
        time_date = time_date.split('-')
        time_time = data[6]
        time_time = time_time.split(':')
        current_time = datetime.datetime(int(time_date[0]),int(time_date[1]),int(time_date[2]),int(time_time[0]),int(time_time[1]),int(time_time[2]))
        gps_list.append([float(data[0]),float(data[1])])
        date.append(current_time)
    return gps_list,date


def smooth_data(gps_data,timestamp,accur):
    for i in range(1,len(gps_data) - 1,1):
        if (timestamp[i] - timestamp[i - 1]).seconds == (timestamp[i + 1] - timestamp[i]).seconds and accur[i] > 60:
            gps_data[i][0] = (gps_data[i + 1][0] + gps_data[i - 1][0]) / 2
            gps_data[i][1] = (gps_data[i + 1][1] + gps_data[i - 1][1]) / 2
    return gps_data
#((timestamp[i] - timestamp[i - 1]).seconds == (timestamp[i + 1] - timestamp[i]).seconds) and 
def smooth_data_2(gps_data):
    for i in range(1,len(gps_data) - 1,1):
        if (gps_data[i][0] > gps_data[i + 1][0] and gps_data[i][0] > gps_data[i - 1][0]) or (gps_data[i][0] < gps_data[i + 1][0] and gps_data[i][0] < gps_data[i - 1][0]) :
            gps_data[i][0] = (gps_data[i + 1][0] + gps_data[i - 1][0]) / 2
        if (gps_data[i][1] > gps_data[i + 1][1] and gps_data[i][1] > gps_data[i - 1][1]) or (gps_data[i][1] < gps_data[i + 1][1] and gps_data[i][1] < gps_data[i - 1][1]):
            gps_data[i][1] = (gps_data[i + 1][1] + gps_data[i - 1][1]) / 2
    return gps_data
    
def smooth_data_3(gps_data):
    for i in range(1,len(gps_data) - 1,1):
         gps_data[i][0] = (gps_data[i + 1][0] + gps_data[i - 1][0]) / 2
         gps_data[i][1] = (gps_data[i + 1][1] + gps_data[i - 1][1]) / 2
    return gps_data

def cal_hist(accur,show = False):
    pylab.hist(accur)
    if(show == True):
        pylab.xlabel('erroe')
        pylab.show()

def cal_fft(gps_data,show = False):
    gps_lat = [data[0] for data in gps_data]
    gps_lng = [data[1] for data in gps_data]
    gps_lat = numpy.fft.fft(gps_lat)
    gps_lng = numpy.fft.fft(gps_lng)
    print gps_lat
    print gps_lng
    if show == True:
        ax1 = pylab.subplot(211)
        ax2 = pylab.subplot(212)
        Z = [i for i in range(len(gps_data))]
        pylab.sca(ax1)
        pylab.plot(Z,gps_lat)
        pylab.sca(ax2)
        pylab.plot(Z,gps_lng)
        pylab.show()
    for i in range(len(gps_data)):
        gps_data[i][0] = gps_lat[i]
        gps_data[i][1] = gps_lng[i]
    return gps_data
def cal_hist_byself(accur,show = False):
    data = set(accur)
    data = sorted(list(data))
    freq = [accur.count(i) for i in data]
    print freq
    plt.figure(figsize = (100,100))
    plt.bar(data,freq,1,color='b',label='error')
    plt.xlabel('error')
    plt.ylabel('number')
    plt.legend()
def smooth_data_4(gps_data,K = 5,show = False):
    gps_lat = [data[0] for data in gps_data]
    gps_lng = [data[1] for data in gps_data]
    gps_lat = signal.medfilt(gps_lat,K)
    gps_lng = signal.medfilt(gps_lng,K)
    if show == True:
        ax1 = pylab.subplot(211)
        ax2 = pylab.subplot(212)
        Z = [i for i in range(len(gps_data))]
        pylab.sca(ax1)
        pylab.plot(Z,gps_lat)
        pylab.sca(ax2)
        pylab.plot(Z,gps_lng)
        pylab.show()
    for i in range(len(gps_data)):
        gps_data[i][0] = gps_lat[i]
        gps_data[i][1] = gps_lng[i]
    return gps_data

def get_data(filename):
    gps_data = []
    timestamp = []
    accur = []
    f = open(filename,'r')
    lines = f.readlines()
    for line in lines:
        line = line[0:len(line) - 1]
        line = json.loads(line)
        if "Location" in line:
            line = line['Location']
            time = line['time']
            accuracy = line['Accuracy']
            time = time.split()
            date = time[0]
            date = date.split('-')
            t = time[1]
            t= t.split(':')
            timestamp.append(datetime.datetime(int(date[2]),int(date[0]),int(date[1]),int(t[0]),int(t[1]),int(t[2])))
            gps_data.append([float(line['Latitude']),float(line['Longitude'])])
            accur.append(float(accuracy))
    return gps_data,timestamp,accur

def normal_data(gps_data,show = False):
    maxValue = numpy.max(gps_data,axis = 0)
    minValue = numpy.min(gps_data,axis = 0)
    gps_data = (gps_data - minValue) / (maxValue - minValue)
    if show == True:
        X = [data[0] for data in gps_data]
        Y = [data[1] for data in gps_data]
        pylab.plot(X,Y,'or')
        pylab.show()
    return gps_data

def display_data(gps_data,color,show = False):
    ch = ''
    if color == 1:
        ch = 'r'
    elif color == 2:
        ch = 'b'
    elif color == 3:
        ch = 'y'
    elif color == 4:
        ch = 'k'
    elif color == 5:
        ch = 'g'
    if show == True:
        X = [data[0] for data in gps_data]
        Y = [data[1] for data in gps_data]
        ax1 = pylab.subplot(211)
        ax2 = pylab.subplot(212)
        Z = [i for i in range(len(gps_data))]
        pylab.sca(ax1)
        pylab.plot(Z,X,ch)
        pylab.sca(ax2)
        pylab.plot(Z,Y,ch)
        pylab.show()

def distance_Gauss(X,Y,sigma = 4):
    c = numpy.dot(numpy.array(X) - numpy.array(Y),numpy.array(X) - numpy.array(Y))
    c = math.exp(-1 * c / (sigma ** 2 * 2))
    return 2 - 2 * c

def distance(X,Y):
    temp = X - Y
    return numpy.dot(temp,temp)

def density(gps_data,radius,show = False):
    Y = [0 for i in range(len(gps_data))]
    Z = [0 for i in range(len(gps_data))]
    radius1 = 0.00015
    for i in range(len(gps_data) - 1):
        for j in range(i + 1,len(gps_data),1):
            if(distance_Gauss(gps_data[i],gps_data[j]) < radius):
                Y[i] += 1
                Y[j] += 1
            if(distance(gps_data[i],gps_data[j]) < radius1):
                Z[i] += 1
                Z[j] += 1
    if show == True:
        X = [i + 1 for i in range(len(gps_data))]
        pylab.plot(X,Y,'r')
        pylab.plot(X,Z,'b')
        pylab.show()
    return Y

def save_gps_data(gps_data):
    f = open('5_21_KalmanByGroup_result.txt','w')
    for i in range(len(gps_data)):
        f.write(str(gps_data[i][0]))
        f.write('\t')
        f.write(str(gps_data[i][1]))
        f.write('\n')
    f.close()

def washLabels(labels):
    labels_contin = []
    cur = 1
    for i in range(1,len(labels),1):
        if labels[i] == labels[i - 1]:
            cur += 1
        else:
            labels_contin.append([cur,labels[i - 1]])
            cur = 1
    labels_contin.append([cur,labels[-1]])
    for i in range(1,len(labels_contin) - 1,1):
        if labels_contin[i - 1][1] == labels_contin[i + 1][1] and labels_contin[i][0] <= 10:
            labels_contin[i][1] = labels_contin[i - 1][1]
    i = 0
    while True:
        if labels_contin[i][1] == labels_contin[i + 1][1]:
            labels_contin[i + 1][0] += labels_contin[i][0]
            labels_contin[i][1] = -2
        i += 1
        if i == len(labels_contin) - 1:
            break
    labels_contin = [[d1,d2] for d1,d2 in labels_contin if d2 != -2]
    return labels_contin

def cal_entropy(labels_contin,timestamp):
    tem = 0
    pre = 0
    for i in range(len(labels_contin)):
        tem += labels_contin[i][0]
        labels_contin[i][0] = (timestamp[tem - 1] - timestamp[pre]).seconds
        pre = tem
    total = {}
    total_time = 0
    for i in range(len(labels_contin)):
        if labels_contin[i][1] not in total:
            total[labels_contin[i][1]] = labels_contin[i][0]
        else:
            total[labels_contin[i][1]] += labels_contin[i][0]
        total_time += labels_contin[i][0]
    entropy = 0.0
    for key in total:
        entropy -= float(total[key]) / float(total_time) * math.log(float(total[key]) / float(total_time),2)
    return entropy


def drawPicture():
    gps_collection = []
    gps_time = []
    gps_data,timestamp,accur = get_data('.\\ubiqlog\\log_5-21-2014.txt')
    gps_data = smooth_data_4(gps_data,False)
    gps_collection.append(gps_data)
    gps_time.append(timestamp)
    gps_data,timestamp,accur = get_data('.\\ubiqlog\\log_5-22-2014.txt')
    gps_data = smooth_data_4(gps_data,False)
    gps_collection.append(gps_data)
    gps_time.append(timestamp)
    gps_data,timestamp,accur = get_data('.\\ubiqlog\\log_5-23-2014.txt')
    gps_data = smooth_data_4(gps_data,False)
    gps_collection.append(gps_data)
    gps_time.append(timestamp)
    gps_data,timestamp,accur = get_data('.\\ubiqlog\\log_5-24-2014.txt')
    gps_data = smooth_data_4(gps_data,False)
    gps_collection.append(gps_data)
    gps_time.append(timestamp)
    gps_data,timestamp,accur = get_data('.\\ubiqlog\\log_5-25-2014.txt')
    gps_data = smooth_data_4(gps_data,False)
    gps_collection.append(gps_data)
    gps_time.append(timestamp)
    for i in range(len(gps_collection)):
        display_data(gps_collection[i],i + 1,True)

def calSpeed(gps_data,timestamp,acc,draw = False):
    speed = []
    gps_data = smooth_data_4(gps_data,False)
    for i in range(0,len(gps_data) - 1,1):
        p1 = CalPointDistance.Point()
        p1.lat = gps_data[i][0]
        p1.lng = gps_data[i][1]
        p2 = CalPointDistance.Point()
        p2.lat = gps_data[i + 1][0]
        p2.lng = gps_data[i + 1][1]
        dis = CalPointDistance.getDistance(p1,p2)
        speed.append(dis / (timestamp[i + 1] - timestamp[i]).seconds)
    acc = acc[1:]
    if draw == True:
        ind = [i for i in range(len(speed))]
        pylab.plot(ind,speed,'r')
        pylab.plot(ind,acc,'g')
        pylab.show()

'''
这是用计算 stay-point的位置信息的函数，输入是numpy格式的gpsdata，[ [x y]....]
'''
def getStayPoint(gps_data,timestamp,disthreshold=130,timethreshold=190):
    labels = []
    count = 0
    SP = []
    i = 0
    while i < len(gps_data)-1:
        for j in range(i + 1,len(gps_data),1):
            dis=GetDistance(gps_data[i][0],gps_data[i][1],gps_data[j][0],gps_data[j][1])
            if dis > disthreshold and (timestamp[j] - timestamp[i]).seconds > timethreshold:
                labels.extend([count for k in range(j - i)])
                count += 1
                point = numpy.array(gps_data[i:j])
                SP.append(numpy.average(point,axis = 0))
                i = j
                break
            elif j == len(gps_data) - 1:
                labels.extend([count for k in range(j - i)])
                point = numpy.array(gps_data[i:j + 1])
                SP.append(numpy.average(point,axis = 0))
                i = j + 1
                break
    return labels,SP

def init_rs_staypoint_time(labels,gps_point,timestamp,accur,StayPoint,labDIC,path_file):
    path_file=path_file.replace('location.txt','RC_stoppoint.txt')
    Fstop=open(path_file,'w+')
    for i in range(0,len(gps_point)):
        Fstop.write(str(gps_point[i][0]))
        Fstop.write(',')
        Fstop.write(str(gps_point[i][1]))
        Fstop.write(',')
        Fstop.write(str(accur[i]))
        Fstop.write(',')
        Fstop.write(str(timestamp[i]))
        Fstop.write(',')
        Fstop.write(str(labDIC[labels[i]]))
        if i !=len(gps_point)-1:
            Fstop.write('\n')


def mian():
    from Semantics_of_Trajectories import Calculate_semantic_of_point
    from stop_points import getfullfilepath
    full=getfullfilepath()
    for n in range(len(full)):
        path_file=full[n].replace('locationGPS.txt','location.txt')

        gps_data,timestamp,accur = get_data(path_file)

        # print len(accur)
        # print len(timestamp)

        labels,SP = getStayPoint(gps_data,timestamp,disthreshold=120,timethreshold=200)

        labels.append(labels[len(labels)-1])

        # print len(labels)
        # print len(SP)
        # print SP

        stoppointlabel=[]
        labDIC={}
        for  i  in range(len(SP)):
            value=Calculate_semantic_of_point.Match_semantics(SP[i],80)
            stoppointlabel.append(value)
            labDIC[i]=value
        init_rs_staypoint_time(labels,gps_data,timestamp,accur,SP,labDIC,path_file)




if __name__ == '__main__':
    mian()
