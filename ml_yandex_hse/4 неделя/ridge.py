import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction import DictVectorizer
from scipy.sparse import hstack
import numpy as np
from sklearn.linear_model import Ridge

data_train = pd.read_csv('salary-train.csv')
data_test = pd.read_csv('salary-test-mini.csv')

# tf-idf vectorizing 
description_train = data_train['FullDescription'].str.lower().replace('[^a-z0-9]', ' ', regex=True)
description_test = data_test['FullDescription'].str.lower().replace('[^a-z0-9]', ' ', regex=True)
vectorizer = TfidfVectorizer(min_df=5)
description_train = vectorizer.fit_transform(description_train)
description_test = vectorizer.transform(description_test)


# one-hot encoding
enc = DictVectorizer()

data_train['LocationNormalized'].fillna('nan', inplace=True)
data_train['ContractTime'].fillna('nan', inplace=True)

data_test['LocationNormalized'].fillna('nan', inplace=True)
data_test['ContractTime'].fillna('nan', inplace=True)

X_train_categ = enc.fit_transform(data_train[['LocationNormalized', 'ContractTime']].to_dict('records'))
X_test_categ = enc.transform(data_test[['LocationNormalized', 'ContractTime']].to_dict('records'))

y = np.array(data_train['SalaryNormalized'])

# description_train = np.array(description_train)
# description_test = np.array(description_test)

# X_train_categ = np.array(X_train_categ)
# X_test_categ = np.array(X_test_categ)

X = hstack([description_train, X_train_categ])
X_test = hstack([description_test, X_test_categ])

clf = Ridge(alpha=1, random_state=241)
clf.fit(X, y)
predict = clf.predict(X_test, )
print(predict)

