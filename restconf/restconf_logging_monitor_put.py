# Configure logging severity
import requests
requests.packages.urllib3.disable_warnings()
IP_ADDRESS="Get IP Address"
RESTCONF_USERNAME= "Get Username"
RESTCONF_PASSWORD="Get Password"
url = f"https://{IP_ADDRESS}/restconf/data/Cisco-IOS-XE-native:native/logging"
auth = (RESTCONF_USERNAME,RESTCONF_PASSWORD)
headers = { "Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json" }
payload = { "Cisco-IOS-XE-native:logging": { "monitor": { "severity": "informational"  } } }
r = requests.put(url, auth=auth, headers=headers, json=payload, verify=False)
print(r.status_code, r.text)
