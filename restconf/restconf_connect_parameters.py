import requests
from requests.auth import HTTPBasicAuth

requests.packages.urllib3.disable_warnings()

CONNECTION_PARAMETERS = {"HOST": "44.201.40.38", "USER": "npe-restconf", "PASS": "C1sco12345"}

url = f"https://{CONNECTION_PARAMETERS['HOST']}/restconf/"
auth = HTTPBasicAuth(CONNECTION_PARAMETERS["USER"], CONNECTION_PARAMETERS["PASS"])

r = requests.get(url, headers={"Accept": "application/yang-data+json"}, auth=auth, verify=False)

print(r.text)
print(r.status_code)
