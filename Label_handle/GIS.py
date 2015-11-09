# coding: utf-8
__author__ = 'WangFeng'
'''
GIS是最大熵模型。用来计算最大熵的，用来预测那些Unknown的label的准取消的算法
'''
from collections import defaultdict
import math

class MaxEnt(object):
    def __init__(self):
        self.feats = defaultdict(int)
        self.trainset = []  #trainset 的标准是这样的[['THbuliding', '28.23101501', '112.99733601', '99.0', '9-18-2015', '07:12:12', '1.456743'].........[]]
        self.labels = set() #

    def load_data(self,file):
        for line in open(file):
            fields = line.strip().split()
            # at least two columns
            if len(fields) < 2: continue
            # the first column is label
            label = fields[0]
            self.labels.add(label)
            for f in set(fields[1:]):
                # (label,f) tuple is feature
                self.feats[(label,f)] += 1
            self.trainset.append(fields)
        print self.trainset
        print self.feats

    def _initparams(self):
        self.size = len(self.trainset)
        # M param for GIS training algorithm
        self.M = max([len(record)-1 for record in self.trainset])
        self.ep_ = [0.0]*len(self.feats)
        for i,f in enumerate(self.feats):
            # calculate feature expectation on empirical distribution
            self.ep_[i] = float(self.feats[f])/float(self.size)
            # each feature function correspond to id
            self.feats[f] = i
        # init weight for each feature
        self.w = [0.0]*len(self.feats)
        self.lastw = self.w

    def probwgt(self,features,label):
        wgt = 0.0
        for f in features:
            if (label,f) in self.feats:
                wgt += self.w[self.feats[(label,f)]]
        return math.exp(wgt)

    """
    calculate feature expectation on model distribution
    """
    def Ep(self):
        ep = [0.0]*len(self.feats)
        for record in self.trainset:
            features = record[1:]
            # calculate p(y|x)
            prob = self.calprob(features)
            for f in features:
                for w,l in prob:
                    # only focus on features from training data.
                    if (l,f) in self.feats:
                        # get feature id
                        idx = self.feats[(l,f)]
                        # sum(1/N * f(y,x)*p(y|x)), p(x) = 1/N
                        ep[idx] += w * (1.0/self.size)
        return ep

    def _convergence(self,lastw,w):
        for w1,w2 in zip(lastw,w):
            if abs(w1-w2) >= 0.01:
                return False
        return True

    def train(self, max_iter =1000):
        self._initparams()
        for i in range(max_iter):
            #print 'iter %d ...'%(i+1)
            # calculate feature expectation on model distribution
            self.ep = self.Ep()
            self.lastw = self.w[:]
            for i,w in enumerate(self.w):
                delta = 1.0/self.M * math.log(self.ep_[i]/self.ep[i])
                # update w
                self.w[i] += delta
            #print self.w
            # test if the algorithm is convergence
            if self._convergence(self.lastw,self.w):
                break

    def calprob(self,features):
        wgts = [(self.probwgt(features, l),l) for l in self.labels]
        Z = sum([ w for w,l in wgts])
        prob = [ (w/Z,l) for w,l in wgts]
        return prob

    def predict(self,input):
        features = input.strip().split()
        prob = self.calprob(features)
        prob.sort(reverse=True)
        return prob
if __name__=='__main__':
    # model = MaxEnt()
    # model.load_data('gis_test')
    # model.train()
    #
    # print('---------')
    # print model.predict('Happy')

    model2 = MaxEnt()
    model2.load_data('label_test')
    model2.train()
    print '----------------------- 我是分割线---------------------------------'
    print (model2.predict('28.22925393 112.99899129 70.0 9-18-2015 07:16:56 0.37483332'))
    print sorted(model2.predict('28.22925393 112.99899129 70.0 9-18-2015 07:16:56 0.37483332'))

    #print model2.predict('bc 0716')