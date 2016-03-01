__author__ = 'WangFeng'
#coding: utf-8
import numpy as np
from getDir import GetDirName
import os
from fp_growth import find_frequent_itemsets
def getAll_label2dic():
    getdir=GetDirName()
    Fulldirlist=[]
    parent_path = os.path.dirname(os.getcwd())
    print(parent_path)
    dirlist=getdir.printPath(parent_path+os.sep+"starlog")
    print(dirlist)
    for dir in dirlist:
        #print(dir)
        seconddir=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+dir))
        for secdir in seconddir:
            Fulldirlist.append(parent_path+os.sep+"starlog"+os.sep+dir+os.sep+secdir+os.sep+'RCed_stoppoint.txt')  #Fulldirlist 是的地方的的的飞艾丝凡安吉拉广发分撒娇课历史的高考了收到就会公司加快的更好
            #  #print(Fulldirlist)  Fulldirlist is all of the user's label tag path


    #############this work want to canculate the dictionary of full label tags,which is like (pdl, bedroom ....) ---> ('1','2'......)
    ############# thus the list could be used to find the frequency item(trajectory model) from user, then translate the item ser to label set
    # order by dictionary ('1','2'......)--->(pdl, bedroom ....)
    allLabelSet=[]
    allLabelDic={}
    for filePath in Fulldirlist:
        labelTag=np.loadtxt(filePath,dtype=str,delimiter=',',usecols=(4,))
        taglist=list(set(labelTag))
        for item in taglist:
            if item not in allLabelSet:
                allLabelSet.append(item)
    for index in range(len(allLabelSet)):
        allLabelDic[allLabelSet[index]]=str(index)

    return allLabelSet,allLabelDic


def getFrequentItem(filepath,labelDic):
    labelTag=np.loadtxt(filepath,dtype=str,delimiter=',',usecols=(4,))
    dic_labelTag=[]
    for item in labelTag:
        if item in labelDic.keys():
            dic_labelTag.append(labelDic[item])

    frequentSet=[]  #frequentSet is the set of frequent item,like:[[['1'], 4], [['2', '1'], 4]] first is frequent tag,second is the support dgree.
    for itemset, support in find_frequent_itemsets(dic_labelTag, 4, True):
        frequentSet.append([itemset,support])

    return dic_labelTag,frequentSet

if __name__=='__main__':

    print getAll_label2dic()