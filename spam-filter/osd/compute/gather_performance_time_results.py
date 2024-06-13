import os

import osd.persistence.database as database
from osd.meta.function_decorator import time_on_call


@time_on_call
def run():
  eng = database.create_engine()
  review = database.get_reviews(eng)
  # review['diff'] = (review['updated_at'] - review['created_at']).astype('timedelta64[ms]')
  # review.to_csv(os.getenv("TAB_TIME_BATCH_CONSTANT"), index=False, header=False)
  return 0


if __name__ == "__main__":
  run()
