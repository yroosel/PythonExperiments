###  Same as previous cell with interactive input of access token
import requests
import json
import datetime
print ("Current date and time: ")
print(datetime.datetime.now())
print('Starting Cisco Webex Teams API, Get Account Information')
# Get an Access Token 12 hours: https://developer.webex.com/docs/api/getting-started
# Bearer Authentication
webex_acccess_token = input("Access Token? ") 
url = 'https://api.ciscospark.com/v1/people/me'
headers = {
    'Authorization': 'Bearer {}'.format(webex_acccess_token),
    'Content-Type': 'application/json'
}
res = requests.get(url, headers=headers)
#print(type(res))
#print(res.json())
#print(res.json()['sipAddresses'][1]['displayName'])
#print(res.json()['displayName'])
#print(res.json()['created'])

print(json.dumps(res.json(), indent=4))