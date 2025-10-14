import requests
import json 

url= "http://localhost:8000/vocation"

data={
    "id":1, 
    "status": "approved" 
}

response= requests.put(url, json=data)

print("Status:", response.status_code)
print("Response:", response.text)

