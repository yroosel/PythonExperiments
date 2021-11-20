import requests
import json
import datetime
print ("Current date and time: ")
print(datetime.datetime.now())
print('Starting Cisco Webex Teams API, Get Account Information')
# This access token may be a (limited duration) personal access token, a Bot token, or an OAuth token from an Integration or Guest Issuer application.
# Make sure to replace access_token with YOUR access token.
# Access Token 12 hours: https://developer.webex.com/docs/api/getting-started
# Bearer
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