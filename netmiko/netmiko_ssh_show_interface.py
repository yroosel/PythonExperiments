from netmiko import ConnectHandler

print("Connecting via SSH => show ip interface brief")

device = {
    "device_type": "cisco_ios",
    "host": "192.168.56.xxx",
    "port": 22,
    "username": "Get username",
    "password": "Get password"
}

ssh = ConnectHandler(**device)
output = ssh.send_command("show ip interface brief")
print(output)

ssh.disconnect()
