import json
import os

import requests
# This script is dedicated to create request examples for the synch, batch and queue architecture
from dotenv import load_dotenv


def run():
  load_dotenv()
  url = os.getenv('URL_CHECK')
  headers = {'Content-Type': 'application/json'}
  # Opening JSON file
  with open(os.getenv('REQUEST_JSON'), "r") as request_file:
    # returns JSON object as
    # a dictionary
    data = json.load(request_file)

    count = 0
    # Iterating through the json
    # list
    for review in data:
      payload = json.dumps(review)
      requests.request("POST", url, headers=headers, data=payload)
      count += 1
      print(count / len(data))


if __name__ == "__main__":
  run()
