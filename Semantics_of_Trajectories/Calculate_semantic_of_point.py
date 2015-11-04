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
from Find_stop_points import multiple_cluster
from Find_stop_points import science_cluster as SC
center_of_budling=Semantics_of_point.Compute_center_of_budling()
road_gps=np.loadtxt('road_point',dtype=float,delimiter=',',usecols=(0,1),unpack=False)

'''
==========================通过stop-point来进行计算===========================================================
'''
def calculate_stop_point_tag():
    fullpath=stop_points.getfullfilepath()
    LABEL=[]
    for temppath in fullpath:
        print(temppath)

        Now_stop_point=stop_points.get_filtered_gps_stop_point(temppath)
        if len(Now_stop_point)!=0:
            for stopint in Now_stop_point:
                sp=calculate_stop_pointstag(stopint)
                LABEL.append( Match_semantics(sp,90))
        write_semantic_of_stoppoint(temppath,depart_same_seq(LABEL))
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
    center_index=[]
    min_distance=9999999999.0
    min_label="Unknown"
    temp_center_googleGPS=gps2googlegps(temp_sp)
    translate_road_point=gps2googlegps(road_gps) #[[28.22980434947592, 113.00367366773305], [28.225867173722641, 113.00181810798254].......]
    for center in center_of_budling: #center_of_budling是 google 坐标
        dis=GetDistance(center[0],center[1],temp_center_googleGPS[0][0],temp_center_googleGPS[0][1])
        # print GetDistance(center[0],center[1],temp_center_googleGPS[0][0],temp_center_googleGPS[0][1]),center[2],temp_center_googleGPS
        # print GetDistance(center[0],center[1],sp[0],sp[1]),center[2],sp

        if dis<=liminal:
            #print GetDistance(center[0],center[1],temp_center_googleGPS[0][0],temp_center_googleGPS[0][1]),center[2],sp
            if dis<=min_distance:
                min_distance=dis
                min_label=center[2]
                center_index.append(center[0])
                center_index.append(center[1])
        else:
            for road_item in translate_road_point:
                disroad=GetDistance(center[0],center[1],road_item[0],road_item[1])
                if disroad<=100:
                    min_label="road"
                    break
            #return center[2]
        # else:
        #     if center==center_of_budling[len(center_of_budling)-1]:
        #         return "Unknown"
    ##print GetDistance(center_index[0],center_index[1],temp_center_googleGPS[0][0],temp_center_googleGPS[0][1]),min_label
    return min_label

'''
==========================通过密度聚类来进行计算===========================================================
采用 dbscan 算法来做，然后在试试sicence的cluster
'''
def dbscan(filepath,EPS=0.000492,MIN_SAMPLE=20):
    semantic_label=[]
    XX=np.loadtxt(filepath,dtype=float,delimiter=',',skiprows=1,usecols=(0,1),unpack=False)
    #print(len(XX))
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
    #print(n_clusters_),'n_clusters_'
    #print(db.core_sample_indices_)

    unique_labels = set(labels)
    #print( len(db.core_sample_indices_)),'---------------'
    for k in unique_labels:
        if k != -1:
            class_member_mask = (labels == k)
            cluster = XX[class_member_mask & core_samples_mask]#cluster 就是每个密度聚类的结果
            #print(cluster)
            centor_point_of_cluster=[sum(cluster[:,0])/len(cluster[:,0]),sum(cluster[:,1])/len(cluster[:,1])]

            for i in db.core_sample_indices_:
                #print Match_semantics(XX[i],200)
                semantic_label.append(Match_semantics(XX[i],100))

            #print Match_semantics(centor_point_of_cluster,350)
    return semantic_label

'''
==========================通过science聚类来进行计算===========================================================
采用sicence的cluster,聚类出你一天之中去过的点，然后根据中心点，把整个轨迹序列+半径里面的点添加进来，最后就形成了一个完整的咯。
'''
def science_cluster_semanstic(filepath):
    gps_semantic=np.loadtxt(filepath,dtype=float,delimiter=',',skiprows=1,usecols=(0,1),unpack=False)
    labels,centers=multiple_cluster.science_cluster(gps_semantic,num=15,cutoff_distance=0.000087,experience=0.000045)
    #print(len(gps_semantic))
    #print(len(labels))
    return labels,centers

def depart_same_seq(seq):   #这个是除去列表中连续的重复的点，相当于是合并相同的
    '''
    currtrn=1
    pre=0
    ans=[]
    temp=[]
    final=[]
    for i in range(0,len(seq)-1):
        if seq[pre]==seq[currtrn]:
            temp.append(seq[pre])
            pre+=1
            currtrn+=1
        else:
            temp.append(seq[pre])
            ans.append(temp)
            temp=[]
            pre+=1
            currtrn+=1
    '''
    currtrn=1
    pre=0
    ans=[]
    temp=[]
    final=[]
    #for i in range(0,len(a)-1):
   # print(len(seq))
    while currtrn<len(seq):

        if seq[pre]==seq[currtrn] :
            temp.append(seq[pre])
            pre+=1
            currtrn+=1

            if currtrn==len(seq)-1:

                if seq[pre-1]==seq[currtrn-1]:
                    temp.append(seq[pre-1])
                    ans.append(temp)
                else:
                    ans.append([seq[pre-1]])
                    ans.append([seq[currtrn-1]])
        else:
            temp.append(seq[pre])
            ans.append(temp)
            temp=[]
            pre+=1
            currtrn+=1
            if currtrn==len(seq)-1:
                if seq[pre-1]==seq[currtrn-1]:
                    temp.append(seq[pre-1])
                    ans.append(temp)
                else:
                    ans.append([seq[pre-1]])
                    ans.append([seq[currtrn-1]])

    for i in ans:
        final.append(i[0])
    return final

'''
这个方法写的是stop-point 聚类的结果 label
'''
def write_semantic_of_stoppoint(path,se):
    spath=path.replace("locationGPS","semanticGPS_stoppoint")
    output=open(spath,'w+')
    for label in se:
        output.write(label)
        output.write('\n')
    output.close()

'''
这个方法写的是science聚类的结果 label
'''
def  write_semantic_tofile(dic,label,path):
    spath=path.replace("locationGPS","semanticGPS")
    output=open(spath,'w+')
    data=np.loadtxt(path,dtype=str,delimiter=',',skiprows=1,usecols=(0,1,2,3,4),unpack=False)
    for la in range(0,len(label)):
        if label[la]==-1:
            output.write(data[la][0])
            output.write(',')
            output.write(data[la][1])
            output.write(',')
            output.write(data[la][2])
            output.write(',')
            output.write(data[la][3])
            output.write(',')
            output.write(data[la][4])
            output.write(',')
            output.write('exception')
            output.write('\n')
        else:
            output.write(data[la][0])
            output.write(',')
            output.write(data[la][1])
            output.write(',')
            output.write(data[la][2])
            output.write(',')
            output.write(data[la][3])
            output.write(',')
            output.write(data[la][4])
            output.write(',')
            output.write(dic[label[la]])
            output.write('\n')
    output.close()

def label_detect(path):
    semantic_label=[]
    adict={}
    labels,centers=science_cluster_semanstic(path)
    # print   sorted(labels)
    # print len(centers)
    # print('----------')
    k=0
    for i in centers:
        if not math.isnan(i[0]):
            temp_label=Match_semantics(i,150)  #150是聚类中心的半径这样算的里面所有的点都是这个聚类label
            semantic_label.append([temp_label,i[0],i[1]])
            adict[k]=temp_label
        # elif i[0]== -1:
        #     print '---------------------------------------'
        #     semantic_label.append(["outlater",i[0],i[1]])
        #     adict[99999]="outlater"
        else:
            semantic_label.append(["Unkonwn",i[0],i[1]])
            adict[k]="Unkonwn"
        k+=1
    #print(adict)
    #print adict[99999]
    # for i in semantic_label:
    #     print i[0],gps2googlegps([i[1:3]])
    semantic_seq=depart_same_seq(labels)
    # ss=[]
    # for key in semantic_seq:
    #     if key != -1:
    #         ss.append(adict[key])
    write_semantic_tofile(adict,labels,path)

if __name__=='__main__':
    calculate_stop_point_tag()

    #下面用的是密度 science聚类的办法
    # fullpath=stop_points.getfullfilepath()
    #
    # for path in fullpath:
    #     label_detect(path)
    #     print 'have done'+path.split("\\")[4]
    # print('process over')


    '''
    #se=dbscan(fullpath[12])
    semantic_label=[]
    adict={}
    labels,centers=science_cluster_semanstic(fullpath[12])
    # print (labels)
    # print(centers)
    # print('----------')
    k=0
    for i in centers:
        if not math.isnan(i[0]):
            temp_label=Match_semantics(i,150)
            semantic_label.append([temp_label,i[0],i[1]])
            adict[k]=temp_label
        else:
            semantic_label.append(["UUUUU",i[0],i[1]])
            adict[k]="Unknown"
        k+=1
    # for i in semantic_label:
    #     print i[0],gps2googlegps([i[1:3]])
    semantic_seq=depart_same_seq(labels)
    ss=[]
    for key in semantic_seq:
        ss.append(adict[key])
    #print(adict)
    print(ss)
    print(depart_same_seq(ss))
    print len(depart_same_seq(ss))
    write_semantic_tofile(adict,labels,fullpath[12])
    '''
