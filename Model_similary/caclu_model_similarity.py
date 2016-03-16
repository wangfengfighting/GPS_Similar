# coding: utf-8
__author__ = 'lym'
from getDir import GetDirName
import os
import math
def calculateModelSimilarity():
    getdir=GetDirName()
    Fulldirlist=[]
    parent_path = os.path.dirname(os.getcwd())
    #print(parent_path)
    dirlist=getdir.printPath(parent_path+os.sep+"starlog")
    usernameGroup=dirlist
    print (dirlist)

    # for dir in dirlist:
    #     #print(dir)
    #     seconddir=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+dir))
    #     for secdir in seconddir:
    #        Fulldirlist.append(parent_path+os.sep+"starlog"+os.sep+dir+os.sep+secdir+os.sep+'appriori_sequence.csv')

def getFolderNum(username):
    getdir=GetDirName()
    dirlist=getdir.printPath(username)
    print(dirlist)


def frequence_mod_sim(user1,user2):
    getdir=GetDirName()
    parent_path = os.path.dirname(os.getcwd())
    user1Floder=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+user1))
    user2Floder=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+user2))
    user1filepath=parent_path+os.sep+"starlog"+os.sep+os.sep+user1+os.sep
    user2filepath=parent_path+os.sep+"starlog"+os.sep+os.sep+user2+os.sep
    num_floder=len(user1Floder) if len(user1Floder)<=len(user2Floder) else len(user2Floder)
    for Floderindex in range(num_floder):
        t_u1_file=user1filepath+user1Floder[Floderindex]+os.sep+'itemfrequence.txt'   #get use's itemfrequence data to caclulate simliarty
        t_u2_file=user2filepath+user2Floder[Floderindex]+os.sep+'itemfrequence.txt'


    print(user1Floder)
    print(user2Floder)

def itemEN(lista,listb):    #The calculated information entropy sequence
    jiaoji=list (set(lista)&set(listb))
    en=0
    for item in jiaoji:
        print (item)
        print lista.count(item)
        print listb.count(item)
        print (len(lista)+len(listb))
        pi = float( lista.count(item)+listb.count(item)) /  (len(lista)+len(listb))
        print pi
        if pi !=0.0:
            en+= (    -pi*math.log(pi)       )
        else:
            en+=0.0

    sim=en*len(jiaoji)/(len(lista)+len(listb))
    #print(en)

    return en,sim



if __name__=='__main__':
    #calculateModelSimilarity()
    frequence_mod_sim('u001','u001')