from netmiko import ConnectHandler
import re

device = {
"device_type": "your_device_type",
"host": "your_host",
"username": "your_username",
"password": "your_password",
"secret": "your_secret",
}

# Connect to device
connection = ConnectHandler(**device)
connection.enable()

show_version = connection.send_command("show version")
show_interfaces = connection.send_command("show ip interface brief")

print(show_version)
print(show_interfaces)

connection.disconnect()

# Now Extract hostname
hostname = "To be Extracted"
# Now Extract model
model = "To be Extracted"
# Now Extract serial number
serial = "To be Extracted"
# Now Print formatted result
print("Device Information")
print("------------------")
print(f"Hostname: {hostname}")
print(f"Model: Cisco {model}")
print(f"Serial Number: {serial}")

# Disconnect
connection.disconnect()
