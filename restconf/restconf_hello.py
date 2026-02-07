# restconf hello
import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()
verify_ssl = False
url = "https://192.168.56.101/restconf/"
headers = { "Accept": "application/yang-data+json"}
auth = HTTPBasicAuth('cisco', 'cisco123!')
response = requests.get(url, headers=headers, auth=auth, verify=verify_ssl)
print(response.text)
print(response.status_code)
