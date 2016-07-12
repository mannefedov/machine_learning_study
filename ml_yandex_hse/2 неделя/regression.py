import numpy as np
from sklearn import datasets
from sklearn.neighbors import KNeighborsRegressor
from sklearn import cross_validation, preprocessing

data = datasets.load_boston()

data_scaled = preprocessing.scale(data.data)
data_target = data.target
ac = -1000
b = 0
for i in np.linspace(1,10, 200):
    cv = cross_validation.KFold(data_scaled.shape[0], n_folds=5, shuffle=True, random_state=42)
    clf = KNeighborsRegressor(p=i, weights='distance')
    scores = cross_validation.cross_val_score(clf, data_scaled, data_target, cv=cv, scoring='mean_squared_error')
    if ac < scores.mean():
        ac = scores.mean()
        b = i
print("p=", b, " accuracy:",ac)


