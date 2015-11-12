# -*- coding: utf-8 -*-
"""
Created on Tue Dec 09 20:18:58 2014

@author: yangruosong
"""
import sklearn
import numpy
import pylab
import readdata
import sciencecluster
import os
import sklearn.decomposition.pca
import DBSCANJoint

def distance(X,Y):
    temp = numpy.array(X) - numpy.array(Y)
    return numpy.dot(temp,temp)

def k_means_cluster(gps_data,n_clusters = 3,cutoff_distance = 0.0000001,number = 50,show = False): 
    exception = []
    data = []
    neigh_num = {}
    neighbor = numpy.zeros(len(gps_data))
    for i in range(len(gps_data) - 1):
        for j in range(i + 1,len(gps_data),1):
            if(distance(gps_data[i],gps_data[j]) < cutoff_distance):
                neighbor[i] += 1
                neighbor[j] += 1
    for i in range(len(gps_data)):
        if neighbor[i] not in neigh_num:
            neigh_num[neighbor[i]] = 1
        else:
            neigh_num[neighbor[i]] += 1
        if neighbor[i] < number:
            exception.append(i)
        else:
            data.append(gps_data[i])
    cluster_centers, labels, inertia = sklearn.cluster.k_means(numpy.array(data),n_clusters,verbose=True)
    labels = list(labels)
    if show == True:
        for i in range(len(gps_data)):
            if neighbor[i] not in neigh_num:
                neigh_num[neighbor[i]] = 1
            else:
                neigh_num[neighbor[i]] += 1
        neigh_num = [[key,neigh_num[key]] for key in neigh_num]
        neigh_num.sort()
        neigh_num = [[sum([neigh_num[i][1] for i in range(j)]),neigh_num[j][0]] for j in range(1,len(neigh_num),1)]
        X = [d[1] for d in neigh_num]
        Y = [d[0] for d in neigh_num]
        pylab.plot(X,Y)
        pylab.show()
    print neigh_num
    
    for i in range(len(exception)):
        labels.insert(exception[i],-1)
    '''
    for i in range(len(gps_data)):
        if labels[i] == -1:
            pylab.plot(gps_data[i][0],gps_data[i][1],'or')
        else:
            pylab.plot(gps_data[i][0],gps_data[i][1],'oy')
    pylab.show()
    print len(gps_data)
    print len(data)
    print len(exception)
    '''
    return cluster_centers,labels

def compute_average_distance(gps_data,centers,labels):
    total = 0.0
    num = 0
    for i in range(len(gps_data)):
        if labels[i] != -1:
            total += distance(gps_data[i],centers[labels[i]])
            num += 1
    return total / float(num) / 0.0000001

def science_cluster(gps_data,number,show = False):
    labels,centers = sciencecluster.science_cluster(numpy.array(gps_data),num = number,cutoff_distance = 0.000005,experience = 0.000811,show = show) #0.0003 \\0.0001
    return centers,labels

def draw_result(gps_data,labels):
    pylab.figure()
    X = [data[0] for data in gps_data]
    Y = [data[1] for data in gps_data]
    ax1 = pylab.subplot(211)
    ax2 = pylab.subplot(212)
    pylab.sca(ax1)
    for i in range(len(X)):
        if labels[i] == 0:
            pylab.plot(X[i],Y[i],'or')
        elif labels[i] == 1:
            pylab.plot(X[i],Y[i],'oy')
        elif labels[i] == 2:
            pylab.plot(X[i],Y[i],'og')
        elif labels[i] == 3 :
            pylab.plot(X[i],Y[i],'ob')
        elif labels[i] == 4:
            pylab.plot(X[i],Y[i],'ok')
        elif labels[i] == -1:
            pylab.plot(X[i],Y[i],'oc')
    pylab.sca(ax2)
    pylab.plot(X,Y,'o')
    pylab.show()

def cal_min_distance(gps,centers):
    gps = numpy.array(gps)
    centers = numpy.array(centers)
    dis = [numpy.dot((gps - center),(gps- center)) for center in centers]
    min_dis = min(dis)
    index = dis.index(min_dis)
    return index
def invariant_k_means(gps_data,centers,number):
    exception = []
    data = []
    neighbor = numpy.zeros(len(gps_data))
    for i in range(len(gps_data) - 1):
        for j in range(i + 1,len(gps_data),1):
            if(distance(gps_data[i],gps_data[j]) < 0.0000001):
                neighbor[i] += 1
                neighbor[j] += 1
    for i in range(len(gps_data)):
        if neighbor[i] < number:
            exception.append(i)
        else:
            data.append(gps_data[i])
    labels = numpy.zeros(len(data))
    for i in range(len(data)):
        labels[i] = cal_min_distance(data[i],centers)
    labels = list(labels)
    for i in range(len(exception)):
        labels.insert(exception[i],-1)
    return labels

def find_N_num(gps_data):
#    centers = []
    ave_dis = []
#    cluster_centers,labels = k_means_cluster(gps_data,n_clusters = 2,number = 0)
    for i in range(50):
        number = 5 * i
        centers,labels = science_cluster(gps_data,number)
        print len([labels[i] for i in range(len(labels)) if labels[i] == -1])
#        labels = invariant_k_means(gps_data,cluster_centers,number)
#        centers += list(cluster_centers)
        ave_dis.append(compute_average_distance(gps_data,centers,labels))
#    print centers
    ave_dis = [ave_dis[i - 1] - ave_dis[i] for i in range(1,len(ave_dis),1)]
    X = [i for i in range(49)]
    print ave_dis
    pylab.plot(X,ave_dis)
    pylab.show()
def split_data_plot(filename):
    plot_data = []
    gps_data,timestamp = readdata.get_network_data(filename)
    for i in range(0,len(gps_data) - len(gps_data) % 30,30):
        temp = numpy.array(gps_data[i:i + 30])
        temp = temp.flatten()
        temp = list(temp)
        plot_data.append(temp)
    return plot_data

def plot_all(path):
    plot = []
    gps_num = []
    filenames = os.listdir(path)
    for name in filenames:
        current = split_data_plot(path + '\\' + name)
        plot = plot + current
        gps_num.append(len(current))
    return plot,gps_num

def calculate_pca(data):
    p = sklearn.decomposition.pca.PCA(n_components = 5)
    p.fit(data)
    feature = p.transform(data)
    return feature

if __name__ == '__main__':
#    '''
    gps_data,timestamp = readdata.get_network_data('.\\ubiqlog\\log_5-21-2014.txt')
#    gps_data,timestamp = readdata.get_network_data('.\\log_10-31-2014.txt')
    print len(gps_data)
#    find_N_num(gps_data)
#    cluster_centers,labels = k_means_cluster(gps_data,n_clusters = 2)
#    labels = DBSCANJoint.dbscan_joint(gps_data,0.000005,30)
    cluster_centers,labels = science_cluster(gps_data,30,show = False)
#    draw_result(gps_data,labels)
    print cluster_centers
    '''
    f = open('labels.txt','w')
    for i in range(len(labels)):
        f.write(str(i + 1))
        f.write('\t')
        f.write(str(labels[i]))
        f.write('\n')
    f.close()
#    labels = DBSCANJoint.dbscan_joint(gps_data,0.0000001,30)
#    draw_result(gps_data,labels)
#    print cluster_centers
#    print len(cluster_centers)
#    '''
    '''
    plot_data,gps_num = plot_all('.\\ubiqlog')

    feature = calculate_pca(plot_data)
    feature = feature[sum(gps_num[:2]):sum(gps_num[:3])]
    print len(feature)
    feature = plot_data[sum(gps_num[:2]):sum(gps_num[:3])]
    cluster_centers,labels = k_means_cluster(feature,n_clusters = 3,cutoff_distance = 0.00001,number = 0)
#    cluster_centers, labels, inertia = sklearn.cluster.k_means(numpy.array(feature),n_clusters = 3,verbose=True)
    label = numpy.zeros(30 * len(labels))
    gps_data,timestamp = readdata.get_network_data('.\\ubiqlog\\log_5-21-2014.txt')
    for i in range(30 * len(labels)):
        label[i] = labels[i / 30]
    draw_result(gps_data[:len(gps_data) - len(gps_data) % 30],label)
    '''