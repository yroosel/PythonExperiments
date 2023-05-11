### Delete loopback
# Ask interactively for the Loopback Interface Details to Delete
# Create an XML filter for targeted NETCONF queries
import xml.dom.minidom
import xmltodict
from ncclient import manager
import datetime
print ("Current date and time: ")
print(datetime.datetime.now())
NETCONF_ROUTER_IP = "192.168.56.107"
NETCONF_SSH_PORT = "830"
NETCONF_user = input("Username? ")  # ciscocisco
NETCONF_psw = input("Password? ")   # cisco123!
### ** kwargs
m = manager.connect(
        host=NETCONF_ROUTER_IP,
        port=NETCONF_SSH_PORT,
        username=NETCONF_user,
        password=NETCONF_psw,
        hostkey_verify=False
        )
# IETF Interface Types
IETF_INTERFACE_TYPES = {
        "loopback": "ianaift:softwareLoopback",
        "ethernet": "ianaift:ethernetCsmacd"
    }

# Create an XML configuration template for ietf-interfaces
netconf_interface_template = """
<config>
    <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
        <interface operation="delete">
            <name>{name}</name>
        </interface>
    </interfaces>
</config>"""

# Ask for the Interface Details to Add
new_loopback = {}
new_loopback["name"] = "Loopback" + input("What loopback number to delete? ")

# Create the NETCONF data payload for this interface
netconf_data = netconf_interface_template.format(
        name = new_loopback["name"]
    )

print("The configuration payload to be sent over NETCONF.\n")
print(netconf_data)

# Make a NETCONF <get-config> query using the filter
netconf_reply = m.edit_config(netconf_data, target = 'running')

print("Here is the raw XML data returned from the device.\n")
# Print out the raw XML that returned
print(xml.dom.minidom.parseString(netconf_reply.xml).toprettyxml())
print("")
m.close_session()
