import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.device import Device
from datetime import datetime
import requests

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
  ret = MSA_API.process_content('ENDED', f'Pinging IP: {ip} successfully. {content["status"]}', context, True)
else:
  dateTimeObj = datetime.now()
  format = "%Y-%m-%dT%H:%M:%S+0000"
  time1 = dateTimeObj.strftime(format)
  format = "%Y-%m-%d"
  date = dateTimeObj.strftime(format)
  url = "http://172.20.0.4:9200/ubilogs-"+date+"/_doc"
  name = context['construction_name']
  device_id = context['additional_device_name']
  payload = {"rawlog": ""+name+" Base config input result: FAIL", "device_id": ""+device_id+"", "date": ""+time1+"", "customer_ref": "TyrellCorp", "severity": "3", "type": "NOTIFICATION", "subtype": "WF"}
  headers = {'content-type': 'application/json'}
  r = requests.post(url, json=payload, headers=headers)
  ret = MSA_API.process_content('FAILED', f'Pinging IP: {ip} failed. {content["status"]}', context, True)
print(ret)