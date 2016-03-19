# coding: utf-8
__author__ = 'lym'
'''
this function is used to  sequence pattern mining
run collect_all2one() the user all sequence_pattern.txt will collect into one file allsequencepattern.txt
and use 'MyPrefixSpan.py' to find out the users' sequence pattern then write into file 'usersequencepattern.txt'
'''
import numpy as np
from getDir import GetDirName
import os
import MyPrefixSpan
import util as u
def getSequencePattern(filepath):

    labelTag=np.loadtxt(filepath,dtype=str,delimiter=',',usecols=(3,4))
    time=1
    savefile=open(filepath.replace('RCed_stoppoint.txt','sequence_pattern.txt'),'w')
    while time<=24:  # we split one day into 12 pices .
        tempLabel=[]
        for item in labelTag:

            labtltime=str2timeNum(item[0]) # here labeltime is a number as we cut one hour into two pices of time(30 min)
            if labtltime>= (time-1)*60 and labtltime<=time*60:

                if not tempLabel:
                    tempLabel.append(item[1])

                else:
                    if tempLabel[-1]!=item[1]:

                        tempLabel.append(item[1])

        time+=1

        if len(tempLabel)==1:
            savefile.write(tempLabel[0])
            savefile.write('\n')
        elif len(tempLabel)==0:
            pass
        else:
            for index in range(len(tempLabel)-1):
                savefile.write(tempLabel[index])
                savefile.write(',')
            savefile.write(tempLabel[len(tempLabel)-1]   )
            savefile.write('\n')
    savefile.close()

def collect_all2one():

    ###################here we collect all of day's data and shows into one file#############
    getdir=GetDirName()
    Fulldirlist=[]
    parent_path = os.path.dirname(os.getcwd())
    dirlist=getdir.printPath(parent_path+os.sep+"starlog")
    for dir in dirlist:
        seconddir=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+dir))
        for secdir in seconddir:
            Fulldirlist.append(parent_path+os.sep+"starlog"+os.sep+dir+os.sep+secdir+os.sep+'sequence_pattern.txt')
    resultPath=[]
    for s in Fulldirlist:

        temppath=s[0:s[0:s.rfind(os.sep)].rfind(os.sep)]+os.sep+'allsequencepattern.txt'
        resultPath.append(temppath)
        output=open(temppath,'a')
        for line in open(s,'r'):
            output.writelines(line)
        output.close()
    resultFloder=list(set(resultPath))
    detect_Sequencepattern(resultFloder)


def str2timeNum(str):
    timestr=str.split(' ')[1]
    temp=timestr.split(':')
    #print(temp)
    timeNum=int(temp[0])*60+int(temp[1])*1
    return  timeNum
def detect_Sequencepattern(resultFloder,min_support=0.05):
    for floderPatn in resultFloder:
        tempfloderPatn=floderPatn.replace('allsequencepattern.txt','usersequencepattern.txt')
        MyPrefixSpan.detectpattern(floderPatn,tempfloderPatn,min_support)




if __name__=='__main__':
    collect_all2one()



    # getdir=GetDirName()
    # Fulldirlist=[]
    # parent_path = os.path.dirname(os.getcwd())
    # dirlist=getdir.printPath(parent_path+os.sep+"starlog")
    # for dir in dirlist:
    #     seconddir=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+dir))
    #     for secdir in seconddir:
    #         Fulldirlist.append(parent_path+os.sep+"starlog"+os.sep+dir+os.sep+secdir+os.sep+'RCed_stoppoint.txt')
    #
    # for i in Fulldirlist:
    #     print(i)
    #     getSequencePattern(i)