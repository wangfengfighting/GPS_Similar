#coding:utf-8
__author__ = 'wf'
import numpy as np
import scipy as sp

nodes = []  # 所有的节点存入数组
nodesnum = 0  # 所有节点的数目
nodes_index = {}  # <节点名，节点在nodes数组中的编号>
damp = 0.8  # 阻尼系数
trans_matrix = np.matrix(0)  # 转移概率矩阵
sim_matrix = np.matrix(0)  # 节点相似度矩阵


def initParam(graphFile):
    '''
    构建nodes、nodes_index、trans_matrix和第0代的sim_matrix.
    输入文件行格式要求：node\toutneighbor\toutneighbor\t...或 node\tinneighbor\tinneighbor\t...
    '''
    global nodes
    global nodes_index
    global trans_matrix
    global sim_matrix
    global damp
    global nodesnum

    link_in = {}
    for line in open(graphFile, "r", 1024):
        arr = line.strip("\n").split()
        node = arr[0]
        nodeid = -1
        if node in nodes_index:
            nodeid = nodes_index[node]
        else:
            nodeid = len(nodes)
            nodes_index[node] = nodeid
            nodes.append(node)
        for ele in arr[1:]:
            outneighbor = ele
            outneighborid = -1
            if outneighbor in nodes_index:
                outneighborid = nodes_index[outneighbor]
            else:
                outneighborid = len(nodes)
                nodes_index[outneighbor] = outneighborid
                nodes.append(outneighbor)
            inneighbors = []
            if outneighborid in link_in:
                inneighbors = link_in[outneighborid]
            inneighbors.append(nodeid)
            link_in[outneighborid] = inneighbors

    nodesnum = len(nodes)
    trans_matrix = np.zeros((nodesnum, nodesnum))
    for node, inneighbors in link_in.items():
        num = len(inneighbors)
        prob = 1.0 / num
        for neighbor in inneighbors:
            trans_matrix[neighbor, node] = prob

    sim_matrix = np.identity(nodesnum) * (1 - damp)


def iterate():
    '''
    迭代更新相似度矩阵
    '''
    global trans_matrix
    global sim_matrix
    global damp
    global nodesnum

    sim_matrix = damp * np.dot(np.dot(trans_matrix.transpose(),
                                      sim_matrix), trans_matrix) + (1 - damp) * np.identity(nodesnum)


def printResult(sim_node_file):
    '''
    打印输出相似度计算结果
    '''
    global sim_matrix
    global link_out
    global link_in
    global nodes
    global nodesnum

    # 打印node之间的相似度
    f_out_user = open(sim_node_file, "w")
    for i in range(nodesnum):
        f_out_user.write(nodes[i] + "\t")
        neighbour = []
        for j in range(nodesnum):
            if i != j:
                sim = sim_matrix[i, j]
                if sim == None:
                    sim = 0
                if sim > 0:
                    neighbour.append((j, sim))
        # 按相似度由大到小排序
        neighbour = sorted(
            neighbour, cmp=lambda x, y: cmp(x[1], y[1]), reverse=True)
        for (u, sim) in neighbour:
            f_out_user.write(nodes[u] + ":" + str(sim) + "\t")
        f_out_user.write("\n")
    f_out_user.close()


def simrank(graphFile, maxIteration):
    global nodes_index
    global trans_matrix
    global sim_matrix

    initParam(graphFile)
    print "nodes:"
    print nodes_index
    print "trans ratio:"
    print trans_matrix
    for i in range(maxIteration):
        print "iteration %d:" % (i + 1)
        iterate()
        print sim_matrix


if __name__ == '__main__':
    graphFile = "linkgraph.txt"
    sim_node_file = "nodesim_naive.txt"
    maxIteration = 10
    simrank(graphFile, maxIteration)
    printResult(sim_node_file)