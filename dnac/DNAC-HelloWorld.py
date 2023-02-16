#### DNA Center Northbound API: Hello Network 
import requests
import datetime
import json
requests.packages.urllib3.disable_warnings()
print ("Current date and time: ")
print(datetime.datetime.now())
# HARD CODED VARIABLES
DNAC_scheme = 'https://'
DNAC_authority='sandboxdnac.cisco.com'
DNAC_port=':443'
DNAC_path_token='/dna/system/api/v1/auth/token'
DNAC_path='/dna/intent/api/v1/network-device'
#### IT IS NECESSARY TO HAVE A USERNAME AND PASSWORD
DNAC_user = input("Username? ") 
DNAC_psw = input("Password? ")  
#REQUEST TOKEN BASED ON devnetuser Cisco123!
token_req_url = DNAC_scheme+DNAC_authority+DNAC_path_token
auth = (DNAC_user, DNAC_psw)
req = requests.post(token_req_url, auth=auth, verify=False)
print("API Return Code: " + str(req.status_code))  
print('Request URI: ' + token_req_url)
print("Username: " + DNAC_user)
resp = req.text
token = req.json()["Token"]
print("Received Token:")
print(token)
print("Length Token:")
print(len(token))
#REQUEST API SERVICE (USING X-AUTH-TOKEN -- INVENTORY REQUEST
req_url = DNAC_scheme+DNAC_authority+DNAC_port+DNAC_path
print(req_url)
headers = {'X-auth-token': token}
resp_devices = requests.request('GET', req_url, headers=headers, verify=False)
print(resp_devices)
resp_devices_json = resp_devices.json()
#print("Response (json):")
#print(json.dumps(resp_devices_json, indent=4))
print('Inventory Request - Filtering output')
# RESPONSE DATA: OUTPUT USING A LOOP TO PROCESS LIST ITEMS
for device in resp_devices_json['response']:
    if device['type'] != None:
        print('===')
        print('Hostname: ' + device['hostname'])
        print('Type: ' + device['type'])
        print('IP: ' + device['managementIpAddress'])
