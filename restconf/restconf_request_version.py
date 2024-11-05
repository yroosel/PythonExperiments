import requests
from requests.auth import HTTPBasicAuth

# The URL to make the request to
url = 'https://192.168.56.103/restconf/'

# Custom headers for the request
headers = {
    "Accept": "application/yang-data+json"
}

# Disable SSL warnings and verification (Equivalent to curl's -k option)
requests.packages.urllib3.disable_warnings()
verify_ssl = False

# Basic authentication credentials
auth = HTTPBasicAuth('cisco', 'cisco123!')

# Making the GET request
response = requests.get(url, headers=headers, auth=auth, verify=verify_ssl)

# Printing the response text (body)
print(response.text)

# Optionally, print the status code
print(response.status_code)
