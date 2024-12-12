import requests
import json

# Define APIC details
apic_url = "https://apic.example.com"
username = "admin"
password = "yourpassword"

# Disable SSL warnings (you can enable SSL verification if needed)
requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

# Login to APIC and get authentication token
def login_to_apic():
    login_url = f"{apic_url}/api/aaaLogin.json"
    login_payload = {
        "aaaUser": {
            "attributes": {
                "name": username,
                "pwd": password
            }
        }
    }
    response = requests.post(login_url, json=login_payload, verify=False)
    if response.status_code == 200:
        token = response.json()['imdata'][0]['aaaLogin']['attributes']['token']
        return token
    else:
        raise Exception("Failed to login to APIC. Check credentials or APIC status.")

# Create a tenant
def create_tenant(token, tenant_name):
    tenant_url = f"{apic_url}/api/node/mo/uni/tn-{tenant_name}.json"
    tenant_payload = {
        "fvTenant": {
            "attributes": {
                "name": tenant_name
            }
        }
    }
    headers = {"Cookie": f"APIC-cookie={token}"}
    response = requests.post(tenant_url, json=tenant_payload, headers=headers, verify=False)
    if response.status_code == 200:
        print(f"Tenant {tenant_name} created successfully.")
    else:
        print(f"Failed to create tenant {tenant_name}.")
        print(response.text)

# Create an Application Profile
def create_app_profile(token, tenant_name, app_profile_name):
    app_profile_url = f"{apic_url}/api/node/mo/uni/tn-{tenant_name}/ap-{app_profile_name}.json"
    app_profile_payload = {
        "fvAp": {
            "attributes": {
                "name": app_profile_name
            }
        }
    }
    headers = {"Cookie": f"APIC-cookie={token}"}
    response = requests.post(app_profile_url, json=app_profile_payload, headers=headers, verify=False)
    if response.status_code == 200:
        print(f"Application Profile {app_profile_name} created successfully.")
    else:
        print(f"Failed to create application profile {app_profile_name}.")
        print(response.text)

# Create an Endpoint Group (EPG)
def create_epg(token, tenant_name, app_profile_name, epg_name):
    epg_url = f"{apic_url}/api/node/mo/uni/tn-{tenant_name}/ap-{app_profile_name}/epg-{epg_name}.json"
    epg_payload = {
        "fvAEPg": {
            "attributes": {
                "name": epg_name
            }
        }
    }
    headers = {"Cookie": f"APIC-cookie={token}"}
    response = requests.post(epg_url, json=epg_payload, headers=headers, verify=False)
    if response.status_code == 200:
        print(f"EPG {epg_name} created successfully.")
    else:
        print(f"Failed to create EPG {epg_name}.")
        print(response.text)

# Associate the EPG with a Bridge Domain (BD)
def associate_epg_to_bd(token, tenant_name, app_profile_name, epg_name, bd_name):
    epg_bd_url = f"{apic_url}/api/node/mo/uni/tn-{tenant_name}/ap-{app_profile_name}/epg-{epg_name}/json"
    epg_bd_payload = {
        "fvRsBd": {
            "attributes": {
                "tnFvBDName": bd_name
            }
        }
    }
    headers = {"Cookie": f"APIC-cookie={token}"}
    response = requests.post(epg_bd_url, json=epg_bd_payload, headers=headers, verify=False)
    if response.status_code == 200:
        print(f"EPG {epg_name} associated with Bridge Domain {bd_name}.")
    else:
        print(f"Failed to associate EPG {epg_name} with BD {bd_name}.")
        print(response.text)

# Main function to execute all tasks
def main():
    tenant_name = "MyTenant"
    app_profile_name = "MyAppProfile"
    epg_name = "VM_EPG"
    bd_name = "BD_VLAN100"
    
    try:
        # Login to APIC
        token = login_to_apic()

        # Create tenant, app profile, EPG, and associate with BD
        create_tenant(token, tenant_name)
        create_app_profile(token, tenant_name, app_profile_name)
        create_epg(token, tenant_name, app_profile_name, epg_name)
        associate_epg_to_bd(token, tenant_name, app_profile_name, epg_name, bd_name)

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()
