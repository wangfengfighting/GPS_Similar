# coding: utf-8
__author__ = 'WangFeng'
'''
这个文件要做的主要是 找到在一个label停留的时间，开始时间，结束时间等
'''
from getDir import GetDirName
import os
import numpy as np
import time
import datetime
from LDA_process_class import ldaHelper
def GetSemanticGPSpath():
    getdir=GetDirName()
    Fulldirlist=[]
    parent_path = os.path.dirname(os.getcwd())
    dirlist=getdir.printPath(parent_path+"\\GPS_Get_PreProcesser")
    for dir in dirlist:
        Fulldirlist.append(parent_path+"\\GPS_Get_PreProcesser"+"\\"+dir+"\\"+'semanticGPS.txt')  #semanticGPS.txt是处理后的gps 加时间， 加label的文件信息
    return Fulldirlist

def Add_timestamp(path):
    tempdata=np.loadtxt(path, dtype={'names': [ 'time','label'] ,'formats': [ 'f18','S16']},
                       delimiter=',',
                       converters={3:lambda s:float(time.mktime((datetime.datetime.strptime(s,'%m-%d-%Y %H:%M:%S')).timetuple()))},
                       usecols=(3,5))
    print tempdata

def write_labelTime2file(seq,filename):
    if  'RC_stoppoint.txt' in filename:
        filename=filename.replace('RC_stoppoint.txt','RClabelTime.txt')
    elif  'RCed_stoppoint.txt' in filename:
        filename=filename.replace('RCed_stoppoint.txt','RCedlabelTime.txt')
    else:
        filename=filename.replace('semanticGPS.txt','labelTime.txt')
    output=open(filename,'w')
    for i in range(0,len(seq)):
        if seq[i][3]!=0:
            if seq[i][0]=='east_door2' or seq[i][0]=='east_door1' or seq[i][0]=='east_door3' or seq[i][0]=='east_door':
                output.write('east_door'  )#label
            elif seq[i][0]=='8_bedroom1' or seq[i][0]=='8_bedroom':
                output.write('8_bedroom'  )#label
            else:
                output.write(seq[i][0])
            output.write(',')
            output.write(seq[i][1])#begintime
            output.write(',')
            output.write(seq[i][2])#endtime
            output.write(',')
            output.write(str(seq[i][3]))#time
            if i != len(seq)-1:
                output.write('\n')
    output.close()



def Label_Time_process():
    filelist=GetSemanticGPSpath()
    lda=ldaHelper()
    for file in filelist:
        write_labelTime2file(lda.Add_timestamp(file),file)
        print('have done %s'%file)
    
def RC_Label_Time_process():
    filelist=GetSemanticGPSpath()
    lda=ldaHelper()
    for file in filelist:
        f=file.replace('semanticGPS.txt','RC_stoppoint.txt')
        write_labelTime2file(lda.Add_RCtimestamp(f),f)
        print('have done %s'%f)

def RCed_Label_Time_process():
    filelist=GetSemanticGPSpath()
    lda=ldaHelper()
    for file in filelist:
        f=file.replace('semanticGPS.txt','RCed_stoppoint.txt')
        write_labelTime2file(lda.Add_RCtimestamp(f),f)
        print('have done %s'%f)

def main():
    #Label_Time_process()
    RC_Label_Time_process()
    RCed_Label_Time_process()
if __name__=='__main__':
    main()

