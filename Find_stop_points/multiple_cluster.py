# -*- coding: utf-8 -*-
"""
Created on Wed Apr 15 15:34:04 2015

@author: yangruosong
"""

import numpy as np
import math
import pylab
from operator import itemgetter

'''.....................................science cluster................................................
@cite [2014] Clustering by fast search and find of density peaks
'''
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

def science_cluster(X,num = 50,cutoff_distance = 0.00005,experience = 0.00031,show = False):
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
    if show == True:
        X1 = [middle_result[i][2] for i in range(len(middle_result))]
        print len(X1)
        X2 = [middle_result[i][0] for i in range(len(middle_result))]
        print len(X2)
        pylab.plot(X2,X1,'o')
        pylab.show()

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
                pylab.plot(V[i],R[i],'or')
            else:
                pylab.plot(V[i],R[i],'og')
        pylab.show()
    '''
    return labels,centers
'''...............................................DJ-cluster....................................................
@cite [2007] Discovering Personally Meaningful Places An Interactive Clustering Approach
'''

def DJ_Cluster(data,radius,density):
    point_density = {}
    centers = []
    for i in range(len(data) - 1):
        sym = 0
        for j in range(i + 1,len(data),1):
            if sum(np.array((data[i]) - np.array(data[j])) ** 2) < radius:
                if i not in point_density:
                    point_density[i] = set()
                point_density[i].add(j)
                if j not in point_density:
                    point_density[j] = set()
                point_density[j].add(i)
                sym = 1
        if sym == 0:
            point_density[i] = set()
    m = 0
    for i in range(len(data)):
        sbo = 0
        if len(point_density[i]) >= density:
            if len(centers) == 0:
                centers.append(i)
            else:
                for j in range(len(centers)):
                    if len(point_density[i] & point_density[centers[j]]) > 0:
                        sbo = 1
                        point_density[centers[j]] |= point_density[i]
                        point_density[centers[j]].add(i)
#                        print centers[j],i
                        m += 1
                        #print point_density[i] & point_density[centers[j]]
                        break;
                if sbo == 0:
                    centers.append(i)
        else:
            continue
    '''
    pylab.plot([data[k][0] for k in point_density[centers[4]]],[data[k][1] for k in point_density[centers[4]]],'oy')
    pylab.plot([data[k][0] for k in point_density[centers[5]]],[data[k][1] for k in point_density[centers[5]]],'ob')
    print len(point_density[centers[4]]);
    print len(point_density[centers[4]]);
    pylab.show()
    return
    '''
    syp = [0 for i in range(len(centers))]
    for i in range(len(centers) - 1):
        if syp[i] == 1:
            continue
        for j in range(i + 1,len(centers),1):
            if syp[j] == 1:
                continue
            if(len(point_density[centers[i]] & point_density[centers[j]])) > 0:
                print i,j
                point_density[centers[i]] |= point_density[centers[j]]
                point_density[centers[i]].add(centers[j])
                syp[j] = 1
                flag = 1
    center = []
    for k  in range(len(centers)):
        if syp[k] == 0:
            center.append(centers[k])
    centers = center
    for i in range(len(data)):
        flag = 0
        if len(point_density[i]) < density:
            for j in range(len(centers)):
                if i in point_density[centers[j]] and len(point_density[centers[j]]) >= density:
                    flag = 1
            if flag == 0:
                centers.append(i)
    labels = np.zeros(len(data))
    for i in range(len(centers)):
        if len(point_density[centers[i]]) >= density:
            for j in point_density[centers[i]] :
                labels[j] = i
            labels[centers[i]] = i
            print centers[i]
        labels[centers[i]] = -1
        #print len(point_density[centers[i]])
    return list(labels)