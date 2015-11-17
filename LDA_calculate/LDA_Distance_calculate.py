# coding: utf-8
__author__ = 'WangFeng'
'''
这个文件的作用是：计算基于LDA的similar，首先是计算词袋的向量距离，再是计算cos向量的相似度
'''
import pandas as pd
import numpy as np
import jieba
from gensim import corpora,models,similarities
import math
import datetime
from label_add_time import GetSemanticGPSpath
def create_model(labelFileName):
    fullpath=GetSemanticGPSpath()
    train_set=[]
    onday=[]
    for file in fullpath:  #一个file 就是一天的数据路径，也就是一天的数据,外层一个for循环就是 写找完一天的记录
        filename=file.replace('semanticGPS.txt',labelFileName)  #这里可以修改是用啥子文件名，就是说用是miss_label后的还之前的
        ondaydata=np.loadtxt(filename,dtype=str,delimiter=',',usecols=(0,1,3)) #label,starttime,continuetime
        tempsentence=[]
        for i in range(len(ondaydata)):
            datasstrip=ondaydata[i][1].split(' ')
            word=ondaydata[i][0]+'_'+datasstrip[0]+'_'+time2hour(datasstrip[1])+'_'+str(int(ondaydata[i][2])//(10*60))
            tempsentence.append(word)
        train_set.append(tempsentence)
    #print(train_set[0])
    dic = corpora.Dictionary(train_set)
    corpus = [dic.doc2bow(text) for text in train_set]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lda = models.LdaModel(corpus_tfidf, id2word = dic, num_topics = 24)
    corpus_lda = lda[corpus_tfidf]
    lda.save("SemanticLda"+str(24)+".txt")
    dic.save("SemanticDic"+str(24)+".txt")
    tfidf.save("SemanticTFIDF"+str(24)+".txt")
    return  lda,dic,tfidf,train_set,[]

def time2hour(strtime):
    d=datetime.datetime.strptime(strtime,'%H:%M:%S')
    return  str((d).hour)

def LDAInference(lda,dic,tfidf,sentence):
    sentence = dic.doc2bow(sentence)
    sentence = tfidf[sentence]
    prob = lda.inference([sentence])
    prob = prob[0][0]
    prob = prob / prob.sum()
    return prob
def find_max_LDA():
    lda,dic,tfidf,trainset,onday=create_model()
    prob_predict=LDAInference(lda,dic,tfidf,onday)
    print(onday)
    print(trainset[0:6])
    prob_train=LDAInference(lda,dic,tfidf,list(trainset[i][0] for i in range(6)))
    fenzi=np.dot(prob_predict,prob_train)
    fenmu=math.sqrt(np.dot(prob_predict,prob_predict))*math.sqrt(np.dot(prob_train,prob_train))
    temp_lda=fenzi/fenmu
    print(temp_lda)


def test_find_max_LDA():
    lda,dic,tfidf,trainset,onday=create_model('RClabelTime.txt')
    groupA,groupB=getpeople()
    for i in range(len(groupA)):
        prob_predict=LDAInference(lda,dic,tfidf,day2sentence(groupA[i]))
        prob_train=LDAInference(lda,dic,tfidf,day2sentence(groupB[i]))
        fenzi=np.dot(prob_predict,prob_train)
        fenmu=math.sqrt(np.dot(prob_predict,prob_predict))*math.sqrt(np.dot(prob_train,prob_train))
        temp_lda=fenzi/fenmu
        print temp_lda,(groupA[i]).split('\\')[4],(groupB[i]).split('\\')[4]

def day2sentence(daypath):
    UserData=[]
    data=np.loadtxt(daypath,dtype=str,delimiter=',',usecols=(0,1,3))
    for i in range(len(data)):
            datasstrip=data[i][1].split(' ')
            word=data[i][0]+'_'+datasstrip[0]+'_'+time2hour(datasstrip[1])+'_'+str(int(data[i][2])//(10*60))
            UserData.append(word)
    return UserData

def  getpeople():
     fullpath=GetSemanticGPSpath()
     fullpath=[fullpath[i].replace('semanticGPS.txt','RClabelTime.txt') for i in range(len(fullpath))]
     fullpath.sort()
     print(fullpath)
     groupA=fullpath[0:7]
     groupB=fullpath[10:17]
     return groupA,groupB

if __name__=='__main__':
    #create_model('RClabelTime.txt')
    #find_max_LDA()
    #getpeople()
    test_find_max_LDA()
