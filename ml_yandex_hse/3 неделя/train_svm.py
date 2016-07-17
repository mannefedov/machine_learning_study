import pandas as pd
import numpy as np
from sklearn.svm import SVC

data = pd.read_csv('train.csv', header=None)
X = np.array(data[[1,2]])
y = np.array(data[0])

clf = SVC(C=100000, kernel='linear')
clf.fit(X, y)

print(clf.support_)

