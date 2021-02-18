from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk import util
import json

dev_var = Variables()
dev_var.add('vlan_id', var_type='String')
context = Variables.task_call(dev_var)

file_system_device_id = "125"
process_id = context['SERVICEINSTANCEID']

order = Order(file_system_device_id)
order.command_execute('IMPORT', {"VLAN_Database":"0"})
order.command_objects_instances("VLAN_Database")

vlans = json.loads(order.content)
util.log_to_process_file(process_id, vlans)

for vlan in vlans:
  order.command_objects_instances_by_id("VLAN_Database", vlan)
  vpn_name = json.loads(order.content)['VLAN_Database'][vlan]['vpn_name']
  vlan_id = json.loads(order.content)['VLAN_Database'][vlan]['object_id']
  util.log_to_process_file(process_id, vpn_name)
  if vlan_id == context['vlan_id']:
    context['vpn_name'] = vpn_name
    context['status'] = json.loads(order.content)['VLAN_Database'][vlan]['status']
    ret = MSA_API.process_content('ENDED', f'VPN {context["vpn_name"]} as VLAN ID {context["vlan_id"]} with status: {context["status"]}', context, True)
    print(ret)
    
ret = MSA_API.process_content('FAILED', f'No VLAN ID for VPN {context["vpn_name"]}', context, True)
print(ret)