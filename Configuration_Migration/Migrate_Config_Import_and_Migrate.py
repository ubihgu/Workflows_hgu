from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.orchestration import Orchestration
from msa_sdk import util
import json

dev_var = Variables()
dev_var.add('source_me', var_type='Device')
dev_var.add('destination_me', var_type='Device')
dev_var.add('ms_name', var_type='String')
context = Variables.task_call(dev_var)

process_id = context['SERVICEINSTANCEID']
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])
source_me_id = context['source_me'][3:]
destination_me_id = context['destination_me'][3:]
updated_routes = list()

Orchestration.update_asynchronous_task_details(*async_update_list, 'Importing '+context['ms_name']+' from:'+context['source_me']+'')

try:
  order = Order(source_me_id)
  order.command_execute('IMPORT', {context['ms_name']:"0"})
  order.command_objects_instances(context['ms_name'])
  ms_instances = json.loads(order.content)

except Exception as e:
  ret = MSA_API.process_content('FAILED', f'IMPORT ERROR: {str(e)}', context, True)
  print(ret)

if len(ms_instances) == 0:
  ret = MSA_API.process_content('ENDED', f'IMPORT empty. Nothing to migrate.', context, True)
  print(ret)
  
for ms_instance in ms_instances:
  order.command_objects_instances_by_id(context['ms_name'], ms_instance)
  subnet = json.loads(order.content)[context['ms_name']][ms_instance]['subnet']
  mask = json.loads(order.content)[context['ms_name']][ms_instance]['mask']
  gateway = json.loads(order.content)[context['ms_name']][ms_instance]['gateway']
  Orchestration.update_asynchronous_task_details(*async_update_list, 'Processing Subnet: '+subnet+' mask:'+mask+' gateway:'+gateway+'')
  micro_service_vars_array = {"object_id": subnet,
                           "mask": mask,
                           "gateway": gateway
                           }
  object_id = "null"
  route = {"Routing": {object_id: micro_service_vars_array}}
  try:
    ms_order = Order(destination_me_id)
    ms_order.command_execute('CREATE', route)
    updated_routes.append({subnet})
  except Exception as e:
    ret = MSA_API.process_content('FAILED', f'CREATE ERROR: {str(e)}', context, True)
    print(ret)

ms_order.command_synchronize(timeout=60)

ret = MSA_API.process_content('ENDED', '{} Migrated'.format(updated_routes), context, True)
print(ret)