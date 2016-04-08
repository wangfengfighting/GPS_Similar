#coding:utf-8
__author__ = 'lym'
import re
from simhash import Simhash
print Simhash('aa').distance(Simhash('bb'))
print Simhash('aa').distance(Simhash('aa'))
sh1 = Simhash(u'你好 世界 呼噜')
sh2 = Simhash(u'你好 世界')
print(sh1.distance(sh2))
print ','.join('fff')
test='的阿斯顿多少多少'
print "this is test1: %s" %test