import requests, urllib3
from requests.auth import HTTPBasicAuth
urllib3.disable_warnings()

PARAMS = {"HOST":"YOUR HOST","USER":"YOUR USER","PASS":"YOUR PASS"}
BASE = f"https://{PARAMS['HOST']}/restconf/data"
auth = HTTPBasicAuth(PARAMS["USER"], PARAMS["PASS"])
headers = {"Accept":"application/yang-data+json"}

# Hostname
hostname = requests.get(f"{BASE}/Cisco-IOS-XE-native:native/hostname",
                        auth=auth, headers=headers, verify=False
                        ).json().get("Cisco-IOS-XE-native:hostname","unknown")

# Hardware / version
hw = requests.get(f"{BASE}/Cisco-IOS-XE-device-hardware-oper:device-hardware-data",
                  auth=auth, headers=headers, verify=False
                  ).json()["Cisco-IOS-XE-device-hardware-oper:device-hardware-data"]

ios = hw["device-hardware"]["device-system-data"]["software-version"]
ios_version = ios.split("Version ")[1].split(",")[0]

inv = hw["device-hardware"]["device-inventory"][0]

print("\nDevice Information")
print("------------------")
print("Hostname :", hostname)
print("IOS      :", ios_version)
print("Model    :", inv.get("part-number","unknown"))
print("Serial   :", inv.get("serial-number","unknown"))
print("Category :", inv.get("hw-description","unknown"))
