# coding: utf-8
__author__ = 'WangFeng'
'''
利用已经生成的一天的语义位置列表，user1=[a,b,c,d,e,f,g,h,i]  user2=[a,b,c,d,e,f,g,h,i]
采用LCS（Longest Common Subsequence ）来实现求解最长公子序列的算法。
查找 LCS 是计算两个序列相似程度的一种方法：LCS 越长，两个序列越相似。
'''
import numpy as np
import mlpy
import pickle
from Init_Label_Dic import *

dic=open('labelDic.pkl','rb')    #打开文件
labeldict= pickle.load(dic)
def caculLCS():
    labelPath=GetLabelFile()
    for index in range(0,len(labelPath)-2):
        seq1=label2number(labelPath[index])
        seq2=label2number(labelPath[index+1])
        print(seq1)
        print seq2
        length, path = mlpy.lcs_std(seq1,seq2)
        print '---------------------------'+str(length)+'-----------------------'


        #length, path = mlpy.lcs_std(seq1,seq2)
        #print length,path[0]


def label2number(TempPath):
    TempPath=TempPath.replace('semanticGPS_stoppoint.txt','semanticGPS.txt')
    templabel=[]
    labeldf=np.loadtxt(TempPath,dtype=str,usecols=(5,))
    for item in labeldf:
        if item in labeldict:
            templabel.append(labeldict[item])
        else: #label 没有在现有的里面找到
            templabel.append(88888)
    return templabel

def number2label(numSeq):
    labelSeq=[]

if __name__=='__main__':
    caculLCS()
