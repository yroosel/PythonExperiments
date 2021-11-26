### RESTCONF IETF-INTERFACES USING CREDENTIALS FROM OS ENVIRONMENT
#### pip install python-decouple
import os
from decouple import config  #create filename .env containing a list of variables e.g. RESTCONFUSER=cisco
import requests
import urllib3
import datetime
print ("Current date and time: ")
print(datetime.datetime.now())
# Disable SSL Verification Warning because of Private SSL Certificate
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
restconf_router_ip = config('CSR1Kv')
restconf_user = config('RESTCONFUSER')
restconf_psw = config('RESTCONFPASW')
api_url = "https://{0}/restconf/data/ietf-interfaces:interfaces".format(restconf_router_ip)
print("restconf url: " + api_url)
# A mistake in the headers generates an HTTP ERROR 406 Not Acceptable
headers = {
    "Accept": "application/yang-data+json",
    "Content-Type": "application/yang-data+json"
}
print(headers)
#A wrong password will generate HTTP ERROR 401 Unauthorized
basicauth =(restconf_user,restconf_psw)
resp = requests.request('GET', api_url, auth=basicauth, headers=headers, verify=False)
print(resp.text)
