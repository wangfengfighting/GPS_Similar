# coding: utf-8
__author__ = 'WangFeng'
from matplotlib import pylab as plt
import math
import numpy as np
import networkx as nx
from decimal import *
data = np.loadtxt('LDAednetwork.txt',dtype=str,delimiter=',',usecols=(0,1,2))

#Dic={'u000':'yrs','u001':'xym','u002':'tzh','u003':'wf','u004':'lh','u005':'xym2'}
Dic={'u000':'user0','u001':'user1','u002':'user2','u003':'user3','u004':'user4','u005':'user5'}

print (data)
G = nx.Graph()
for i in range(0,len(data)):
    if float(data[i][2])!=0.0:
        G.add_node(Dic[data[i][0]])
        G.add_node(Dic[(data[i][1])])

for i in range(0,len(data)):
    G.add_edge(Dic[(data[i][0])],Dic[(data[i][1])],weight=float((data[i][2]))*30.5)

#pos=nx.circular_layout(G,iterations=20)
pos=nx.shell_layout(G)
edgewidth=[]
for (u,v,d) in G.edges(data=True):
    #print G.get_edge_data(u,v).values()
    edgewidth.append(round(G.get_edge_data(u,v).values()[0],2))

nx.draw_networkx_edges(G,pos,width=edgewidth,with_labels=True,edge_color='k')
#nx.draw_networkx_nodes(G,pos,with_labels=True,node_color='y')
nx.draw(G,pos,with_labels=True, node_size=100,node_color='y')
nx.draw(G,pos,with_labels=True, node_size=1200,node_color='y',label='ll')
plt.show()