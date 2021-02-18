from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

dev_var = Variables()
context = Variables.task_call()

file_system_device_id = "125"

# build the Microservice JSON params for the order
micro_service_vars_array = {"object_id": context["vlan_id"],
                           "vpn_name": context['vpn_name'],
                           "status": "Reserved"
                           }
object_id = context["vlan_id"]

vlan_database = {"VLAN_Database": {object_id: micro_service_vars_array}}

# call the CREATE for simple_firewall MS for each device
order = Order(file_system_device_id)
order.command_execute('CREATE', vlan_database)

if order.response.ok:
  ret = MSA_API.process_content('ENDED', f'VLAN Database updated: {context["vlan_id"]} (CUSTOM)', context, True)
else:
  ret = MSA_API.process_content('FAILED', f'VLAN Database update for: {context["vlan_id"]} failed (CUSTOM)', context, True)

print(ret)