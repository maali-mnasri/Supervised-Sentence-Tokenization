# coding=utf-8
from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
import os
from sklearn.metrics import average_precision_score
import pickle


def trigram_featurizer(trigram):
    x = []
    if trigram[0][0].isupper():
        x.append(1)
    else:
        x.append(0)  # if left word starts with upper case
    if trigram[2][0].isupper():
        x.append(1)
    else:
        x.append(0)  # if right word starts with upper case
    if trigram[0].isupper():
        x.append(1)
    else:
        x.append(0)  # if left word is all upper case
    if trigram[2].isupper():
        x.append(1)
    else:
        x.append(0)  # if right word is all upper case
    x.append(len(trigram[0]))  # length of left word
    x.append(len(trigram[2]))  # length of right word
    if trigram[2] in ['$', '£', '€']:  # if right word is a currency
        x.append(1)
    else:
        x.append(0)
    if trigram[2].isdigit(): # if right word is a number
        x.append(1)
    else:
        x.append(0)
    print(x)
    return x


def featurizer(data_path):
    X = []
    y = []
    all_lines = map(str.strip, open(data_path, 'r').readlines())
    for line in all_lines:
        trigram = line.split('\t')
        x = trigram_featurizer(trigram)
        target = int(trigram[3])
        X.append(x)
        y.append(target)
    return X, y


def train_model(xtrain, ytrain):
    clf = svm.SVC()
    clf.fit(xtrain, ytrain)
    pickle.dump(clf, open(os.environ['HOME']+'/SupervisedSB/data/SB_Classifier', 'wb'))
    return clf


def test_model(clf, xtest, ytest):
    ypredict = clf.predict(xtest)
    print(ypredict)
    print(ytest)
    average_precision = average_precision_score(ytest, ypredict)
    print(average_precision)


if __name__ == '__main__':
    data = os.environ['HOME'] + '/SupervisedSB/data/labelled_trigrams.csv'
    X, y = featurizer(data)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
    classifier = train_model(X_train,y_train)
    #print(classifier.predict([trigram_featurizer(['Inc','.','said'])]))
    test_model(classifier, X_test, y_test)