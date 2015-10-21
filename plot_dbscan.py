# -*- coding: utf-8 -*-
"""
===================================
Demo of DBSCAN clustering algorithm
===================================

Finds core samples of high density and expands clusters from them.

"""


import numpy as np
from sklearn.cluster import DBSCAN
from sklearn import metrics
from sklearn.datasets.samples_generator import make_blobs
from sklearn.preprocessing import StandardScaler
import GPS_Kalman_Filter
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
##############################################################################
# Generate sample data
#Latitude,Lat,XX=GPS_Kalman_Filter.Get_Prime_GpsData(".\\GPS_Get_PreProcesser\\7-11-2015\\locationGPS.txt")
#centers = [[1, 1], [-1, -1], [1, -1]]
##############################################################################
# Compute DBSCAN



def dbscan(EPS,MIN_SAMPLE):
    XX=np.loadtxt(".\\GPS_Get_PreProcesser\\7-11-2015\\locationGPS.txt",dtype=float,delimiter=',',skiprows=1,usecols=(0,1),unpack=False)
    #Latitude,Lat,XX=GPS_Kalman_Filter.Get_Prime_GpsData(".\\GPS_Get_PreProcesser\\7-11-2015\\locationGPS.txt")
    centers = [[1, 1], [-1, -1], [1, -1]]
    db = DBSCAN(eps=EPS, min_samples=MIN_SAMPLE).fit(XX)
    #db = DBSCAN(eps=0.002, min_samples=10).fit(XX)  3
    #db = DBSCAN(eps=0.0032, min_samples=10).fit(XX)   2
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_
    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)

    ##############################################################################
    # Plot result

    # Black removed and is used for noise instead.
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        class_member_mask = (labels == k)

        xy = XX[class_member_mask & core_samples_mask]

        #ax.scatter(xy[:, 0], xy[:, 1],np.array([1]*len(xy[:, 0])), 'o', markerfacecolor=col,
             #markeredgecolor='k', markersize=8)
        ax.scatter(xy[:, 0], xy[:, 1],np.array([1]*len(xy[:, 0])), c=col)
        #xy = XX[class_member_mask & ~core_samples_mask]
        #plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
         #    markeredgecolor='k', markersize=4)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    plt.show()
    '''
    unique_labels = set(labels)
    colors = plt.cm.Spectral(np.linspace(0, 1, len(unique_labels)))
    for k, col in zip(unique_labels, colors):
        if k == -1:
            # Black used for noise.
            col = 'k'

        class_member_mask = (labels == k)

        xy = XX[class_member_mask & core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=8)
        xy = XX[class_member_mask & ~core_samples_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col,
             markeredgecolor='k', markersize=4)
    plt.title('Estimated number of clusters: %d' % n_clusters_)
    #plt.show()
    '''
if __name__=='__main__':
    dbscan(0.0002, 10)