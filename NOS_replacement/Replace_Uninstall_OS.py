from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration
from msa_sdk.order import Order
from msa_sdk.device import Device
import time

dev_var = Variables()
dev_var.add('new_os', var_type='String')
context = Variables.task_call(dev_var)

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])

'''Orchestration.update_asynchronous_task_details(*async_update_list, 'Importing '+context['ms_name']+' from:'+context['source_me']+'')'''

mode = "uninstall"
melongid = context['switch'][-3:]
device = Device(device_id=melongid)
device.update_credentials(login="root", password="onl")
device.activate()

# build the Microservice JSON params for the order
micro_service_vars_array = {"object_id": context["new_os"],
                           "mode": mode
                           }

object_id = context["new_os"]

os = {"OS": {object_id: micro_service_vars_array}}

melongid = context['switch'][-3:]

# call the UPDATE MS method
order = Order(melongid)
order.command_execute('UPDATE', os)

if order.response.ok:
  order.command_synchronize(timeout=60)
  ret = MSA_API.process_content('ENDED', f'{context["switch"]} is rebooting', context, True)
  Orchestration.update_asynchronous_task_details(*async_update_list, 'NOS replacement triggered on '+context['switch']+'')
  time.sleep(30)
else:
  ret = MSA_API.process_content('WARNING', f'NOS Replacement on {context["switch"]} failed', context, True)

print(ret)

# END OF FILE
