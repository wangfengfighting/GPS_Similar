# coding: utf-8
__author__ = 'WangFeng'
'''
主要是找出每个聚类结果的的点语义信息，把轨迹序列语义化，返回的是一个列表[[纬度，经度，tag],........[]..]
'''
import  numpy as np
import pandas as pd
def Compute_center_of_budling():
    center_of_budling=[]
    gpsdata=np.loadtxt(".\\TAG_file.txt", dtype=str, delimiter=',', skiprows=1,usecols=(2,))
    #print(gpsdata)
    ds=pd.read_table("TAG_file.txt",delimiter=',')
    ds['index_all']=pd.Series(range(len(ds)),index=ds.index)
    #print(ds)
    gps_tag=set((gpsdata))
    for tag_key in gps_tag:
        #print tag_key
        building_area=ds.query('tag=="%s"'%(tag_key))
        #print((building_area['lat'][(building_area['index_all']).tolist()]))
        temp_centre=[ sum (  np.array(building_area['lat'][(building_area['index_all']).tolist()]) )/len(building_area),
                      sum (  np.array(building_area['long'][(building_area['index_all']).tolist()]) )/len(building_area)]#计算平均值 利用平均值来找中心点
        temp_centre.append(tag_key)
        center_of_budling.append(temp_centre)

    return center_of_budling  #[[28.226690250000001, 113.00321249999999, 'phd_mess'].....]]


if __name__=='__main__':
    print Compute_center_of_budling()
