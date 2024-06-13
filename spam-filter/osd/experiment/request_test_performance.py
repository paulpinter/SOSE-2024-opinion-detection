import json
import os

import pandas as pd

from osd.classification import metric


def run():
  results = pd.read_csv(os.getenv('REQUEST_Y_SYNCH'))
  print(results)
  numbers = metric.performance(results['label'], results['true_label'])
  filename = os.getenv('REQUEST_PERFORMANCE_SYNCH')  # use the file extension .json
  with open(filename, 'w') as file_object:  # open the file in write mode
    json.dump(numbers, file_object)


if __name__ == "__main__":
  run()
