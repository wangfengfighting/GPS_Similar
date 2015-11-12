# -*- coding: utf-8 -*-
"""
Created on Sat Dec 20 15:59:23 2014

@author: yangruosong
"""
import numpy
import pylab

def dbscan_joint(data,radius,density):
    point_density = {}
    centers = []
    for i in range(len(data) - 1):
        sym = 0
        for j in range(i + 1,len(data),1):
            if sum(numpy.array((data[i]) - numpy.array(data[j])) ** 2) < radius:
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
                    if m == -1:
                        print centers
                        pylab.plot([data[k][0] for k in point_density[58]],[data[k][1] for k in point_density[58]],'oy')
                        pylab.plot([data[k][0] for k in point_density[77]],[data[k][1] for k in point_density[77]],'ob')
                        pylab.show()
                    if len(point_density[i] & point_density[centers[j]]) > 0:
                        if m == -1:
                            print centers
                            for n in range(len(centers)):
                                pylab.plot([data[k][0] for k in point_density[centers[n]]],[data[k][1] for k in point_density[centers[n]]],'oy')
                            pylab.plot([data[k][0] for k in point_density[i]],[data[k][1] for k in point_density[i]],'or')
                            pylab.plot([data[k][0] for k in point_density[centers[j]]],[data[k][1] for k in point_density[centers[j]]],'oy')
                            pylab.plot([data[k][0] for k in point_density[i] & point_density[centers[j]]],[data[k][1] for k in point_density[i] & point_density[centers[j]]],'ob')
                            pylab.show()
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
    labels = numpy.zeros(len(data))
    for i in range(len(centers)):
        if len(point_density[centers[i]]) >= density:
            for j in point_density[centers[i]] :
                labels[j] = i
            labels[centers[i]] = i
            print centers[i]
        labels[centers[i]] = -1
        #print len(point_density[centers[i]])
    return list(labels)