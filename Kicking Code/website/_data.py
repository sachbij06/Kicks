import json


stats_file = 'categorized_kicks.json'

def get_data():
  with open(stats_file) as f:
    return json.load(f)


def get_all_data():

  attempts = get_data()
  return attempts['attempts']