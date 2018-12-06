#!/usr/bin/env python3

import pickle,json, random
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error
from scipy.stats import pearsonr
from sklearn.model_selection import KFold

def train_test_week_split(X, y, weeks, test_size=0.33, random_state=0):
    """
        train test split on each weeks
    """
    # seperate X, y on weeks
    X_week = {}
    y_week = {}
    for i in range(len(weeks)):
        w = weeks[i]
        if w not in X_week:
            X_week[w] = X[i]
            y_week[w] = y[i]
        else:
            X_week[w] = np.vstack((X_week[w], X[i]))
            y_week[w] = np.append(y_week[w], y[i])

    X_train, y_train, weeks_train = np.array([]), np.array([]), np.array([])
    X_test, y_test, weeks_test = np.array([]), np.array([]), np.array([])

    # split X, y
    weeks_unique = set(weeks)
    for i in weeks_unique:
        X_train_i, X_test_i, y_train_i, y_test_i = train_test_split(X_week[i], y_week[i], test_size=test_size, random_state=random_state)

        y_train = np.append(y_train, y_train_i)
        y_test = np.append(y_test, y_test_i)
        weeks_train = np.append(weeks_train, np.ones(len(X_train_i))*i)
        weeks_test = np.append(weeks_test, np.ones(len(X_test_i))*i)

        if len(X_train) == 0:
            X_train = X_train_i
            X_test = X_test_i
        else:
            X_train = np.vstack((X_train, X_train_i))
            X_test = np.vstack((X_test, X_test_i))
    return X_train, X_test, y_train, y_test, weeks_train, weeks_test

with open('data-10.p', 'rb') as f:
    weeks, X, y = pickle.load(f)

scaler = StandardScaler()
X = scaler.fit_transform(X)
y = np.array(y)

X_train, X_test, y_train, y_test, weeks_train, weeks_test = train_test_week_split(X, y, weeks, 0.33)


clf = MLPRegressor(solver='lbfgs', activation='logistic', max_iter=10000,
                hidden_layer_sizes=(200,  100), random_state=0)

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)


y_pred_week = {}
y_test_week = {}

with open("results", 'w') as f:
    res = []
    for i in range(len(weeks_test)):
        # print (weeks_test[i], y_pred[i], y_test[i])
        if weeks_test[i] not in y_pred_week:
            y_pred_week[weeks_test[i]] = []

        y_pred_week[weeks_test[i]].append(y_pred[i])
        y_test_week[weeks_test[i]] = y_test[i]
        res.append((int(weeks_test[i]), float(y_pred[i]), float(y_test[i])))

    for w in y_pred_week:
        print (w, np.mean(y_pred_week[w]), y_test_week[w])

    json.dump(res, f)

kf = KFold(n_splits=5, random_state=0)
for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    error = mean_squared_error(y_test, y_pred)
    print ("mean square error: ", error)
    score = mean_absolute_error(y_test, y_pred)
    print ("mean absolute error: ", score)
    corr = pearsonr(y_test, y_pred)
    print ("pearson corr: ", np.square(corr))

