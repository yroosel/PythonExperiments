import requests
data = requests.get("https://api.myip.com", timeout=10).json()
print(data["ip"], data["country"])
