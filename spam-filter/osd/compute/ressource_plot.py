import matplotlib
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from functools import reduce


def calculate_y(path, column):
  df = pd.read_json(path)
  group_size = len(df['Container'].value_counts())
  if column == 'CPUPerc':
    df[column] = df[column].apply(lambda x: float(x[:-1]) / group_size)
  elif column == 'MemPerc':
    df[column] = df[column].apply(lambda x: float(x[:-1]) * 0.08236)
  gb = df.groupby('Container')
  groups = [gb.get_group(x).reset_index()[column] for x in gb.groups]
  total = reduce(lambda a, b: a + b, groups)
  return total.to_numpy().flatten()


def draw_plot(config):
  matplotlib.rcParams.update({'font.size': 22})
  fig, ax = plt.subplots(figsize=(16, 10), layout='constrained')
  for i in range(3):
    y = calculate_y(config['data'][i], config['column'])
    print(config['data'][i])
    print(np.mean(y))

    x = np.linspace(0, 100, len(y))
    ax.plot(x, y, linewidth=5.0, label=config['label'][i])

  plt.style.use('_mpl-gallery')
  ax.set(xlabel='Completion(%)', ylabel=config['y_label'])
  plt.grid(visible=True)
  plt.ylim(config['ylim'])
  plt.legend(loc="upper right")
  plt.savefig(config['target'])
  plt.show()


def run():
  constant_cpu = {"column": "CPUPerc", 'y_label': "CPU(%)", "label": ['SYNCH', 'BATCH', 'QUEUE'],
                  "data": ['/Users/paulpinter/Desktop/Tables/resource_synch_constant.json',
                           '/Users/paulpinter/Desktop/Tables/resource_batch_constant.json',
                           '/Users/paulpinter/Desktop/Tables/resource_queue_constant.json'],
                  "target": "constant_cpu.pdf", "ylim": [0, 100]}
  draw_plot(constant_cpu)
  variable_cpu = {"column": "CPUPerc", 'y_label': "CPU(%)", "label": ['SYNCH', 'BATCH', 'QUEUE'],
                  "data": ['/Users/paulpinter/Desktop/Tables/resource_synch_variable.json',
                           '/Users/paulpinter/Desktop/Tables/resource_batch_variable.json',
                           '/Users/paulpinter/Desktop/Tables/resource_queue_variable.json'],
                  "target": "variable_cpu.pdf", "ylim": [0, 100]}
  draw_plot(variable_cpu)
  constant_mem = {"column": "MemPerc", 'y_label': "GiB", "label": ['SYNCH', 'BATCH', 'QUEUE'],
                  "data": ['/Users/paulpinter/Desktop/Tables/resource_synch_constant.json',
                           '/Users/paulpinter/Desktop/Tables/resource_batch_constant.json',
                           '/Users/paulpinter/Desktop/Tables/resource_queue_constant.json'],
                  "target": "constant_mem.pdf", "ylim": [0, 4]}
  draw_plot(constant_mem)
  variable_mem = {"column": "MemPerc", 'y_label': "GiB", "label": ['SYNCH', 'BATCH', 'QUEUE'],
                  "data": ['/Users/paulpinter/Desktop/Tables/resource_synch_variable.json',
                           '/Users/paulpinter/Desktop/Tables/resource_batch_variable.json',
                           '/Users/paulpinter/Desktop/Tables/resource_queue_variable.json'],
                  "target": "variable_mem.pdf", "ylim": [0, 4]}
  draw_plot(variable_mem)
  return 0


if __name__ == "__main__":
  run()
