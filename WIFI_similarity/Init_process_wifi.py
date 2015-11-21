# coding: utf-8
__author__ = 'Administrator'

from getDir import GetDirName
import os
import numpy as np
def get_fenlei_user():
    getdir=GetDirName()
    parent_path = os.path.dirname(os.getcwd())
    AllUserFiles,AllFiles,other=getdir.getUserFiles(parent_path+'\\'+'starlog')
    for path_file in other:
        for i in range(len(path_file)):
            path_file_name=parent_path+path_file[i]+os.sep+'RCed_stoppoint.txt'


if __name__=='__main__':
    get_fenlei_user()