#### RESTCONF LAB 8.3.7
#### Use a Python Script to Send a PUT Request
#### Step 1: Import modules and disable SSL warnings
import json
import requests
requests.packages.urllib3.disable_warnings()
#### Step 2: Create the variables that will be the components of the request
IP_ADDRESS="192.168.56.10x"  ### "10.10.20.48"
RESTCONF_USERNAME="Your User" 
RESTCONF_PASSWORD="Your Pw" 

LOOPBACK_NAME="Loopback113"
LOOPBACK_IP_ADDR="10.113.10.1"

api_url = f"https://{IP_ADDRESS}/restconf/data/ietf-interfaces:interfaces/interface={LOOPBACK_NAME}"
headers = { "Accept": "application/yang-data+json",  "Content-type":"application/yang-data+json"  }
basicauth = (RESTCONF_USERNAME, RESTCONF_PASSWORD)

yangConfig = {
  "ietf-interfaces:interface": {
     "name": LOOPBACK_NAME,
     "description": "RESTCONF loopback",
     "type": "iana-if-type:softwareLoopback",
     "enabled": True,
     "ietf-ip:ipv4": {
         "address": [
             {
                 "ip": LOOPBACK_IP_ADDR,
                 "netmask": "255.255.255.0"
             }
         ]
     },
 "ietf-ip:ipv6": {}
 }
}

#### Step 3: Send the request and store the JSON response
#### Select required action below:
ACTION_REQUIRED = "PUT"  ### ACTION_REQUIRED = "DELETE"

resp = requests.request(ACTION_REQUIRED,api_url, data=json.dumps(yangConfig), auth=basicauth, headers=headers, verify=False)

if(resp.status_code >= 200 and resp.status_code <= 299):
 print("STATUS OK: {}".format(resp.status_code))
else:
 print("Error. Status Code: {} \nError message: {}".format(resp.status_code,resp.json()))
