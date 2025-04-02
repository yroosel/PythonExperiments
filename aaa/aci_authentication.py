#### ACI REST API authentication
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import datetime

APIC_URL = "https://sandboxapicdc.cisco.com"

def apic_login():
    """ Login to APIC """
    token = ""
    try:
        response = requests.post(
            url=APIC_URL + "/api/aaaLogin.json",
            headers={
                "Content-Type": "application/json; charset=utf-8",
            },
            data=json.dumps({
                "aaaUser": {
                    "attributes": {
                        "name": "admin",
                        "pwd": "!v3G@!4@Y"
                    }
                }
            }),
            verify=False
        )

        response.raise_for_status()
        json_response = response.json()
        token = json_response['imdata'][0]['aaaLogin']['attributes']['token']
        print("Token obtained: " + token)
        print(f"Response HTTP Status Code: {response.status_code}")

    except requests.exceptions.RequestException as err:
        print("HTTP Request failed")
        print(err)

    return token

def main(): 
    print("Current date and time: ")
    print(datetime.datetime.now())
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

    print('Creating function apic_login')
    token = apic_login()
    if not token:
        print("Login failed. Exiting.")
        return

    url = APIC_URL + "/api/node/class/topology/pod-1/topSystem.json"
    try:
        response = requests.get(
            url,
            headers={
                "Cookie": "APIC-cookie=" + token,
                "Content-Type": "application/json; charset=utf-8"
            },
            verify=False
        )
        response.raise_for_status()
        response_dict = response.json()

        print("Number of devices detected: " + str(len(response_dict["imdata"])))
        for i, s in enumerate(response_dict["imdata"], 1):
            print(f"===== Device: {i} =====")
            print("IP: "+s["topSystem"]["attributes"]["address"])
            print("Role: "+s["topSystem"]["attributes"]["role"])
            print("State: "+s["topSystem"]["attributes"]["state"])

    except requests.exceptions.RequestException as err:
        print("Failed to retrieve topology data")
        print(err)

if __name__ == '__main__':
    main()
