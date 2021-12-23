import requests
import json
import datetime
print ("Current date and time: ")
print(datetime.datetime.now())
api_scheme = "https://"
api_authority = "maps.googleapis.com"
api_path = "/maps/api/geocode/json"
main_api = api_scheme + api_authority + api_path # main_api = "https://maps.googleapis.com/maps/api/geocode/json"
api_key = input("Paste API Key ") 
address = input("Please enter: Full Address, Town or City? ")
api_query = "?"+"key"+"="+api_key+"&"+"address"+"="+address
uri = main_api + api_query # uri = main_api+"?"+"key"+"="+api_key+"&"+"address"+"="+address
print('Creating full request: ' + uri)
resp  = requests.get(uri)
print("Response Status Code: " + str(resp.status_code))
json_data = resp.json()
print(json_data)
### extra output example
print('--------------')
if resp.status_code == 200:
    print("LOOPING THROUGH RESULTS")
    for each in json_data["results"][0]["address_components"]:
        print(each["long_name"])
print('--------------')
