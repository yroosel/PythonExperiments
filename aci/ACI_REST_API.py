#### ACI REST API authentication and JSON Filtering
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import datetime
print ("Current date and time: ")
print(datetime.datetime.now())
print('Creating function apic_login')

APIC_URL = "https://sandboxapicdc.cisco.com"

def apic_login():
    """ Login to APIC """

    token = ""
    err = ""

    try:
        response = requests.post(
            url=APIC_URL+"/api/aaaLogin.json",
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps(
                {
                    "aaaUser": {
                        "attributes": {
                            "name": "admin",
                            "pwd": "Insert Your Password"
                        }
                    }
                }
            ),
            verify=False
        )

        json_response = json.loads(response.content)
        token = json_response['imdata'][0]['aaaLogin']['attributes']['token']
        print("Token obtained: " )
        print(token)

        print('Response HTTP Status Code: {status_code}'.format(
            status_code=response.status_code))
    except requests.exceptions.RequestException as err:
        print("HTTP Request failed")
        print(err)

    return token

def get_tenants():
    """ Get Tenants """

    token = apic_login()
    url=APIC_URL+"/api/node/class/fvTenant.json"
    print('GET request resource: ',url)

    try:
        response = requests.get(
            url,
            headers={
                "Cookie": "APIC-cookie=" + token,
                "Content-Type": "application/json; charset=utf-8",
            },
            verify=False
        )

        print('Response HTTP Status Code: {status_code}'.format(
           status_code=response.status_code))
        print('Response HTTP Response Body:', json.dumps(response.json(), indent=4))

    except requests.exceptions.RequestException:
        print("HTTP Request failed")

def get_devices():
    token = apic_login()
    url=APIC_URL+"/api/node/class/topology/pod-1/topSystem.json"
    print('GET request resource: ',url)

    try:
        response = requests.get(
            url,
            headers={
                "Cookie": "APIC-cookie=" + token,
                "Content-Type": "application/json; charset=utf-8"
                },
                verify=False)

        print('Response HTTP Status Code: {status_code}'.format(status_code=response.status_code))
        print('Response HTTP Response Body:', json.dumps(response.json(), indent=4))

    except requests.exceptions.RequestException:
        print("HTTP Request failed")
    
# print('Full JSON output of get_tenants')
# Suppress credential warning for this exercise
# requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
# print('=========================GET TENANTS=======================')
# get_tenants()

print('Full JSON output of get_devices')
# Suppress credential warning for this exercise
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
print('=========================GET DEVICES=======================')
get_devices()


