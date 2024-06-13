import os
from datetime import datetime

import pandas
import pandas as pd

header = ['date', 'user', 'facility', 'label', 'rating', 'text']
index_name = 'review_id'


def meta_date_parser_chi(date):
  meta_date_format = '%m/%d/%Y'
  return datetime.strptime(date, meta_date_format).date()


def read_review_data(review_file):
  # $^ regex that never matches -> ensures that review text is loaded into one column
  # ref https://stackoverflow.com/questions/1723182/a-regex-that-will-never-be-matched-by-anything
  return pandas.read_csv(review_file, sep='$^', names=[header[5]], engine='python')


# Y -> spam -> 1, N -> ham -> 0
def meta_label_parser_chi(label):
  return 1 if label == 'Y' else 0


def meta_label_parser_nyc(label):
  return 1 if label == -1 else 0


def check_lines(meta_file, review_file):
  meta_line_count = 0
  for meta_line_count, m in enumerate(meta_file, 1):
    pass
  review_line_count = 0
  for review_line_count, l in enumerate(review_file, 1):
    pass
  if review_line_count != meta_line_count:
    raise Exception('Line numbers of review file and meta file differ')

  # reset read position
  meta_file.seek(0, 0)
  review_file.seek(0, 0)


def read(dataset):
  meta_path = get_meta_path(dataset)
  review_path = get_review_path(dataset)
  with open(meta_path, 'r') as meta_file, open(review_path, 'r') as review_file:
    check_lines(meta_file, review_file)
    if dataset == 'CHI':
      return read_chi(meta_file, review_file)
    elif dataset == 'NYC' or dataset == 'ZIP':
      return read_nyc_or_zip(meta_file, review_file)


def get_meta_path(dataset):
  path_env = '_'.join(['DATASET', dataset, 'META'])
  return os.getenv(path_env)


def get_review_path(dataset):
  path_env = '_'.join(['DATASET', dataset, 'CONTENT'])
  return os.getenv(path_env)


def read_nyc_or_zip(meta_file, review_file):
  date_colum_name = header[0]
  meta_header = [header[2], header[1], header[4], header[3], header[0]]
  data = pandas.read_csv(meta_file, sep='\t', names=meta_header, parse_dates=[date_colum_name])
  review_data = read_review_data(review_file)
  data = data.join(review_data)
  data = data.reindex(columns=header)
  data.index.name = index_name
  data.label = data['label'].apply(meta_label_parser_nyc)
  data.rating = data.rating.astype(int)
  data.date = pd.to_datetime(data['date']).dt.date
  print(data)
  return data


def read_chi(meta_file, review_file):
  date_colum_name = header[0]
  meta_header = [date_colum_name, index_name, header[1], header[2], header[3], header[4]]
  meta_columns = [0, 1, 2, 3, 4, 8]
  data = pandas.read_csv(meta_file, sep=' ', names=meta_header, usecols=meta_columns, parse_dates=[date_colum_name],
                         date_parser=meta_date_parser_chi)
  review_data = read_review_data(review_file)
  data = data.join(review_data)
  data.label = data['label'].apply(meta_label_parser_chi)
  data = data.set_index(index_name, drop=True)
  data.date = pd.to_datetime(data['date']).dt.date
  print(data)
  return data
