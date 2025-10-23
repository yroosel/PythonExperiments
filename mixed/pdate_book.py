import requests

APIKEY = "yourtoken"
BOOK = 1
url = f"http://library.demo.local/api/v1/books/{BOOK}"

headers = {
    "Accept": "application/json",
    "Content-Type": "application/json",
    "X-API-KEY": APIKEY
}

payload = {
    "id": BOOK,
    "title": "Python for Me",
    "author": "M. Self"
}

try:
    response = requests.put(url, json=payload, headers=headers)
    response.raise_for_status()
    print(f"Success: {response.status_code}")
    print("Response body:", response.text)
except requests.exceptions.HTTPError as err:
    print(f"HTTP error occurred: {err}")
    print("Response body:", response.text)
except Exception as e:
    print(f"Other error occurred: {e}")
