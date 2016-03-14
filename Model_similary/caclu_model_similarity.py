# coding: utf-8
__author__ = 'lym'
from getDir import GetDirName
import os
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



if __name__=='__main__':
    calculateModelSimilarity()