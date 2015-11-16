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
from label_add_time import GetSemanticGPSpath
def create_model():
    fullpath=GetSemanticGPSpath()
    train_set=[]
    for file in fullpath:
        filename=file.replace('semanticGPS.txt','RClabelTime.txt')  #这里可以修改是用啥子文件名，就是说用是miss_label后的还之前的
        tempdata=np.loadtxt(filename,dtype=str,delimiter=',',usecols=(0,1,3)) #label,starttime,continuetime
        for i in range(len(tempdata)):
            tempword=[]
            s=tempdata[i][0]+'_'+(tempdata[i][0]).replace(' ','_')+'_'+tempdata[i][0]
            tempword.append(s)
            train_set.append(tempword)

    dic = corpora.Dictionary(train_set)
    corpus = [dic.doc2bow(text) for text in train_set]
    tfidf = models.TfidfModel(corpus)
    corpus_tfidf = tfidf[corpus]
    lda = models.LdaModel(corpus_tfidf, id2word = dic, num_topics = 27)
    corpus_lda = lda[corpus_tfidf]
    lda.save("SemanticLda"+str(27)+".txt")
    dic.save("SemanticDic"+str(27)+".txt")
    tfidf.save("SemanticTFIDF"+str(27)+".txt")
    return  lda,dic,tfidf



if __name__=='__main__':
    create_model()