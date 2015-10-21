__author__ = 'WangFeng'
'''
using mean and use the pre-data of windows size of data from now
'''
# coding: utf-8
import copy
def  mean_filter(point,windowsize):
    point_filtered=copy.deepcopy(point)
    print(point)
    for section in range(windowsize+1,len(point)):
        mean=(point[section-1:section-windowsize-1:-1])
        MEAN=(mean[0]*0.1+mean[1]*0.2+mean[2]*0.2+mean[3]*0.5)
        point_filtered[section]=MEAN
    print((point_filtered))
    return point_filtered
