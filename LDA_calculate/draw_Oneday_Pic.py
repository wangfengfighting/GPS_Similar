# coding: utf-8
__author__ = 'WangFeng'
'''
这个函数的作用的画出每个用户每天的label分布图，便于观察，便于分析
2015/11/15
'''
import  numpy as np
from  matplotlib import pylab as plt
import datetime
import seaborn as sns
labelColor={'pdl':'#FF0000','backYH':'#FF34B3','5_bedroom':'#FF7F00','baskball_5':'#CD661D','601':'#C71585','103':'#BFEFFF'
    ,'102':'#C0FF3E','101':'#C67171','playground':'#BDB76B','gym':'#B03060','library':'#FFFF00','hpcl':'#FFE7BA','8_bedroom':'#7D26CD',
    'THbuliding':'#7CCD7C','phd_mess':'#708090','east_door':'#8B2323','gym_101':'#7EC0EE','north_door':'#8B814C',
    'north_community':'#8B475D','club':'#218868','Unknown':'#000000','nodata':'#FFFFFF','ease_door1':'#8B2323'}
def denggaoxian():
    sns.set(style="darkgrid")
    iris = sns.load_dataset("iris")
    # Subset the iris dataset by species
    setosa = iris.query("species == 'setosa'")
    virginica = iris.query("species == 'virginica'")
    # Set up the figure
    f, ax = plt.subplots(figsize=(8, 8))
    ax.set_aspect("equal")
    # Draw the two density plots
    ax = sns.kdeplot(setosa.sepal_width, setosa.sepal_length,cmap="Reds", shade=True, shade_lowest=False)
    ax = sns.kdeplot(virginica.sepal_width, virginica.sepal_length,cmap="Blues", shade=True, shade_lowest=False)
    # Add labels to the plot
    red = sns.color_palette("Reds")[-2]
    blue = sns.color_palette("Blues")[-2]
    ax.text(2.5, 8.2, "user1", size=16, color=blue)
    ax.text(3.8, 4.5, "user2", size=16, color=red)
    plt.show()

def draw_Label_Time(picName):
    from label_add_time import GetSemanticGPSpath
    labelpath=GetSemanticGPSpath()
    TimePic=[]
    for path in labelpath:
        temp=[]
        path=path.replace('semanticGPS.txt',picName)#'RClabelTime.txt'
        data = np.loadtxt(path,dtype=str,delimiter=',',usecols=(0,1,2),unpack=False)
        start=data[1][1].split(' ')[0]
        for i in range(len(data)):
            tmp=[]
            tmp.append(canculateDate(data[i][1],start))
            tmp.append(canculateDate(data[i][2],start))
            tmp.append(data[i][0])
            temp.append(tmp)
        TimePic.append(temp)
    drewPic(TimePic)


def canculateDate(str,strbegin):
    datestar=datetime.datetime.strptime(strbegin,'%Y-%m-%d')
    datenow=datetime.datetime.strptime(str,'%Y-%m-%d %H:%M:%S')
    return (datenow-datestar).seconds

def drewPic(seq):#seq=[  [  [],[],[]  ], .....   ]  s,e,label
    plt.xlim(0,60*60*24+1)
    k=1
    for i in range(len(seq)):
        for j in range(len(seq[i])):
            plt.plot([seq[i][j][0],seq[i][j][1]],[k,k],color=labelColor[seq[i][j][2]],linewidth=5)
        k+=1

    plt.show()

if __name__=='__main__':
    #denggaoxian()
    draw_Label_Time('RClabelTime.txt')
    draw_Label_Time('RCedlabelTime.txt')