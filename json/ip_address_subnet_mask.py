import json
single_address =  {"ip": "192.168.56.101","netmask": "255.255.255.192"}
prefixes = { "255.255.255.0": "/24" , "255.255.255.192": "/26" , "255.255.255.252": "/30"}
address = single_address["ip"]
print(address)
mask = single_address["netmask"]
print(mask)
print(prefixes["255.255.255.0"])
print(prefixes["255.255.255.252"])
