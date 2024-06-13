import os

from osd.persistence import files
from osd.persistence import database as db
from osd.classification import feature_matrix

classifier = files.load_classifier(os.getenv('CLASSIFIER'), os.getenv('DATASET'))


def label(engine, target_ids=None):
  source_reviews = db.get_depetend_reviews(target_ids, engine) if target_ids else db.get_reviews(engine)
  if source_reviews.empty:
    return [-1]
  x = feature_matrix.calculate(source_reviews, target_ids)
  return classifier.predict(x).tolist()
