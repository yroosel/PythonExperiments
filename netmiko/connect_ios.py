from netmiko import ConnectHandler

device = {
"device_type": "cisco_ios",
"host": "your_host",
"username": "your_username",
"password": "your_pass",
"secret": "your_sec",
}

# passwords only in an initial training environment
device = {
"device_type": "cisco_ios",
"host": "10.101.11.152",
"username": "cisco",
"password": "cisco123!",
"secret": "cisco123!",
}

connection = ConnectHandler(**device)
connection.enable()

output = connection.send_command("show ssh")
print(output)

connection.disconnect()
