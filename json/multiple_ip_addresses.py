import json
multiple_addresses = [{"ip": "192.168.56.101", "netmask": "255.255.255.0"},
                      {"ip": "192.0.2.1", "netmask": "255.255.255.252"} ]
prefixes = { "255.255.255.0": "/24" , "255.255.255.192": "/26" , "255.255.255.252": "/30"}

print(multiple_addresses)
which_address = 0
address = multiple_addresses[which_address]["ip"]
print(address)
mask = multiple_addresses[which_address]["netmask"]
print(mask)
prefix = prefixes[mask]
print(prefix)
print(address+prefix)
