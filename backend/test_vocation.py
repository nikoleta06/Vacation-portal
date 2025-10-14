import requests
import json

url="http://localhost:8000/vocation"

data = {
    "user_id": 1, 
    "start_date": "2025-10-25",
    "end_date": "2025-10-30",
    "reason": "Vocation to rest"
}

response = requests.post(url, json=data)
print("Status:", response.status_code)
print("Response:", response.text)


