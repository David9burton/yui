import subprocess
import re

# Get list of Wi-Fi profiles
command_output = subprocess.run(["netsh", "wlan", "show", "profiles"], capture_output=True, text=True)
profile_names = re.findall("All User Profile\s+:\s+(.*)", command_output.stdout)

# Iterate through profiles and extract information
wifi_list = []
for name in profile_names:
    wifi_profile = {}
    profile_info = subprocess.run(["netsh", "wlan", "show", "profile", name], capture_output=True, text=True)
    if re.search("Security key           : Absent", profile_info.stdout):
        continue
    else:
        wifi_profile["ssid"] = name
        profile_info_pass = subprocess.run(["netsh", "wlan", "show", "profile", name, "keyMaterial"], capture_output=True, text=True)
        password = re.search("Key Content\s+:\s+(.*)", profile_info_pass.stdout)
        if password is None:
            wifi_profile["password"] = None
        else:
            wifi_profile["password"] = password[1]
        wifi_list.append(wifi_profile)

# Print list of Wi-Fi profiles and passwords
for wifi_profile in wifi_list:
    print(f"SSID: {wifi_profile['ssid']}, Password: {wifi_profile['password']}")
