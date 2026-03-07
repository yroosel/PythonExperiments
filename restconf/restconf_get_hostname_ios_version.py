import requests
import urllib3
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings()

# Connection parameters
CONNECTION_PARAMETERS = {
    "HOST": "Your Host",
    "USER": "Your User",
    "PASS": "Your Pass"
}

# Base RESTCONF URL
BASE = f"https://{CONNECTION_PARAMETERS['HOST']}/restconf/data"

# Headers
HEADERS = {
    "Accept": "application/yang-data+json"
}

# Authentication
AUTH = HTTPBasicAuth(
    CONNECTION_PARAMETERS["USER"],
    CONNECTION_PARAMETERS["PASS"]
)

# --- Get hostname ---
url_host = f"{BASE}/Cisco-IOS-XE-native:native/hostname"

r1 = requests.get(url_host, auth=AUTH, headers=HEADERS, verify=False)

hostname = r1.json().get("Cisco-IOS-XE-native:hostname", "unknown")

# --- Get IOS version ---
url_ver = f"{BASE}/Cisco-IOS-XE-device-hardware-oper:device-hardware-data"

r2 = requests.get(url_ver, auth=AUTH, headers=HEADERS, verify=False)

hardware = r2.json()

full_version = hardware["Cisco-IOS-XE-device-hardware-oper:device-hardware-data"] \
               ["device-hardware"] \
               ["device-system-data"] \
               ["software-version"]

short_version = full_version.split("Version ")[1].split(",")[0]

# --- Output ---
print("Hostname:", hostname)
print("IOS Version:", short_version)
