import requests
import urllib3
from requests.auth import HTTPBasicAuth

urllib3.disable_warnings()

# Connection parameters
CONNECTION_PARAMETERS = {
    "HOST": "Your Host",
    "USER": "Your User",
    "PASS": "Your Pass"
}

# Base RESTCONF URL
BASE = f"https://{CONNECTION_PARAMETERS['HOST']}/restconf"

# Headers
HEADERS = {
    "Accept": "application/yang-data+json"
}

# Authentication
AUTH = HTTPBasicAuth(
    CONNECTION_PARAMETERS["USER"],
    CONNECTION_PARAMETERS["PASS"]
)

# SSL verification
VERIFY_SSL = False

# --- Retrieve RESTCONF root information ---
response = requests.get(
    BASE,
    headers=HEADERS,
    auth=AUTH,
    verify=VERIFY_SSL
)

# --- Output ---
print("HTTP Status:", response.status_code)
print(response.text)
