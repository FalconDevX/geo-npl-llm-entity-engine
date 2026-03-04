import requests

def search_place_by_name(query: str):
    url = "http://127.0.0.1:8000/search"
    params = {"q": query}
    response = requests.get(url, params=params)
    response.raise_for_status()
    response = response.json()
    if response:
        return response[0]["kod"]
    else:
        return "None"