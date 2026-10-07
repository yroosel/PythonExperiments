# Reserve a CML Sandbox prior to executing this script
from netmiko import ConnectHandler

routers = [
    {
        "name": "R1",
        "device_type": "cisco_ios_telnet",
        "host": "10.10.20.171",
        "username": "cisco",
        "password": "cisco",
    },
    {
        "name": "R2",
        "device_type": "cisco_ios_telnet",
        "host": "10.10.20.172",
        "username": "cisco",
        "password": "cisco",
    }
]

for router in routers:

    print(f"\nConnecting to {router['name']} ({router['host']})")
    print("=" * 60)

    connection = ConnectHandler(
        device_type=router["device_type"],
        host=router["host"],
        username=router["username"],
        password=router["password"]
    )

    output = connection.send_command("show version")

    print(output)

    connection.disconnect()
