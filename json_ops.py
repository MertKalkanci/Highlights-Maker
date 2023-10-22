import json
import os

def load_dict_from_json(file_name):
  if not os.path.isfile(file_name):
    return {}
  with open(file_name, "r") as f:
    return json.load(f)
  
def save_dict_to_json(file_name, list):
  with open(file_name, "w") as f:
    json.dump(list, f)