import json, requests, urllib3
urllib3.disable_warnings()
H="192.168.56.101"; U="cisco"; P="cisco123!"; F="application/yang-data+json"
auth=(U,P); hdr={"Accept":F,"Content-type":F}
cfg=json.load(open("loopback_config.json"))
name=cfg["ietf-interfaces:interface"]["name"]
put=f"https://{H}/restconf/data/ietf-interfaces:interfaces/interface={name}"
get=f"https://{H}/restconf/data/ietf-interfaces:interfaces"
r=requests.put(put, json=cfg, auth=auth, headers=hdr, verify=False)
print("PUT", r.status_code, r.text if r.status_code>=300 else "")
g=requests.get(get, auth=auth, headers=hdr, verify=False)
print("GET", g.status_code, g.text)


