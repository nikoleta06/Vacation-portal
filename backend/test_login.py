import requests

url = "http://localhost:8000/login"

data = {
    "email": "maria@google.com",
    "password": "12345"
}

response = requests.post(url, json=data)
print("Status:", response.status_code)
print("Response:", response.text)

