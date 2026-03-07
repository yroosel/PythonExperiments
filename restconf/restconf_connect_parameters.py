import requests
from requests.auth import HTTPBasicAuth

# Disable SSL warnings
requests.packages.urllib3.disable_warnings()
verify_ssl = False

# Connection parameters
CONNECTION_PARAMETERS = {
    "HOST": "44.201.40.38",
    "USER": "npe-restconf",
    "PASS": "C1sco12345"
}

# RESTCONF URL
url = f"https://{CONNECTION_PARAMETERS['HOST']}/restconf/"

# Headers
headers = {
    "Accept": "application/yang-data+json"
}

# Authentication
auth = HTTPBasicAuth(
    CONNECTION_PARAMETERS["USER"],
    CONNECTION_PARAMETERS["PASS"]
)

# Send request
response = requests.get(url, headers=headers, auth=auth, verify=verify_ssl)

print(response.text)
print(response.status_code)
