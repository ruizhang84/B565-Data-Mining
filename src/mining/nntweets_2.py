import pickle,json, random
import numpy as np
from sklearn.neural_network import MLPRegressor
from sklearn.metrics import mean_absolute_error
from sklearn.model_selection import train_test_split

with open('data_small.p', 'rb') as f:
    weeks, X, y = pickle.load(f)


X_train, X_test, y_train, y_test, weeks_train, weeks_test = train_test_split(X, y, weeks, test_size=0.33, random_state=0)

clf = MLPRegressor(solver='lbfgs', activation='logistic', max_iter=10000,
                hidden_layer_sizes=(200,  100), random_state=0)

clf.fit(X_train, y_train)
y_pred = clf.predict(X_test)

print (len(y_pred))
# score = mean_absolute_error(y_test, y_pred)
with open("results.txt", 'w') as f:
    res = []
    for i in range(len(y_pred)):
        print (weeks_test[i], y_pred[i], y_test[i])
        res.append((weeks_test[i], y_pred[i], y_test[i]))
    print (sorted(res))
    json.dump(res, f)



