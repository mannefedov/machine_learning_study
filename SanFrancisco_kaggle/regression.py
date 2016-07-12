import pandas as pd
from sklearn import preprocessing
from sklearn.cross_validation import StratifiedShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import log_loss
from time import time

# загружаем данные из файла, в котором дата раделена на категории: час, день, месяц, год
print('Loading data... ')
data = pd.read_csv('train_adr_time.csv')

# выбрасываем неиспользуемые в дальнейшем признаки 
data = data.drop("Address",axis=1)
data = data.drop("Resolution",axis=1)
print('Scaling data... ')

# масштабируем переменные координат
xy_scaler=preprocessing.StandardScaler()
xy_scaler.fit(data[["X","Y"]])
data[["X","Y"]]=xy_scaler.transform(data[["X","Y"]])
data=data[abs(data["Y"])<100]
data.index=range(len(data))

# one-hot encoding для категориальных признаков
print('Getiing dummies... ')
dummy_ranks_DIST = pd.get_dummies(data['PdDistrict'], prefix='PD')
dummy_ranks_DAY = pd.get_dummies(data["DayOfWeek"], prefix='DAY')
dummy_ranks_MONTH = pd.get_dummies(data["month"], prefix='MONTH')
dummy_ranks_YEAR = pd.get_dummies(data["year"], prefix='YEAR')
dummy_ranks_HOUR = pd.get_dummies(data["time"], prefix='HOUR')

# выбрасываем уже ненужные колонки
data = data.drop("PdDistrict",axis=1)
data = data.drop("DayOfWeek",axis=1)
data = data.drop("month",axis=1)
data = data.drop("year",axis=1)
data = data.drop("time",axis=1)

# соединяем все в датафрейм
print('Joining dummies... ')
feature_list=data.columns.tolist()
if 'Category' in feature_list:
    feature_list.remove('Category')
features = data[feature_list].join(dummy_ranks_DIST.ix[:,:]).join(dummy_ranks_DAY.ix[:,:]).join(dummy_ranks_MONTH.ix[:,:]).join(dummy_ranks_YEAR.ix[:,:]).join(dummy_ranks_HOUR.ix[:,:])
labels = data['Category'].astype('category')

# масштабируем данные
collist=features.columns.tolist()
scaler = preprocessing.StandardScaler()
scaler.fit(features)
features[collist]=scaler.transform(features)

# разбиваем данные на обучающую и тест выборки
print('Separating data...')
sss = StratifiedShuffleSplit(labels, train_size=0.7)
for train_index, test_index in sss:
    features_train,features_test=features.iloc[train_index],features.iloc[test_index]
    labels_train,labels_test=labels[train_index],labels[test_index]
features_test.index=range(len(features_test))
features_train.index=range(len(features_train))
labels_train.index=range(len(labels_train))
labels_test.index=range(len(labels_test))
features.index=range(len(features))
labels.index=range(len(labels))

# кодируем данные категорий для классификации
print('Building model... ')
t = time()
le = preprocessing.LabelEncoder()
le_t = le.fit(labels_train)
labels_train = le_t.transform(labels_train)
le_a = le.fit(labels)
labels = le_a.transform(labels)
le_te = le.fit(labels_test)
labels_test = le_te.transform(labels_test)


# обучаем модель
model = LogisticRegression()
model.fit(features_train,labels_train)
print(str((time() - t)/60))

# отчет по всем данным, обучающей и тест выборках
print("all", log_loss(labels, model.predict_proba(features.as_matrix())))
print("train", log_loss(labels_train, model.predict_proba(features_train.as_matrix())))
print("test", log_loss(labels_test, model.predict_proba(features_test.as_matrix())))
