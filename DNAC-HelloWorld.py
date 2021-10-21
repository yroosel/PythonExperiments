# pip install requests
#!/usr/bin/env python
"""DNAv3 - DNAC Northbound API - Hands on exercise 01
In this exercise we create helper functions to get an auth token
from DNAC - get_auth_token() and also get_url(), create_url() and
list_network_devices() to get a list of all network devices managed
by Cisco DNA Center. In the main function we extract some data we find useful
and pretty print the result.

Copyright (c) 2018 Cisco and/or its affiliates.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import sys
import json
import requests
import os
from requests.auth import HTTPBasicAuth
import datetime

print ("Current date and time: ")
print(datetime.datetime.now())
print('STARTING Cisco DNA Center Northbound API Hello Network Script & Creating variables')

requests.packages.urllib3.disable_warnings()

DNAC=os.environ.get('DNAC','sandboxdnac.cisco.com')
DNAC_PORT=os.environ.get('DNAC_PORT',443)
DNAC_USER=os.environ.get('DNAC_USER','devnetuser')
DNAC_PASSWORD=os.environ.get('DNAC_PASSWORD','Cisco123!')


def get_auth_token(controller_ip=DNAC, username=DNAC_USER, password=DNAC_PASSWORD):
    """ Authenticates with controller and returns a token to be used in subsequent API invocations
    """

    login_url = "https://{0}:{1}/dna/system/api/v1/auth/token".format(controller_ip, DNAC_PORT)
    result = requests.post(url=login_url, auth=HTTPBasicAuth(DNAC_USER, DNAC_PASSWORD), verify=False)
    result.raise_for_status()

    token = result.json()["Token"]
    return {
        "controller_ip": controller_ip,
        "token": token
    }

def create_url(path, controller_ip=DNAC):
    """ Helper function to create a DNAC API endpoint URL
    """

    return "https://%s:%s/dna/intent/api/v1/%s" % (controller_ip, DNAC_PORT, path)

def get_url(url):

    url = create_url(path=url)
    print(url)
    token = get_auth_token()
    headers = {'X-auth-token' : token['token']}
    try:
        response = requests.get(url, headers=headers, verify=False)
    except requests.exceptions.RequestException as cerror:
        print("Error processing request", cerror)
        sys.exit(1)

    return response.json()

def list_network_devices():
    return get_url("network-device")

print ("Current date and time: ")
print(datetime.datetime.now())
print('RESULTS of Cisco DNA Center Northbound API Hello Network Script')
#if name == "main":
response = list_network_devices()
#type(response)
#print(response)
#print("Version: " +response['version'])
print(json.dumps(response, indent=4))

#Print response in nice format
print("{0:25}{1:16}{2:12}{3:18}{4:12}{5:16}{6:15}".
    format("hostname","IP","serial",
    "platformId","SW Version","role","Uptime"))

for device in response['response']:
    if device['type'] != None:
        uptime = "N/A" if device['upTime'] is None else device['upTime']
        print("{0:25}{1:16}{2:12}{3:18}{4:12}{5:16}{6:15}".
            format(device['hostname'],
                   device['managementIpAddress'],
                   device['serialNumber'],
                   device['platformId'],
                   device['softwareVersion'],
                   device['role'],
                   device['upTime']))

        
