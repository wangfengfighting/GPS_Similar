# coding: utf-8
__author__ = 'WangFeng'
'''
这个类主要是用来处理一些常见的lda前期处理函数
'''
import os
import numpy as np
import time
import datetime

class ldaHelper:

    def Add_timestamp(self,path):
        # tempdata=np.loadtxt(path, dtype={'names': [ 'time','label'] ,'formats': [ 'f18','S16']},
        #                delimiter=',',
        #                #converters={3:lambda s:float(time.mktime((time.strptime(s,'%m-%d-%Y %H:%M:%S'))))},
        #                converters={3:lambda s:float(time.mktime((datetime.datetime.strptime(s,'%m-%d-%Y %H:%M:%S')).timetuple()))},
        #                usecols=(3,5))
        tempdata=np.loadtxt(path, dtype=str,delimiter=',',usecols=(3,5))

        #print tempdata
        # for i in tempdata:
        #     print float(i[0])

        return self.calculateTimestamp(tempdata)

    def calculateTimestamp(self,tempdata):
         labeldata=tempdata.tolist()
         #print labeldata

         labeldata.reverse()
         temp=[]
         templast=[]
         finaltimestamp=[]
         while labeldata:
            tuple=labeldata.pop()
            if not len(temp)==0:
                if tuple[1]==temp[len(temp)-1][1]:
                    temp.append(tuple)
                    templast.append(tuple)
                else:
                    #print temp.__str__()
                    finaltimestamp.append(temp)
                    temp=[]
                    templast=[]
                    temp.append(tuple)
                    templast.append(tuple)
            else:
                temp.append(tuple)
         finaltimestamp.append(templast)
         #print finaltimestamp
         theLast=[]
         t=[]
         for item in finaltimestamp:
             beginTime=item[0][0]
             endTime=item[len(item)-1][0]
             statelabel=item[0][1]
             #theLast.append([beginTime,endTime,statelabel])
             # t.append(beginTime)
             # t.append(endTime)
             t.append(str2Time(beginTime,endTime))
             t.append(statelabel)
             theLast.append(t)
             t=[]
         #return finaltimestamp
         return theLast

def str2Time(timeStr1,timeStr2):
    t1 = datetime.datetime.strptime(timeStr1,'%m-%d-%Y %H:%M:%S')
    t2 = datetime.datetime.strptime(timeStr2,'%m-%d-%Y %H:%M:%S')
    return (t2-t1).seconds


if __name__=='__main__':
    a=ldaHelper()
    ans=a.Add_timestamp('G:\\PostgraduatePROJECT\\GPS_Similar\\GPS_Get_PreProcesser\\7-10-2015\\semanticGPS.txt')
    for i in ans:
        print i