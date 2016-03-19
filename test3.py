__author__ = 'Administrator'
#coding: utf-8
import numpy as np
import  math
from distance_mean_filter import GetDistance
#print GetDistance(28.231411466944447, 112.99413170166666,28.226883, 113.003083)
c=[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 6, 6, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 2, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 2, 1, 2, 2, 5, 0, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]
b=['8_bedroom', '8_bedroom', '8_bedroom', 'Unknown', 'Unknown', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'backYH', '103', '103', '103', '103', '103', '601', '601', '601', '601', '601', '601', '601', '103', '103', 'backYH', 'pdl', 'pdl', 'pdl', 'pdl', 'backYH', 'pdl', 'backYH', 'pdl', 'backYH', 'pdl', 'pdl', 'backYH', 'pdl', 'pdl', 'backYH', 'pdl', 'backYH', 'pdl', 'backYH', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'backYH', '103', '103', '103', '601', '103', '102', '601', '601', '601', '601', '601', '103', '103', 'backYH', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'Unknown', 'Unknown', '8_bedroom', '8_bedroom', '8_bedroom', '8_bedroom', '8_bedroom', '8_bedroom', 'Unknown', 'Unknown', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'backYH', '103', '103', '102', '102', '101', '101', 'playground', 'library', 'library', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'east_door', 'east_door', 'east_door', 'east_door', 'east_door', 'east_door', 'east_door', 'east_door', 'east_door', 'east_door', 'east_door', 'east_door', 'east_door', 'east_door', 'east_door', 'east_door', 'Unknown', 'Unknown', 'Unknown', 'Unknown', 'library', 'library', '101', '102', '102', '103', '103', '103', 'backYH', 'pdl', 'pdl', 'pdl', 'backYH', 'pdl', 'backYH', 'pdl', 'backYH', 'THbuliding', 'THbuliding', 'pdl', 'backYH', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'THbuliding', 'Unknown', 'THbuliding', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'pdl', 'Unknown', 'Unknown', '8_bedroom', '8_bedroom']
e=[['a', 'b'], ['b', 'c', 'd'], ['a', 'c', 'd', 'e'], ['a', 'd', 'e'], ['a', 'b', 'c'], ['a', 'b', 'c', 'd'], ['a'], ['a', 'b', 'c'], ['a', 'b', 'd'], ['b', 'c', 'e']]
f=[['1', '2', '3', '4', '5'], ['1', '2', '4'], ['2', '3', '5'], ['3', '4', '5'], ['1', '2', '3', '4'], ['1', '2', '3']]
lll=[['15', '15', '15', '15', '15',],['15', '3', '3', '3', '3', '5'], ['5', '6', '6', '6', '2'], ['2', '6', '6', '6', '6', '1', '1', '1', '3', '3', '2', '2', '3', '1', '3', '3', '3', '1', '1', '1', '1', '1', '4', '4', '4', '4', '4', '4'], ['4', '4', '4', '4', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '3', '2', '2', '2', '2', '2', '13', '13', '13', '13', '13', '13', '15', '15', '15', '15', '13', '13', '13', '13', '13', '13', '2', '13', '13', '13', '13', '13', '13', '13', '2', '2', '2', '2', '2', '8', '8', '8', '8', '8', '8', '8', '8', '8', '8', '8', '15', '15', '15', '15', '15', '15', '15', '15', '15', '7', '7', '7', '7', '7', '17', '17', '17', '17', '17', '17', '17', '17', '17', '17', '17', '17', '17', '17', '17', '17', '17', '17', '17', '17', '17', '17', '17', '4', '4', '4', '4', '4', '4', '6', '6', '6', '6', '5', '5', '5', '5', '2', '2', '2', '5', '5', '5', '5', '5', '3', '3', '3', '3', '3', '15', '15', '15', '15', '13', '13', '13', '13', '13', '13', '13', '13', '13']]

ll=[ 8, 8, 8, 8, 8, 8, 8, 8, 15, 15, 15, 15, 15, 15, 15, 15, 15, 7, 7, 7, 7, 7, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 17, 4, 4, 4, 4, 4, 4, 6, 6, 6, 6, 5, 5, 5, 5, 2, 2, 2, 5, 5, 5, 5, 5, 3, 3, 3, 3, 3, 15, 15, 15, 15, 13, 13, 13, 13, 13, 13, 13, 13, 13]
def kk(a):
    currtrn=1
    pre=0
    ans=[]
    temp=[]
    f=[]
    #for i in range(0,len(a)-1):
    print(len(a))
    while currtrn<len(a):

        if a[pre]==a[currtrn] :
            temp.append(a[pre])
            pre+=1
            currtrn+=1

            if currtrn==len(a)-1:
                print('------------')
                print(a[pre-1],a[currtrn-1])
                if a[pre-1]==a[currtrn-1]:
                    temp.append(a[pre-1])
                    ans.append(temp)
                else:
                    ans.append([a[pre-1]])
                    ans.append([a[currtrn-1]])
        else:
            temp.append(a[pre])
            ans.append(temp)
            temp=[]
            pre+=1
            currtrn+=1
            if currtrn==len(a)-1:
                print('------------')
                print(a[pre-1],a[currtrn-1])
                if a[pre-1]==a[currtrn-1]:
                    temp.append(a[pre-1])
                    ans.append(temp)
                else:
                    ans.append([a[pre-1]])
                    ans.append([a[currtrn-1]])

    for i in ans:
        f.append((i[0]))
    return f

def testFrequency():
    from fp_growth import find_frequent_itemsets
    k=[]

    for itemset, support in find_frequent_itemsets(lll, 0.7, True):
        print itemset,support

        k.append([itemset,support])

    print k
def ALL_user_table2dic(semantic):
    temp_semanic=list(set(semantic))
    dic_temp={}
    for i in range(len(temp_semanic)):
        dic_temp[temp_semanic[i]]=str(i)

    listDict=[]
    for item in semantic:
        if dic_temp.has_key(item):
            listDict.append(dic_temp[item])

    return listDict

def collection():
    a=set(['gym_101','pdl','101'])
    b=set(['gym_101','8_bedroom1'])
    #print a&b
    print( En(list(a),list(b)))

def En(lista,listb):
    jiaoji=list (set(lista)&set(listb))
    en=0
    for item in jiaoji:
        print (item)
        print lista.count(item)
        print listb.count(item)
        print (len(lista)+len(listb))
        pi = float( lista.count(item)+listb.count(item)) /  (len(lista)+len(listb))
        print pi
        if pi !=0.0:
            en+= (    -pi*math.log(pi)       )
        else:
            en+=0.0

    sim=en*len(jiaoji)/(len(lista)+len(listb))
    print(en)

    return sim



if __name__=='__main__':
    #print(kk(c))
    #print(kk(b))
    '''
    output=open('network.txt','w+')
    a=[1,2,0.4]
    output.writelines(a[0],a[1])
    output.close()
    '''
    # m=[[(1, 2, 3, 4),(1, 2, 3, 4)]]
    # for i in m:
    #     print(len(i))
    #     for j in i:
    #         print(j)
    # for i in range(9):
    #     a=[1,2,3,4,5,6,7,8,9,11,12]
    #     for k in a:
    #         if k>=5:
    #             print(k)
    #             break
    #testFrequency()
    #print table2dic(b)
    # print('-----------------')
    # import apriori
    # z=apriori.apriori(f,0.7)
    # print(z)
    #collection()
    t=[3]
    print(t[-1])

