#!/usr/bin/python
from ncclient import manager
import xml.etree.ElementTree as ET

# Device connection info
HOST = "192.168.56.105"
PORT = 830
USER = "Your User"
PASS = "Your Password"

# Cisco IOS XE operational YANG model filter
FILTER = """
<filter xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
  <interfaces xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper"/>
</filter>
"""

def get_interfaces_with_ips():
    """Connect and retrieve interface XML via NETCONF."""
    with manager.connect(
        host=HOST,
        port=PORT,
        username=USER,
        password=PASS,
        hostkey_verify=False,
        device_params={'name': 'csr'},
        allow_agent=False,
        look_for_keys=False
    ) as m:
        return m.get(filter=FILTER).xml

def parse_and_display_interfaces(xml_data):
    """Parse XML and display interface names and IP addresses."""
    ns = {'cisco': 'http://cisco.com/ns/yang/Cisco-IOS-XE-interfaces-oper'}
    root = ET.fromstring(xml_data)

    for interface in root.findall(".//cisco:interface", ns):
        name_elem = interface.find("cisco:name", ns)
        name = name_elem.text if name_elem is not None else "unknown"

        # Try to get flat IPv4 and mask values
        ipv4_elem = interface.find("cisco:ipv4", ns)
        mask_elem = interface.find("cisco:ipv4-subnet-mask", ns)

        if ipv4_elem is not None and mask_elem is not None:
            ip = ipv4_elem.text
            netmask = mask_elem.text
            print(f"✅ Interface: {name} | IP Address: {ip}/{netmask}")
        else:
            print(f"⚠️ Interface: {name} | No IP address or mask found")

def main():
    xml_response = get_interfaces_with_ips()
    parse_and_display_interfaces(xml_response)

if __name__ == '__main__':
    main()
