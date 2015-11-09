__author__ = 'Administrator'
# coding: utf-8
import mlpy
import numpy as np
import time
import datetime
from distance_mean_filter import GetDistance


def solveline(x,y):
    x=np.array(x)
    y=np.array(y)
    z=np.linalg.solve(x,y)
    return z

def solve(eq,var='x'):
    eq1 = eq.replace("=","-(")+")"
    c = eval(eq1,{var:1j})
    return -c.real/c.imag



if __name__=='__main__':
    a='9-29-2015 07:14:56'
    b='9-29-2015 07:14:30'
    t1 = datetime.datetime.strptime('9-29-2015 07:14:56', '%m-%d-%Y %H:%M:%S')
    t2 = datetime.datetime.strptime('9-29-2015 07:14:30', '%m-%d-%Y %H:%M:%S')
    print (t1-t2).seconds

   # a=[1,1,1,2,2,3,4,4,5,5,3,3,5,5,6,6,7,7,9]
   # a.reverse()
   # temp=[]
   # templast=[]
   # while a:
   #      t1=a.pop()
   #      if not len(temp)==0:
   #          if t1==temp[len(temp)-1]:
   #              temp.append(t1)
   #              templast.append(t1)
   #          else:
   #             print temp.__str__()
   #             temp=[]
   #             templast=[]
   #             temp.append(t1)
   #             templast.append(t1)
   #      else:
   #          temp.append(t1)
   # print templast

   # for i in range(len(a)):
   #     t1=a.pop()
   #     if not len(temp)==0:
   #         if t1==temp[len(temp)-1]:
   #             temp.append(t1)
   #         else:
   #             print temp.__str__()
   #             temp=[]
   #             temp.append(t1)
   #     # elif i==len(a)-1:
   #     #     temp.append(t1)
   #     #     print temp.__str__()
   #     else:
   #         temp.append(t1)
