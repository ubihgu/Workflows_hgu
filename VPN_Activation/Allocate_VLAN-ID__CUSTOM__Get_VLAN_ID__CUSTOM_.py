from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
import json

dev_var = Variables()
context = Variables.task_call()

file_system_device_id = "125"

order = Order(file_system_device_id)
order.command_execute('IMPORT', {"VLAN_Database":"0"})
vlan_database = order.command_objects_instances("VLAN_Database")

vlan = 1001
for i in range(512, 1002):
  if str(vlan) in vlan_database:
    vlan = vlan - 1
    continue
  else:
    break

context['vlan_id'] = str(vlan) 


ret = MSA_API.process_content('ENDED', f'Available VLAN-ID: {vlan} (CUSTOM)', context, True)
print(ret)