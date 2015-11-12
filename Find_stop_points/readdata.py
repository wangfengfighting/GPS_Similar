# -*- coding: utf-8 -*-
"""
Created on Thu Oct 23 14:51:06 2014

@author: yangruosong
"""

import json
import datetime
import sciencecluster
import numpy
import pylab
import sklearn.cluster
import matplotlib.pyplot as plt


def get_data(filename):
    gps_data = []
    timestamp = []
    f = open(filename,'r')
    lines = f.readlines()
    for line in lines:
        line = line[0:len(line) - 1]
        line = json.loads(line)
        if "Location" in line:
            line = line['Location']
            time = line['time']
            time = time.split()
            date = time[0]
            date = date.split('-')
            t = time[1]
            t= t.split(':')
            timestamp.append(datetime.datetime(int(date[2]),int(date[0]),int(date[1]),int(t[0]),int(t[1]),int(t[2])))
            gps_data.append([float(line['Latitude']),float(line['Longtitude'])])
    return gps_data,timestamp

def get_network_data(filename):
    gps_data = []
    timestamp = []
    f = open(filename,'r')
    lines = f.readlines()
    for line in lines:
        line = line[0:len(line) - 1]
        line = json.loads(line)
        if "Location" in line:
            line = line['Location']
            time = line['time']
            time = time.split()
            date = time[0]
            date = date.split('-')
            t = time[1]
            t= t.split(':')
            timestamp.append(datetime.datetime(int(date[2]),int(date[0]),int(date[1]),int(t[0]),int(t[1]),int(t[2])))
            gps_data.append([float(line['Latitude']),float(line['Longtitude'])])
    return gps_data,timestamp
def save_gps_data(gps_data,labels):
    f = open('5_21_result.txt','w')
    for i in range(len(gps_data)):
        if labels[i] != -1:
            f.write(str(gps_data[i][0]))
            f.write('\t')
            f.write(str(gps_data[i][1]))
            f.write('\n')
    f.close()
def draw_gps(gps_data):
    X = [data[0] for data in gps_data]
    Y = [data[1] for data in gps_data]
    pylab.plot(X,Y,'o')
    pylab.show()

def draw_gps_color(gps_data,labels):
    X = [data[0] for data in gps_data]
    Y = [data[1] for data in gps_data]
    for i in range(len(X)):
        if(labels[i] == 0):
            pylab.plot(X[i],Y[i],'or')
        elif(labels[i] == 1):
            pylab.plot(X[i],Y[i],'ob')
    pylab.show()


if __name__ == '__main__':
    gps_data,timestamp = get_network_data('.\\ubiqlog\\log_5-21-2014.txt')
    print len(gps_data)
    
    '''
    X = range(len(gps_data))
    Y = [data[2] for data in gps_data]
    Z = set(Y)
    M = [[z,Y.count(z)] for z in Z]
    M.sort()
    M.reverse()
    X = [data[0] for data in M]
    Y = [data[1] for data in M]
    '''
    #Y = [sum(Y[:i]) / float(len(gps_data)) for i in range(1,len(M) + 1,1)]
    '''
    plt.bar(X, Y, width=0.25)
    plt.show()
    '''
    #pylab.plot(X,Y,'o')
    #pylab.show()
    
    labels,centers = sciencecluster.science_cluster(numpy.array(gps_data),cutoff_distance = 0.0000001)
    save_gps_data(gps_data,labels)
    '''
    eps = 0.00001
    min_samples = 15
    metric = 'euclidean'
    core_samples, labels = sklearn.cluster.dbscan(numpy.array(gps_data), metric=metric, eps=eps,min_samples=min_samples)
    print labels[:100]
    '''
    '''
    X = [data[0] for data in gps_data]
    Y = [data[1] for data in gps_data]
    ax1 = pylab.subplot(211)
    ax2 = pylab.subplot(212)
    pylab.sca(ax1)
    for i in range(len(X)):
        if(labels[i] == 0):
            pylab.plot(X[i],Y[i],'or')
        elif(labels[i] == 1):
            pylab.plot(X[i],Y[i],'ob')
        elif(labels[i] == 2):
            pylab.plot(X[i],Y[i],'og')
        elif(labels[i] == 3):
            pylab.plot(X[i],Y[i],'oy')
    pylab.sca(ax2)
    pylab.plot(X,Y,'o')
    pylab.show()
    '''
    #draw_gps_color(gps_data,labels)
    print centers
    #print len(gps_data)