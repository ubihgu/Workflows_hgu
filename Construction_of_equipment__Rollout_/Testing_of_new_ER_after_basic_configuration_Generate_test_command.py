import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device

dev_var = Variables()
dev_var.add('construction_name', var_type='String')
context = Variables.task_call(dev_var)

device_id = context['additional_device_name']
ip = context['adjacent_cr_ip']

new_device = Device(device_id)
new_device.read()
ping = new_device.ping(ip)
content = json.loads (ping)
#ret = MSA_API.process_content('ENDED', f'Pinging IP: {new_device.management_address} successfully', context, True)
if content["status"] == "OK":
  ret = MSA_API.process_content('ENDED', f'Pinging IP: {ip} successfully. {content["status"]} STAT', context, True)
else:
  ret = MSA_API.process_content('FAILED', f'Pinging IP: {ip} failed. {content["status"]} STAT', context, True)
print(ret)