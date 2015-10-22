# coding: utf-8
'''
这是一个讲dtw的例子

'''
from dtw import dtw
import  numpy as np
import  mlpy
import math
def testdtw(tra1,tra2):

    dist, cost, path = dtw(tra1, tra2)
    print 'Minimum distance found:', dist,math.log(dist,0.4),math.atan(dist)*2/math.pi



def Get_Prime_GpsData(filepath_name1,filepath_name2):
    trajectory1=np.loadtxt(filepath_name1,dtype=float,delimiter=',',skiprows=1,usecols=(0,1),unpack=False)
    tra1=trajectory1.tolist()
    trajectory2=np.loadtxt(filepath_name2,dtype=float,delimiter=',',skiprows=1,usecols=(0,1),unpack=False)
    tra2=trajectory2.tolist()
    return tra1,tra2

'''
def dtw(X,Y):
     X=[1,2,3,4]
     Y=[1,2,7,4,5]
     M=[[distance(X[i],Y[i]) for i in range(len(X))] for j in range(len(Y))]
     l1=len(X)
     l2=len(Y)
     D=[[0 for i in range(l1+1)] for i in range(l2+1)]
     D[0][0]=0
     for i in range(1,l1+1):
         D[0][i]=sys.maxint
     for j in range(1,l2+1):
         D[j][0]=sys.maxint
     for j in range(1,l2+1):
         for i in range(1,l1+1):
             D[j][i]=M[j-1][i-1]+Min(D[j-1][i],D[j][i-1],D[j-1][i-1]+M[j-1][i-1])
'''



if __name__=='__main__':

    tra1,tra2=Get_Prime_GpsData(".\\GPS_Get_PreProcesser\\10-21-2015\\locationGPS.txt",".\\GPS_Get_PreProcesser\\10-20-2015\\locationGPS.txt")
    testdtw(tra1,tra2)

    tra3,tra4=Get_Prime_GpsData(".\\GPS_Get_PreProcesser\\7-18-2015\\locationGPS.txt",".\\GPS_Get_PreProcesser\\10-20-2015\\locationGPS.txt")
    testdtw(tra3,tra4)
