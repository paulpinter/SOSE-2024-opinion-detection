import os
import osd.classification.feature_matrix as fm
import osd.classification.feature as fe

import pandas as pd


def test_x_rlw():
  data = pd.DataFrame({'text': ['Hello World.', 'Hello paul']})
  assert fm.x_rlw(data).tolist() == [2, 2]


def test_x_alw():
  data = pd.DataFrame(
    {'user': [1, 2, 1], 'text': ['Hello World.', 'Hello paul', ' Hello sweetheart, you are beautiful']}).groupby('user')
  assert fm.x_alw(data).tolist() == [3.5, 2.0]


def test_x_rsw():
  data = pd.DataFrame({'text': ['Textblob is amazingly simple to use. What great fun!',
                                'Textblob s amazingly simple to use. What great fun!']})
  assert fm.x_rsw(data).tolist() == [0.4357142857142857, 0.4357142857142857]


def test_x_rac():
  data = pd.DataFrame({'text': ['HELLO world', 'HELLO WORLD']})
  assert fm.x_rac(data).tolist() == [0.5, 1]


def test_x_rcl():
  data = pd.DataFrame({'text': ['hellO World', 'HELLO World']})
  assert fm.x_rcl(data).tolist() == [0.5, 1]


def test_x_rpp():
  data = pd.DataFrame({'text': ['Who am I?', 'I am who I am!']})
  assert fm.x_rcl(data).tolist() == [0.6666666666666666, 0.4]


def test_x_isr():
  data = pd.DataFrame({'user': [1, 2, 1], 'rating': [1, 2, 3]}).groupby('user')
  assert fm.x_isr(data).tolist() == [0, 1]


def test_x_res():
  data = pd.DataFrame({'text': ['Who am I? I am who I am!', 'I am who I am!']})
  assert fm.x_res(data).tolist() == [0.5, 1]


def test_x_acs():
  data = pd.DataFrame({'user': [1, 1, 2, 2],
                       'text': ['I like beer and pizza', 'I love pizza and pasta', 'I prefer wine over beer',
                                'Thou shalt not pass']}).groupby('user')['text']
  sim = data.apply(fe.similarity)
  assert fm.x_acs(sim).tolist() == [0.3360969272762575, 0.0]


def test_x_mcs():
  data = pd.DataFrame({'user': [1, 1, 2, 2],
                       'text': ['I like beer and pizza', 'I love pizza and pasta', 'I prefer wine over beer',
                                'Thou shalt not pass']}).groupby('user')['text']
  sim = data.apply(fe.similarity)
  assert fm.x_mcs(sim).tolist() == [0.3360969272762575, 0.0]


def test_x_ipo():
  data = pd.DataFrame({'rating': [1, 1, 5, 4]})
  assert fm.x_ipo(data).tolist() == [0, 0, 1, 1]


def test_x_rpr():
  data = pd.DataFrame({'user': [1, 1, 1, 2], 'rating': [1, 1, 5, 4]}).groupby('user')
  assert fm.x_rpr(data).tolist() == [0.3333333333333333, 1.0]


def test_x_rnr():
  data = pd.DataFrame({'user': [1, 1, 1, 2], 'rating': [1, 1, 5, 4]}).groupby('user')
  assert fm.x_rnr(data).tolist() == [0.6666666666666666, 0.0]


def test_x_prd():
  data = {'facility': [1, 1, 2], 'rating': [3, 4, 1]}
  assert fm.x_prd(pd.DataFrame(data)).tolist() == [0.5, 0.5, 0]


def test_x_ard():
  data = {'date': ['2012-04-21', '2012-04-22', '2012-04-23', '2012-04-25', '2012-04-26'], 'user': [1, 2, 3, 1, 2],
          'rating': [5, 4, 5, 1, 1], 'facility': [1, 2, 1, 1, 2]}
  assert fm.x_ard(pd.DataFrame(data)).tolist() == [2.0, 1.5, 1.3333333333333335, 2.0, 1.5]


def test_x_rbd():
  data = pd.DataFrame({'facility': [1, 2, 1, 1], 'date': [pd.to_datetime('2012-04-21'), pd.to_datetime('2012-04-21'),
                                                          pd.to_datetime('2012-04-21'), pd.to_datetime('2013-04-21')]})
  data['date'] = pd.to_datetime(data['date']).dt.date
  assert fm.x_rbd(data).tolist() == [2, 1, 2, 3]


def test_x_wrd():
  data = {'date': ['2012-04-21', '2012-04-22', '2012-04-23', '2012-04-25', '2012-04-26'], 'user': [1, 2, 3, 1, 2],
          'rating': [5, 4, 5, 1, 1], 'facility': [1, 2, 1, 1, 2]}
  assert fm.x_wrd(pd.DataFrame(data)).tolist() == [1.5485206370618785, 1.5, 1.3333333333333335, 1.5485206370618785, 1.5]


def test_x_erd():
  data = pd.DataFrame({'user': [1, 1, 1, 2], 'rating': [1, 1, 5, 4]}).groupby('user')
  assert fm.x_erd(data).tolist() == [0.9182958340544894, 0.0]


def test_x_mnr():
  data = pd.DataFrame({'date': [pd.to_datetime('2012-04-21'), pd.to_datetime('2012-04-21'),
                                pd.to_datetime('2012-04-21'), pd.to_datetime('2013-04-22'),
                                pd.to_datetime('2013-04-21')], 'user': [1, 1, 1, 2, 2]})
  data['date'] = pd.to_datetime(data['date']).dt.date
  assert fm.x_mnr(data.groupby('user')).tolist() == [3, 1]


def test_x_etg():
  data = pd.DataFrame({'date': [pd.to_datetime('2010-04-21'), pd.to_datetime('2013-04-24'),
                                pd.to_datetime('2014-04-21'), pd.to_datetime('2013-04-22'),
                                pd.to_datetime('2013-04-24')], 'user': [1, 1, 1, 2, 2]})
  data['date'] = pd.to_datetime(data['date']).dt.date
  assert fm.x_etg(data.groupby('user')).tolist() == [1.0, 0.0]


def test_x_brt():
  data = pd.DataFrame({'date': [pd.to_datetime('2010-04-21'), pd.to_datetime('2013-04-24'),
                                pd.to_datetime('2014-04-21'), pd.to_datetime('2013-04-22'),
                                pd.to_datetime('2013-04-24')], 'user': [1, 1, 1, 2, 2]})
  data['date'] = pd.to_datetime(data['date']).dt.date
  assert fm.x_brt(data.groupby('user')).tolist() == [0.0, 0.9285714285714286]


def test_extract_all():
  data = pd.read_csv(os.getenv('TEST_DATASET'), parse_dates=['date'])
  fm.calculate(data).to_csv(os.getenv('TEST_FEATURE_TEMP'), index=False)
  temp = pd.read_csv(os.getenv('TEST_FEATURE_TEMP'))
  os.remove(os.getenv('TEST_FEATURE_TEMP'))
  fixed = pd.read_csv(os.getenv('TEST_FEATURE_FIXED'))
  assert temp.equals(fixed)


def test_target_1():
  data = pd.read_csv(os.getenv('TEST_DATASET'), parse_dates=['date'])
  fm.calculate(data, [1]).to_csv(os.getenv('TEST_FEATURE_TEMP'), index=False)
  temp = pd.read_csv(os.getenv('TEST_FEATURE_TEMP')).reset_index(drop=True)
  os.remove(os.getenv('TEST_FEATURE_TEMP'))
  fixed = pd.read_csv(os.getenv('TEST_FEATURE_FIXED'))
  fixed = fixed.loc[1:1].reset_index(drop=True)
  assert temp.equals(fixed)


def test_target_3():
  data = pd.read_csv(os.getenv('TEST_DATASET'), parse_dates=['date'])
  fm.calculate(data, [1, 2, 3]).to_csv(os.getenv('TEST_FEATURE_TEMP'), index=False)
  temp = pd.read_csv(os.getenv('TEST_FEATURE_TEMP')).reset_index(drop=True)
  os.remove(os.getenv('TEST_FEATURE_TEMP'))
  fixed = pd.read_csv(os.getenv('TEST_FEATURE_FIXED'))
  fixed = fixed.loc[[1, 2, 3]].reset_index(drop=True)
  assert temp.equals(fixed)
