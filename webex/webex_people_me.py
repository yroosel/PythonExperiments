##### WEBEX TEAMS API - USER ACCOUNTS - SPACES/ ROOMS - MEMBERS - MESSAGES
### ACCESS TOKEN REQUESTED THROUGH LOGIN IN WEBEX DEVELOPER WEBSITE
### Access Token 12 hours: https://developer.webex.com/docs/api/getting-started (login required)
##### BEGIN #####
import requests
import json
print("----------1----------")
current_access_token = "Your Access Token"
uri_scheme = 'https://'
uri_authority_server = 'api.ciscospark.com'
uri_api_path = '/v1/people/me'
url = uri_scheme + uri_authority_server + uri_api_path 
headers = {
    'Authorization': 'Bearer {}'.format(current_access_token),
    'Content-Type': 'application/json'
}
print('******')
for h in headers.items():
    print(h)
print('******')
# res = requests.request('GET', url, headers=headers)
res = requests.get(url, headers=headers)
##### END #####
#
### PRINTING RELEVANT DEBUGGING INFORMATION REGARDING THE API REQUEST
print("Access Token: " + current_access_token)
print("----------2----------")
print('Request URI: ' + url)
print('Request Header: ' + json.dumps(headers))
print("API Return Code: " + str(res.status_code))  
user_name = res.json()['displayName']
print("Username: " + user_name)
print("----------3----------")
#
#print("Displaying all returned information in formatted json")
#print(json.dumps(res.json(), indent=2))
if res.status_code == 200:
    print("Status is OK")
else:
    print("Status is not OK")
	
print('--------------------------------')
# => DISPLAY FILTERED RESULTS 
print("Displaying partial information")
#print(type(res))
print("Name: " + res.json()['displayName'])
print("Created: " + res.json()['created'])
print("User Type: " + res.json()['type'])
print("User Status: " + res.json()['status'])
print("--------------------------------")
