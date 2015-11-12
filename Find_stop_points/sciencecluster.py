# -*- coding: utf-8 -*-
"""
Created on Sun Oct 19 15:15:05 2014

@author: yangruosong
"""

import numpy as np
import math
import random
import pylab as pl
from operator import itemgetter
import sklearn.cluster

def distance_Poly(X,Y,p = 2):
    a = np.dot(X,X)
    a = math.pow(a + 1,p)
    b = np.dot(Y,Y)
    b = math.pow(b + 1,p)
    c = np.dot(X,Y)
    c = math.pow(c + 1,p)
    return a + b - 2 * c

def distance_Gauss(X,Y,sigma = 4):
    c = np.dot(np.array(X) - np.array(Y),np.array(X) - np.array(Y))
    c = math.exp(-1 * c / (sigma ** 2 * 2))
    return 2 - 2 * c

def distance_Sigmoid(X,Y,a,r):
    d = np.dot(X,X)
    d = math.tanh(a * d + r)
    b = np.dot(Y,Y)
    b = math.tanh(a * b + r)
    c = np.dot(X,Y)
    c = math.tanh(a * c + r)
    return a + b - 2 * c

def distance(X,Y):
    temp = X - Y
    return np.dot(temp,temp)
def get_shortest(X,Y):
    m = 1000000
    for i in range(Y.shape[0]):
        dis = distance(X,Y[i])
        if(dis < m):
            m = dis
    return m
def get_longest(X,Y):
    m = -1;
    for i in range(Y.shape[0]):
        dis = distance(X,Y[i])
        if(dis > m):
            m = dis
    return m
def get_shortest_index(X,Y):
    m = 1000000
    index = -1
    for i in range(Y.shape[0]):
        dis = distance(X,Y[i])
        if(dis < m):
            m = dis
            index = i
    return m,index

def guiyihua(X,maxValue,minValue):
    return (X - minValue) / (maxValue - minValue)

def science_cluster(X,num = 50,cutoff_distance = 0.1,experience = 0.0003,show = False):
    if not cutoff_distance > 0.0:
        raise ValueError("eps must be positive.")
    X = np.asarray(X)
    maxValue = np.max(X,axis = 0)
    minValue = np.min(X,axis = 0)
    Y = guiyihua(X,maxValue,minValue)
    n = X.shape[0]
    middle_result = [[0,0,0,i,-1] for i in range(n)]
    R = [0 for i in range(n)]
    for i in range(n - 1):
        for j in range(i + 1,n,1):
            if(distance(X[i],X[j]) < cutoff_distance):
                middle_result[i][0] += 1
                middle_result[j][0] += 1
                R[i] += 1
                R[j] += 1
    middle_result.sort()
    middle_result.reverse()
    for i in range(len(middle_result)):
        if i == 0:
            middle_result[i][1] = get_longest(X[middle_result[i][3]],X)
        else:
            Z = np.array([X[middle_result[j][3]] for j in range(i) if middle_result[j][0] >= num])
            middle_result[i][1],index = get_shortest_index(X[middle_result[i][3]],Z)
            middle_result[i][4] = middle_result[index][3]
    for i in range(len(middle_result)):
        middle_result[i][2] = middle_result[i][0] * middle_result[i][1]
#    middle_result.sort(key = itemgetter(1))
#    middle_result.reverse()
    middle_result.sort(key = itemgetter(2))
    middle_result.reverse()
#    '''
    X1 = [middle_result[i][2] for i in range(len(middle_result))]
    print len(X1)
    X2 = [middle_result[i][0] for i in range(len(middle_result))]
    print len(X2)
    pl.plot(X2,X1,'o')
    pl.show()
#    '''
#    centers = np.array([X[middle_result[i][3]] for i in range(len(middle_result)) if middle_result[i][1] > experience])
    centers = np.array([X[middle_result[i][3]] for i in range(len(middle_result)) if middle_result[i][2] > experience and (i == 0 or distance_Gauss(Y[middle_result[i][3]],Y[middle_result[i - 1][3]]) > cutoff_distance)])
    label = {}
    for i in range(len(centers)):
        label[middle_result[i][3]] = i
    labels = [-2 for i in range(X.shape[0])]
    while labels.count(-2) > 0:
        for i in range(X.shape[0]):
            if labels[middle_result[i][3]] > -2:
                continue
            if middle_result[i][0] < num:
                labels[middle_result[i][3]] = -1
            if middle_result[i][3] in label.keys() and labels[middle_result[i][3]] == -2:
                labels[middle_result[i][3]] = label[middle_result[i][3]]
            if labels[middle_result[i][4]] > -2:
                labels[middle_result[i][3]] = labels[middle_result[i][4]]
    '''
    for j in range(len(centers)):
        a = [X[i] for i in range(len(labels)) if labels[i] == j]
        a = np.array(a)
        centers[j] = a.mean(0)
    '''
    if show == True:
        V = [i + 1 for i in range(n)]
        for i in range(n):
            if labels[i] == -1:
                print R[i]
                pl.plot(V[i],R[i],'or')
            else:
                pl.plot(V[i],R[i],'og')
        pl.show()
    return labels,centers

'''
X = []
for i in range(100):
    r = random.random()
    X.append([1 * math.cos(2 * math.pi * r),1 * math.sin(2 * math.pi * r)])
    r = random.random()
    X.append([3 * math.cos(2 * math.pi * r),3 * math.sin(2 * math.pi * r)])
    r = random.random()
    X.append([6 * math.cos(2 * math.pi * r),6 * math.sin(2 * math.pi * r)])
X1 = [X[i][0] for i in range(len(X))]
X2 = [X[i][1] for i in range(len(X))]
pl.plot(X2,X1,'o')
pl.show()
labels,centers = science_cluster(np.array(X),cutoff_distance = 1)
#cluster_centers, labels, inertia = sklearn.cluster.k_means(np.array(X),n_clusters = 3,verbose=True)
for i in range(len(X)):
    if labels[i] == 0:
        pl.plot(X[i][0],X[i][1],'or')
    elif labels[i] == 1:
        pl.plot(X[i][0],X[i][1],'og')
    elif labels[i] == 2:
        pl.plot(X[i][0],X[i][1],'ob')
pl.show()
print labels[0:100]
print 'haha'
'''
if __name__ == '__main__':
    x = [124.73483,33.458967]
    y = [124.77145,33.458397]
    
#    print distance_Gauss(x,y,0.01)
#    '''
    data = []
    data.append(x)
    data.append(y)
    data = np.array(data)
    maxValue = np.max(data,axis = 0)
    minValue = np.min(data,axis = 0)
#    ma = np.max(data,axis = 0)
    data = guiyihua(data,maxValue,minValue)
    print data
    print distance_Gauss(data[0],data[1],0.1)