from sklearn import naive_bayes
from sklearn.model_selection import GridSearchCV
from sklearn.pipeline import Pipeline
from sklearn import linear_model
from sklearn import svm

from osd.meta.function_decorator import time_on_call


def model(classifier):
  if classifier == 'NB':
    return naive_bayes.GaussianNB()
  elif classifier == 'LOG':
    return linear_model.LogisticRegression()
  elif classifier == 'SVM':
    return svm.LinearSVC()


def params(classifier):
  if classifier == 'NB':
    return {'model__var_smoothing': [0.0000000001, 0.000000001, 0.00000001]}
  elif classifier == 'LOG':
    return {'model__C': [0.00001, 0.0001, 0.001, 0.1, 1, 10, 100, 1000], 'model__penalty': ['l1', 'l2'],
            'model__solver': ['liblinear'], 'model__max_iter': [1000], 'model__dual': [False],
            'model__class_weight': ['balanced']}
  elif classifier == 'SVM':
    return {'model__C': [0.00001, 0.0001, 0.001, 0.1, 1, 10], 'model__max_iter': [100000],
            'model__class_weight': ['balanced'], 'model__dual': [False], 'model__penalty': ['l1', 'l2']}


@time_on_call
def grid(classifier):
  m = model(classifier)
  p = params(classifier)
  pipeline = Pipeline([('model', m)])
  return GridSearchCV(pipeline, cv=10, n_jobs=8, param_grid=p, scoring='f1', verbose=10)
