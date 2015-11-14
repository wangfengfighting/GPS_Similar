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
    #print RC_stop
    RCedSP=[]
    #print str2time(RC_stop[199][3],RC_stop[0][3])
    index=0
    while index < len(RC_stop)-1:
        temp=[]
        if RC_stop[index][4]==RC_stop[index+1][4]:
            # temp.append(RC_stop[index][0])
            # temp.append(RC_stop[index][1])
            # temp.append(RC_stop[index][2])
            # temp.append(RC_stop[index][3])
            # temp.append(RC_stop[index][4])
            temp.extend(RC_stop[index][0:5])
            RCedSP.append(temp)
        else:
            if str2time(RC_stop[index][3],RC_stop[index+1][3])>=20*60:
                temp.extend(RC_stop[index][0:5])
                RCedSP.append(temp)
                temp=[]
                temp.extend(RC_stop[index][0:5])

                # for i in range(5):
                #     print(i)
                #     print(temp[0][i])
                temp[3]=timedela(RC_stop[index+1][3])
                RCedSP.append(temp)
                #print(index)
            else:
                temp.extend(RC_stop[index][0:5])
                RCedSP.append(temp)
        index+=1
    last=[]
    last.extend(RC_stop[len(RC_stop)-1][0:5])
    RCedSP.append(last)
    #print(RCedSP)
    writeRCstop2addLabel(path,RCedSP)

def timedela(str):
    date_time1 = datetime.datetime.strptime(str,'%Y-%m-%d %H:%M:%S')
    predate=date_time1+datetime.timedelta(seconds=-20)
    s=predate.strftime('%Y-%m-%d %H:%M:%S')
    return s

def str2time(str1,str2):
    date_time1 = datetime.datetime.strptime(str1,'%Y-%m-%d %H:%M:%S')
    date_time2 = datetime.datetime.strptime(str2,'%Y-%m-%d %H:%M:%S')
    return (date_time2-date_time1).seconds

def writeRCstop2addLabel(filename,SP):
    file_name=filename.replace('RC_stoppoint.txt','RCed_stoppoint.txt')
    AfterSP=open(file_name,'w+')
    for i in range(len(SP)):
        AfterSP.write(SP[i][0])
        AfterSP.write(',')
        AfterSP.write(SP[i][1])
        AfterSP.write(',')
        AfterSP.write(SP[i][2])
        AfterSP.write(',')
        AfterSP.write(SP[i][3])
        AfterSP.write(',')
        AfterSP.write(SP[i][4])
        if i != len(SP)-1:
            AfterSP.write('\n')
    AfterSP.close()
def main():
    from label_add_time import GetSemanticGPSpath
    full=GetSemanticGPSpath()
    for n in range(len(full)):
        path_file=full[n].replace('semanticGPS.txt','RC_stoppoint.txt')
        print(path_file)
        Read_RC_stoppoint(path_file)

    print 'ok.....have process over'

if __name__=='__main__':
    main()
    # s1='2014-05-22 07:02:32'
    # s2='2014-05-22 08:48:32'
    # print(len(s1))
    # date_time1 = datetime.datetime.strptime(s1,'%Y-%m-%d %H:%M:%S')
    # date_time2 = datetime.datetime.strptime(s2,'%Y-%m-%d %H:%M:%S')
    # d=date_time1+datetime.timedelta(seconds=-3)
    # print(d)

    # Read_RC_stoppoint('E:\\Research_Study\\GPS_Similar\\GPS_Get_PreProcesser\\11-9-2015\\RC_stoppoint.txt')
    # print('over')