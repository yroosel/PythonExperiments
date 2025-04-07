import yaml
import json
import requests
requests.packages.urllib3.disable_warnings()

IP_HOST="192.168.56.10x"
RESTCONF_USERNAME="Your Username"
RESTCONF_PASSWORD="Your Password"

DATA_FORMAT="application/yang-data+json"

ACTION_REQUIRED = "PUT"  ### 
ACTION_REQUIRED = "DELETE"

LOOPBACK_INTERFACE="Loopback199"
LOOPBACK_IP="10.199.10.1"

### INPUT IN YAML => TRANSFORM INTO DICT & JSON
yangConfig_yaml = f"""
---
ietf-interfaces:interface:
  description: restconf => { LOOPBACK_INTERFACE }
  enabled: true
  ietf-ip:ipv4:
    address:
    - ip: { LOOPBACK_IP }
      netmask: 255.255.255.0
  name: { LOOPBACK_INTERFACE }
  type: iana-if-type:softwareLoopback
"""
# Convert yaml to dict
yangConfig_dict = yaml.safe_load(yangConfig_yaml)
# Convert to JSON: yangConfig_json = json.dumps(yangConfig_dict, indent=2)

api_url = f"https://{IP_HOST}/restconf/data/ietf-interfaces:interfaces/interface={LOOPBACK_INTERFACE}"
headers = { "Accept": DATA_FORMAT ,  "Content-type": DATA_FORMAT }
basicauth = (RESTCONF_USERNAME, RESTCONF_PASSWORD)

resp = requests.request(ACTION_REQUIRED,api_url, json=yangConfig_dict, auth=basicauth, headers=headers, verify=False)

if resp.status_code in range(200,300):
    print(f"STATUS OK: {resp.status_code}") 
else:
    print("ERROR") 
    print(resp.status_code)
    print(resp.text)
