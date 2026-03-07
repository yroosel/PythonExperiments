# DEFINE VARIABLES
v_device_type = "cisco_ios"
v_host =  "your_host"  
v_ssh_port =  22
v_username = "your_username"
v_password = "your password"
v_secret = "your secret"

from netmiko import ConnectHandler

device = {
"device_type": v_device_type,
"host": v_host,
"username": v_username,
"password": v_password,
"secret": v_secret,
}

connection = ConnectHandler(**device)
connection.enable()

output = connection.send_command("show ssh")
print(output)

connection.disconnect()
