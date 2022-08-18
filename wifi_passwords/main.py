import os
import subprocess

files_storage = "/etc/NetworkManager/system-connections"
bash_command = ["ls", files_storage]
result = subprocess.run(bash_command, capture_output=True, text=True)
wifis = result.stdout.split("\n")[:-1]

for wifi in wifis:
    wifi_file_path = os.path.join(files_storage, wifi)
    cmd = ["sudo", "cat", wifi_file_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    out = result.stdout
    idx_pwd = out.find("psk=")
    pwd = out[idx_pwd:].split("\n")[0].split("=")[-1]
    if pwd != "":
        print(f"Wifi {wifi.split('.nmconnection')[0]} | Password: {pwd}")
