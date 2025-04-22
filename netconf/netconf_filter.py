from ncclient import manager
import xml.dom.minidom

# Courseware Cisco DevNet Sandbox
HOST = "192.168.56.101"
USER = "Your User"
PASS = "Your Password"
PORT = 830

# filter
netconf_filter = """
<filter>
  <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native"/>
</filter>
"""
m = manager.connect(host=HOST, port=PORT, username=USER, password=PASS, hostkey_verify=False, device_params={'name': 'csr'})
# 'csr' refers to Cisco CSR1000v

reply = m.get_config(source='running', filter = netconf_filter)
# Pretty print the XML reply
print(xml.dom.minidom.parseString(reply.xml).toprettyxml())
m.close_session()
