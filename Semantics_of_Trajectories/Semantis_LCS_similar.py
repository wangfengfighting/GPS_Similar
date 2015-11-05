# coding: utf-8
__author__ = 'WangFeng'
'''
利用已经生成的一天的语义位置列表，user1=[a,b,c,d,e,f,g,h,i]  user2=[a,b,c,d,e,f,g,h,i]
采用LCS（Longest Common Subsequence ）来实现求解最长公子序列的算法。
查找 LCS 是计算两个序列相似程度的一种方法：LCS 越长，两个序列越相似。
'''
import numpy as np
import mlpy
user1=['road','103','pdl','road','pdl','road','pdl','road','baskball_5','road']
user2=['103''road','101','pdl','road','102','gym_101','103','road','pdl','road','pdl','road','102','east_door3']
a=[1,2,3,2,4,1,2]
b=[2,4,3,1,2,1]

length, path = mlpy.lcs_std(a,b)
print(length)
print(path)
