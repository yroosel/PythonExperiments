import datetime
print ("Current date and time: ")
print(datetime.datetime.now())
print('Starting  -- Cisco SD-WAN -- Authentication and Devices')
import requests
import pprint 
import urllib3 
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
vmanage_host = 'devasc-sdwan-1.cisco.com'
vmanage_port = '443'
vmanage_username = input("Username? ")
vmanage_password = input("Password? ")
base_url = 'https://%s:%s'%(vmanage_host, vmanage_port)
login_action = '/j_security_check' # Session token is retrieved from the path '/j_security_check' 
login_data = {'j_username' : vmanage_username, 'j_password' : vmanage_password}
login_url = base_url + login_action  
session = requests.session()
login_response = session.post(url=login_url, data=login_data, verify=False)
if b'<html>' in login_response.content: # If the response is in HTML, it means that a login error has occurred
    print ("Login Failed")
    exit(1)
# XSRF Token is used to prevent cross-site request forgery attacks and is required in vManage 19.X
xsrf_token_url = base_url + '/dataservice/client/token'
login_token = session.get(url=xsrf_token_url, verify=False)
if login_token.status_code == 200:
    if b'<html>' in login_token.content:
        print ("Login Token Failed")
        exit(1)
    session.headers['X-XSRF-TOKEN'] = login_token.content
device_url = base_url + '/dataservice/device'
device_list = session.get(url=device_url, verify=False)
if device_list.status_code == 200:
    json_data = device_list.json()
    pp = pprint.PrettyPrinter(indent=4)
    pp.pprint (json_data)
else:
    print (device_list.status_code)
    exit(1)
