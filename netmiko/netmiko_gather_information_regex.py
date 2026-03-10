from netmiko import ConnectHandler
import re

v_device_type = "cisco_ios"
v_host =  "YOUR HOST"
v_ssh_port =  22
v_username = "YOUR USER"
v_password = "YOUR PASS"
v_secret = "YOUR PASS"

device = {
"device_type": v_device_type,
"host": v_host,
"username": v_username,
"password": v_password,
"secret": v_secret,
}

# Connect to device
connection = ConnectHandler(**device)
connection.enable()

# Run command
output = connection.send_command("show version")

# Extract hostname
hostname_match = re.search(r"(\S+) uptime is", output)
hostname = hostname_match.group(1) if hostname_match else "Unknown"

# Extract model
model_match = re.search(r"(?i)cisco\s+(\S+)\s+\(", output)
model = model_match.group(1) if model_match else "Unknown"

# Extract serial number
serial_match = re.search(r"Processor board ID (\S+)", output)
serial = serial_match.group(1) if serial_match else "Unknown"

# Print formatted result
print("Device Information")
print("------------------")
print(f"Hostname: {hostname}")
print(f"Model: Cisco {model}")
print(f"Serial Number: {serial}")

# Disconnect
connection.disconnect()
