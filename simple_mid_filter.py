__author__ = 'WangFeng'
'''
use simple mid filter to Filter gps data points and return filtered_points in list[]
'''
# coding: utf-8

def filter(point,windows):
    filtered_point=[]
    global  mid_p
    if (windows%2)==0:
        mid_p=windows/2-1
    else:
        mid_p=windows/2
    for section in range(0,len(point)/windows):
        temp=point[section*windows:(section+1)*windows]
        temp_temp=sorted(temp)
        temp[mid_p]=temp_temp[mid_p]
        point[section*windows:(section+1)*windows]=temp[:]
    return point


