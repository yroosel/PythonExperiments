import json, requests, urllib3
urllib3.disable_warnings()

PARAMS = {"HOST":"YOUR HOST","USER":"YOUR USER","PASS":"YOUR PASS"}
PARAMS = {"HOST": "192.168.0.200", "USER": "cisco", "PASS": "cisco123!"}
HEADERS = {"Accept":"application/yang-data+json","Content-Type":"application/yang-data+json"}

cfg = json.load(open("loopback_config.json"))
name = cfg["ietf-interfaces:interface"]["name"]

base = f"https://{PARAMS['HOST']}/restconf/data"
auth = (PARAMS["USER"], PARAMS["PASS"])

r = requests.put(f"{base}/ietf-interfaces:interfaces/interface={name}", json=cfg, auth=auth, headers=HEADERS, verify=False)
print("PUT:", r.status_code, r.text if r.status_code >= 300 else "")

g = requests.get(f"{base}/ietf-interfaces:interfaces", auth=auth, headers=HEADERS, verify=False)
print("GET:", g.status_code)
print(g.text)
