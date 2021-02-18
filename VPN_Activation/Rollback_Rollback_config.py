from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk import util
from msa_sdk.orchestration import Orchestration

dev_var = Variables()
dev_var.add('vpn_name', var_type='String')
dev_var.add('ce_list.0.id', var_type='Device')
dev_var.add('er_list.0.id', var_type='Device')
dev_var.add('vlan_id', var_type='Integer')
dev_var.add('vpn_id', var_type='String')
dev_var.add('warning', var_type='Integer')
context = Variables.task_call(dev_var)

context['warning'] = 0
process_id = context['SERVICEINSTANCEID']
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])

ce_list = context['ce_list']
er_list = context['er_list']

error_devices = list()
file_system_device_id = "125"

# build the Microservice JSON params for the order
micro_service_vars_array = {"object_id": context["vlan_id"],
                           "vpn_name": context['vpn_name'],
                           "status": "Allocated"
                           }
object_id = context["vlan_id"]

vlan_database = {"VLAN_Database": {object_id: micro_service_vars_array}}

# call the DELETE method of vlan_database MS to delete the VLANID from the used ones
order = Order(file_system_device_id)
order.command_execute('DELETE', vlan_database)  

vpn_import = {"vpn_conf":"0"}

for i in range(len(ce_list)):
  # extract the database ID for ce ID
  devicelongid=ce_list[i]['id'][-3:]
  util.log_to_process_file(process_id, devicelongid)
  Orchestration.update_asynchronous_task_details(*async_update_list, 'Processing '+ce_list[i]["id"]+'')
  object_id = "ce_"+context['vpn_id']+"_vpn_conf"
  # build the Microservice JSON params for the DELETE
  micro_service_vars_array = {"object_id": object_id,
                              "router": ce_list[i]['id'],
                              "vlan_id": context['vlan_id'],
                              "vpn_id": context['vpn_id'],
                              "sla": context['sla'],
                              "bandwidth": context['bandwidth'],
                            }
  vpn = {"vpn_conf": {object_id: micro_service_vars_array}}
  # call the DELETE method of vpn_conf MS for each ME
  order = Order(devicelongid)
  order.command_execute('DELETE', vpn)
  #order.command_execute('IMPORT', {"vpn_conf":"0"})
  order.command_synchronize(timeout=60)
  if order.response.ok:
      util.log_to_process_file(process_id, vpn)
  else:
    error_devices.append({devicelongid})
    #ret = MSA_API.process_content('FAILED', f'update for: {me_id} failed', context, True)
    #print (ret)
  order.command_execute('IMPORT', vpn_import)
  
  # extract the database ID for er ID
  devicelongid=er_list[i]['id'][-3:]
  util.log_to_process_file(process_id, devicelongid)
  Orchestration.update_asynchronous_task_details(*async_update_list, 'Processing '+er_list[i]["id"]+'')
  object_id = "er_"+context['vpn_id']+"_vpn_conf"
  # build the Microservice JSON params for the DELETE
  micro_service_vars_array = {"object_id": object_id,
                              "router": er_list[i]['id'],
                              "vlan_id": context['vlan_id'],
                              "vpn_id": context['vpn_id'],
                              "sla": context['sla'],
                              "bandwidth": context['bandwidth'],
                            }
  vpn = {"vpn_conf": {object_id: micro_service_vars_array}}
  # call the DELETE method of vpn_conf MS for each ME
  order = Order(devicelongid)
  order.command_execute('DELETE', vpn)
  order.command_synchronize(timeout=60)

  if order.response.ok:
      util.log_to_process_file(process_id, vpn)
  else:
    error_devices.append({devicelongid})
    #ret = MSA_API.process_content('FAILED', f'update for: {me_id} failed', context, True)
    #print (ret)
  order.command_execute('IMPORT', vpn_import)

if len(error_devices) == 0:
  ret = MSA_API.process_content('ENDED', f'{ce_list} and {er_list} Rollback completed', context, True)
  print(ret)
else:
  context['warning'] = 1
  ret = MSA_API.process_content('WARNING', f'Rollback done except {error_devices}', context, True)
  print(ret)
