#@title ##Imports [run the cell]
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import style
style.use("ggplot")
from sklearn import svm
from sklearn.datasets import load_breast_cancer
import pandas as pd
from sklearn import metrics

# let's try to divide some observations based on some two features
x = [1, 5, 30, 10, 35, 40]
y = [20, 25, 37, 15, 40, 52]
## First, let's see how the observations look in a 2D viz
plt.scatter(x,y)
plt.show()

X = np.array([[1,20], 
             [5,25],
             [30,37],
             [10,15],
             [35,40],
             [40,52]])
y = np.array([0,0,1,0,1,1])

clf = svm.SVC(kernel='linear')
## Fitting the classifier
clf.fit(X,y)

w = clf.coef_[0]
print(w)
a = -w[0] / w[1]
xx = np.linspace(0,40)
yy = a * xx - clf.intercept_[0] / w[1]

h0 = plt.plot(xx, yy, 'k-', label="non weighted div")
plt.scatter(X[:, 0], X[:, 1], c = y)
plt.legend()
plt.show()

data = load_breast_cancer()
X= pd.DataFrame(data.data, columns = data.feature_names)
y= pd.Series(data.target)

X = np.array([[1,20], 
             [5,25],
             [30,37],
             [20,35],
             [35,40],
             [40,52]])
y = np.array([0,0,1,0,1,1])

C = 0.5
classifier = svm.LinearSVC(C=C, max_iter=10000)
classifier.fit(X,y)

w = clf.coef_[0]
print(w)
a = -w[0] / w[1]
xx = np.linspace(0,40)
yy = a * xx - clf.intercept_[0] / w[1]

h0 = plt.plot(xx, yy, 'k-', label="non weighted div")
plt.scatter(X[:, 0], X[:, 1], c = y)
plt.legend()
plt.show()

data = load_breast_cancer()
X= pd.DataFrame(data.data, columns = data.feature_names)
y= pd.Series(data.target)


C = 1.0  # SVM regularization parameter, should be determined using cross-val
models = (svm.LinearSVC(C=C, max_iter=10000),
          svm.SVC(kernel='linear', C=C),
          svm.SVC(kernel='rbf', gamma=0.7, C=C),
          svm.SVC(kernel='poly', degree=2, gamma='auto', C=C, coef0=0.5))

models = (clf.fit(X, y) for clf in models)

titles = ('SVC with linear kernel',
          'LinearSVC (linear kernel)',
          'SVC with RBF kernel',
          'SVC with polynomial (degree 3) kernel')

svms= []
for title, clf in zip(titles, models):
    svms.append(clf)  
    print("Accurary score for {0} is \n {1} on train \n".format(title, \
                                                metrics.accuracy_score(y, clf.predict(X)) 
                                                 ))

## pick a linear kernel model 
model = svms[1]

plt.scatter(X.iloc[:,3], X.iloc[:,2], c=y, cmap='winter');

ax = plt.gca()
xlim = ax.get_xlim()
w = model.coef_[0]
a = -w[0] / w[1]
xx = np.linspace(xlim[0], xlim[1])
yy = a * xx - model.intercept_[0] / w[1]
plt.plot(xx, yy)
yy = a * xx - (model.intercept_[0] - 1) / w[1]
plt.plot(xx, yy, 'k--')
yy = a * xx - (model.intercept_[0] + 1) / w[1]
plt.plot(xx, yy, 'k--')

from sklearn.model_selection import cross_val_score
from sklearn.model_selection import ShuffleSplit
from sklearn.model_selection import GridSearchCV

parameter_candidates = [
  {'C': [0, 0.5, 1.0, 10], 
   'gamma': [0.0001, 0.001, 0.01, 0.1, 0.5, 1], 
   'kernel': ['rbf']},
   {'C': [0, 0.5, 1.0, 10], 
   'gamma': [ 0.01, 0.1, 0.5, 1], 
   'degree': [2,3,4],
   'kernel': ['poly']}
]

cv = ShuffleSplit(n_splits=5, test_size=0.1, random_state=123)
clf = GridSearchCV(estimator=svm.SVC(), param_grid=parameter_candidates, n_jobs=20, 
                   cv=cv, scoring="roc_auc", verbose=1)

clf.fit(X, y) 

# View the best parameters for the model found using grid search
print('\n######### GridSearchCV results ##########')
print('Best C:',clf.best_estimator_.C) 
print('Best score:', clf.best_score_)
print('Best Kernel:',clf.best_estimator_.kernel)
print('Best Gamma:',clf.best_estimator_.gamma)
