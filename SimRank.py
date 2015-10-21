__author__ = 'Administrator'
from dtw import dtw
import mlpy
import numpy
import networkx as nx
import itertools
import matplotlib.pyplot as plt
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

            sim[nodes_i[u]][nodes_i[v]] = (r * s_uv) / chushu
            #sim[nodes_i[u]][nodes_i[v]] = (r * s_uv) / ((len(u_ns) * len(v_ns)+1))

    return sim

if __name__=='__main__':

    G = nx.DiGraph()
    G.add_node(1)
    G.add_node(2)
    G.add_nodes_from([3,4,5,6])
    G.add_cycle([1,2,3,4])
    G.add_edge(1,3)
    G.add_edges_from([(3,5),(3,6),(6,7)])
    nx.draw(G,with_labels=True)
    #plt.savefig("youxiangtu.png")
    plt.show()

    G1=G.to_undirected()
    nx.draw(G1,with_labels=True)
    plt.show()

    #print(simrank(G))
    print(simrank(G))
    print('-----------------------------')
    print(simrank(G1))