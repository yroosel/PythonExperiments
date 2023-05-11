### Based on ETW Network Programmability Lab 2.7 
### and   on DEVNET Learning Track: "Exploring IOS XE YANG Data Models with NETCONF"
### !pip install ncclient
import datetime
print ("Current date and time: ")
print(datetime.datetime.now())
print("Starting Application")
print("Selecting  ncclient library for NETCONF operations")
from ncclient import manager
print('Setup connection using the manager.connect() function')
print('Using hard-coded variable values for training purposes')
NETCONF_ROUTER_IP = input("IP Address? ")
NETCONF_SSH_PORT = "830"
NETCONF_user = input("Username? ")
NETCONF_psw = input("Password? ")
print('------1-------')
print('NETCONF <hello> Operation')
"""
<?xml version="1.0" encoding="UTF-8"?>
<hello xmlns="urn:ietf:params:xml:ns:netconf:base:1.1">
 <capabilities>
   <capability>urn:ietf:params:netconf:base:1.1</capability>
 </capabilities>
</hello>
"""
### ** kwargs
m = manager.connect(
        host=NETCONF_ROUTER_IP,
        port=NETCONF_SSH_PORT,
        username=NETCONF_user,
        password=NETCONF_psw,
        hostkey_verify=False
        )
#print(dir(m))
print('------2-------')
print(m.connected)
print('------3-------')
print('Supported capabilities')
i = 0
for capability in m.server_capabilities:
    print (capability)
    i = i+1
print(i)
m.close_session()

