import requests

BASE_URL = "http://127.0.0.1:5000"

def test_initial(query):
    url = f"{BASE_URL}/initial"
    payload = {"query": query}
    resp = requests.post(url, json=payload)
    print(resp.json())

def test_final(query):
    url = f"{BASE_URL}/final"
    payload = {"query": query}
    resp = requests.post(url, json=payload)
    print(resp.json())

if __name__ == "__main__":
    # Change this to whatever test query you like
    test_query = "Show me NDVI over Delhi from 2020-01-01 to 2020-12-31"
    
    test_initial(test_query)
    test_final(test_query)
