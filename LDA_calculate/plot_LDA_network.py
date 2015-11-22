# coding: utf-8
__author__ = 'WangFeng'
from matplotlib import pylab as plt
import math
import numpy as np
import networkx as nx
from decimal import *
data = np.loadtxt('LDAednetwork.txt',dtype=str,delimiter=',',usecols=(0,1,2))

#Dic={'u000':'yrs','u001':'xym','u002':'tzh','u003':'wf','u004':'lh','u005':'xym2'}
Dic={'u000':'u000','u001':'u001','u002':'u002','u003':'u003','u004':'u004','u005':'u005'}

print (data)
G = nx.Graph()
for i in range(0,len(data)):
    if float(data[i][2])!=0.0:
        G.add_node(Dic[data[i][0]])
        G.add_node(Dic[(data[i][1])])

for i in range(0,len(data)):
        G.add_edge(Dic[(data[i][0])],Dic[(data[i][1])],weight=float((data[i][2]))*19.5)

pos=nx.spring_layout(G,iterations=20)
edgewidth=[]
for (u,v,d) in G.edges(data=True):
    #print G.get_edge_data(u,v).values()
    edgewidth.append(round(G.get_edge_data(u,v).values()[0],2))

nx.draw_networkx_edges(G,pos,width=edgewidth,with_labels=True,edge_color='k')
#nx.draw_networkx_nodes(G,pos,with_labels=True,node_color='y')
nx.draw(G,pos,with_labels=True, node_size=1000,node_color='y')
plt.show()