from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk import util

dev_var = Variables()
dev_var.add('name', var_type='String')
dev_var.add('device.0.target', var_type='Device')
dev_var.add('version', var_type='String')
dev_var.add('additional_device', var_type='String')
dev_var.add('additional_version', var_type='String')
context = Variables.task_call(dev_var)

process_id = context['SERVICEINSTANCEID']

devices = context['device']
for i in range(len(devices)):
  # extract the database ID for ce ID
  devicelongid=devices[i]['target'][-3:]
  order = Order(devicelongid)
  order.command_execute('IMPORT', {"Apache_Version":"0"})
  version = order.command_objects_instances("Apache_Version")
  ver = order.command_objects_instances_by_id("Apache_Version", version)
ret = MSA_API.process_content('ENDED', f'Version is {ver}', context, True)
print(ret)