"""
Cisco CSR1000v / IOS XE 16.9+ RESTCONF Inventory Script
Collects device characteristics, interfaces, routing, and neighbor info.
"""
###  unified Python RESTCONF script optimized for Cisco CSR1000v / IOS XE 16.9, including:
### Hostname
### Platform + Software Version
### Inventory-style hardware components (model, serial, description)
### Interfaces
### OSPF info (if configured)
### CDP/LLDP neighbors
### It automatically skips unsupported or empty datasets.
#!/usr/bin/env python3
import requests
from requests.auth import HTTPBasicAuth
import json

# --- Router details ---
ROUTER = {
    "host": "Your IP",   # IP address of the router
    "user": "Your Username",
    "password": "Your Pw"
}

# --- Disable SSL warnings for self-signed certs ---
requests.packages.urllib3.disable_warnings()

# --- RESTCONF base URL ---
BASE_URL = f"https://{ROUTER['host']}/restconf/data"

# --- Common headers ---
HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# --- Helper: perform RESTCONF GET ---
def restconf_get(resource):
    """Send a RESTCONF GET and return parsed JSON or None"""
    url = f"{BASE_URL}/{resource}"
    response = requests.get(url,
                            auth=HTTPBasicAuth(ROUTER["user"], ROUTER["password"]),
                            headers=HEADERS,
                            verify=False)
    if response.status_code == 200:
        return response.json()
    elif response.status_code == 204:
        print(f"[i] {resource}: No content (empty dataset).")
    elif response.status_code == 404:
        print(f"[w] {resource}: Not supported on this version.")
    else:
        print(f"[!] HTTP {response.status_code} for {resource}")
    return None


print("\nNow connecting to router via RESTCONF...\n")

# === [1] Hostname ===
data = restconf_get("Cisco-IOS-XE-native:native/hostname")
if data:
    hostname = data.get("Cisco-IOS-XE-native:hostname", "N/A")
    print(f"Hostname: {hostname}")

# === [2] Platform / Version ===
data = restconf_get("Cisco-IOS-XE-platform-software-oper:platform-software-version")
if data:
    info = data["Cisco-IOS-XE-platform-software-oper:platform-software-version"]
    print(f"Platform: {info.get('platform','unknown')} | Version: {info.get('version','N/A')}")

# === [3] Inventory (Hardware Components) ===
inv_data = restconf_get("Cisco-IOS-XE-platform-oper:components")
if inv_data:
    comps = inv_data.get("Cisco-IOS-XE-platform-oper:components", {}).get("component", [])
    print("\nHardware Inventory:")
    for c in comps:
        name = c.get("name", "N/A")
        desc = c.get("description", "")
        model = c.get("model-name", "")
        serial = c.get("serial-number", "")
        print(f"- {name}: {desc} | Model={model} | SN={serial}")

# === [4] Interfaces ===
int_data = restconf_get("ietf-interfaces:interfaces/interface")
if int_data:
    print("\nInterfaces:")
    for i in int_data["ietf-interfaces:interface"]:
        desc = i.get("description", "no description")
        ipv4s = i.get("ietf-ip:ipv4", {}).get("address", [])
        iplist = ", ".join([ip["ip"] for ip in ipv4s]) if ipv4s else "no IP"
        print(f"- {i['name']}: {desc} ({iplist})")

# === [5] Routing (OSPF example) ===
ospf = restconf_get("Cisco-IOS-XE-ospf-oper:ospf-oper-data")
if ospf:
    ospf_data = ospf.get("Cisco-IOS-XE-ospf-oper:ospf-oper-data", {}).get("ospf-processes", [])
    print("\nRouting (OSPF):")
    for proc in ospf_data:
        pid = proc.get("process-id")
        rid = proc.get("router-id")
        areas = proc.get("ospf-area", [])
        print(f"- Process {pid} | Router ID {rid} | Areas: {[a['area-id'] for a in areas]}")

# === [6] Neighbors (CDP/LLDP) ===
print("\nNeighbors:")
cdp = restconf_get("Cisco-IOS-XE-cdp-oper:cdp-neighbor-details")
if cdp:
    neigh = cdp.get("Cisco-IOS-XE-cdp-oper:cdp-neighbor-details", {}).get("cdp-neighbor-detail", [])
    for n in neigh:
        print(f"- CDP: {n['device-id']} via {n['local-intf-name']} ({n['port-id']})")

lldp = restconf_get("Cisco-IOS-XE-lldp-oper:lldp-entries")
if lldp:
    neigh = lldp.get("Cisco-IOS-XE-lldp-oper:lldp-entries", {}).get("lldp-entry", [])
    for n in neigh:
        print(f"- LLDP: {n['device-id']} via {n['local-intf-name']}")

print("\nOK: RESTCONF inventory query complete.\n")
