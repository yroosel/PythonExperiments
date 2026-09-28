import requests
import json
### Access Token 12 hours: https://developer.webex.com/docs/api/getting-started (login required)

print("---------- 1. API REQUEST ----------")

# Personal Access Token
current_access_token = "Your Access Token"

# Webex API endpoint
url = "https://webexapis.com/v1/people/me"

# HTTP headers
headers = {
    "Authorization": f"Bearer {current_access_token}",
    "Content-Type": "application/json"
}

# Send GET request
res = requests.get(
    url,
    headers=headers,
    timeout=10
)

print("Request URI:", url)
print("API Return Code:", res.status_code)

print("\n---------- 2. API RESPONSE ----------")

# Check whether the request was successful
if res.ok:
    print("Status is OK")

    # Convert JSON response into a Python dictionary
    data = res.json()

    print("\nDisplaying partial information")
    print("Name:", data.get("displayName"))
    print("Created:", data.get("created"))
    print("User Type:", data.get("type"))
    print("User Status:", data.get("status"))

else:
    print("Status is NOT OK")
    print("Response:", res.text)

print("\n---------- 3. COMPLETE JSON ----------")

if res.ok:
    print(json.dumps(data, indent=4))
