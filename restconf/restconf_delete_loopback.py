import json
import requests
import urllib3

urllib3.disable_warnings()

# Connection parameters
CONNECTION_PARAMETERS = {
    "HOST": "Your Host",
    "USER": "Your User",
    "PASS": "Your Pass"
}

# RESTCONF headers
HEADERS = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}

# Load configuration from JSON file (only used to get interface name)
with open("loopback_config.json") as f:
    config = json.load(f)

# Extract interface name
interface_name = config["ietf-interfaces:interface"]["name"]

# RESTCONF URLs
base_url = f"https://{CONNECTION_PARAMETERS['HOST']}/restconf/data"

delete_url = f"{base_url}/ietf-interfaces:interfaces/interface={interface_name}"
get_url = f"{base_url}/ietf-interfaces:interfaces"

# Authentication
auth = (
    CONNECTION_PARAMETERS["USER"],
    CONNECTION_PARAMETERS["PASS"]
)

# --- Delete interface ---
response_delete = requests.delete(
    delete_url,
    auth=auth,
    headers=HEADERS,
    verify=False
)

print("DELETE status:", response_delete.status_code)

if response_delete.status_code >= 300:
    print("Error:", response_delete.text)

# --- Retrieve interfaces to verify ---
response_get = requests.get(
    get_url,
    auth=auth,
    headers=HEADERS,
    verify=False
)

print("GET status:", response_get.status_code)
print(response_get.text)
