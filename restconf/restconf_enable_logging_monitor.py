IP_ADDRESS="192.168.56.103"  ### "10.10.20.48"
RESTCONF_USERNAME="cisco"  ### "developer"
RESTCONF_PASSWORD="cisco123!" ### "C1sco12345"
sshCli = ConnectHandler(
    device_type="cisco_ios",
    host=IP_ADDRESS,
    port="22",
    username=RESTCONF_USERNAME,
    password=RESTCONF_PASSWORD
    )
config_commands = (
    'logging monitor' ,
    )
output=sshCli.send_config_set(config_commands)
output=sshCli.send_command("show logging")
print(output)
