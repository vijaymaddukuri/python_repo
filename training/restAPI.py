import requests

task=   {
    "id": 1,
    "name": "VijayKumar",
    "username": "M",
    "email": "vijay@april.biz",
    "address": {
      "street": "Kulas Light",
      "suite": "Apt. 556",
      "city": "Gwenborough",
      "zipcode": "9620143143",
      "geo": {
        "lat": "-37.3159",
        "lng": "81.1496"
      }
    },
    "phone": "1-7701111111",
    "website": "vijay.org",
    "company": {
      "name": "vijay-M",
      "catchPhrase": "Multi-layered client-server neural-net",
      "bs": "harness real-time e-markets"
    }
  }

add=requests.post('https://jsonplaceholder.typicode.com/users',json=task)

edit=requests.put('https://jsonplaceholder.typicode.com/users',json=task)
print edit

print edit.status_code
resp=edit.get('https://jsonplaceholder.typicode.com/users')
print edit.json()
print edit.json()['phone']

