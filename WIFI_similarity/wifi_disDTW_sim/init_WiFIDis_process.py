# coding: utf-8
__author__ = 'Administrator'

from getDir import GetDirName
import os
import json
import numpy as np
import sys
from  WIFI_similarity.Init_process_wifi import get_fenlei_user



def main():
    user=[]
    wifi_file=get_fenlei_user()
    for file in wifi_file:
        if not os.path.exists(file):
            wifi_file.remove(file)
        else:
            user.append(file.split(os.sep)[-4])
    user=list(set(user))
    print(user)

if __name__=='__main__':
    main()