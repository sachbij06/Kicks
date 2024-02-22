import json


stats_file = 'Week1Stats.json'

def get_data():
  with open(stats_file) as f:
    return json.load(f)

def set_data(attempts):
  with open(stats_file, 'w') as f:   
    json.dump(attempts, f)


def get_all_data():

  attempts = get_data()
  return attempts['attempts']


def add_attempt(attempt):
  attempts = get_data()
  attempts['attempts'].append(attempt)
  set_data(attempts)