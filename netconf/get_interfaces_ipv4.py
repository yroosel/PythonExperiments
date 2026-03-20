#!/usr/bin/python
# Get configured interfaces using Netconf
# darien@sdnessentials.com

from ncclient import manager
import sys
import xml.dom.minidom
NETCONF_ROUTER_IP = "192.168.56.101"
NETCONF_SSH_PORT = "830"
NETCONF_user = "cisco"
NETCONF_psw = "cisco123!"
# XML file to open
XML_FILE = 'get_interfaces_ipv4.xml'


# create a main() method
def get_configured_interfaces():
    """Main method that retrieves the interfaces from config via NETCONF."""
    with manager.connect(host=NETCONF_ROUTER_IP, port=NETCONF_SSH_PORT, username=NETCONF_user, password=NETCONF_psw,
                         hostkey_verify=False, device_params={'name': 'default'},
                         allow_agent=False, look_for_keys=False) as m:

        with open(XML_FILE) as f:
            return(m.get_config('running', f.read()))


def main():
    """Simple main method calling our function."""
    interfaces = get_configured_interfaces()
    print(xml.dom.minidom.parseString(interfaces.xml).toprettyxml())


if __name__ == '__main__':
    sys.exit(main())
