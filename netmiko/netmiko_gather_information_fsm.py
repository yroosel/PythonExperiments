# FSM
# pip3 install netmiko ntc-templates
# export NET_TEXTFSM=$(python3 -c "import ntc_templates; print(ntc_templates.__path__[0] + '/templates')")

from netmiko import ConnectHandler
import re

v_device_type = "cisco_ios"
v_host =  "Your host" 
v_ssh_port =  22
v_username = "Your user"
v_password = "Your PW"
v_secret = "Your PW"

from netmiko import ConnectHandler

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
output_fsm = connection.send_command("show version", use_textfsm=True)
# print("Output FSM: " , output_fsm)

# Extract hostname
hostname = output_fsm[0]['hostname']

# Extract model
model =  output_fsm[0]['hardware']

# Extract serial number
serial =  output_fsm[0]['serial']

# Print formatted result
print("Device Information")
print("------------------")
print(f"Hostname: {hostname}")
print(f"Model: Cisco {model}")
print(f"Serial Number: {serial}")

# Disconnect
connection.disconnect()
