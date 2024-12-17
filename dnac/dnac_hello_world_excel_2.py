import requests
import json
from tabulate import tabulate
from openpyxl import Workbook

# Disable warnings about unverified HTTPS requests
requests.packages.urllib3.disable_warnings()

# Constants for DNA Center API access
DNAC_SCHEME = 'https://'
DNAC_AUTHORITY = 'sandboxdnac.cisco.com'
DNAC_PORT = ':443'
DNAC_PATH_TOKEN = '/dna/system/api/v1/auth/token'
DNAC_PATH_NETWORK_DEVICES = '/dna/intent/api/v1/network-device'
DNAC_USER = "add user name"
DNAC_PASSWORD = "add password"

def get_auth_token():
    """Request an authentication token from DNA Center."""
    url = f"{DNAC_SCHEME}{DNAC_AUTHORITY}{DNAC_PATH_TOKEN}"
    response = requests.post(url, auth=(DNAC_USER, DNAC_PASSWORD), verify=False)
    if response.status_code == 200:
        return response.json()['Token']
    else:
        raise Exception(f"Failed to obtain token: {response.status_code}")

def get_network_devices(token):
    """Retrieve the list of network devices from DNA Center."""
    url = f"{DNAC_SCHEME}{DNAC_AUTHORITY}{DNAC_PORT}{DNAC_PATH_NETWORK_DEVICES}"
    headers = {'X-auth-token': token}
    response = requests.get(url, headers=headers, verify=False)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Failed to get network devices: {response.status_code}")

def print_device_info_table(devices):
    """Prints device information in a table format."""
    headers = ["Hostname", "Type", "IP Address"]
    data = [[device['hostname'], device['type'], device['managementIpAddress']] 
            for device in devices['response'] if device['type'] is not None]
    print(tabulate(data, headers=headers, tablefmt="grid"))

def write_devices_to_excel(devices, filename='dnac_output.xlsx'):
    """Writes device information to an Excel file."""
    wb = Workbook()
    ws = wb.active
    ws.append(["Hostname", "Type", "IP Address"])
    for device in devices['response']:
        if device['type'] is not None:
            ws.append([device['hostname'], device['type'], device['managementIpAddress']])
    wb.save(filename)
    print(f"Device information written to {filename}")

def main():
    try:
        print("Requesting Authentication Token...")
        token = get_auth_token()
        print(f"Received Token: {token[:10]}... [Truncated]")
        
        print("Requesting Network Devices Information...")
        devices = get_network_devices(token)
        
        print("Printing Device Information in Table Format...")
        print_device_info_table(devices)
        
        print("Writing Device Information to Excel...")
        write_devices_to_excel(devices)
        
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
