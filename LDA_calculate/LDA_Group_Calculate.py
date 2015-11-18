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
import os
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

    return  lda,dic,tfidf,train_set,AllUserFiles

def LDAInference(lda,dic,tfidf,sentence):
    sentence = dic.doc2bow(sentence)
    sentence = tfidf[sentence]
    prob = lda.inference([sentence])
    prob = prob[0][0]
    prob = prob / prob.sum()
    return prob

def find_max_LDA(lda,dic,tfidf,userGroup,labelFileName='RClabelTime.txt'):
    # 两个for循环 就把group 内的用户组给循环完毕
    final=[]
    for UserNameIndex in range(len(userGroup)):
        for UserNameIndexNext in range(UserNameIndex+1,len(userGroup)):
            avg=[]
            for dayindex in range   (       len(userGroup[UserNameIndex]) if len(userGroup[UserNameIndex])<=len(userGroup[UserNameIndexNext])
            else  len(userGroup[UserNameIndexNext])   ):
                prob_a=LDAInference(lda,dic,tfidf,day2sentence(userGroup[UserNameIndex][dayindex]+os.sep+labelFileName  )     )
                prob_b=LDAInference(lda,dic,tfidf,day2sentence(userGroup[UserNameIndexNext][dayindex]+os.sep+labelFileName))
                fenzi=np.dot(prob_a,prob_b)
                fenmu=math.sqrt(np.dot(prob_a,prob_a))*math.sqrt(np.dot(prob_b,prob_b))
                temp_lda=fenzi/fenmu
                avg.append(temp_lda)
            Average=sum(np.array(avg))/len(avg)
            final.append( [ (userGroup[UserNameIndex][0]).split('\\')[4],(userGroup[UserNameIndexNext][0]).split('\\')[4],Average])
                # prob_predict=LDAInference(lda,dic,tfidf)
                # prob_train=LDAInference(lda,dic,tfidf,list(trainset[i][0] for i in range(6)))
                # fenzi=np.dot(prob_predict,prob_train)
                # fenmu=math.sqrt(np.dot(prob_predict,prob_predict))*math.sqrt(np.dot(prob_train,prob_train))
                # temp_lda=fenzi/fenmu
                # print(temp_lda)
    print(final)
    writeLDAans2file(final)

def writeLDAans2file(seq):
    file=open('LDAnetwork.txt','w+')
    for ans in seq:
        file.write(ans[0])
        file.write(',')
        file.write(ans[1])
        file.write(',')
        file.write(str(ans[2]))
        file.write('\n')

def day2sentence(daypath):
    UserData=[]
    data=np.loadtxt(daypath,dtype=str,delimiter=',',usecols=(0,1,3))
    for i in range(len(data)):
            datasstrip=data[i][1].split(' ')
            word=data[i][0]+'_'+datasstrip[0]+'_'+time2hour(datasstrip[1])+'_'+str(int(data[i][2])//(10*60))
            UserData.append(word)
    return UserData

def time2hour(strtime):
    d=datetime.datetime.strptime(strtime,'%H:%M:%S')
    return  str((d).hour)


def main():
    lda,dic,tfidf,trainset,other=create_model('RCedlabelTime.txt')
    find_max_LDA(lda,dic,tfidf,other,'RCedlabelTime.txt')
if __name__=='__main__':
    main()