# coding: utf-8
__author__ = 'lym'
from getDir import GetDirName
import os
import math
import numpy as np
def getUserFloderpath():
    getdir=GetDirName()
    Usernamepath=[]
    parent_path = os.path.dirname(os.getcwd())
    print(parent_path)
    dirlist=getdir.printPath(parent_path+os.sep+"starlog")
    usernameGroup=dirlist
    #print (dirlist)

    for dir in dirlist:
       # seconddir=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+dir))
        #for secdir in seconddir:
           Usernamepath.append(parent_path+os.sep+"starlog"+os.sep+dir)
    return (usernameGroup)

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

    similary_dgree=0.0
    for Floderindex in range(num_floder):
        t_u1_file=user1filepath+user1Floder[Floderindex]+os.sep+'itemfrequence.txt'   #get use's itemfrequence data to caclulate simliarty
        t_u2_file=user2filepath+user2Floder[Floderindex]+os.sep+'itemfrequence.txt'

        # if len(user1Floder)<=len(user2Floder):
        #     t_u1_file=user1filepath+user1Floder[Floderindex]+os.sep+'itemfrequence.txt'   #get use's itemfrequence data to caclulate simliarty
        #     t_u2_file=user2filepath+user2Floder[Floderindex+len(user2Floder)-len(user1Floder)]+os.sep+'itemfrequence.txt'
        # elif len(user1Floder)>len(user2Floder):
        #     t_u1_file=user1filepath+user1Floder[Floderindex+len(user1Floder)-len(user2Floder)]+os.sep+'itemfrequence.txt'   #get use's itemfrequence data to caclulate simliarty
        #     t_u2_file=user2filepath+user2Floder[Floderindex]+os.sep+'itemfrequence.txt'

        listuser1=[]
        listuser2=[]
        listinlisetuser1=[]
        listinlisetuser2=[]
        for line in open(t_u1_file):
            listuser1.extend(line.replace("\n","").split(','))
            listinlisetuser1.append(line.replace("\n","").split(','))
        for line in open(t_u2_file):
            listuser2.extend(line.replace("\n","").split(','))
            listinlisetuser2.append(line.replace("\n","").split(','))
        similary_dgree+=currentFileSim(listuser1,listuser2,listinlisetuser1,listinlisetuser2)

    return similary_dgree

def currentFileSim(list1,list2,listinlist1,listinlist2):
    sim=0.0
    for frequence_item in listinlist1:
        flog=False
        currentEN=0.0
        matchcount=0

        notfullmatch=0.0
        for compare_item in listinlist2:
            if cmp(sorted(frequence_item),sorted(compare_item))==0 and flog==False:
                currentEN=itemEN(list1,list2,frequence_item)
                flog=True
                matchcount+=1
            elif cmp(sorted(frequence_item),sorted(compare_item))==0 and flog==True:
                matchcount+=1
            elif cmp(sorted(frequence_item),sorted(compare_item))!=0:
                if len(list(set(frequence_item)&set(compare_item)))>0:
                    notfull=itemEN(list1,list2,list(set(frequence_item)&set(compare_item)))
                    l=len(set(frequence_item)&set(compare_item))
                    d=len(frequence_item)+len(compare_item)
                    notfullmatch+=notfull*l/d
                # notfull=itemEN(list1,list2,list(set(frequence_item)&set(compare_item)))
                # notfullmatch+=(len(set(frequence_item)&set(compare_item))/(len(frequence_item)+len(compare_item)))*notfull

            else:
                pass
        sim=matchcount*currentEN+notfullmatch
        #print(matchcount,currentEN)
    return sim




def itemEN(lista,listb,jiaoji):    #The calculated information entropy sequence
    en=0
    for item in jiaoji:
        # print (item)
        # print lista.count(item)
        # print listb.count(item)
        #print (len(lista)+len(listb))
        pi = float( lista.count(item)+listb.count(item)) /  (len(lista)+len(listb))
        #print pi
        if pi !=0.0:
            en+= (    -pi*math.log(pi)       )
        else:
            en+=0.0

    #sim=en*len(jiaoji)/(len(lista)+len(listb))
    #print(en)

    return en

#------------------------------------------caclulate sequence pattern similary----------------------------#
def sequence_mod_sim(user1,user2):
    parent_path = os.path.dirname(os.getcwd())
    se_user1_file=parent_path+os.sep+'starlog'+os.sep+user1+os.sep+'usersequencepattern.txt'
    se_user2_file=parent_path+os.sep+'starlog'+os.sep+user2+os.sep+'usersequencepattern.txt'
    listuser1=[]
    listuser2=[]
    listinlisetuser1=[]
    listinlisetuser2=[]
    for line in open(se_user1_file):
            listuser1.extend(line.replace("\n","").split(' ')[:len(line.replace("\n","").split(' '))-1:])
            listinlisetuser1.append(line.replace("\n","").split(' ')[:len(line.replace("\n","").split(' '))-1:])
    for line in open(se_user2_file):
            listuser2.extend(line.replace("\n","").split(' ')[:len(line.replace("\n","").split(' '))-1:])
            listinlisetuser2.append(line.replace("\n","").split(' ')[:len(line.replace("\n","").split(' '))-1:])
    similary_dgree=currentSequenceSim(listuser1,listuser2,listinlisetuser1,listinlisetuser2)
    return (similary_dgree)


def currentSequenceSim(list1,list2,listinlist1,listinlist2):
    sim=0.0
    for frequence_item in listinlist1:
        flog=False
        currentEN=0.0
        matchcount=0
        notfullmatch=0.0
        for compare_item in listinlist2:
            if cmp((frequence_item),(compare_item))==0 and flog==False:
                currentEN=itemEN(list1,list2,frequence_item)
                flog=True
                matchcount+=1
            elif cmp((frequence_item),(compare_item))==0 and flog==True:
                matchcount+=1
            elif cmp((frequence_item),(compare_item))!=0:
                if len(list(set(frequence_item)&set(compare_item)))>0:
                    notfull=itemEN(list1,list2,list(set(frequence_item)&set(compare_item)))
                    l=len(set(frequence_item)&set(compare_item))
                    d=len(frequence_item)+len(compare_item)
                    notfullmatch+=notfull*l/d


                #print(notfullmatch)
            #
            # $else:
            #     #pass
        sim=matchcount*currentEN+notfullmatch
        #print(matchcount,currentEN)
    return sim


if __name__=='__main__':
    print getUserFloderpath()
    #s=frequence_mod_sim('u001','u002')
    #print('u001:u002 is '+str(s))
    #
    # s1=frequence_mod_sim('u001','u001')
    # print('u001:u001 is '+str(s1))
    # s2=frequence_mod_sim('u001','u003')
    # print('u001:u003 is '+str(s2))
    #sequence_mod_sim('u001','u002')
    #sequence_mod_sim('u001','u001')
    #sequence_mod_sim('u001','u003')