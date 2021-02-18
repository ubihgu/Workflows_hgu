from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk import util
import json

dev_var = Variables()
dev_var.add('name', var_type='String')
dev_var.add('device.0.target', var_type='Device')
dev_var.add('version', var_type='String')
dev_var.add('additional_device', var_type='String')
dev_var.add('additional_version', var_type='String')
context = Variables.task_call(dev_var)

process_id = context['SERVICEINSTANCEID']
matched_devices = dict()
error_devices = dict()
'''
devices = context['device']
for i in range(len(devices)):
  try:
    # extract the database ID for ce ID
    devicelongid = devices[i]['target'][-3:]
    order = Order(devicelongid)
    order.command_execute('IMPORT', {"Apache_Version":"0"})
    order.command_objects_instances("Apache_Version")
    version = json.loads(order.content)[0]
    # order.command_objects_instances_by_id("Apache_Version", "8_5_59")
    order.command_objects_instances_by_id("Apache_Version", version)
    ver = json.loads(order.content)['Apache_Version'][version]['object_id']
    if ver != context['version']:
      micro_service_vars_array = {"object_id": context['version']}
      version = context['version'].replace(".", "_")
      #{"Apache_Files":{"9_0_39":{"object_id":"9.0.39","param":{"_order":"2000"}}}}
      apache = {"Apache_Files": {version: micro_service_vars_array}}
      # call the UPDATE method
      order.command_execute('UPDATE', apache)
      matched_devices[devicelongid] = list()
      matched_devices[devicelongid].append({'id': devicelongid})
  except:
    error_devices[devicelongid] = list()
    error_devices[devicelongid].append({'id': devicelongid})    

try:
  devicelongid = context['additional_device'][-3:]
  order = Order(devicelongid)
  order.command_execute('IMPORT', {"Apache_Version":"0"})
  order.command_objects_instances("Apache_Version")
  version = json.loads(order.content)[0]
  # order.command_objects_instances_by_id("Apache_Version", "8_5_59")
  order.command_objects_instances_by_id("Apache_Version", version)
  ver = json.loads(order.content)['Apache_Version'][version]['object_id']
  if ver != context['additional_version']:
    micro_service_vars_array = {"object_id": context['additional_version']}
    version = context['additional_version'].replace(".", "_")
    apache = {"Apache_Files": {version: micro_service_vars_array}}
    order.command_execute('UPDATE', apache)
    matched_devices[devicelongid] = list()
    matched_devices[devicelongid].append({'id': devicelongid})
except:
  error_devices[devicelongid] = list()
  error_devices[devicelongid].append({'id': devicelongid}) 

ret = MSA_API.process_content('ENDED', f'Apache updated on {matched_devices}. Errors happened on {error_devices}', context, True)
print(ret)
'''
ret = MSA_API.process_content('WARNING', f'WIP', context, True)
print(ret)