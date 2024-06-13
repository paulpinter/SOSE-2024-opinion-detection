import json
import os
import sys

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from osd.persistence import database
from osd.persistence import reset

from osd.classification.filter import label
from kafka import KafkaProducer

app = Flask(__name__)


@app.post("/check")
def check_review():
  if request.is_json:
    review_json = request.get_json()
    target = [database.append_one_review_get_id(review_json, query.engine)]
    newly_labeled = label(query.engine, target)
    database.update_label(target, newly_labeled, query.engine)
    return {"label": newly_labeled[0]}
  return {"error": "Request must be JSON"}, 415


@app.post("/store")
def store_review():
  if request.is_json:
    review_json = request.get_json()
    review_id = database.append_one_review_get_id(review_json, query.engine)
    return create_asynch_response(review_id), 202
  return {"error": "Request must be JSON"}, 415


@app.post("/produce")
def produce():
  if request.is_json:
    review_json = request.get_json()
    review_id = database.append_one_review_get_id(review_json, query.engine)
    # producer.send('test', review_id)
    return create_asynch_response(review_id), 202
  return {"error": "Request must be JSON"}, 415


@app.get("/status/<review_id>")
def status(review_id):
  label = database.get_label_by_review_id(review_id, query.engine)
  return {"label": label}, 200


def create_asynch_response(review_id):
  return {"task": {"href": host + str(port) + '/status/' + str(review_id), "id": review_id}}


if __name__ == "__main__":
  if os.getenv('SERVER_RESET_DB') == 'true':
    reset.db()
  app.config['SQLALCHEMY_DATABASE_URI'] = database.connection_str
  app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
  query = SQLAlchemy(app)
  # producer = KafkaProducer(security_protocol="SSL",
  #   bootstrap_servers=os.getenv('KAFKA_BOOTSTRAP_SERVER'),
  #                          value_serializer=lambda x: x.to_bytes(x.bit_length() + 7, sys.byteorder))
  debug = os.getenv('SERVER_DEBUG') == 'true'
  port = int(os.getenv('SERVER_PORT'))
  host = os.getenv('SERVER_HOST')
  app.run(debug=debug, port=port, host=host)
