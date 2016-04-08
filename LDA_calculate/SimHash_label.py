from __future__ import division
# coding: utf-8
__author__ = 'lym'

from simhash import Simhash
from Model_similary.caclu_model_similarity import getUserFloderpath
from getDir import GetDirName
import os

def getUserFloderList(user0,user1):

    getdir=GetDirName()
    parent_path = os.path.dirname(os.getcwd())
    user1Floder=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+user0))
    user2Floder=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+user1))
    user1filepath=parent_path+os.sep+"starlog"+os.sep+os.sep+user0+os.sep
    user2filepath=parent_path+os.sep+"starlog"+os.sep+os.sep+user1+os.sep
    num_floder=len(user1Floder) if len(user1Floder)<=len(user2Floder) else len(user2Floder)
    user1Floder.sort()
    user2Floder.sort()
    return simHashLabel(user1filepath,user2filepath,user1Floder,user2Floder,num_floder)
    #print(user1Floder)
    #print(user2Floder)
    #print(user1filepath)
    #print(user2filepath)
def simHashLabel(user1filepath,user2filepath,user1Floder,user2Floder,num_floder):
    ans=0.0
    for i in range(num_floder):
        labeluser1=''
        labeluser2=''
        tempmax1=0
        tempmax2=0
        f1=open(user1filepath+user1Floder[i]+os.sep+'RCed_stoppoint.txt')
        for line in f1:
            labeluser1+=line.split(',')[4]
            labeluser1+=','
            tempmax1+=1
        f2=open(user2filepath+user2Floder[i]+os.sep+'RCed_stoppoint.txt')
        for line in f2:
            labeluser2+=line.split(',')[4]
            labeluser2+=','
            tempmax2+=1
        sh1 = Simhash(u'%s'%labeluser1)
        sh2 = Simhash(u'%s'%labeluser2)
        maxlen=tempmax1 if tempmax1>=tempmax2 else tempmax2

        ans+= sh1.distance(sh2)/maxlen

    return ans




def main():
    user=getUserFloderpath()
    result=open('simhash.txt','a')
    for i in range(len(user)-1):
        for j in range(i,len(user)):
            user0=user[i]
            user1=user[j]
            print user0,user1,getUserFloderList(user0,user1)
            s=''
            s=s+user0+','+user1+','+str(1-getUserFloderList(user0,user1))
            result.write(s)
            result.write('\n')
    result.close()





if __name__=='__main__':
    main()