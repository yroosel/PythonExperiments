import json
import requests
requests.packages.urllib3.disable_warnings()
IP_ADDRESS = "Get IP Address"
api_url = f"https://{IP_ADDRESS}/restconf/data/Cisco-IOS-XE-native:native/logging/monitor/severity"

headers = {"Accept":"application/yang-data+json",
           "Content-type":"application/yang-data+json"
           }
username = "Get Username"
password = "Get Password"
basicauth = (username, password)
warconf = {"severity": "warnings"}
resp = requests.put(api_url, data=json.dumps(warconf), auth=basicauth, headers=headers, verify=False)
print(resp)
