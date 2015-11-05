# coding: utf-8
__author__ = 'WangFeng'
from matplotlib import pylab as plt
import math
import numpy as np
import networkx as nx
from decimal import *
data = np.loadtxt('network_stoppoint.txt',dtype=str,delimiter=',',usecols=(0,1,2))

print (data)
G = nx.Graph()
for i in range(0,len(data)):
    if float(data[i][2])!=0.0:
        G.add_node(int(data[i][0]))
        G.add_node(int(data[i][1]))

for i in range(0,len(data)):
        G.add_edge(int(data[i][0]),int(data[i][1]),weight=float((data[i][2])))

pos=nx.spring_layout(G,iterations=20)
edgewidth=[]
for (u,v,d) in G.edges(data=True):
    #print G.get_edge_data(u,v).values()
    edgewidth.append(round(G.get_edge_data(u,v).values()[0]*90,2))

nx.draw_networkx_edges(G,pos,width=edgewidth,with_labels=True,edge_color='k')
#nx.draw_networkx_nodes(G,pos,with_labels=True)
nx.draw(G,pos,with_labels=True)
plt.show()