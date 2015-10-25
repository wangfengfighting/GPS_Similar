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

    x1=[[28.228225, 1],[28.228168,1]]
    y1=[112.999492,112.999898]
    x2=[[28.228047,1],[28.228062,1]]
    y2=[112.999500,112.999898]
    z1=solveline(x1,y1)
    z2=solveline(x2,y2)
    x_ans=solve("%s*x+%s=%s*x+%s"%(z1[0],z1[1],z2[0],z2[1]))
    print x_ans
    print  z1[0]*x_ans+z1[1]
    print  z2[0]*x_ans+z2[1]

    print (sum(np.array(x1))+sum(np.array(x2)))/4,(sum(np.array(y1))+sum(np.array(y2)))/4