import requests

url = "http://127.0.0.1:5003/recommend"
payload = {"movie": "101 Dalmatians (1996)"}
headers = {"Content-Type": "application/json"}

response = requests.post(url, json=payload, headers=headers)
print(response.json())
