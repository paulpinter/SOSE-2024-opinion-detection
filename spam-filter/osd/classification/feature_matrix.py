import pandas as pd

import osd.classification.feature as feature


def calculate(source_reviews, target_ids=None):
  if target_ids:
    target_reviews = source_reviews.loc[target_ids]
    user_group = reviews_of_targeted_user_group(source_reviews, target_reviews)
    facility_reviews = reviews_of_targeted_facilities(source_reviews, target_reviews)
  else:
    target_reviews = source_reviews
    user_group = source_reviews.groupby('user')
    facility_reviews = source_reviews

  x = pd.DataFrame()
  x['rlw'] = x_rlw(target_reviews)
  x['rsw'] = x_rsw(target_reviews)
  x['rac'] = x_rac(target_reviews)
  x['rcl'] = x_rcl(target_reviews)
  x['rpp'] = x_rpp(target_reviews)
  x['res'] = x_res(target_reviews)
  x['ipo'] = x_ipo(target_reviews)

  x_user = calculate_user_features(user_group)
  x['user'] = target_reviews['user']
  x = x.merge(x_user, how='left', left_on='user', right_index=True)
  x = x.drop(columns='user')

  x_facility = calculate_facility_features(source_reviews, facility_reviews)
  x = x.merge(x_facility, how='left', left_index=True, right_index=True)

  x = x.sort_index(axis=1)
  return x


def calculate_user_features(user_group):
  x_user = pd.DataFrame()
  x_user['alw'] = x_alw(user_group)
  x_user['rpr'] = x_rpr(user_group)
  x_user['rnr'] = x_rnr(user_group)
  x_user['erd'] = x_erd(user_group)
  x_user['mnr'] = x_mnr(user_group)
  x_user['etg'] = x_etg(user_group)
  x_user['brt'] = x_brt(user_group)
  x_user['isr'] = x_isr(user_group)
  similarity = sim(user_group)
  x_user['acs'] = x_acs(similarity)
  x_user['mcs'] = x_mcs(similarity)

  return x_user


def calculate_facility_features(source_reviews, facility_reviews):
  x_facility = pd.DataFrame()
  x_facility['prd'] = x_prd(facility_reviews)
  x_facility['rbd'] = x_rbd(facility_reviews)
  x_facility['ard'] = x_ard(source_reviews)
  x_facility['wrd'] = x_wrd(source_reviews)
  return x_facility


def reviews_of_targeted_user_group(source, target_reviews):
  new_users = target_reviews["user"].unique()
  return source.loc[(source["user"].isin(new_users))].groupby('user')


def reviews_of_targeted_facilities(source, target_reviews):
  new_facilities = target_reviews["facility"].unique()
  return source.loc[(source["facility"].isin(new_facilities))]


def x_alw(user_group):
  return user_group['text'].apply(feature.average_word_length)


def x_acs(similarity):
  return similarity.apply(feature.average_content_similarity)


def x_mcs(similarity):
  return similarity.apply(feature.maximum_content_similarity)


def x_rpr(user_group):
  return user_group['rating'].apply(feature.ratio_of_positive_reviews)


def x_rnr(user_group):
  return user_group['rating'].apply(feature.ratio_of_negative_reviews)


def x_prd(facility_reviews):
  return feature.product_rating_deviation(facility_reviews)


def x_ard(user_facility_reviews):
  return feature.average_rating_deviation(user_facility_reviews)


def x_rbd(facility_reviews):
  return feature.rank_by_date(facility_reviews)


def x_wrd(user_facility_reviews):
  return feature.weighted_rating_deviation_by_user(user_facility_reviews)


def x_erd(user_group):
  return user_group['rating'].apply(feature.entropy_of_ratings)


def x_mnr(user_group):
  return user_group['date'].apply(feature.maximum_number_of_reviews_of_a_day)


def x_etg(user_group):
  return user_group['date'].apply(feature.entropy_of_temporal_gaps)


def x_brt(user_group):
  return user_group['date'].apply(feature.burstiness)


def x_rlw(dataset):
  return dataset.text.apply(feature.number_of_words)


def x_rsw(dataset):
  return dataset.text.apply(feature.relative_word_subjectivity)


def x_rac(dataset):
  return dataset.text.apply(feature.ratio_of_upper_case_words)


def x_rcl(dataset):
  return dataset.text.apply(feature.ratio_of_capital_letters)


def x_rpp(dataset):
  return dataset.text.apply(feature.ratio_of_first_person_pronouns)


def x_res(dataset):
  return dataset.text.apply(feature.ratio_of_exclamation_sentences)


def x_isr(user_group):
  return user_group['rating'].apply(feature.is_singleton_review)


def x_ipo(dataset):
  return dataset.rating.apply(feature.is_positive_review)


def sim(user_group):
  return user_group['text'].apply(feature.similarity)
