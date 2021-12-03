import requests
import urllib.parse
address = 'Liedekerke, Belgium'
url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(address) +'?format=json'
response = requests.get(url).json()
#print(response)
print(response[0]["lat"])
print(response[0]["lon"])
