import os

import joblib
import pandas as pd


def store_fm(x, dataset):
  x.to_csv(os.getenv('X_' + dataset), index=None)


def load_fm(dataset):
  return pd.read_csv(os.getenv('X_' + dataset))


def store_label(labels, dataset):
  labels.to_csv(os.getenv('Y_' + dataset), index=None)


def load_label(dataset):
  return pd.read_csv(os.getenv('Y_' + dataset))


def store_x_test(x_test, dataset, suffix=None):
  path_env = '_'.join([s for s in ['X', dataset, 'TEST', suffix] if s is not None])
  x_test.to_csv(os.getenv(path_env), index=None)


def load_x_test(dataset, suffix=None):
  path_env = '_'.join([s for s in ['X', dataset, 'TEST', suffix] if s is not None])
  return pd.read_csv(os.getenv(path_env))


def store_y_test(y_test, dataset):
  y_test.to_csv(os.getenv('_'.join(['Y', dataset, 'TEST'])), index=None)


def load_y_test(dataset):
  return pd.read_csv(os.getenv('_'.join(['Y', dataset, 'TEST'])))


def store_classifier(classifier, dataset, trained, suffix=None):
  path_env = '_'.join([s for s in ['CLASSIFIER', classifier, dataset, suffix] if s is not None])
  return joblib.dump(trained, os.getenv(path_env))


def load_classifier(classifier, dataset, suffix=None):
  path_env = '_'.join([s for s in ['CLASSIFIER', classifier, dataset, suffix] if s is not None])
  return joblib.load(os.getenv(path_env))


def store_performance(performance, suffix=None):
  path_env = '_'.join([s for s in ['TAB', 'PERFORMANCE', suffix] if s is not None])
  return performance.to_csv(os.getenv(path_env), index=None)
