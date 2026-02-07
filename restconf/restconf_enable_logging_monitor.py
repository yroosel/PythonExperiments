# Configure logging severity
import requests
IP_ADDRESS="192.168.56.xxx"  
RESTCONF_USERNAME="Get uername"  
RESTCONF_PASSWORD="Get Password!" 
url = f"https://{IP_ADDRESS}/restconf/data/Cisco-IOS-XE-native:native/logging"
auth = (RESTCONF_USERNAME,RESTCONF_PASSWORD)
headers = { "Content-Type": "application/yang-data+json", "Accept": "application/yang-data+json" }
payload = { "Cisco-IOS-XE-native:logging": { "monitor": { "severity": "informational"  } } }
r = requests.put(url, auth=auth, headers=headers, json=payload, verify=False)
print(r.status_code, r.text)
