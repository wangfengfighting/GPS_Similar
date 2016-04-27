# coding: utf-8
__author__ = 'Administrator'

from getDir import GetDirName
import os
import json
import numpy as np
import sys

def get_fenlei_user():
    wifi_path=[]
    getdir=GetDirName()
    parent_path = os.path.dirname(os.getcwd())
    AllUserFiles,AllFiles,other=getdir.getUserFiles(parent_path+os.sep+'starlog')
    for path_file in other:
        for i in range(len(path_file)):
            path_file_name=parent_path+path_file[i]+os.sep+'wifi.txt'
            wifi_path.append(path_file_name)
    return wifi_path

def wifi_file_filter(wifi_file_path):
    for path in wifi_file_path:
        if os.path.exists(path):
            reload(sys)
            sys.setdefaultencoding( "utf-8" )
            f=open(path.replace('wifi.txt','Downwifi.txt'),'w')
            f.writelines('SSID,BSSID,state,time,level')
            f.write('\n')
            prefile=open(path,'r').readlines()
            for line in prefile:
                s=json.loads(line)
                #print s['Wifi']['SSID']
                if s['Wifi']['SSID']=='':
                    f.write('HIDE')
                elif not  s['Wifi']['SSID'].strip():
                    f.write('Unkonwn')
                else:
                    f.write(str(s['Wifi']['SSID']).strip('\n'))
                f.write(',')
                f.write(str(s['Wifi']['BSSID']).strip('\n'))
                f.write(',')
                f.write(str(s['Wifi']['state']).strip('\n'))
                f.write(',')
                f.write(str(s['Wifi']['time']).strip('\n'))
                f.write(',')
                f.write(str(s['Wifi']['level']).strip('\n'))
                f.write('\n')
            f.close()
        else:
            pass


if __name__=='__main__':
    #print get_fenlei_user()
    wifi_file_filter(get_fenlei_user())