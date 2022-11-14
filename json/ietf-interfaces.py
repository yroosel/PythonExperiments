ietf_json = {'ietf-interfaces:interfaces': {'interface': 
    [{'name': 'GigabitEthernet1', 'description': 'VBox', 'type': 'iana-if-type:ethernetCsmacd', 'enabled': True, 
    'ietf-ip:ipv4': {'address': [{'ip': '10.1.1.1', 'netmask': '255.255.255.0'}]}, 
    'ietf-ip:ipv6': {}}, 
    {'name': 'Loopback999', 'description': '999', 'type': 'iana-if-type:softwareLoopback', 'enabled': True, 
    'ietf-ip:ipv4': {'address': [{'ip': '10.9.9.9', 'netmask': '255.255.255.0'}]}, 
    'ietf-ip:ipv6': {}}]}}
print(type(ietf_json))
print(ietf_json['ietf-interfaces:interfaces']['interface'][0].keys())
print(ietf_json['ietf-interfaces:interfaces']['interface'][0]['name'])
print(ietf_json['ietf-interfaces:interfaces']['interface'][0]['ietf-ip:ipv4']['address'][0]['ip'])
print(ietf_json['ietf-interfaces:interfaces']['interface'][1]['name'])
print(ietf_json['ietf-interfaces:interfaces']['interface'][1]['ietf-ip:ipv4']['address'][0]['ip'])
