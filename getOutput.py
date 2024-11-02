import requests

def getRecommendation(movie = "101 Dalmatians (1996)"):
    url = "http://127.0.0.1:5003/recommend"
    payload = {"movie": movie}
    headers = {"Content-Type": "application/json"}

    response = requests.post(url, json=payload, headers=headers)
    print(response.json())
    return response.json()

if __name__ == '__main__':
    getRecommendation()
