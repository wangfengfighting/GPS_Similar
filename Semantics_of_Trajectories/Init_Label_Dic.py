# coding: utf-8
__author__ = 'WangFeng'

from getDir import GetDirName
import os
import numpy as np
import pickle
def GetLabelFile():
    getdir=GetDirName()
    Fulldirlist=[]
    parent_path = os.path.dirname(os.getcwd())
    dirlist=getdir.printPath(parent_path+"\\GPS_Get_PreProcesser")
    for dir in dirlist:
        Fulldirlist.append(parent_path+"\\GPS_Get_PreProcesser"+"\\"+dir+"\\"+'semanticGPS_stoppoint.txt')
    return Fulldirlist

def InitDictionary():
    labelDic={}
    label_value=0
    SemanticPath=GetLabelFile()
    for TempPath in SemanticPath:
        print TempPath
        labeldf=np.loadtxt(TempPath,dtype=str)
        for tempLabel in labeldf:
            if  tempLabel not in labelDic:
                labelDic[tempLabel]=label_value
                label_value+=1
    output = open('labelDic.pkl', 'wb')
    pickle.dump(labelDic, output)
    output.close()




if __name__=='__main__':
    print GetLabelFile()
    InitDictionary()
    # a=open('labelDic.pkl','rb')    #打开文件
    # k= pickle.load(a)
    #print(k)
    #print(k['road'])