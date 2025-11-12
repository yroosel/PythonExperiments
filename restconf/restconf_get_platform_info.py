#!/usr/bin/env python3
import requests
import json
from requests.auth import HTTPBasicAuth

# --- Router details ---
ROUTER = {
    "host": "Your IP",   # CSR1Kv IP
    "user": "Your User",
    "password": "Your Pw"
}

# --- Disable SSL warnings for self-signed certs ---
requests.packages.urllib3.disable_warnings()

# --- RESTCONF base URL ---
base_url = f"https://{ROUTER['host']}/restconf/data"

# --- Common headers for RESTCONF JSON ---
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# --- Function to GET data from RESTCONF ---
def restconf_get(resource):
    url = f"{base_url}/{resource}"
    response = requests.get(url,
                            auth=HTTPBasicAuth(ROUTER['user'], ROUTER['password']),
                            headers=headers,
                            verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"[!] Error {response.status_code} for {url}")
        print("ietf-system not fully supported or exposed through RESTCONF until IOS XE 16.10+\n")
        return None


# === [1] Get hostname ===
hostname_data = restconf_get("ietf-system:system")
if hostname_data:
    hostname = hostname_data["ietf-system:system"]["hostname"]
    print(f"Hostname: {hostname}")
hostname_data = restconf_get("Cisco-IOS-XE-native:native/hostname")
if hostname_data:
    hostname = hostname_data["Cisco-IOS-XE-native:hostname"]
    print(f"Hostname: {hostname}")


# === [2] Get platform info ===
platform_data = restconf_get("Cisco-IOS-XE-native:native/version")
if platform_data:
    version = platform_data["Cisco-IOS-XE-native:version"]
    print(f"IOS XE Version: {version}")

# === [3] Get interfaces ===
interfaces_data = restconf_get("ietf-interfaces:interfaces/interface")
if interfaces_data:
    print("\nInterfaces:")
    for intf in interfaces_data["ietf-interfaces:interface"]:
        print(f"- {intf['name']} : {intf.get('description', 'no description')}")

print("\nOK: RESTCONF query complete.")

