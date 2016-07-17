from math import exp, sqrt
import pandas as pd
import numpy as np
from sklearn.metrics import roc_auc_score
def get_gradient(w1, w2, y, x1, x2, k=0.1, C=1):
    l = len(y)
    cost_x1 = 0
    cost_x2 = 0
    for i in range(len(y)):
        cost_x1 += y[i]*x1[i]*(1-(1/(1+exp(-y[i]*(w1*x1[i]+w2*x2[i])))))
        cost_x2 += y[i]*x2[i]*(1-(1/(1+exp(-y[i]*(w1*x1[i]+w2*x2[i])))))
    w1_updated = w1 + k*(1/l) * cost_x1 - k*C*w1
    w2_updated = w2 + k*(1/l) * cost_x2 - k*C*w2
    dist = sqrt((w1- w1_updated)**2 + (w2 - w2_updated)**2)
    return w1_updated, w2_updated, dist

if __name__ == '__main__':
    data = pd.read_csv('data-logistic.csv', header=None)
    y = np.array(data[0])
    x1 = np.array(data[1])
    x2 = np.array(data[2])
    w1, w2 = (0, 0)
    l = len(y)
    for i in range(10000):
        w1, w2, dist = get_gradient(w1,w2, y, x1, x2, C=0)
        if dist <= 1e-05:
            break
    print(w1, w2)
    predict = []
    for i in range(l):
        predict.append((1/(1+exp(-w1*x1[i]-w2*x2[i]))))
    print(roc_auc_score(y, np.array(predict)))
    w1, w2 = (0, 0)

    for i in range(10000):
        w1, w2, dist = get_gradient(w1,w2, y, x1, x2, C=10)
        if dist <= 1e-05:
            break
    print(w1, w2)
    predict = []
    for i in range(l):
        predict.append((1/(1+exp(-w1*x1[i]-w2*x2[i]))))
    print(roc_auc_score(y, np.array(predict)))

