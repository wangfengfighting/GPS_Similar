#coding: utf-8
__author__ = 'WangFeng'

'''
1.首先循环读出滤波后的文件，然后依次遍历？计算distance和给定的距离阈值相比较，这样就可以知道是属于啥语义信息的
2.也可以首先计算聚类后的结果，然后把聚类中心拿来做比较，这样就可以计算出每一个聚类结果的文本信息，后续就是计算他们的in  out 时间
3.也可以先找到stop point 在根据这些来找标签
'''
from Find_stop_points import stop_points
def calculate_stop_point_tag():
    fullpath=stop_points.getfullfilepath()
    for temppath in fullpath:
        #print(temppath)
        Now_stop_point=stop_points.get_filtered_gps_stop_point(temppath)
        if len(Now_stop_point)!=0:
            for stopint in Now_stop_point:

        #print(Now_stop_point)
        #print('\n')

def calculate_stop_pointstag(stopint):
    sum_lat=0.0
    sum_long=0.0
    for item_item in  stopint:
        sum_lat+=item_item[0]
        sum_long+=item_item[1]
    return sum_lat/len(stopint),sum_long/len(stopint)#计算每个stop point 列表的中心点



if __name__=='__main__':
    calculate_stop_point_tag()