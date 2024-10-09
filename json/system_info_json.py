import json

system_info = {
"System Name" : "MSI"
, "OS Name" : "Microsoft Windows 10 Pro"
, "Version" : "10.0.19042"
, "Processor" : "Inter Core i7-1185G7 11th Gen"
, "BIOS Mode" : "UEFI"
, "RAM" : "32GB"
, "storage_devices" : 
[
    {
        "Volume": "Disk 0 partition 1",
        "Layout": "Simple",
        "Type": "Basic",
        "File System": "",
        "Status": "Healthy",
        "Capacity": "300 MB",
        "Free Space": "300 MB",
        "% Free": "100%"
    },
    {
        "Volume": "Disk 0 partition 4",
        "Layout": "Simple",
        "Type": "Basic",
        "File System": "",
        "Status": "Healthy",
        "Capacity": "900 MB",
        "Free Space": "900 MB",
        "% Free": "100%"
    },
    {
        "Volume": "Disk 0 partition 5",
        "Layout": "Simple",
        "Type": "Basic",
        "File System": "",
        "Status": "Healthy",
        "Capacity": "20,34 MB",
        "Free Space": "20,34 MB",
        "% Free": "100%"
    },
    {
        "Volume": "Samsung_T5",
        "Layout": "Simple",
        "Type": "Basic",
        "File System": "exFAT",
        "Status": "Healthy",
        "Capacity": "465,75",
        "Free Space": "306,57",
        "% Free": "66%"
    },
    {
        "Volume": "USBData",
        "Layout": "Simple",
        "Type": "Basic",
        "File System": "NTFS",
        "Status": "Healthy",
        "Capacity": "445,13 GB",
        "Free Space": "444,97 GB",
        "% Free": "100%"
    },
    {
        "Volume": "USBRecovery",
        "Layout": "Simple",
        "Type": "Basic",
        "File System": "NTFS",
        "Status": "Healthy",
        "Capacity": "30,63 GB",
        "Free Space": "515 MB",
        "% Free": "2%"
    },
    {
        "Volume": "Windows (C:)",
        "Layout": "Simple",
        "Type": "Basic",
        "File System": "NTFS",
        "Status": "Healthy",
        "Capacity": "932,23 GB",
        "Free Space": "821,95 GB",
        "% Free": "88%"
    }
]
}
print(type(system_info))
print(json.dumps(system_info, indent=8))
