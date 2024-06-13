import pandas as pd
from numpy import array

import osd.classification.feature as feature


def test_number_of_words():
  assert feature.number_of_words('Hello World.') == 2


def test_average_word_length():
  assert feature.average_word_length(['Hello World.', 'Hello Ladies and Gentlemen.']) == 3


def test_relative_word_subjectivity():
  assert feature.relative_word_subjectivity(
    'Textblob is amazingly simple to use. What great fun!') == 0.4357142857142857


def test_ratio_of_upper_case_words():
  assert feature.ratio_of_upper_case_words('HELLO world') == 0.5


def test_ratio_of_capital_letters():
  assert feature.ratio_of_capital_letters('HELLO world') == 0.5


def test_ratio_of_first_person_pronouns():
  assert feature.ratio_of_first_person_pronouns('I am myself now.') == 0.5


def test_ratio_of_exclamation_sentences():
  assert feature.ratio_of_exclamation_sentences('Who am I? I am who I am!') == 0.5


def test_similarity():
  assert feature.similarity(['I like beer and pizza', 'I love pizza and pasta']) == array([0.3360969272762575])


def test_average_content_similarity():
  data = ['I like beer and pizza', 'I love pizza and pasta', 'I prefer wine over beer', 'Thou shalt not pass']
  assert feature.average_content_similarity(feature.similarity(data)) == 0.1001388397930119


def test_maximum_content_similarity():
  data = ['I like beer and pizza', 'I love pizza and pasta', 'I prefer wine over beer', 'Thou shalt not pass']
  assert feature.maximum_content_similarity(feature.similarity(data)) == array(0.40785379655752624)


def test_is_singleton_review_return_0():
  assert feature.is_singleton_review(['a', '2']) == 0


def test_is_singleton_review_return_1():
  assert feature.is_singleton_review(['a']) == 1


def test_is_positive_review_0():
  assert feature.is_positive_review(3) == 0


def test_is_positive_review_1():
  assert feature.is_positive_review(4) == 1


def test_ratio_of_positive_reviews():
  assert feature.ratio_of_positive_reviews([3, 5, 4, 2]) == 0.5


def test_ratio_of_negative_reviews():
  assert feature.ratio_of_negative_reviews([3, 5, 4, 2]) == 0.25


def test_product_rating_deviation():
  data = {'facility': [1, 1, 2], 'rating': [3, 4, 1]}
  assert feature.product_rating_deviation(pd.DataFrame(data)).tolist() == [0.5, 0.5, 0]


def test_deviation_weight_1():
  assert feature.deviation_weight(1) == 1.0


def test_deviation_weight_2():
  assert feature.deviation_weight(2) == 0.35355339059327373


def test_average_rating_deviation():
  data = {'date': ['2012-04-21', '2012-04-22', '2012-04-23', '2012-04-25', '2012-04-26'], 'user': [1, 2, 3, 1, 2],
          'rating': [5, 4, 5, 1, 1], 'facility': [1, 2, 1, 1, 2]}
  assert feature.average_rating_deviation(pd.DataFrame(data)).tolist() == [2.0, 1.5, 1.3333333333333335, 2.0, 1.5]


def test_weighted_rating_deviation_by_user():
  data = {'date': ['2012-04-21', '2012-04-22', '2012-04-23', '2012-04-25', '2012-04-26'], 'user': [1, 2, 3, 1, 2],
          'rating': [5, 4, 5, 1, 1], 'facility': [1, 2, 1, 1, 2]}
  assert feature.weighted_rating_deviation_by_user(pd.DataFrame(data)).tolist() == [1.5485206370618785, 1.5,
                                                                                    1.3333333333333335,
                                                                                    1.5485206370618785, 1.5]


def test_weighted_rating_deviation():
  data = {'prd': [1.5, 2.5], 'weight': [1, 0.35355339059327373]}
  assert feature.weighted_rating_deviation(pd.DataFrame(data)) == 1.7612038749637415


def test_entropy_of_ratings():
  assert feature.entropy_of_ratings(pd.Series([1, 2, 3, 4])) == 2


def test_maximum_number_of_reviews_of_a_day():
  assert feature.maximum_number_of_reviews_of_a_day(pd.Series(['2012-04-21', '2012-04-22', '2012-04-22'])) == 2


def test_entropy_of_temporal_gaps():
  data = pd.DataFrame(
    {'date': [pd.to_datetime('2012-04-21'), pd.to_datetime('2012-04-22'), pd.to_datetime('2012-04-21')]})
  data['date'] = pd.to_datetime(data['date']).dt.date
  assert feature.entropy_of_temporal_gaps(data['date']) == 1.0


def test_burstiness_7_by_28():
  data = pd.DataFrame(
    {'date': [pd.to_datetime('2012-04-21'), pd.to_datetime('2012-04-27'), pd.to_datetime('2012-04-21')]})
  data['date'] = pd.to_datetime(data['date']).dt.date
  assert feature.burstiness(data['date']) == 0.7857142857142857


def test_burstiness_0():
  data = pd.DataFrame(
    {'date': [pd.to_datetime('2012-04-21'), pd.to_datetime('2012-04-27'), pd.to_datetime('2013-04-21')]})
  data['date'] = pd.to_datetime(data['date']).dt.date
  assert feature.burstiness(data['date']) == 0


def test_rank_by_date():
  data = pd.DataFrame({'facility': [1, 2, 1, 1], 'date': [pd.to_datetime('2012-04-21'), pd.to_datetime('2012-04-21'),
                                                          pd.to_datetime('2012-04-21'), pd.to_datetime('2013-04-21')]})
  data['date'] = pd.to_datetime(data['date']).dt.date
  assert feature.rank_by_date(data).tolist() == [2, 1, 2, 3]
