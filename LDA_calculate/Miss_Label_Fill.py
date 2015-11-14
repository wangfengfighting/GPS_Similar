# coding: utf-8
__author__ = 'WangFeng'
'''
这个文件的主要功能是 根据初步找到的stay-point 里面会缺失一些时间和label的点，所以现在要找到那种是 缺失的label
再补上缺失的经纬度和时间
'''
import numpy as np
import time
import datetime
def  Read_RC_stoppoint(path):
    RC_stop=np.loadtxt(path,dtype=str, delimiter=',',usecols=(0,1,2,3,4))
                       #dtype={'names': [ 'Latitude', 'Longitude','accur','time','label'] ,'formats': [ 'f18','f18','f6','S20','S16']},

                       #converters={3:lambda s:datetime.datetime.strptime(s,'%Y-%m-%d %H:%M:%S')},

    print RC_stop
    RCedSP=[]
    temp=[]
    print str2time(RC_stop[199][3],RC_stop[0][3])
    index=0
    while index < len(RC_stop)-2:
        if RC_stop[index][4]==RC_stop[index+1][4]:
            temp.extend(RC_stop[index])
            RCedSP.append(temp)
            temp=[]
        else:
            if str2time(RC_stop[index][3],RC_stop[index+1][3])>=28*60:
                temp.append([RC_stop[index][0:4]])

def str2time(str1,str2):
    date_time1 = datetime.datetime.strptime(str1,'%Y-%m-%d %H:%M:%S')
    date_time2 = datetime.datetime.strptime(str2,'%Y-%m-%d %H:%M:%S')
    return (date_time2-date_time1).seconds

def writeRCstop2addLabel(filename,SP):
    filename=filename.replace('RC_stoppoint.txt','RCed_stoppoint.txt')
    AfterSP=open(filename)



if __name__=='__main__':
    s1='2014-05-22 07:02:32'
    s2='2014-05-22 08:48:32'
    print(len(s1))
    date_time1 = datetime.datetime.strptime(s1,'%Y-%m-%d %H:%M:%S')
    date_time2 = datetime.datetime.strptime(s2,'%Y-%m-%d %H:%M:%S')
    print (date_time2-date_time1).seconds
    t=[['28.2296884085' '112.991525366' '16.0' '2014-05-22 23:57:32' '601']
 ['28.2296880819' '112.991550017' '16.0' '2014-05-22 23:57:42' '601']
 ['28.2297067478' '112.99157344' '24.0' '2014-05-22 23:57:52' '601']]
    temp=[]
    #temp.extend()
    print(temp)
    Read_RC_stoppoint('E:\\Research_Study\\GPS_Similar\\GPS_Get_PreProcesser\\5-23-2014\\RC_stoppoint.txt')