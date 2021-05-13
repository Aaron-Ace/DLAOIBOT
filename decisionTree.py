#********************
#   NDHU    CSIE    *
#  Author:Aaronace  *
#    2020-2021      *
#  GraduateProject  *
#   Professor:CCC   *
#********************

import csv
import random
import math
import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.naive_bayes import GaussianNB
from sklearn import tree


def loadcsv(filename):
    f1 = open(filename, 'r')
    df1 = pd.read_csv(f1)
    data = df1.to_numpy()
    X, Y = data[:,:-1], data[:,-1]
    return X, Y

def build_clf(nutX, nutY, screwX, screwY):
    nut_clf = tree.DecisionTreeClassifier()
    screw_clf = tree.DecisionTreeClassifier()
    nut_clf.fit(nutX, nutY)
    screw_clf.fit(screwX, screwY)
    psy = screw_clf.predict(screwX)
    #print(np.sum(psy!=screwY))
    #pny = nut_clf.predict(nutX)
    #print(np.sum(pny!=nutY))
    return nut_clf, screw_clf

def preprocessor(X):
    scaler = StandardScaler()
    scaler.fit(X)
    return scaler

def classify(clf_type, inX, sclf, nclf, scaler1, scaler2):
    if clf_type==1:
        # inX = scaler1.transform(inX)
        out = sclf.predict(inX)
    else:
        # inX = scaler2.transform(inX)
        # print(inX)
        out = nclf.predict(inX)
    return out

def Classify(which, data1, data2, data3):
    nutX, nutY = loadcsv('NutCsv/train.csv')
    #print(nutX.shape)
    screwX, screwY = loadcsv('ScrewCsv/train.csv')
    scaler1 = preprocessor(screwX)
    scaler2 = preprocessor(nutX)
    # nutX = scaler1.transform(nutX)
    # screwX = scaler2.transform(screwX)
    nclf, sclf = build_clf(nutX, nutY, screwX, screwY)
    x1, x2 = data1, data2
    inX = np.array([[x1, x2, x1**2+x2**2]])
    out = classify(which, inX, sclf, nclf, scaler1, scaler2)
    #print(out)
    return out
