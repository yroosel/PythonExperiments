import requests, urllib3
from requests.auth import HTTPBasicAuth
urllib3.disable_warnings()

PARAMS = {"HOST":"YOUR HOST","USER":"YOUR USER","PASS":"YOUR PASS"}
BASE = f"https://{PARAMS['HOST']}/restconf/data"
auth = HTTPBasicAuth(PARAMS["USER"], PARAMS["PASS"])
headers = {"Accept":"application/yang-data+json"}

hostname = requests.get(f"{BASE}/Cisco-IOS-XE-native:native/hostname",
                        auth=auth, headers=headers, verify=False
                        ).json().get("Cisco-IOS-XE-native:hostname","unknown")

hw = requests.get(f"{BASE}/Cisco-IOS-XE-device-hardware-oper:device-hardware-data",
                  auth=auth, headers=headers, verify=False
                  ).json()

ver = hw["Cisco-IOS-XE-device-hardware-oper:device-hardware-data"]["device-hardware"]["device-system-data"]["software-version"]
print("Hostname:", hostname)
print("IOS Version:", ver.split("Version ")[1].split(",")[0])
