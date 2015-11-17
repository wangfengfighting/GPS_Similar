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
            if (os.path.isdir((path+'\\'+f))):
                if(f[0]=='.'):
                    pass
                else:
                    dirList.append(f)


        return dirList

def getUserFile():
    import os
    import os.path
    rootdir =".\\starlog"                                 # 指明被遍历的文件夹
    for parent,dirnames,filenames in os.walk(rootdir):
        for dirname in dirnames:
            print 'parent is:'+parent
            print 'dirname is:'+dirname
            print('full is')+os.path.join(parent,dirname)



#     for parent,dirnames,filenames in os.walk(rootdir):    #三个参数：分别返回1.父目录 2.所有文件夹名字（不含路径） 3.所有文件名字
# 　      for dirname in  dirnames:                       #输出文件夹信息
#     　　    print "parent is:" + parent
# 　　　　    print  "dirname is" + dirname


if __name__=='__main__':
    a=GetDirName()
    dir=a.printPath(".\\starlog")
    dir.sort()
    print(len(dir))
    for i in dir :
        print(a.printPath('.\\starlog'+'\\'+i))
        print('-------------------------------')
    getUserFile()
