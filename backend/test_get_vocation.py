import requests
import json

url= "http://localhost:8000/vocation?user_id=1"
response = requests.get(url)

print("Status:", response.status_code)
print("Response:", response.text) 