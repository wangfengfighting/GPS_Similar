# coding: utf-8
__author__ = 'WangFeng'
'''
这个函数的作用的画出每个用户每天的label分布图，便于观察，便于分析
2015/11/15
'''
import  numpy as np
from  matplotlib import pylab as plt
import seaborn as sns

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

def draw_Label_Time():
    labelColor={'pdl':'#FF0000','backYH':'#FF34B3','5_bedroom':'#FF7F00','baskball_5':'#CD661D','601':'#C71585','103':'#BFEFFF'
    ,'102':'#C0FF3E','101':'#C67171','playground':'#BDB76B','gym':'#B03060','library':'#FFFF00','hpcl':'#FFE7BA','8_bedroom':'#7D26CD',
    'THbuliding':'#7CCD7C','phd_mess':'#708090','east_door':'#8B2323','gym_101':'#7EC0EE','north_door':'#8B814C',
    'north_community':'#8B475D','club':'#218868','Unknown':'#000000','nodata':'#FFFFFF'}

    from label_add_time import GetSemanticGPSpath
    labelpath=GetSemanticGPSpath()
    for path in labelpath:
        path=path.replace('semanticGPS.txt','RClabelTime.txt')
if __name__=='__main__':
    denggaoxian()