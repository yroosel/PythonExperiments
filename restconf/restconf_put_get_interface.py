import requests
requests.packages.urllib3.disable_warnings()

IP_HOST="192.168.56.107"
RESTCONF_USERNAME="ADD YOUR USERNAME"
RESTCONF_PASSWORD="AA YOUR PASSWORD"
DATA_FORMAT="application/yang-data+json"
LOOPBACK_INTERFACE="Loopback199"
LOOPBACK_IP="10.1.99.1"

api_url_put = f"https://{IP_HOST}/restconf/data/ietf-interfaces:interfaces/interface={LOOPBACK_INTERFACE}"
api_url_get = f"https://{IP_HOST}/restconf/data/ietf-interfaces:interfaces"
headers = { "Accept": DATA_FORMAT ,  "Content-type": DATA_FORMAT }
basicauth = (RESTCONF_USERNAME, RESTCONF_PASSWORD)
yangConfig = {
  "ietf-interfaces:interface": {
     "name": LOOPBACK_INTERFACE,
     "description": f"RESTCONF => {LOOPBACK_INTERFACE}",
     "type": "iana-if-type:softwareLoopback",
     "enabled": True,
     "ietf-ip:ipv4": {
         "address": [
             {
                 "ip": LOOPBACK_IP,
                 "netmask": "255.255.255.0"
             }
         ]
     }
 }
}

resp_put = requests.put(api_url_put, json=yangConfig, auth=basicauth, headers=headers, verify=False)

if resp_put.status_code in range(200,300):
    print(f"STATUS OK: {resp_put.status_code}") 
else:
    print("ERROR") 
    print(resp_put.status_code)
    print(resp_put.text)

resp_get = requests.get(api_url_get, auth=basicauth, headers=headers, verify=False)
print(resp_get.text)
