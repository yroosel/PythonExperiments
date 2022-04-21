#### ACI REST API authentication
import json
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
import datetime

APIC_URL = "https://sandboxapicdc.cisco.com"
APIC_USER = "***UPON REQUEST***"
APIC_PW = "***UPON REQUEST***"

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
                            "name": APIC_USER,
                            "pwd": APIC_PW

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

def main(): 
    print("Current date and time: ")
    print(datetime.datetime.now())
    print('Creating function apic_login')
	requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
    ### get token
    token = apic_login()
    print(token)
    ### execute request using cookie + token
    url=APIC_URL+"/api/node/class/topology/pod-1/topSystem.json"
    #print('GET request resource: ',url)
    response = requests.get(
        url,
        headers={
            "Cookie": "APIC-cookie=" + token,
            "Content-Type": "application/json; charset=utf-8"
            }, verify=False)
    response_dict = response.json()
    print("Number of devices detected:  " + str(response_dict["totalCount"]))
    line = 1
    for s in response_dict["imdata"]:
        print("===== Device: " + str(line) + " =====")
        print(s["topSystem"]["attributes"]["address"])
        print(s["topSystem"]["attributes"]["role"])
        print(s["topSystem"]["attributes"]["state"])
        line = line+1

#### execute main() when called directly        
if __name__ == '__main__':
    main()
