# coding: utf-8
__author__ = 'WangFeng'
'''
主要是找出每个聚类结果的的点语义信息，把轨迹序列语义化
'''
import  numpy as np
import pandas as pd
def Compute_center_of_budling():
    gpsdata=np.loadtxt("TAG_file.txt", dtype={'names': ['lat', 'long', 'tag'] ,'formats': ['f', 'f', 'S12']},
                       delimiter=',', skiprows=1,usecols=(0,1,2))
    #print(gpsdata)


    ds=pd.read_table("TAG_file.txt",delimiter=',')
    print(pd.read_sql_query("select * FROM DATA WHERE tag=pdl",ds))

if __name__=='__main__':
    Compute_center_of_budling()
