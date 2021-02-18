from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk import util
import json

dev_var = Variables()
dev_var.add('order', var_type='String')
context = Variables.task_call(dev_var)

file_system_device_id = "125"
process_id = context['SERVICEINSTANCEID']

order = Order(file_system_device_id)
order.command_execute('IMPORT', {"VLAN_Database":"0"})
order.command_objects_instances("VLAN_Database")

vlans = json.loads(order.content)
if context['order'] == "ASC":
  vlans.sort(key=int)
else:
  vlans.sort(key=int, reverse=True)
util.log_to_process_file(process_id, vlans)

#Create context variable to show in GUI
context['vlan'] = list()

for vlan in vlans:
  order.command_objects_instances_by_id("VLAN_Database", vlan)
  vpn_name = json.loads(order.content)['VLAN_Database'][vlan]['vpn_name']
  status = json.loads(order.content)['VLAN_Database'][vlan]['status']
  util.log_to_process_file(process_id, vpn_name)
  context['vlan'].append({'vlan_id': vlan,
                             'vpn_name': vpn_name,
                             'status': status
                            })

  
ret = MSA_API.process_content('ENDED', f'VLAN list sorted in {context["order"]} order', context, True)
print(ret)
    