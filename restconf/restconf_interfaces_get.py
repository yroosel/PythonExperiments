#### RESTCONF LAB 8.3.7
#### Part 6: Use a Python script to Send GET Requests

#### Step 1: Create the RESTCONF directory and start the script
import json
import requests
requests.packages.urllib3.disable_warnings()

#### Step 2: Create the variables that will be the components of the request
IP_HOST="192.168.56.101"
RESTCONF_USERNAME="cisco"
RESTCONF_PASSWORD="cisco123!"
DATA_FORMAT="application/yang-data+json"
LOOPBACK_INTERFACE="Loopback11"
LOOPBACK_IP="10.1.1.11"
basicauth = (RESTCONF_USERNAME, RESTCONF_PASSWORD)
api_url = f"https://{IP_HOST}/restconf/data/ietf-interfaces:interfaces/interface={LOOPBACK_INTERFACE}"
headers = { "Accept": "application/yang-data+json",  "Content-type":"application/yang-data+json" }

#### Step 3: Create a variable to send the request and store the JSON response
resp = requests.get(api_url, auth=basicauth, headers=headers, verify=False)
print(resp.status_code)
#print(dir(resp))
#print(resp.text)

#### Step 4: Format and display the JSON data received from the CSR1kv.
response_json = resp.json()
#print(response_json)
print(json.dumps(response_json, indent=4))