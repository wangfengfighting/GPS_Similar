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
from Calculate_semantic_of_point import depart_same_seq
dic=open('labelDic.pkl','rb')    #打开文件
labeldict= pickle.load(dic)
def caculLCS():
    labelPath=GetLabelFile()
    for i in range(0,len(labelPath)-1):
        for j in range(i+1,len(labelPath)):
            seqi=label2number(labelPath[i])
            namei=labelPath[i].split('\\')[4]
            seqj=label2number(labelPath[j])
            namej=labelPath[j].split('\\')[4]
            length, path = mlpy.lcs_std(seqi,seqj)
            Write_LCS_Ans([namei,namej,length])

    # for index in range(0,len(labelPath)-2):
    #     print labelPath[index].split('\\')[4]   #文件夹的name
    #     seq1=label2number(labelPath[index])
    #     seq2=label2number(labelPath[index+1])
    #     # print(seq1)
    #     # print seq2
    #     length, path = mlpy.lcs_std(seq1,seq2)
    #     print '---------------------------'+str(length)+'-----------------------'


        #length, path = mlpy.lcs_std(seq1,seq2)
        #print length,path[0]


def label2number(TempPath):
    tempPath=TempPath.replace('semanticGPS_stoppoint.txt','semanticGPS.txt')
    #print tempPath
    templabel=[]
    labeldf=np.loadtxt(tempPath,dtype=str,delimiter=',',usecols=(5,))
    labeldf_removeRE=depart_same_seq(labeldf)
    for item in labeldf_removeRE:
        if item in labeldict:
            templabel.append(labeldict[item])
            #else: #label 没有在现有的里面找到
            #templabel.append(88888)
    return templabel

def  Write_LCS_Ans(lcsLength):
    lcsFile=open('LCS_Length.txt','a')
    lcsFile.write(lcsLength[0])
    lcsFile.write(',')
    lcsFile.write(lcsLength[1])
    lcsFile.write(',')
    lcsFile.write(str(lcsLength[2]))
    lcsFile.write('\n')
    lcsFile.close()



def number2label(numSeq):
    labelSeq=[]

if __name__=='__main__':
    caculLCS()
