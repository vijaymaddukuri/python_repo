import requests

result = requests.post("https://10.100.26.90/api/v1.3/Auth",json = {"username": "1a@VSFL.LAB", "password": "Password1"},json = {'Accept': "application/json", 'Content-Type': "application/json"}, verify=False)

output= result.json()
print output['Token']