from ncclient import manager
import xml.dom.minidom
import datetime
print ("Current date and time: ")
print(datetime.datetime.now())
print('Starting NETCONFIG')
print('Connecting to virtual router with ncclient')
NETCONF_ROUTER_IP = "192.168.56.101"
NETCONF_SSH_PORT = "830"
NETCONF_user = "cisco"
NETCONF_psw = "cisco123!"
# FILTER is needed for netconf
FILTER = """
<filter>
  <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
    <interface>
       <name></name>
    </interface>
  </interfaces>
</filter>
"""
# CONNECTING
m = manager.connect(
        host=NETCONF_ROUTER_IP,
        port=NETCONF_SSH_PORT,
        username=NETCONF_user,
        password=NETCONF_psw,
        hostkey_verify=False
        )
# OUTPUTS
print("Connection Succeeded:", end=" ")
print(m.connected)
print('Retrieving get-config from virtual router')
netconfig_reply = m.get_config("running", FILTER)
print('Parsing and printing XML')
print(xml.dom.minidom.parseString(netconfig_reply.xml).toprettyxml())
m.close_session()
