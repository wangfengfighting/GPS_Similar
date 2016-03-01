# coding: utf-8
'''
time 2015/10/13
__author__ = 'WangFeng'
'''

import os
class GetDirName:
    allFileNum=0

    def printPath(self,path):
        global  allFileNum
        dirList=[]
        files=os.listdir(path)
        for f in files:
            if (os.path.isdir((path+os.sep+f))):
                if(f[0]=='.'):
                    pass
                else:
                    dirList.append(f)
        return dirList

    def getUser(self,spath='.\\starlog'):
        a=os.walk(spath)
        for i in a:
            print(i)

    def getUserFiles(self,sPath=".\\starlog"):
        a=GetDirName()
        dir=a.printPath(sPath)
        dir.sort()
        AllUserFiles=[] #一个用户是一个列表
        AllFiles=[]  # 所有用户的文件列表列表
        otherwenjian=[]
        for i in dir :
            otherwenjian.append([os.sep+'starlog'+os.sep+i+os.sep+s for s in a.printPath(sPath+os.sep+i) ])
            AllUserFiles.append( [ sPath+os.sep+i+os.sep+s for s in a.printPath(sPath+os.sep+i) ])
        print(AllUserFiles)
        for f in AllUserFiles:
            for k in range(len(f)):
                AllFiles.append(f[k])
    #print(AllFiles)
        print(otherwenjian)
        return AllUserFiles,AllFiles,otherwenjian





def getUserFiles():
        a=GetDirName()
        dir=a.printPath("starlog")
        dir.sort()
        AllUserFiles=[] #一个用户是一个列表
        AllFiles=[]  # 所有用户的文件列表列表
        otherwenjian=[]
        for i in dir :
            otherwenjian.append(['\\starlog'+os.sep+i+os.sep+s for s in a.printPath('.\\starlog'+os.sep+i) ])
            AllUserFiles.append( [ '.\\starlog'+os.sep+i+os.sep+s for s in a.printPath('.\\starlog'+os.sep+i) ])
    #print(AllUserFiles)
        for f in AllUserFiles:
            for k in range(len(f)):
                AllFiles.append(f[k])
    #print(AllFiles)
        print(otherwenjian)
        return AllUserFiles,AllFiles,otherwenjian



if __name__=='__main__':
    a=GetDirName()
    # dir=a.printPath(".\\starlog")
    # dir.sort()
    #getUserFiles()
    # print(len(dir))
    # for i in dir :
    #     print(a.printPath('.\\starlog'+'\\'+i))
    #     print('-------------------------------')
    a.getUser('\starlog')
