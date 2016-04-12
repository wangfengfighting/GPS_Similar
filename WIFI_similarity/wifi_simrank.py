__author__ = 'Administrator'
from dtw import dtw
import mlpy
import numpy
import networkx as nx
import itertools
import matplotlib.pyplot as plt
from  Init_process_wifi import get_fenlei_user
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
def canclulate_wifi():
    print()

def main():
    userfile=get_fenlei_user()
    print(len(userfile))
    for file in userfile:
        if not os.path.exists(file):
            userfile.remove(file)
    print(len(userfile))



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