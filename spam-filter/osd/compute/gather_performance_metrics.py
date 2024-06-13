import pandas as pd

from osd.classification import metric
from osd.meta.function_decorator import time_on_call
from osd.persistence import files


@time_on_call
def run():
  for suffix in [None, 'L', 'B', 'R', 'UP']:
    performance_pd = pd.DataFrame()
    for c in ['NB', 'LOG', 'SVM']:
      for ds in ['CHI', 'NYC', 'ZIP']:
        performance_pd = update_metrics(c, ds, performance_pd, suffix)
    performance_pd.sort_index(axis=1, inplace=True)
    print(performance_pd)
    performance_pd = performance_pd.round(3)
    files.store_performance(performance_pd, suffix)
  return 0


@time_on_call
def update_metrics(c, ds, performance_pd, suffix=None):
  x_test = files.load_x_test(ds, suffix)
  y_test = files.load_y_test(ds)
  classifier = files.load_classifier(c, ds, suffix)
  y_pred = classifier.predict(x_test)
  metric.summarize(y_test, y_pred)
  p = metric.performance(y_test, y_pred)
  p['_ds'] = ds
  p['_c'] = c
  return performance_pd.append(p, ignore_index=True)


def run2():
  performance_pd = pd.DataFrame()
  for c in ['NB', 'LOG', 'SVM']:
    for ds in ['CHI', 'NYC', 'ZIP']:
      performance_pd = update_metrics(c, ds, performance_pd, 'R')
      performance_pd = update_metrics(c, ds, performance_pd, 'UP')
  performance_pd.sort_index(axis=1, inplace=True)
  print(performance_pd)
  performance_pd = performance_pd.round(3)
  files.store_performance(performance_pd, 'UP')


if __name__ == "__main__":
  run2()
