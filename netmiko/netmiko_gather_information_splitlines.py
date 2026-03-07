from netmiko import ConnectHandler

v_device_type = "cisco_ios"
v_host = "YOUR HOST"
v_ssh_port = 22
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

# Convert output to list of lines (similar to readlines())
lines = output.splitlines()

hostname = "Unknown"
model = "Unknown"
serial = "Unknown"

for line in lines:

    if "uptime is" in line:
        hostname = line.split()[0]

    if "Cisco" in line and "(" in line:
        parts = line.split()
        model = parts[1]

    if "Processor board ID" in line:
        serial = line.split()[-1]

# Print formatted result
print("Device Information")
print("------------------")
print(f"Hostname: {hostname}")
print(f"Model: Cisco {model}")
print(f"Serial Number: {serial}")

# Disconnect
connection.disconnect()
