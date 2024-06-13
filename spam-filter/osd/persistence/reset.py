import os

from osd.persistence import database
from osd.persistence import dataset


def db():
  ds = dataset.read(os.getenv('DATASET'))
  engine = database.create_engine()
  database.create_table(engine)
  # database.append_reviews(ds, engine)


if __name__ == "__main__":
  db()
