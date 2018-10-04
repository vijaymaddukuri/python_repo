import json
import os

json_filepath = "C:\\Users\\madduv\\Desktop\\updateJson.json"

def read_update_json_file(file_name=None, key=None, newValue=None):
    with open(json_filepath, 'rb') as f:
        data = json.load(f)
    data["content"][0][key] = newValue
    with open(json_filepath, "w") as jsonFile:
        json.dump(data, jsonFile)


output = read_update_json_file(file_name=json_filepath, key='id', newValue='[]')