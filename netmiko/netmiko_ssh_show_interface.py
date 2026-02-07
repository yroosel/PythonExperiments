from netmiko import ConnectHandler

print("Connecting via SSH => show ip interface brief")

device = {
    "device_type": "cisco_ios",
    "host": "192.168.56.101",
    "port": 22,
    "username": "cisco",
    "password": "cisco123!"
}

ssh = ConnectHandler(**device)
output = ssh.send_command("show ip interface brief")
print(output)

ssh.disconnect()
