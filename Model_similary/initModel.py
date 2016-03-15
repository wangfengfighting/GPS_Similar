__author__ = 'WangFeng'
#coding: utf-8
import numpy as np
from getDir import GetDirName
import os
from fp_growth import find_frequent_itemsets
import pickle
import csv
from apriori_git import *
from itertools import izip
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
    output=open('alllabelDic.pkl','wb')
    pickle.dump(allLabelDic,output)
    return allLabelSet,allLabelDic


def getFrequentItem(filepath):
    dicfile=file('alllabelDic.pkl','rb')
    labelDic=pickle.load(dicfile)
    invertlabelDic=dict(izip(labelDic.itervalues(),labelDic.iterkeys()))

    dic_labelTag=[]
    # labelTag=np.loadtxt(filepath,dtype=str,delimiter=',',usecols=(4,))
    # dic_labelTag=[]
    # for item in labelTag:
    #     if item in labelDic.keys():
    #         #print (labelDic[item])
    #         dic_labelTag.append(labelDic[item])
    # print(dic_labelTag)
    # frequentSet=[]  #frequentSet is the set of frequent item,like:[[['1'], 4], [['2', '1'], 4]] first is frequent tag,second is the support dgree.
    # for itemset, support in find_frequent_itemsets(dic_labelTag, 4, True):
    #     #frequentSet.append([itemset,support])
    #     print itemset,support


    labelTag=np.loadtxt(filepath,dtype=str,delimiter=',',usecols=(3,4))
    time=1
    while time<=48:
        tempLabel=[]
        for item in labelTag:

            labtltime=str2timeNum(item[0]) # here labeltime is a number as we cut one hour into two pices of time(30 min)
            if labtltime>= (time-1)*30 and labtltime<=time*30:
                if item[1] in labelDic.keys():
                    tempLabel.append(labelDic[item[1]])
                else:
                    tempLabel.append('999999999')
        if tempLabel:
            dic_labelTag.append(tempLabel)
        time+=1

    #print(dic_labelTag)
    # dic_labelTag=[]
    # for item in labelTag:
    #     if item in labelDic.keys():
    #         #print (labelDic[item])
    #         dic_labelTag.append(labelDic[item])
    # print(dic_labelTag)
    frequentSet=[]  #frequentSet is the set of frequent item,like:[[['1'], 4], [['2', '1'], 4]] first is frequent tag,second is the support dgree.
    for itemset, support in find_frequent_itemsets(dic_labelTag,0.2, True):
        frequentSet.append([itemset,support])


    savefile=open(filepath.replace('RCed_stoppoint.txt','itemfrequence.txt'),'w')
    for item, support in sorted(frequentSet, key=lambda (item, support): support):
        #print item,support
        if len(item)==1:
            savefile.write(invertlabelDic[item[0]])
            savefile.write('\n')
        else:
            for index in range(len(item)-1):
                savefile.write(invertlabelDic[item[index]])
                savefile.write(',')
            savefile.write(invertlabelDic[item[len(item)-1]]    )
            savefile.write('\n')
    savefile.close()








    return dic_labelTag,frequentSet

def str2timeNum(str):
    timestr=str.split(' ')[1]
    temp=timestr.split(':')
    #print(temp)
    timeNum=int(temp[0])*60+int(temp[1])*1
    return  timeNum


def getSequenceItem(filepath):  #get sequence pattern mining
    dicfile=file('alllabelDic.pkl','rb')
    labelDic=pickle.load(dicfile)
    dic_labelTag=[]   #dic_labelTag is the all translated semantics label like ['1','2',.....] from ['bedroom','pdl'....]
    labelTag=np.loadtxt(filepath,dtype=str,delimiter=',',usecols=(3,4))
    time=1
    while time<=48:
        tempLabel=[]
        for item in labelTag:

            labtltime=str2timeNum(item[0]) # here labeltime is a number as we cut one hour into two pices of time(30 min)
            if labtltime>= (time-1)*30 and labtltime<=time*30:
                if item[1] in labelDic.keys():
                    tempLabel.append(labelDic[item[1]])
                else:
                    tempLabel.append('999999999')
        if tempLabel:
            dic_labelTag.append(tempLabel)
        time+=1


def initAprioriitem():
    getdir=GetDirName()
    Fulldirlist=[]
    parent_path = os.path.dirname(os.getcwd())
    #print(parent_path)
    dirlist=getdir.printPath(parent_path+os.sep+"starlog")
    #print(dirlist)
    for dir in dirlist:
        #print(dir)
        seconddir=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+dir))
        for secdir in seconddir:
            Fulldirlist.append(parent_path+os.sep+"starlog"+os.sep+dir+os.sep+secdir+os.sep+'RCed_stoppoint.txt')


    for path in Fulldirlist:
        data=np.loadtxt(path,dtype=str,delimiter=',',usecols=(3,4))
        data_moring=[]
        data_noon=[]
        data_night=[]
        i=1
        for item in data:

            labtltime=str2timeNum(item[0]) # here labeltime is a number as we cut one hour into two pices of time(30 min)
            if labtltime>=0 and labtltime <=8*60:   #item is ['2015-07-07 00:00:00', '5_bedroom']
                data_moring.append(item[1])
            elif labtltime >8*60 and labtltime<= 16*60:
                data_noon.append(item[1])
            elif labtltime >16*60 and labtltime< 24*60:
                data_night.append(item[1])
        # print(data_night)
        # print(data_moring)
        savefile=open(path.replace('RCed_stoppoint.txt','appriori_sequence.csv'),'wb')
        SaveFile=csv.writer(savefile)
        SaveFile.writerow(data_moring)
        SaveFile.writerow(data_noon)
        SaveFile.writerow(data_night)
        savefile.close()


def getAprioriItem(minSupport=0.5,minConfidence=0.8):  #minSupport=0.5,minConfidence=0.8
    getdir=GetDirName()
    Fulldirlist=[]
    parent_path = os.path.dirname(os.getcwd())
    #print(parent_path)
    dirlist=getdir.printPath(parent_path+os.sep+"starlog")
    #print(dirlist)
    for dir in dirlist:
        #print(dir)
        seconddir=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+dir))
        for secdir in seconddir:
            Fulldirlist.append(parent_path+os.sep+"starlog"+os.sep+dir+os.sep+secdir+os.sep+'appriori_sequence.csv')
    #print(Fulldirlist)

    for infile in Fulldirlist: #infile is the path of appriori_sequence.csv
        #print(infile)
        sequence_Frequence=[]
        inFile = dataFromFile(infile)
        items, rules = runApriori(inFile, minSupport, minConfidence)
        #printResults(items, rules)
        savefile=open(infile.replace('appriori_sequence.csv','sequencefrequence.txt'),'w')
        for item, support in sorted(items, key=lambda (item, support): support):
            #print "item: %s , %.3f" % (str(item), support)
            seitem=list(item)
            if len(seitem)>1:
                sequence_Frequence.append(seitem)
                for index in range(len(seitem)-1):
                    savefile.write(seitem[index])
                    savefile.write(',')
                savefile.write(seitem[len(seitem)-1])
                savefile.write('\n')


        #savefile=open(infile.replace('appriori_sequence.csv','sequencefrequence.txt'),'w')
        # for subitem in
        # savefile.write(str(sequence_Frequence))
        # savefile.close()
    #return sequence_Frequence














if __name__=='__main__':
    #initAprioriitem()

    #print getAll_label2dic()

    getdir=GetDirName()
    Fulldirlist=[]
    parent_path = os.path.dirname(os.getcwd())
    #print(parent_path)
    dirlist=getdir.printPath(parent_path+os.sep+"starlog")
    #print(dirlist)
    for dir in dirlist:
        #print(dir)
        seconddir=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+dir))
        for secdir in seconddir:
            Fulldirlist.append(parent_path+os.sep+"starlog"+os.sep+dir+os.sep+secdir+os.sep+'RCed_stoppoint.txt')


    for i in Fulldirlist:
        print(i)
        dic_labelTag,frequentSet= getFrequentItem(i)




    # dic_labelTag,frequentSet= getFrequentItem('/home/lym/workspace/GPS_Similar/starlog/u001/8-29-2015/RCed_stoppoint.txt')
    # print(dic_labelTag)
    # print(frequentSet)
    # str2timeNum('2015-08-29 01:00:00')
    # print('begin.......')
    # getAprioriItem()
