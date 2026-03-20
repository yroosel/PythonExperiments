from netmiko import ConnectHandler

# Connection parameters
v_device_type = "cisco_ios"
v_host =  "YOUR HOST"  
v_ssh_port =  22
v_username = "YOUR USER"
v_password = "YOUR PASS"
v_secret = "YOUR SECRET"

device = {
    "device_type": v_device_type,
    "host": v_host,
    "username": v_username,
    "password": v_password,
    "secret": v_secret,
}

device = {
"device_type": "cisco_ios",
"host": "192.168.0.200",
"username": "cisco",
"password": "cisco123!",
"secret": "cisco123!",
}

# Connect to the device
connection = ConnectHandler(**device)
connection.enable()

# Configuration commands
config_commands = [
    "banner motd #Unauthorized access is prohibited by Netmiko#"
]

# Send configuration commands
output = connection.send_config_set(config_commands)
print(output)

# Save the configuration
# connection.save_config()

# Verify banner
output = connection.send_command("show running-config | include banner")

print("Verification result:")
print(output)

# Disconnect
connection.disconnect()
