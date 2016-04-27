#coding:utf-8
__author__ = 'wangfeng'
"""This .py file is used to calculate the wifi similarity according to
the DTW distance. think that there are two sequence of user`s wifi A=[a1,a2,a3 .....an]
B=[b1,b2,b3...bn] each item has there wifi strength(level). At that moument phone sensor wifi singal is specifical that
we can assume they order by dictionary (ASE), with index as x-axis 'level' as y-axis,we can detected the DTW distance
"""
from getDir import GetDirName
import os
import json
import numpy as np
import sys
from Init_process_wifi import get_fenlei_user
import datetime
from  dtw import dtw
from scipy.spatial.distance import euclidean
from numpy.linalg import norm
from sklearn.metrics.pairwise import euclidean_distances
def main():
    user=[]
    wifi_file=get_fenlei_user()
    for file in wifi_file:
        if not os.path.exists(file):
            wifi_file.remove(file)
        else:
            user.append(file.split(os.sep)[-3])
    user=list(set(user))
    print(user)
    file=open('simlarBaseonDTWdis.txt','w')
    for i in range(len(user)):
        for j in range(i+1,len(user)):
            sim= canclulate_dtw_wifi(user[i],user[j])
            file.write(user[i])
            file.write(',')
            file.write(user[j])
            file.write(',')
            file.write(str(sim))
            file.write('\n')
    file.close()


def canclulate_dtw_wifi(user1,user2):
    getdir=GetDirName()
    parent_path = os.path.dirname(os.getcwd())
    user1Floder=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+user1))
    user2Floder=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+user2))
    user1filepath=parent_path+os.sep+"starlog"+os.sep+os.sep+user1+os.sep
    user2filepath=parent_path+os.sep+"starlog"+os.sep+os.sep+user2+os.sep
    num_floder=len(user1Floder) if len(user1Floder)<=len(user2Floder) else len(user2Floder)
    sum_sim=0.0
    for i in range(num_floder):
        u1file=user1filepath+user1Floder[i]+os.sep+'Downwifi.txt'
        u2file=user2filepath+user2Floder[i]+os.sep+'Downwifi.txt'
        sum_sim+=daily_dtw_wifisim(u1file,u2file)


    return sum_sim


def daily_dtw_wifisim(file1,file2):
    '''
    :param file1:
    :param file2:
    :return: double distance
    '''
    wifiuser1list=[]
    wifiuser2list=[]
    user1data=np.loadtxt(file1,dtype=str,delimiter=',',skiprows=1,usecols=(0,3,4))
    user2data=np.loadtxt(file2,dtype=str,delimiter=',',skiprows=1,usecols=(0,3,4))

    for hour in range(24):
        temp1=[]
        temp2=[]

        for i in  range(len(user1data)):
            temp11=[]
            if str2Time(user1data[i][1]) == hour:
                temp11.append((user1data[i][0]))
                temp11.append((user1data[i][2]))
                temp1.append(temp11)
        wifiuser1list.append(temp1)

        for j in  range(len(user2data)):
            temp22=[]
            if str2Time(user2data[j][1]) == hour:
                temp22.append((user2data[j][0]))
                temp22.append((user1data[i][2]))
                temp2.append(temp22)
        wifiuser2list.append(temp2)

    # wifiuser2list=[ [hou1] [hour2] [] [] [] [ hour2[wifi1] [wifi2] [wifi3] [....]  ].......]
    name1=file1.split(os.sep)[-3]
    name2=file2.split(os.sep)[-3]
    sum_wifi_dtw=0.0
    # wifi_dtw1=[]
    # wifi_dtw2=[]
    for h_index in range(24):
        wifi_dtw1=[]
        wifi_dtw2=[]
        if len(wifiuser1list[h_index])>0 and len(wifiuser2list[h_index])>0:
            #print len(wifiuser1list[h_index])
            user1wifi=sorted(wifiuser1list[h_index],key=lambda t:t[0])
            user2wifi=sorted(wifiuser2list[h_index],key=lambda t:t[0])

            for index1 in range(len(user1wifi)):
                # print '------------------'
                # print  user1wifi
                wifitemp1=[float(index1),float(user1wifi[index1][1])]
                wifi_dtw1.append(wifitemp1)
            for index2 in range(len(user2wifi)):
                wifitemp2=[float(index2),float(user2wifi[index2][1])]
                wifi_dtw2.append(wifitemp2)

            # print (wifi_dtw1)
            # print (wifi_dtw2)
            # dtw1=np.array(wifi_dtw1)
            # dtw2=np.array(wifi_dtw2)
            dist, cost, acc, path  = dtw(wifi_dtw1, wifi_dtw2,dist=euclidean_distances)
            sum_wifi_dtw+=dist
        else:
            sum_wifi_dtw+=0.0

    return sum_wifi_dtw


def my_custom_norm(x, y):
    return (x * x) + (y * y)


def str2Time(timeStr):
    t1 = datetime.datetime.strptime(timeStr,'%m-%d-%Y %H:%M:%S')

    return int(t1.hour)


if __name__=='__main__':
    main()


    s=[['508',-70],['fgada',-89],['as',90]]
    s1=sorted(s,key=lambda ss:ss[0])

    x='   '
    if not x.strip():
        print 'null'
