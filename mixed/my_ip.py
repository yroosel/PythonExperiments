import requests, sys
import datetime
now = datetime.datetime.now()
print(now)
r = requests.get("https://api.myip.com", timeout=10)
print("Status Code: " + str(r.status_code))
if r.status_code != 200:
    print("Error:", r.status_code, r.text, file=sys.stderr)
    sys.exit(1)
data = r.json()
print(data)
json_str = json.dumps(data)
print(json_str)
ip = data.get("ip")  # alternative ip = data["ip"]
country = data.get("country") # alternative country = data["country"]
if ip is None or country is None:
    print("Unexpected response:", data, file=sys.stderr)
    sys.exit(1)
print("IP Address:", ip)
print("Country:", country)
