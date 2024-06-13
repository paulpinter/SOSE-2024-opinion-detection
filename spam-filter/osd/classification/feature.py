import nltk
import scipy.stats
from numpy import triu_indices_from
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from textblob import TextBlob
import numpy as np
import pandas as pd

from osd.meta.function_decorator import time_on_call


def number_of_words(text):
  return len(text.split())


def average_word_length(text_list):
  text_length_list = [number_of_words(text) for text in text_list]
  return sum(text_length_list) / len(text_length_list)


def relative_word_subjectivity(text):
  return TextBlob(text).sentiment.subjectivity


def ratio_of_upper_case_words(text):
  upper = [w for w in text.split() if w.isupper()]
  return len(upper) / number_of_words(text)


def ratio_of_capital_letters(text):
  capital = [w for w in text.split() if w[0].isupper()]
  return len(capital) / number_of_words(text)


def ratio_of_first_person_pronouns(text):
  first_person_pronouns = ["i", "me", "my", "mine", "myself", "we", "us", "our", "ours", "ourselves"]
  fpp = [w for w in text.split() if w.lower() in first_person_pronouns]
  return len(fpp) / number_of_words(text)


def ratio_of_exclamation_sentences(text):
  doc = nltk.tokenize.sent_tokenize(text)
  exclamation = [s for s in doc if '!' in s]
  return len(exclamation) / len(doc)


def similarity(text_list):
  try:
    vec = TfidfVectorizer()
    x = vec.fit_transform(text_list)
  except ValueError:
    return np.array([])
  s = cosine_similarity(x)
  return s[triu_indices_from(s, 1)]


def average_content_similarity(sim):
  if sim.size == 0:
    return 0
  return np.mean(sim)


def maximum_content_similarity(sim):
  if sim.size == 0:
    return 0
  return np.max(sim)


def is_singleton_review(rating_list):
  return 1 if len(rating_list) == 1 else 0


def is_positive_review(rating):
  return 1 if rating in [4, 5] else 0


def ratio_of_positive_reviews(rating_list):
  positive = [r for r in rating_list if r in [4, 5]]
  return len(positive) / len(rating_list)


def ratio_of_negative_reviews(rating_list):
  negative = [r for r in rating_list if r in [1, 2]]
  return len(negative) / len(rating_list)


def product_rating_deviation(dataset):
  return abs(dataset['rating'] - dataset.groupby("facility")['rating'].transform('mean'))


def average_rating_deviation(dataset):
  temp = pd.DataFrame()
  temp['prd'] = product_rating_deviation(dataset)
  temp['user'] = dataset['user']
  ard = temp.groupby("user")['prd'].apply(np.mean)
  ard.name = 'ard'
  temp = temp.merge(ard, how='left', left_on='user', right_index=True)
  return temp['ard']


def deviation_weight(x_rbd):
  return 1 / x_rbd ** 1.5


def weighted_rating_deviation_by_user(dataset):
  temp = pd.DataFrame()
  temp['rbd'] = rank_by_date(dataset)
  temp['weight'] = temp['rbd'].apply(deviation_weight)
  temp['prd'] = product_rating_deviation(dataset)
  temp['user'] = dataset['user']
  wrd = temp.groupby("user").apply(weighted_rating_deviation)
  wrd.name = 'wrd'
  temp = temp.merge(wrd, how='left', left_on='user', right_index=True)
  return temp['wrd']


def weighted_rating_deviation(dataset):
  return sum(dataset['prd'] * dataset['weight']) / sum(dataset['weight'])


def entropy_of_ratings(rating_list):
  ratings = list(rating_list.values)
  ratios = [ratings.count(value) / len(ratings) for value in set(ratings)]
  return scipy.stats.entropy(ratios, base=2)


def maximum_number_of_reviews_of_a_day(date_list):
  dates = list(date_list.values)
  return max([dates.count(d) for d in set(dates)])


def entropy_of_temporal_gaps(date_list):
  if len(date_list) == 1:
    return 0
  sorted_dates = date_list.sort_values()
  gaps = list(np.diff(sorted_dates))
  ratios = [gaps.count(value) / len(gaps) for value in set(gaps)]
  return scipy.stats.entropy(ratios, base=2)


def burstiness(date_list):
  delta = (max(date_list) - min(date_list))
  if delta.days > 28:
    return 0
  else:
    return 1 - (delta.days / 28)


def rank_by_date(dataset):
  return dataset.groupby("facility").date.transform('rank', axis=0, method='max')
