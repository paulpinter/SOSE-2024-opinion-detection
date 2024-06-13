from sklearn.model_selection import train_test_split

from osd.classification import classifier
from osd.meta.function_decorator import time_on_call
from osd.persistence import files

['acs', 'alw', 'ard', 'brt', 'erd', 'etg', 'ipo', 'isr', 'mcs', 'mnr', 'prd', 'rac', 'rbd', 'rcl', 'res', 'rlw', 'rnr',
 'rpp', 'rpr', 'rsw', 'wrd']


@time_on_call
def run():
  for c in ['NB', 'LOG', 'SVM']:
    for ds in ['CHI', 'NYC', 'ZIP']:
      # update_classifier(c, ds)
      update_classifier(c, ds, drop=['acs', 'alw', 'mcs', 'rac', 'rcl', 'res', 'rlw', 'rpp', 'rsw'], suffix='B')
      update_classifier(c, ds,
                        drop=['ard', 'brt', 'erd', 'etg', 'ipo', 'isr', 'mnr', 'prd', 'rbd', 'rnr', 'rpr', 'wrd'],
                        suffix='L')
      update_classifier(c, ds, drop=['acs', 'alw', 'ard', 'brt', 'erd', 'etg', 'mcs', 'mnr', 'prd', 'rbd', 'rnr', 'rpr',
                                     'wrd'], suffix='R')
      update_classifier(c, ds, drop=['ipo', 'isr', 'rac', 'rcl', 'res', 'rlw', 'rpp', 'rsw'], suffix='UP')
      update_classifier(c, ds)
  return 0


@time_on_call
def update_classifier(c, ds, drop=None, suffix=None):
  x = files.load_fm(ds)
  x = x if drop is None else x.drop(drop, axis=1)
  print(x)
  y = files.load_label(ds)
  x_train, x_test, y_train, y_test = train_test_split(x, y['label'], random_state=0)
  grid = classifier.grid(c)
  grid.fit(x_train, y_train)
  print(grid.cv_results_)
  files.store_classifier(c, ds, grid, suffix)
  files.store_x_test(x_test, ds, suffix)
  files.store_y_test(y_test, ds)


if __name__ == "__main__":
  run()
