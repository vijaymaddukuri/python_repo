import jmespath
import json
import os

json_filepath = "C:\\Users\\madduv\\Desktop\\resourceOperations.json"

def read_json_file(file_name=None):
    with open(json_filepath, 'rb') as f:
        json_data = json.load(f)
    return json_data

jsonInput = read_json_file(json_filepath)
id= "content[?targetResourceTypeRef.label=='VEC Connection'].id"
exId= "content[?targetResourceTypeRef.label=='VEC Connection'].externalId"
refId= "content[?targetResourceTypeRef.label=='VEC Connection'].targetResourceTypeRef.id"
print(jmespath.search(id,jsonInput))
print(jmespath.search(exId,jsonInput))
print(jmespath.search(refId,jsonInput))

