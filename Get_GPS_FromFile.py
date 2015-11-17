__author__ = 'WangFeng'
# coding: utf-8
import  json
from getDir import GetDirName
from matplotlib import pylab as plt
import  os
#f=open(".\\GPS_Get_PreProcesser\\10-10-2015\\location.txt",'r')
#file_processGPS=open(r'.\\GPS_Get_PreProcesser\\10-10-2015\\location_process.txt','w+')
def readfile(filename,date):
    #f=open(".\\GPS_Get_PreProcesser\\10-10-2015\\location.txt",'r')
    #file_processGPS=open(r'.\\GPS_Get_PreProcesser\\10-10-2015\\location_process.txt','w+')
    f=open(filename,'r')
    location=[]
    weidu=[]
    jindu=[]
    for line in f:
        temp_location=[]
        sjson=json.loads(line)
        if line[2:10]=="Location":
            #print(line[2:10])
            temp_location.append(sjson["Location"]["Latitude"])
            temp_location.append(sjson["Location"]["Longitude"])
            temp_location.append(sjson["Location"]["Altitude"])
            temp_location.append(sjson["Location"]["time"])
        #temp_location.append(sjson["Location"]["Speed"])
            weidu.append(float(temp_location[0]))
            jindu.append(float(temp_location[1]))
            location.append(temp_location)
    writeANS(filename,location)
    #drewgps(weidu,jindu,date)
def writeANS(txtfilename,data):
    txtfilename=txtfilename.replace("location","locationGPS")
    file_processGPS=open(r'%s'%txtfilename,'w+')
    file_processGPS.writelines("Latitude,Longitude,Altitude,time,Speed")
    file_processGPS.write('\n')
    for i in data:
        file_processGPS.writelines(i[0])
        file_processGPS.writelines(',')
        file_processGPS.writelines(i[1])
        file_processGPS.writelines(',')
        file_processGPS.writelines(i[2])
        file_processGPS.writelines(',')
        file_processGPS.writelines(i[3])
        file_processGPS.writelines(',')
        file_processGPS.writelines('0.0')
        file_processGPS.write('\n')
    file_processGPS.close()
def drewgps(weidu,jindu,date):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.scatter(jindu,weidu,c='r',marker='.')
    plt.title('location of : %s' % date)
    plt.savefig('.\\GPS_pic\\'+date+'.png',dpi=800)
    plt.close()
    #plt.show()
if __name__=='__main__':
    getdir=GetDirName()
    dirlist=[]
    dirlist=getdir.printPath(".\\GPS_Get_PreProcesser")
    print(dirlist)
    for wenjianjia in dirlist:
        print ".\\GPS_Get_PreProcesser"+  '\\'  +  wenjianjia  +  '\\'  +   'location.txt',wenjianjia
        readfile(".\\GPS_Get_PreProcesser"+  '\\'  +  wenjianjia  +  '\\'  +   'location.txt',wenjianjia)
    #下面是写分开每个用户的结果哦
    AllUserFiles,AllFiles,other=getdir.getUserFiles()
    for wenjianjia in AllFiles:
        readfile(wenjianjia  + os.sep+ 'location.txt',wenjianjia)
