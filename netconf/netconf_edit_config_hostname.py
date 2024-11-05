import sys
from argparse import ArgumentParser
from ncclient import manager
import xml.dom.minidom

data = '''
  <config>
    <native xmlns="http://cisco.com/ns/yang/Cisco-IOS-XE-native">
      <hostname>NC-WAS-HERE</hostname>
    </native>
  </config>
'''

if __name__ == '__main__':
    v_host = "192.168.56.101" 
    v_port = 830
    v_username = "cisco"
    v_password = "cisco123!"

    try:
        m = manager.connect(
            host=v_host,
            port=v_port,
            username=v_username,
            password=v_password,
            hostkey_verify=False,
            device_params={'name': "csr"}
        )
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

    if m:
        response = m.edit_config(target='running', config=data)
        xmlDom = xml.dom.minidom.parseString(response.xml)
        print(xmlDom.toprettyxml(indent="  "))
