from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration
from msa_sdk.order import Order
from msa_sdk.device import Device
import time
import json


dev_var = Variables()
context = Variables.task_call()

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])

timeout = 0
melongid = context['switch'][-3:]

device = Device(device_id=melongid)
# build the Microservice JSON params for the order
micro_service_vars_array = {"object_id": context["new_os"],
                           }
object_id = context["new_os"]
os = {"OS": {object_id: micro_service_vars_array}}

while timeout <= 50:
  device.activate()
  # call the IMPORT MS method
  order = Order(melongid)
  order.command_execute('IMPORT', os)
  order.command_objects_instances("OS")
  os = json.loads(order.content)
  os = str(os)
  Orchestration.update_asynchronous_task_details(*async_update_list, 'OS is '+os+'')
  time.sleep(10)
#  if order.response.ok:
  if order.response.ok and context["new_os"] in str(os):
    ret = MSA_API.process_content('ENDED', f'{context["switch"]} is running {os}', context, True)
    break
  else:
    i = 1
    timer = str(timeout)
    while i < 11:
      testtimer = str(i)
      Orchestration.update_asynchronous_task_details(*async_update_list, 'Next test in '+testtimer+' Seconds. '+timer+' seconds spent out of 1800 max (30 minutes)')
      time.sleep(1)
    ret = MSA_API.process_content('WARNING', f'Cannot verify OS on {context["switch"]}', context, True)
    timeout += 10

print(ret)

# END OF FILE
