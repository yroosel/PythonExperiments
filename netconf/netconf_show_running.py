from ncclient import manager
from ncclient.xml_ import to_ele
import xml.dom.minidom

# Device details
HOST = "192.168.56.101"
USER = "Your User"
PASS = "Your Password"
PORT = 830

# Filter for Cisco native model
netconf_filter = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"/>
</filter>
"""

with manager.connect(
    host=HOST,
    port=PORT,
    username=USER,
    password=PASS,
    hostkey_verify=False,
    device_params={'name': 'csr'}
) as m:

    reply = m.get_config(source='running', filter=to_ele(netconf_filter))

    # Pretty print the XML
    print(xml.dom.minidom.parseString(reply.xml).toprettyxml())
