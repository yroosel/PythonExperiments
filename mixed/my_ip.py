#pip install requests
### MY IP
import requests

try:
    # Send a GET request to the API
    response = requests.get('https://api.myip.com/')
    response.raise_for_status()  # Raise an error for bad status codes

    # Parse the JSON response
    
    data = response.json()
    print (data)

    # Extract information
    ip_address = data.get('ip', 'N/A')
    country = data.get('country', 'N/A')
    country_code = data.get('cc', 'N/A')

    # Display the information
    print(f"Public IP Address: {ip_address}")
    print(f"Country: {country}")
    print(f"Country Code: {country_code}")

except requests.exceptions.RequestException as e:
    print(f"An error occurred: {e}")
  
