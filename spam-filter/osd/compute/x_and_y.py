from osd.classification import feature_matrix
from osd.meta.function_decorator import time_on_call
from osd.persistence import dataset
from osd.persistence import files


@time_on_call
def run():
  for ds in ['CHI', 'NYC', 'ZIP']:
    update_x_and_y(ds)
  return 0


@time_on_call
def update_x_and_y(ds):
  data = dataset.read(ds)
  x = feature_matrix.calculate(data)
  files.store_fm(x, ds)
  files.store_label(data['label'], ds)


if __name__ == "__main__":
  run()
