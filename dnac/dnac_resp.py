dnac_resp = {
    "response": [{
        "family": "Switches and Hubs",
        "hostname": "cat_9k_1",
        "macAddress": "f8:7b:20:67:62:80",
        "serialNumber": "FCW2136L0AK",
        "upTime": "25 days, 19:42:18.12",
        "softwareType": "IOS-XE",
        "softwareVersion": "17.3.1",
        "bootDateTime": "2020-12-24 17:11:54",
        "managementIpAddress": "10.10.22.66",
        "platvormId": "C9300-24UX",
        "reachabilityStatus": "Reachable",
        "series": "Cisco Catalyst 9300 Series Switches",
        "type": "Cisco Catalyst 9300 Switch",
        "role": "ACCESS",
        "instanceUuid": "21335daf-f5a1-4e97-970f-ce4eaec339f6",
        "id": "21335daf-f5a1-4e97-970f-ce4eaec339f6"
    }],
    "version": "1.0"
}

#print(resp)
dev_list = []   #create empty list
# looping through results and filter needed information
# creating new JSON structure
for device  in resp['response']:
    if device['type'] != None:
        dev_dict = {} #create empty dict
        dev_dict['hostname'] = device['hostname']
        dev_dict['managementIpAddress'] = device['managementIpAddress']
        dev_dict['softwareType'] = device['softwareType']
        dev_dict['softwareVersion'] = device['softwareVersion']
        dev_dict['reachabilityStatus'] = device['reachabilityStatus']
        dev_list.append(dev_dict)
#print(dev_dict)
print('--------1--------')
print("Printing Keys")
for k in dev_dict.keys():
    print(k)
#print(dir(dev_dict))
print('--------2--------')
print("Printing Keys and Values")
for k,v in dev_dict.items():
    print(k + " ==> " + v )
