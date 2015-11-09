__author__ = 'Administrator'
# coding: utf-8
import mlpy
import numpy as np
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
   a=[1,1,1,2,2,3,3,5,4,4,6,6,7,7,7,8,8,8,8,8]
   a.reverse()
   temp=[]
   for i in range(len(a)):
       t1=a.pop()
       if not len(temp)==0:
           if t1==temp[len(temp)-1]:
               temp.append(t1)
           else:
               print temp.__str__()
               temp=[]
               temp.append(t1)
       # elif i==len(a)-1:
       #     temp.append(t1)
       #     print temp.__str__()
       else:
           temp.append(t1)
