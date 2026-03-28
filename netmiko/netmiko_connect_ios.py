from netmiko import ConnectHandler
device = {
"device_type": "cisco_ios",
"host": "your_host",
"username": "your_username",
"password": "your_pass",
"secret": "your_sec",
}

device = {
"device_type": "cisco_ios",
"host": "Your Host",
"username": "Your User",
"password": "Your Pass",
"secret": "Your Pass",
}



connection = ConnectHandler(**device)
connection.enable()

output = connection.send_command("show ssh")
print(output)

connection.disconnect()
