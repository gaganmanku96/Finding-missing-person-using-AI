import os
from random import shuffle
from sklearn import svm, neighbors
import pickle
import numpy as np
import pandas as pd
from connect_DB import *
from sklearn.preprocessing import LabelEncoder


def convert_keypts(pt):
    keypt = []
    keypt.append(pt)
    encoded = []
    text = keypt[0].split('@')
    text = text[1:]
    for t in text:       
        t = t.replace('$','.')
        if t[0:1] == '1':
            t = '-' + t[1:]
        else:
            pass
        # print(t)        
        encoded.append(float(t))  
    return encoded

def train():
    uniqueKeys = []
    keypts = []

    result = db.reference('stationID').get()
    for stationID,value in result.items():
        if stationID == 'ABC123':
            for status,v1 in value.items():
                if status == 'pending':
                    for uniqueKey, v2 in v1.items():
                        uniqueKeys.append(uniqueKey)
                        for keypt, v3 in v2.items():
                            keypts.append(v3)

    le = LabelEncoder()
    uniqueKeys = le.fit_transform(uniqueKeys)

    x = []
    for keypt in keypts:
        x.append(convert_keypts(keypt))

    # print(x)
    x = pd.DataFrame(x)


    clf = neighbors.KNeighborsClassifier(n_neighbors=x.shape[0], algorithm='ball_tree', weights='distance')
    clf.fit(x,uniqueKeys)


    fName = "./classifier.pkl"


    # save the classifier pickle
    with open(fName, 'wb') as f:
        pickle.dump((le, clf), f)
    print("Saving classifier to '{}'".format(fName))

