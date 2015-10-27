#coding: utf-8
__author__ = 'WangFeng'

'''
1.首先循环读出滤波后的文件，然后依次遍历？计算distance和给定的距离阈值相比较，这样就可以知道是属于啥语义信息的
2.也可以首先计算聚类后的结果，然后把聚类中心拿来做比较，这样就可以计算出每一个聚类结果的文本信息，后续就是计算他们的in  out 时间
3.也可以先找到stop point 在根据这些来找标签
'''
from Find_stop_points import stop_points
import Semantics_of_point
from distance_mean_filter import GetDistance
import numpy as np
from sklearn.cluster import DBSCAN
from matplotlib import pylab as plt
from mpl_toolkits.mplot3d import Axes3D
from Point_Transform import *
center_of_budling=Semantics_of_point.Compute_center_of_budling()
'''
==========================通过stop-point来进行计算===========================================================
'''
def calculate_stop_point_tag():
    fullpath=stop_points.getfullfilepath()
    for temppath in fullpath:
        #print(temppath)
        Now_stop_point=stop_points.get_filtered_gps_stop_point(temppath)
        if len(Now_stop_point)!=0:
            for stopint in Now_stop_point:
                sp=calculate_stop_pointstag(stopint)
                print Match_semantics(sp,250)

        #print(Now_stop_point)
        #print('\n')
def calculate_stop_pointstag(stopint):
    sum_lat=0.0
    sum_long=0.0
    for item_item in  stopint:
        sum_lat+=item_item[0]
        sum_long+=item_item[1]
        #这里还没有进行时间的计算，也就是说没有计算停留时间的统计。后续可以考虑进来，时间=item_item[2]
    return [sum_lat/len(stopint),sum_long/len(stopint)]#计算每个stop point 列表的中心点
def Match_semantics(sp,liminal=100):
    temp_sp=[]
    temp_sp.append(sp)
    #print(temp_sp)
    min_distance=9999999999.0
    min_label="Unknown"
    temp_center_googleGPS=gps2googlegps(temp_sp)
    for center in center_of_budling: #center_of_budling是 google 坐标
        dis=GetDistance(center[0],center[1],temp_center_googleGPS[0][0],temp_center_googleGPS[0][1])
        if dis<=liminal:
            #print GetDistance(center[0],center[1],temp_center_googleGPS[0][0],temp_center_googleGPS[0][1]),center[2],sp
            if dis<=min_distance:
                min_distance=dis
                min_label=center[2]
            #return center[2]
        # else:
        #     if center==center_of_budling[len(center_of_budling)-1]:
        #         return "Unknown"
    return min_label

'''
==========================通过密度聚类来进行计算===========================================================
采用 dbscan 算法来做，然后在试试sicence的cluster
'''
def dbscan(filepath,EPS=0.0002,MIN_SAMPLE=14):
    XX=np.loadtxt(filepath,dtype=float,delimiter=',',skiprows=1,usecols=(0,1),unpack=False)
    print(len(XX))
    #Latitude,Lat,XX=GPS_Kalman_Filter.Get_Prime_GpsData(".\\GPS_Get_PreProcesser\\7-11-2015\\locationGPS.txt")
    centers = [[1, 1], [-1, -1], [1, -1]]
    db = DBSCAN(eps=EPS, min_samples=MIN_SAMPLE).fit(XX)
    #db = DBSCAN(eps=0.002, min_samples=10).fit(XX)  3
    #db = DBSCAN(eps=0.0032, min_samples=10).fit(XX)  2
    core_samples_mask = np.zeros_like(db.labels_, dtype=bool)
    core_samples_mask[db.core_sample_indices_] = True
    labels = db.labels_

    # Number of clusters in labels, ignoring noise if present.
    n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
    print(n_clusters_),'n_clusters_'
    print(db.core_sample_indices_)

    unique_labels = set(labels)
    for k in unique_labels:
        if k != -1:
            class_member_mask = (labels == k)
            cluster = XX[class_member_mask & core_samples_mask]#cluster 就是每个密度聚类的结果
            #print(cluster)
            centor_point_of_cluster=[sum(cluster[:,0])/len(cluster[:,0]),sum(cluster[:,1])/len(cluster[:,1])]

            # for i in db.core_sample_indices_:
            #     print Match_semantics(XX[i],200)

            print Match_semantics(centor_point_of_cluster,9450)

if __name__=='__main__':
    #calculate_stop_point_tag()
    fullpath=stop_points.getfullfilepath()
    print fullpath[8]
    dbscan(fullpath[8])