import os

from sklearn.model_selection import train_test_split

from osd.persistence import dataset


# This script is dedicated to create request examples for the synch, batch and queue architecture
def run():
  data = dataset.read('CHI')
  data.rename(columns={'label': 'true_label'}, inplace=True)
  x_train, x_test, y_train, y_test = train_test_split(data, data['true_label'], random_state=0)
  request_json = x_test.to_json(orient='records', date_format='iso')
  with open(os.getenv('REQUEST_JSON'), "w") as outfile:
    outfile.write(request_json)


if __name__ == "__main__":
  run()
