'''
time 2015/10/13
__author__ = 'WangFeng'
'''
# coding: utf-8
import os
class GetDirName:
    allFileNum=0

    def printPath(self,path):
        global  allFileNum
        dirList=[]
        files=os.listdir(path)
        for f in files:
            if (os.path.isdir((path+'\\'+f))):
                if(f[0]=='.'):
                    pass
                else:
                    dirList.append(f)


        return dirList



'''
if __name__=='__main__':
    a=GetDirName()
    dir=a.printPath(".\\GPS_Get_PreProcesser")
    dir.sort()
    print(len(dir))
    for i in dir :
        print(i)
'''