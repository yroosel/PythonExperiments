import requests, sys
import datetime
now = datetime.datetime.now()
print(now)
r = requests.get("https://api.ipify.org/", timeout=10) 
# print(dir(r))
print(r.text)
