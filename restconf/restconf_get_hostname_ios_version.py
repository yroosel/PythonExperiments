import requests
import urllib3

urllib3.disable_warnings()

CONNECTION_PARAMETERS = {HOST: "44.201.40.38", USER: "npe-restconf", PASS:"C1sco12345"}
url = f"https://{CONNECTION_PARAMETERS[HOST]}/restconf/"
BASE = f"https://{CONNECTION_PARAMETERS[HOST]}/restconf/data"
HEADERS = {"Accept": "application/yang-data+json"}
AUTH  = HTTPBasicAuth(CONNECTION_PARAMETERS[USER], CONNECTION_PARAMETERS[PASS])

# Hostname
url_host = f"{BASE}/Cisco-IOS-XE-native:native/hostname"
r1 = requests.get(url_host, auth=(USER, PASS), headers=HEADERS, verify=False)
hostname = r1.json().get("Cisco-IOS-XE-native:hostname", "unknown")

# Version
url_ver = f"{BASE}/Cisco-IOS-XE-device-hardware-oper:device-hardware-data"
r2 = requests.get(url_ver, auth=AUTH, headers=HEADERS, verify=False)

hardware = r2.json()
full_version = hardware["Cisco-IOS-XE-device-hardware-oper:device-hardware-data"] \
                       ["device-hardware"] \
                       ["device-system-data"] \
                       ["software-version"]

short_version = full_version.split("Version ")[1].split(",")[0]

print("Hostname:", hostname)
print("IOS Version:", short_version)
