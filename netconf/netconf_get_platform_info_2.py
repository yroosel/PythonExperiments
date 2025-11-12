#!/usr/bin/env python3
"""
Cisco CSR1000v / IOS XE 16.9+ NETCONF Inventory Script
Collects device characteristics, hardware inventory, interfaces,
routing (OSPF), and neighbor info (CDP/LLDP).
"""

from ncclient import manager
from xml.dom.minidom import parseString

# --- Router details ---
ROUTER = {
    "host": "192.168.56.101",
    "port": 830,
    "user": "Your User",
    "password": "Your PW!",
}

# --- Connect to router ---
print("\n Now connecting to router via NETCONF...\n")
m = manager.connect(
    host=ROUTER["host"],
    port=ROUTER["port"],
    username=ROUTER["user"],
    password=ROUTER["password"],
    hostkey_verify=False,
    device_params={"name": "csr"},
    look_for_keys=False,
    allow_agent=False
)

# --- Helper: send NETCONF <get> with filter ---
def netconf_get(filter_xml):
    reply = m.get(filter_xml)
    return reply.data_xml

# === [1] Hostname ===
hostname_filter = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
    <hostname/>
  </native>
</filter>
"""
hostname_xml = netconf_get(hostname_filter)
print("Hostname:")
print(parseString(hostname_xml).toprettyxml())

# === [2] Platform / Version ===
version_filter = """
<filter>
  <platform-software-version xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-platform-software-oper"/>
</filter>
"""
version_xml = netconf_get(version_filter)
print("Platform / Software Version:")
print(parseString(version_xml).toprettyxml())

# === [3] Hardware Inventory ===
inventory_filter = """
<filter>
  <components xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-platform-oper"/>
</filter>
"""
inventory_xml = netconf_get(inventory_filter)
print("Hardware Inventory:")
print(parseString(inventory_xml).toprettyxml())

# === [4] Interfaces ===
interfaces_filter = """
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface/>
  </interfaces>
</filter>
"""
interfaces_xml = netconf_get(interfaces_filter)
print("Interfaces:")
print(parseString(interfaces_xml).toprettyxml())

# === [5] Routing (OSPF) ===
ospf_filter = """
<filter>
  <ospf-oper-data xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-ospf-oper"/>
</filter>
"""
ospf_xml = netconf_get(ospf_filter)
print("Routing (OSPF):")
print(parseString(ospf_xml).toprettyxml())

# === [6] Neighbors (CDP & LLDP) ===
cdp_filter = """
<filter>
  <cdp-neighbor-details xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-cdp-oper"/>
</filter>
"""
cdp_xml = netconf_get(cdp_filter)
print("CDP Neighbors:")
print(parseString(cdp_xml).toprettyxml())

lldp_filter = """
<filter>
  <lldp-entries xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-lldp-oper"/>
</filter>
"""
lldp_xml = netconf_get(lldp_filter)
print("LLDP Neighbors:")
print(parseString(lldp_xml).toprettyxml())

print("\nOK: NETCONF inventory query complete.\n")
m.close_session()
