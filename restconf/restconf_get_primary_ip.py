import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()

CONNECTION_PARAMETERS = {"HOST": "Your Host", "USER": "Your User", "PASS": "Your Pass"}
CONNECTION_PARAMETERS = {"HOST": "192.168.56.101", "USER": "cisco", "PASS": "cisco123!"}

url = f"https://{CONNECTION_PARAMETERS['HOST']}/restconf/data/Cisco-IOS-XE-native:native/interface/GigabitEthernet=1/ip/address/primary/address"
auth = HTTPBasicAuth(CONNECTION_PARAMETERS["USER"], CONNECTION_PARAMETERS["PASS"])

r = requests.get(url, headers={"Accept": "application/yang-data+json"}, auth=auth, verify=False)

print(r.status_code)
print(r.text)
