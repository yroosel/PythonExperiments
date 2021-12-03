#NSO -- Get Devices
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import datetime
print ("Current date and time: ")
print(datetime.datetime.now())
print('Retrieving -- Cisco NSO -- Get Devices')
NSO_user = input("Username? ")
NSO_psw = input("Password? ")
url = "https://devasc-nso-1.cisco.com/restconf/data/tailf-ncs:devices/device=ios0/config"
headers = {"Content-Type": "application/yang-data+json" }
# Supress credential warning for this exercise
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
response = requests.get(url,
                        auth=(NSO_user, NSO_psw),
                        headers=headers,
                        verify=False)
print(response.text)