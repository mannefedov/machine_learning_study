import pandas as pd
from sklearn.ensemble import RandomForestRegressor as RF
from sklearn.metrics import r2_score
from sklearn.cross_validation import KFold
import numpy as np

data = pd.read_csv('abalone.csv')
data['Sex'] = data['Sex'].map(lambda x: 1 if x == "M" else (-1 if x == 'F' else 0))
X = np.array(data.drop('Rings', axis=1))
y = np.array(data['Rings'])

for i in range(1, 50):
    clf = RF(n_estimators=i, random_state=1)
    cv = KFold(n=X.shape[0], n_folds=5, random_state=1, shuffle=True)
    score = 0
    for train_index, test_index in cv:
        clf.fit(X[train_index], y[train_index])
        predict = clf.predict(X[test_index])
        score += r2_score(y[test_index], predict)
    score = score/5
    print('i={0} score={1}'.format(i, score))
