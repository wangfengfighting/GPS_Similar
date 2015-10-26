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
        stop_points.getfullfilepath()


if __name__=='__main__':
    calculate_stop_point_tag()