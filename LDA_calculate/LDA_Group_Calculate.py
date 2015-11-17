# coding: utf-8
__author__ = 'WangFeng'
'''
这个文件的功能是：对 u000  u001 之类的整体的用户  计算他们之间的形似度。lda
'''
import pandas as pd
import numpy as np
import jieba
from gensim import corpora,models,similarities
import math
from label_add_time import GetSemanticGPSpath
import datetime
def create_model(labelFileName='RClabelTime.txt'):
    FileName=[]
    from getDir import GetDirName
    import os
    getdir=GetDirName()
    parent_path = os.path.dirname(os.getcwd())
    AllUserFiles,AllFiles,other=getdir.getUserFiles(parent_path+'\\'+'starlog')
    for path_file in other:
        for i in range(len(path_file)):
            path_file_name=parent_path+path_file[i]+os.sep+labelFileName
            FileName.append(path_file_name)

    train_set=[]
    for file in FileName:  #一个file 就是一天的数据路径，也就是一天的数据,外层一个for循环就是 写找完一天的记录
        ondaydata=np.loadtxt(file,dtype=str,delimiter=',',usecols=(0,1,3)) #label,starttime,continuetime
        tempsentence=[]
        for i in range(len(ondaydata)):
            datasstrip=ondaydata[i][1].split(' ')
            word=ondaydata[i][0]+'_'+datasstrip[0]+'_'+time2hour(datasstrip[1])+'_'+str(int(ondaydata[i][2])//(10*60))
            tempsentence.append(word)
        train_set.append(tempsentence)

    dic = corpora.Dictionary(train_set)
    corpus = [dic.doc2bow(text) for text in train_set]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lda = models.LdaModel(corpus_tfidf, id2word = dic, num_topics = 24)
    corpus_lda = lda[corpus_tfidf]
    lda.save(".\\LDA_all_27\\SemanticLda"+str(24)+".txt")
    dic.save(".\\LDA_all_27\\SemanticDic"+str(24)+".txt")
    tfidf.save(".\\LDA_all_27\\SemanticTFIDF"+str(24)+".txt")
    return  lda,dic,tfidf,train_set,[]

def time2hour(strtime):
    d=datetime.datetime.strptime(strtime,'%H:%M:%S')
    return  str((d).hour)

if __name__=='__main__':
    create_model()