import numpy as np
from sklearn.linear_model import Perceptron
import pandas
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()
train = scaler.fit_transform(np.array(pandas.read_csv('perceptron-train.csv',header=None))[0:,1:])
train_p = np.array(pandas.read_csv('perceptron-train.csv',header=None))[0:,0]
test = scaler.transform(np.array(pandas.read_csv('perceptron-test.csv',header=None))[0:,1:])
test_p = np.array(pandas.read_csv('perceptron-test.csv',header=None))[0:,0]

clf = Perceptron(random_state=241)
clf.fit(train, train_p)
predictions = clf.predict(test)

acc = accuracy_score(test_p, predictions)
print(acc)