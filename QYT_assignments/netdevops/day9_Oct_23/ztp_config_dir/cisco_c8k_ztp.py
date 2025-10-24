#!/usr/bin/python3

# Importing cli module
import cli, json, os, re

print("\n\n *** Sample ZTP Day0 Python Script *** \n\n")

# --------------Obtain device type and sn--------------
version_result = cli.execute('show version')
version_list = version_result.split('\n')

device_type = ""
device_sn = ""


for x in version_list:
    if "processor (revision VXE)" in x:
        device_type = x.split()[1]
    elif "Processor board ID" in x:
        device_sn = x.split()[3]


# --------------Obtain device interfaces info--------------
device_if_list = []
cmd_result = cli.execute('show ip inter brie').split('\n')
if_pattern = re.compile(r'^[A-Z]\w+\d+')
for line in cmd_result:
    find_res = re.findall(if_pattern, line)
    if find_res:
        device_if_list.append(find_res[0])

# --------------Use linux curl post data(device_type, device_if_list and device_sn) to http://10.10.1.200/device_config_json--------------
if device_sn:
    data = json.dumps({
                        "device_type": device_type,
                        "device_if_list": device_if_list,
                        "device_sn": device_sn
                       })
    yin = "'"  # SyntaxError: f-string expression part cannot include a backslash
    result = os.popen(f'curl -X POST -H "Content-Type: application/json" -d {yin}{data}{yin} http://10.10.1.200/device_config_json')
    config_list = json.loads(result.read()).get('config')

    if config_list:
        cli.configurep(config_list)

print("\n\n *** ZTP Day0 Python Script Execution Complete *** \n\n")