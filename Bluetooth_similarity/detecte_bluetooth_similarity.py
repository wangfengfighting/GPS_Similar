from __future__ import division
#coding=utf-8
__author__ = 'feng'

from getDir import GetDirName
import os
import numpy as np
import datetime
import math
import traceback


def calculate_bluetooth_sim(user1,user2):
    sum_sim = 0.0
    UserFile1=[]
    UserFile2=[]
    getdir=GetDirName()
    parent_path = os.path.dirname(os.getcwd())
    user1Floder=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+user1))
    user2Floder=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+user2))
    user1filepath=parent_path+os.sep+"starlog"+os.sep+os.sep+user1+os.sep
    user2filepath=parent_path+os.sep+"starlog"+os.sep+os.sep+user2+os.sep
    try:
        for i in range(len(user1Floder)):
            u1file=user1filepath+user1Floder[i]+os.sep+'Processed_bluetooth.txt'
            if os.path.exists(u1file):
                UserFile1.append(u1file)

        for j in range(len(user1Floder)):
            u2file=user2filepath+user2Floder[j]+os.sep+'Processed_bluetooth.txt'
            if os.path.exists(u2file):
                UserFile2.append(u2file)
    except Exception ,e:
        print e
        traceback.print_exc()


    num_floder=len(UserFile1) if len(UserFile1)<=len(UserFile2) else len(UserFile2)

    try:
        for i in range(num_floder):
            sum_sim+=daily_dtw_wifisim(UserFile1[i],UserFile2[i])
    except Exception ,e:
        print 'e'
        traceback.print_exc()
        sum_sim+=0.0

    return sum_sim



def daily_dtw_wifisim(file1,file2):
    '''
    :param file1:
    :param file2:
    :return: double distance
    '''
    print 'exec daily_dtw_wifisim s%,s%'

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

        else:
            sum_bluetooth_sim+=calculate_blueseq_sim(bluetoothuser1list[h_index],bluetoothuser2list[h_index])

            #
            #continue write if and judge sim with seq
            #


    return sum_bluetooth_sim


def calculate_blueseq_sim(blueseq1,blueseq2):
    temp_sim = 0.0
    inter_section = list(set(blueseq1) & set(blueseq2))
    temp_sim = len(inter_section) / math.sqrt( square(blueseq1)+square(blueseq2)  )
    return  temp_sim

def square(x):
    return len(x) * len(x)



def str2Time(timeStr):
    t1 = datetime.datetime.strptime(timeStr,'%m-%d-%Y %H:%M:%S')
    mint = int(t1.minute)+int(t1.hour)*60
    return mint


def calculate_user_sim_onBluetooth():
    userlist = []
    getdir = GetDirName()
    parent_path = os.path.dirname(os.getcwd())
    AllUserFiles,AllFiles,other = getdir.getUserFiles(parent_path+os.sep+'starlog')
    for path_file in other:
        for i in range(len(path_file)):
            path_file_name = parent_path+path_file[i]+os.sep+'bluetooth.txt'
            if os.path.exists(path_file_name):
                userlist.append(path_file_name.split(os.sep)[-3])

    userlist = list(set(userlist))
    print userlist
    for i in range(len(userlist)-1):
        for j in range(i,len(userlist)):
            print userlist[i],userlist[j]
            result= calculate_bluetooth_sim(userlist[i],userlist[j])
            ans.write(userlist[i])
            ans.write(',')
            ans.write(userlist[j])
            ans.write(',')
            ans.write(str(result))
            ans.write('\n')


if __name__ == '__main__':
    ans = open('similarBaseonBlutetooth.txt','a')
    calculate_user_sim_onBluetooth()
    ans.close()
