# coding: utf-8
__author__ = 'wangfeng'
from gensim import models,similarities,corpora
from  gensim.models.doc2vec import Doc2Vec,LabeledSentence,TaggedDocument,TaggedLineDocument
from  gensim.models.word2vec import Word2Vec
from sklearn.cross_validation import train_test_split
import datetime
import numpy as np
from label_add_time import GetSemanticGPSpath
def time2hour(strtime):
    d=datetime.datetime.strptime(strtime,'%H:%M:%S')
    return  str((d).hour)
def create_model(labelFileName):
    fullpath=GetSemanticGPSpath()
    train_set=[]
    onday=[]
    for file in fullpath:
        filename=file.replace('semanticGPS.txt',labelFileName)
        ondaydata=np.loadtxt(filename,dtype=str,delimiter=',',usecols=(0,1,3)) #label,starttime,continuetime
        tempsentence=[]
        for i in range(len(ondaydata)):
            datasstrip=ondaydata[i][1].split(' ')
            word=ondaydata[i][0]+'_'+datasstrip[0]+'_'+time2hour(datasstrip[1])+'_'+str(int(ondaydata[i][2])//(10*60))
            tempsentence.append(word)
        train_set.append(tempsentence)
    dic = corpora.Dictionary(train_set)
    #model=Doc2Vec(dic,size=100, window=8, min_count=5, workers=4)
    model = Word2Vec(dic, size=100, window=5, min_count=5, workers=4)
    print(dic)
def _load_data(data):
    from keras.models import Sequential
    from keras.layers.core import Dense, Activation, Dropout
    from keras.layers.recurrent import LSTM
    n_prev = 10
    docX, docY = [], []
    for i in range(len(data)-n_prev):
        docX.append(data.iloc[i:i+n_prev].as_matrix())
        docY.append(data.iloc[i+n_prev].as_matrix())
    if not docX:
        pass
    else:
        alsX = np.array(docX)
        alsY = np.array(docY)
        return alsX, alsY

    X, y = _load_data(df_test)

    X_train = X[:25]
    X_test = X[25:]

    y_train = y[:25]
    y_test = y[25:]

    in_out_neurons = 2
    hidden_neurons = 300
    model = Sequential()
    model.add(LSTM(in_out_neurons, hidden_neurons, return_sequences=False))
    model.add(Dense(hidden_neurons, in_out_neurons))
    model.add(Activation("linear"))
    model.compile(loss="mean_squared_error", optimizer="rmsprop")
    model.fit(X_train, y_train, nb_epoch=10, validation_split=0.05)

    predicted = model.predict(X_test)




if __name__=='__main__':
    #create_model('RClabelTime.txt')
    test()