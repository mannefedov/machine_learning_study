from sklearn import datasets
from sklearn.cross_validation import KFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.grid_search import GridSearchCV
import numpy as np

newsgroups = datasets.fetch_20newsgroups(
                    subset='all', 
                    categories=['alt.atheism', 'sci.space'])
X = newsgroups.data
y = newsgroups.target
print('loaded')
vectorizer = TfidfVectorizer()
X_train = vectorizer.fit_transform(X)

# ___grid search____________________
# grid = {'C': np.power(10.0, np.arange(-5, 6))}
# cv = KFold(y.size, n_folds=5, shuffle=True, random_state=241)
# clf = LinearSVC(random_state=241)

# gs = GridSearchCV(clf, grid, scoring='accuracy', cv=cv)
# print('training...')
# gs.fit(X_train, y)
# for a in gs.grid_scores_:
#     print(a.mean_validation_score)
#     print(a.parameters)
# _______________________

#__________training svm on good params_____
clf = LinearSVC(random_state=241, C=10)
clf.fit(X_train, y)
top = np.argsort(abs(clf.coef_)[0])[-10:]
feature_mapping = vectorizer.get_feature_names()
words = [feature_mapping[x] for x in top]
with open('tf_idf_sub.txt', 'w', encoding='utf-8') as submission:
    submission.write(' '.join(sorted(words)))

