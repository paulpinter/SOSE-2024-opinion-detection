import os
import time
from osd.persistence import database
from osd.classification.filter import label


def batch_job():
  target_ids = database.get_unlabeled_ids(engine)
  print(target_ids)
  if not target_ids:
    return
  newly_labeled = label(engine, target_ids)
  print(newly_labeled)
  database.update_label(target_ids, newly_labeled, engine)


if __name__ == "__main__":
  engine = database.create_engine()
  polling_rate = int(os.getenv('BATCH_POLLING'))
  while True:
    time.sleep(polling_rate)
    batch_job()
