### TAKEN FROM DEVNET LEARNING TRACK Exploring IOS XE YANG Data Models with NETCONF
# Adding Loopback interface to the Configuration
# Ask interactively for the Loopback Interface Details 
# Create the NETCONF data payload for this interface
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
        <interface>
            <name>{if_name}</name>
            <description>{if_desc}</description>
            <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">
                {if_type}
            </type>
            <enabled>{if_status}</enabled>
            <ipv4 xmlns="urn:ietf:params:xml:ns:yang:ietf-ip">
                <address>
                    <ip>{ip_address}</ip>
                    <netmask>{subnet_mask}</netmask>
                </address>
            </ipv4>
        </interface>
    </interfaces>
</config>"""

# Ask for the Interface Details to Add
new_loopback = {}
new_loopback["if_name"] = "Loopback" + input("What loopback number to add? ")
new_loopback["if_desc"] = input("What description to use? ")
new_loopback["if_type"] = IETF_INTERFACE_TYPES["loopback"]
new_loopback["if_status"] = "true"
new_loopback["ip_address"] = input("What IP address? ")
new_loopback["subnet_mask"] = input("What network mask? ")

# Create the NETCONF data payload for this interface
netconf_data = netconf_interface_template.format(
        if_name = new_loopback["if_name"],
        if_desc = new_loopback["if_desc"],
        if_type = new_loopback["if_type"],
        if_status = new_loopback["if_status"],
        ip_address = new_loopback["ip_address"],
        subnet_mask = new_loopback["subnet_mask"]
)

netconf_reply = m.edit_config(netconf_data, target = 'running')
m.close_session()
