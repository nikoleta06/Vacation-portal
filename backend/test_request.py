import requests
import json

url = "http://localhost:8000/users"

data = {
    "name": "Maria",
    "email": "maria@google.com",
    "role" : "employee",
    "password":"12345"
}

response = requests.post(url, json=data)
print("Status:", response.status_code)
print("Response:", response.text)
