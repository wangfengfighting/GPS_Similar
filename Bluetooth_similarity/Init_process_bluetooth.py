#coding=utf-8
__author__ = 'feng'

from getDir import GetDirName
import os
import json
import numpy as np
import sys
import os
import traceback
def get_fenlei_user():
    wifi_path = []
    getdir = GetDirName()
    parent_path = os.path.dirname(os.getcwd())
    AllUserFiles,AllFiles,other = getdir.getUserFiles(parent_path+os.sep+'starlog')
    for path_file in other:
        for i in range(len(path_file)):
            path_file_name = parent_path+path_file[i]+os.sep+'bluetooth.txt'
            if os.path.exists(path_file_name):
                wifi_path.append(path_file_name)
                #####Trans_btoothjson_txt(path_file_name)  first time to excue this func will create blueeth csv file with add model to do 
    return wifi_path


def Trans_btoothjson_txt(filefullpath):
    try:
        btoothjson = open(filefullpath,'r')
        filename = filefullpath.replace('bluetooth.txt','Processed_bluetooth.txt')

        writefile = open(filename,'a')
        for line in btoothjson:
            temp_json = json.loads(line)
            writefile.write(temp_json['Bluetooth']['name'])
            writefile.write(',')
            writefile.write(temp_json['Bluetooth']['address'])
            writefile.write(',')
            writefile.write(temp_json['Bluetooth']['bond status'])
            writefile.write(',')
            writefile.write(temp_json['Bluetooth']['time'])
            writefile.write('\n')
        #os.remove(filename)
    except Exception , e:
        print(e)




if __name__ == '__main__':
    reload(sys)
    sys.setdefaultencoding('utf-8')
    print  get_fenlei_user()

