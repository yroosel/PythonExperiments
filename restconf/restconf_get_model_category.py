import requests
import urllib3

urllib3.disable_warnings()

HOST = "Your Host"
USER = "Your User"
PASS = "Your Pass"

BASE = f"https://{HOST}/restconf/data"
HEADERS = {"Accept": "application/yang-data+json"}

# --- Hostname ---
url_host = f"{BASE}/Cisco-IOS-XE-native:native/hostname"
r1 = requests.get(url_host, auth=(USER, PASS), headers=HEADERS, verify=False)
hostname = r1.json().get("Cisco-IOS-XE-native:hostname", "unknown")

# --- Hardware / Version ---
url_ver = f"{BASE}/Cisco-IOS-XE-device-hardware-oper:device-hardware-data"
r2 = requests.get(url_ver, auth=(USER, PASS), headers=HEADERS, verify=False)

hardware = r2.json()["Cisco-IOS-XE-device-hardware-oper:device-hardware-data"]

# IOS version
full_version = hardware["device-hardware"]["device-system-data"]["software-version"]
ios_version = full_version.split("Version ")[1].split(",")[0]

# Device inventory
inventory = hardware["device-hardware"]["device-inventory"][0]

model = inventory.get("part-number", "unknown")
serial = inventory.get("serial-number", "unknown")
category = inventory.get("hw-description", "unknown")

# --- Output ---
print("\nDevice Information")
print("------------------")
print("Hostname       :", hostname)
print("IOS Version    :", ios_version)
print("Model          :", model)
print("Serial Number  :", serial)
print("Device Category:", category)
