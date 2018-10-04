import requests
from pprint import pprint as pp

response=requests.get('http://google.com')
print(response.content)
print(response.status_code)
pp(response.headers)
