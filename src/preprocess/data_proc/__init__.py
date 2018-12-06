import json
import os

curr_path = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(curr_path, 'states_hash.json'), 'r') as states_f:
    states = json.load(states_f)
