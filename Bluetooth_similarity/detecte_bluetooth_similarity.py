#coding=utf-8
__author__ = 'feng'

from getDir import GetDirName
import os
import numpy as np
import datetime


def calculate_bluetooth_sim(user1,user2):
    getdir=GetDirName()
    parent_path = os.path.dirname(os.getcwd())
    user1Floder=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+user1))
    user2Floder=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+user2))
    user1filepath=parent_path+os.sep+"starlog"+os.sep+os.sep+user1+os.sep
    user2filepath=parent_path+os.sep+"starlog"+os.sep+os.sep+user2+os.sep
    num_floder=len(user1Floder) if len(user1Floder)<=len(user2Floder) else len(user2Floder)
    sum_sim=0.0

    try:
        for i in range(num_floder):
            u1file=user1filepath+user1Floder[i]+os.sep+'Processed_bluetooth.txt'
            u2file=user2filepath+user2Floder[i]+os.sep+'Processed_bluetooth.txt'
            sum_sim+=daily_dtw_wifisim(u1file,u2file)
    except Exception ,e:
        sum_sim+=0.0

    return sum_sim



def daily_dtw_wifisim(file1,file2):
    '''
    :param file1:
    :param file2:
    :return: double distance
    '''
    bluetoothuser1list=[]
    bluetoothuser2list=[]
    user1data=np.loadtxt(file1,dtype=str,delimiter=',',skiprows=1,usecols=(0,1,2,3))
    user2data=np.loadtxt(file2,dtype=str,delimiter=',',skiprows=1,usecols=(0,1,2,3))

    for minutes in range(144):  # one day has 1440 minutes,the buletooth scan data ever 10 minutes.....
        temp1=[]
        temp2=[]

        for i in  range(len(user1data)):

            if minutes*60 <=str2Time(user1data[i][3]) <= (minutes+1)*60:
                temp1.append((user1data[i][0]))
                temp1=list(set(temp1))
        bluetoothuser1list.append(temp1)

        for j in  range(len(user2data)):

            if minutes*60 <= str2Time(user2data[j][3]) <= (minutes+1)*60 :
                temp2.append((user2data[j][0]))
                temp2=list(set(temp2))
        bluetoothuser2list.append(temp2)

    # bluetoothuser2list=[ [hou1] [hour2] [] [] [] [ hour2[wifi1] [wifi2] [wifi3] [....]  ].......]
    name1=file1.split(os.sep)[-3]
    name2=file2.split(os.sep)[-3]
    sum_bluetooth_sim=0.0
    # wifi_dtw1=[]
    # wifi_dtw2=[]
    for h_index in range(144):

        if len(bluetoothuser1list[h_index])== 0 or len(bluetoothuser2list[h_index]) == 0:
            sum_bluetooth_sim += 0.0
            #
            #continue write if and judge sim with seq
            #


    return sum_bluetooth_sim

def str2Time(timeStr):
    t1 = datetime.datetime.strptime(timeStr,'%m-%d-%Y %H:%M:%S')

    return int(t1.hour)
