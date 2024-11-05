from ncclient import manager
import xml.dom.minidom

# Courseware Cisco DevNet Sandbox
HOST = "192.168.56.101"
USER = "cisco"
PASS = "cisco123!"
PORT = 830

# filter
netconf_filter = """
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
       <name>GigabitEthernet1</name>
    </interface>
  </interfaces>
</filter>
"""
m = manager.connect(host=HOST, port=PORT, username=USER, password=PASS, hostkey_verify=False, device_params={'name': 'csr'})

reply = m.get_config(source='running', filter = netconf_filter)
# Pretty print the XML reply
print(xml.dom.minidom.parseString(reply.xml).toprettyxml())
m.close_session()
