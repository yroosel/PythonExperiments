import xml.dom.minidom
import datetime
print ("Current date and time: ")
print(datetime.datetime.now())
NETCONF_ROUTER_IP = "192.168.56.107"
NETCONF_SSH_PORT = "830"
NETCONF_user = input("Username? ")  # ciscocisco
NETCONF_psw = input("Password? ")   # cisco123!
from ncclient import manager
print('Starting NETCONFIG')
print('Connecting to virtual router with ncclient')
m = manager.connect(
        host=NETCONF_ROUTER_IP,
        port=NETCONF_SSH_PORT,
        username=NETCONF_user,
        password=NETCONF_psw,
        hostkey_verify=False
        )
print("Connection Succeeded:", end=" ")
print(m.connected)
print('Retrieving get-config from virtual router')
netconfig_reply = m.get_config(source="running")
print('Parsing and printing XML')
print(xml.dom.minidom.parseString(netconfig_reply.xml).toprettyxml())
