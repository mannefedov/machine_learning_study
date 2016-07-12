import pandas
import numpy as np
from sklearn import cross_validation, neighbors, preprocessing

data = pandas.read_csv('wine.csv', header=None,)
data = np.array(data)
datas = data[0:,1:]
datas = preprocessing.scale(datas)
for n in range(1, 50):

    cv = cross_validation.KFold(178, n_folds=5, shuffle=True, random_state=42)
    clf = neighbors.KNeighborsClassifier(n_neighbors=n)

    scores = cross_validation.cross_val_score(clf, datas, data[0:,0], cv=cv)
    print("neighbors=", n, " accuracy:",scores.mean())

