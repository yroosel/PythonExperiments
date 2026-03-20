from ncclient import manager 
from xml.dom import minidom

exp_host = "192.168.56.101"
exp_user = "cisco"
exp_pass = "cisco123!"

class InterfaceManager: 
    def __init__(self, host, username, password):  
         # Define device connection parameters  
         self.device_params = {  
             "host": host,  
             "port": 830,  
             "username": username,  
             "password": password,  
             "hostkey_verify": False }
    
    def test_netconf_connection(self): 
        """  
        Test NETCONF connectivity to the device using ncclient.  
        Returns a string message indicating success or failure.  
        """  
        try:  
            with manager.connect(**self.device_params, timeout=10) as m:  
                return "NETCONF connection successful"  
        except Exception as e:  
            return f"Connection error error: {e}"  
    
    def get_interface(self, interface_name):
        filter_xml = f"""
        <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
            <interface>
                <name>{interface_name}</name>
            </interface>
        </interfaces>
        """
        with manager.connect(**self.device_params) as m:
            config = m.get_config(source="running", filter=("subtree", filter_xml))
            
            xml_dom = minidom.parseString(config.xml)
            return xml_dom.toprettyxml(indent="    ")
    
    def update_interface_description(self, interface_name, description):
        config_xml = f"""
        <config>
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>{interface_name}</name>
                    <description>{description}</description>
                    <enabled>true</enabled>
                    <type xmlns:ianaift="urn:ietf:params:xml:ns:yang:iana-if-type">ianaift:ethernetCsmacd</type>
                </interface>
            </interfaces>
        </config>
        """
        with manager.connect(**self.device_params, timeout=10) as m:
            response = m.edit_config(target="running", config=config_xml)
            return response.xml

    def delete_interface_description(self, interface_name):
        config_xml = f"""
        <config xmlns="urn:ietf:params:xml:ns:netconf:base:1.0">
            <interfaces xmlns="urn:ietf:params:xml:ns:yang:ietf-interfaces">
                <interface>
                    <name>{interface_name}</name>
                    <description nc:operation="delete" xmlns:nc="urn:ietf:params:xml:ns:netconf:base:1.0"/>
                </interface>
            </interfaces>
        </config>
        """
        with manager.connect(**self.device_params) as m:
            m.edit_config(target="running", config=config_xml)
            print(f"Deleted description from interface {interface_name}.")

if __name__ == "__main__":
    manager_obj = InterfaceManager(exp_host, exp_user, exp_pass) 
    result = manager_obj.test_netconf_connection() 
    print(result)
    print("Current Interface Configuration:")
    print(manager_obj.get_interface("GigabitEthernet1"))
    print("Update Interface description:")
    print(manager_obj.update_interface_description ("GigabitEthernet1", "CCNA utomation: NETCONF"))
    print(manager_obj.delete_interface_description ("GigabitEthernet1"))
