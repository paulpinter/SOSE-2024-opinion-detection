import os

from osd.persistence import database


def run():
  eng = database.create_engine()
  review = database.get_reviews(eng)
  review[['label', 'true_label', 'created_at', 'updated_at']].to_csv(os.getenv('REQUEST_Y_SYNCH'))


if __name__ == "__main__":
  run()
