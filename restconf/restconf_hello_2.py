import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()
verify_ssl = False
CONNECTION_PARAMETERS = {HOST: "Your IP", USER: "Your User", PASS:"Your Pass"}
url = f"https://{CONNECTION_PARAMETERS[HOST]}/restconf/"
headers = { "Accept": "application/yang-data+json"}
auth = HTTPBasicAuth(CONNECTION_PARAMETERS[USER], CONNECTION_PARAMETERS[PASS])
response = requests.get(url, headers=headers, auth=auth, verify=verify_ssl)
print(response.text)
print(response.status_code)
