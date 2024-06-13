import os
import sys

from kafka import KafkaConsumer

from osd.classification.filter import label
from osd.persistence import database

if __name__ == "__main__":
  engine = database.create_engine()
  print('try to connect')
  consumer = KafkaConsumer('test', heartbeat_interval_ms=100, value_deserializer=lambda x: int.from_bytes(x, sys.byteorder),
                           bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVER'))
  print('connected')
  for m in consumer:
    print(m.value)
    target = [m.value]
    newly_labeled = label(engine, target)
    print(newly_labeled)
    if newly_labeled == [-1]:
      continue
    database.update_label(target, newly_labeled, engine)
