import os

import pandas as pd
import sqlalchemy
from sqlalchemy import BigInteger
from sqlalchemy import Column
from sqlalchemy import Date
from sqlalchemy import DateTime
from sqlalchemy import MetaData
from sqlalchemy import SmallInteger
from sqlalchemy import Table
from sqlalchemy import Text
from sqlalchemy import func
from sqlalchemy import insert
from sqlalchemy import select
from sqlalchemy import text
from sqlalchemy import update

connection_str = os.getenv('DB_CONNECTION')
metadata_obj = MetaData()
reviews = Table('reviews', metadata_obj, Column('review_id', BigInteger, primary_key=True, autoincrement=True),
                Column('date', Date), Column('user', Text), Column('facility', Text),
                Column('label', SmallInteger), Column('rating', SmallInteger), Column('text', Text),
                Column('true_label', SmallInteger),
                Column('created_at', DateTime(timezone=True), server_default=func.now()),
                Column('updated_at', DateTime(timezone=True), onupdate=func.now()))


def create_engine():
  return sqlalchemy.create_engine(connection_str)


def create_table(engine):
  metadata_obj.drop_all(engine)
  return metadata_obj.create_all(engine)


def append_one_review_get_id(review, engine):
  connection = engine.connect()
  review_id = connection.execute(insert(reviews).values(review)).inserted_primary_key
  return review_id[0]


def append_reviews(df, engine):
  return df.to_sql('reviews', con=engine, if_exists='append', index=False)


def get_reviews(engine):
  return pd.read_sql_table('reviews', con=engine, index_col='review_id')


def get_unlabeled_ids(engine):
  connection = engine.connect()
  unlabeled_ids = connection.execute(select(reviews.c.review_id).where(reviews.c.label.is_(None)))
  if unlabeled_ids.rowcount == 0:
    return []
  else:
    return [row[0] for row in unlabeled_ids]


def get_depetend_reviews(review_ids, engine):
  return pd.read_sql(text(
    'select * from reviews where facility in (select distinct facility from reviews where "user" in (select distinct '
    '"user" from reviews where review_id in :r))'), params={'r': tuple(review_ids)}, con=engine, index_col='review_id')


def get_labeled_reviews(engine):
  return pd.read_sql(select(reviews).where(reviews.c.label.is_not(None)), con=engine, index_col='review_id')


def get_label_by_review_id(review_id, engine):
  connection = engine.connect()
  row = connection.execute(select(reviews).where(reviews.c.review_id == review_id)).fetchone()
  if row is None:
    return -1
  return row['label']


def update_label(review_ids, labels, engine):
  connection = engine.connect()
  for i in range(len(review_ids)):
    connection.execute(update(reviews).where(reviews.c.review_id == review_ids[i]).values(label=labels[i]))


if __name__ == "__main__":
  res = get_depetend_reviews([137, 309],
                             sqlalchemy.create_engine('postgresql+psycopg2://postgres@127.0.0.1:32768/postgres'))
