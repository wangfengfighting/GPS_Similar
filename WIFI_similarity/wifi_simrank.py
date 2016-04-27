from __future__ import division
__author__ = 'Administrator'
from dtw import dtw
import mlpy
import numpy
import networkx as nx
import itertools
import matplotlib.pyplot as plt
from  Init_process_wifi import get_fenlei_user
from getDir import GetDirName
import numpy as np
import datetime
import os
def simrank(G, r=0.9, max_iter=100, eps=1e-4):

    nodes = G.nodes()
    nodes_i = {k: v for(k, v) in [(nodes[i], i) for i in range(0, len(nodes))]}

    sim_prev = numpy.zeros(len(nodes))
    sim = numpy.identity(len(nodes))

    for i in range(max_iter):
        if numpy.allclose(sim, sim_prev, atol=eps): break
        sim_prev = numpy.copy(sim)
        for u, v in itertools.product(nodes, nodes):
            if u is v: continue
            u_ns, v_ns = G.neighbors(u), G.neighbors(v)
            s_uv = sum([sim_prev[nodes_i[u_n]][nodes_i[v_n]] for u_n, v_n in itertools.product(u_ns, v_ns)])
            if (len(u_ns) * len(v_ns))==0:
                chushu=(len(u_ns) * len(v_ns)+1)
            else:
                chushu=(len(u_ns) * len(v_ns))

            #sim[nodes_i[u]][nodes_i[v]] = (r * s_uv) / chushu
            sim[nodes_i[u]][nodes_i[v]] = (r * s_uv) / ((len(u_ns) * len(v_ns)+1))

    return sim
def canclulate_wifi(user1,user2):
    getdir=GetDirName()
    parent_path = os.path.dirname(os.getcwd())
    user1Floder=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+user1))
    user2Floder=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+user2))
    user1filepath=parent_path+os.sep+"starlog"+os.sep+os.sep+user1+os.sep
    user2filepath=parent_path+os.sep+"starlog"+os.sep+os.sep+user2+os.sep
    num_floder=len(user1Floder) if len(user1Floder)<=len(user2Floder) else len(user2Floder)
    sum_sim=0.0
    for i in range(num_floder):
        u1file=user1filepath+user1Floder[i]+os.sep+'Downwifi.txt'
        u2file=user2filepath+user2Floder[i]+os.sep+'Downwifi.txt'

        sum_sim+= daily_wifi_sim(u1file,u2file)
    return sum_sim


def daily_wifi_sim(file1,file2):
    '''
    give two user's wifi file. we devided the wifi file into 24 pices by 24hours.

    :param file1:
    :param file2:
    :return:
    '''
    '''
    :param file1:
    :param file2:
    :return:
    '''
    #print(file1)
    #print(file2)
    wifiuser1list=[]
    wifiuser2list=[]
    user1data=np.loadtxt(file1,dtype=str,delimiter=',',skiprows=1,usecols=(0,3))
    user2data=np.loadtxt(file2,dtype=str,delimiter=',',skiprows=1,usecols=(0,3))
    for hour in range(24):
        temp1=[]
        temp2=[]

        for i in  range(len(user1data)):
            if str2Time(user1data[i][1]) == hour:
                temp1.append((user1data[i][0]))
        #if len(temp1)>0:
        wifiuser1list.append(temp1)

        for j in  range(len(user2data)):
            if str2Time(user2data[j][1]) == hour:
                temp2.append((user2data[j][0]))
        #if len(temp2)>0:
        wifiuser2list.append(temp2)
    #print '------------------------------------------'
    #print(wifiuser1list)
    #print(wifiuser2list)

    # bulid wifi map------------------------------------------
    name1=file1.split(os.sep)[-3]
    name2=file2.split(os.sep)[-3]
    sum_wifi_sim=0.0
    g1=[]
    g2=[]
    for h_index in range(24):
        if len(wifiuser1list[h_index])>0:
            for i in range(len(wifiuser1list[h_index])):
                tuple1=(name1,wifiuser1list[h_index][i])
                g1.append(tuple1)
                del tuple1
        if len(wifiuser2list[h_index])>0:
            for j in range(len(wifiuser2list[h_index])):
                tuple2=(name2,wifiuser2list[h_index][j])
                g2.append(tuple2)
                del tuple2
                #g2.append(tuple(name2,wifiuser2list[h_index][j]))
    #print(g1)
    G = nx.DiGraph()
    G.add_edges_from(g1)
    G.add_edges_from(g2)
    t=simrank((G))
    key= list(G.node.keys())
    #print('*********')
    #print t[key.index(name1)][key.index(name2)]
    sum_wifi_sim+=t[key.index(name1)][key.index(name2)]

    return sum_wifi_sim#/24

    # print G.node.keys()[7:10]
    # #print(simrank(G1))

            # G = nx.DiGraph()
            # G.add_node('1')
            # G.add_node('2')
            # G.add_nodes_from(['3'])
            # #G.add_weighted_edges_from([(1,2,3.0),(1,3,7.5)])
            # #G.add_weighted_edges_from([(2,3,2.5)])

            # # G.add_cycle([1,2,3,4])
            # G.add_edge(1,3)

def str2Time(timeStr):
    t1 = datetime.datetime.strptime(timeStr,'%m-%d-%Y %H:%M:%S')

    return int(t1.hour)

def main():
    user=[]
    wifi_file=get_fenlei_user()
    for file in wifi_file:
        if not os.path.exists(file):
            wifi_file.remove(file)
        else:
            user.append(file.split(os.sep)[-3])
    user=list(set(user))
    # getdir=GetDirName()
    # parent_path = os.path.dirname(os.getcwd())
    # user1Floder=(getdir.printPath(parent_path+os.sep+"starlog"+os.sep+user[0]))
    file=open('simlarBaseonGraphSim.txt','w')
    for i in range(len(user)):
        for j in range(i+1,len(user)):
            #print user[i],user[j]
            sim= canclulate_wifi(user[i],user[j])
            file.write(user[i])
            file.write(',')
            file.write(user[j])
            file.write(',')
            file.write(str(sim))
            file.write('\n')
    file.close()







    # wifi_path=[]
    # getdir=GetDirName()
    # parent_path = os.path.dirname(os.getcwd())+os.sep+'starlog'
    # users= os.listdir(parent_path)
    # for user in users:
    #     if not os.path.exists(parent_path+os.sep+user+os.sep+'wifi.txt'):
    #         users.remove(user)
    # print users
        # userfile=get_fenlei_user()
    # print(len(userfile))
    # for file in userfile:
    #     if not os.path.exists(file):
    #         userfile.remove(file)
    # print(len(userfile))



if __name__=='__main__':
    main()
    # G = nx.DiGraph()
    # G.add_node('1')
    # G.add_node('2')
    # G.add_nodes_from(['3'])
    # #G.add_weighted_edges_from([(1,2,3.0),(1,3,7.5)])
    # #G.add_weighted_edges_from([(2,3,2.5)])
    #
    # # G.add_cycle([1,2,3,4])
    # # G.add_edge(1,3)
    #
    #
    # G.add_edges_from([('1','CMCCC'),('1','535'),('1','SGB201505'),('1','D635'),('1','FAST_xxty'),('1','TP-LINK_IPTV_34F972')
    #                   ,('1','TP-LINK_IPTV_7B7410'),('1','TP-LINK_IPTV_3C56B8')])
    #
    # G.add_edges_from([('2','CMCCC'),('2','535'),('2','SGB201505'),('2','D635'),('2','FAST_xxty'),('2','TP-LINK_IPTV_34F972')
    #                   ,('2','TP-LINK_IPTV_7B7410'),('2','TP-LINK_IPTV_3C56B8')])
    #
    # G.add_edges_from([('3','CMCCC'),('3','5t35'),('3','SGB201505'),('3','D635'),('3','tt'),('3','TP-')])
    # #G.add_edges_from([('1','2'),('1','3'),('2','3')])
    #
    #
    #
    # nx.draw(G,with_labels=True)
    # #plt.savefig("youxiangtu.png")
    # plt.show()
    #
    # G1=G.to_undirected()
    # nx.draw(G1,with_labels=True)
    # plt.show()
    #
    # #print(simrank(G))
    # #print type(simrank(G))
    # t=simrank((G))
    # print (t)
    # numpy.savetxt('ttt.txt',t)
    # print('-----------------------------')
    # print type(G.node)
    # print (G.node.keys())
    # print G.node.keys()[7:10]
    # #print(simrank(G1))