import subprocess
import re

# Get list of Wi-Fi profiles
command_output = subprocess.run(["sudo", "wpa_cli", "scan_results"], capture_output=True, text=True)
profile_names = re.findall("(?<=\n)[^ \n]+", command_output.stdout)

# Iterate through profiles and extract information
wifi_list = []
for name in profile_names:
    wifi_profile = {"ssid": name}
    profile_info = subprocess.run(["sudo", "wpa_passphrase", name], capture_output=True, text=True, input="password\n")
    password = re.search("(?<=\n\tssid=\")[^\"]+", profile_info.stdout)
    if password is not None:
        wifi_profile["password"] = password.group(0)
    else:
        wifi_profile["password"] = None
    wifi_list.append(wifi_profile)

# Print list of Wi-Fi profiles and passwords
for wifi_profile in wifi_list:
    print(f"SSID: {wifi_profile['ssid']}, Password: {wifi_profile['password']}")
