# restconf hello
import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()
verify_ssl = False
url = "https://x01.y01.z01.xxx/restconf/"
headers = { "Accept": "application/yang-data+json"}
auth = HTTPBasicAuth('Your User', 'Your Pass')
response = requests.get(url, headers=headers, auth=auth, verify=verify_ssl)
print(response.text)
print(response.status_code)
