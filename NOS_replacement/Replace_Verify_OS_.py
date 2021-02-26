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

Orchestration.update_asynchronous_task_details(*async_update_list, 'Updating credentials')
device.update_credentials(login="admin", password="YourPaSsWoRd")
time.sleep(1)

while timeout <= 1800:
  device.activate()
  # call the IMPORT MS method
  order = Order(melongid)
  order.command_execute('IMPORT', {"OS":"0"})
  order.command_objects_instances("OS")
  osystem = json.loads(order.content)
  osystem = str(osystem)
  Orchestration.update_asynchronous_task_details(*async_update_list, 'OS is '+osystem+'')
  time.sleep(5)
#  if order.response.ok:
  if order.response.ok and context["new_os"] in osystem:
    ret = MSA_API.process_content('ENDED', f'{context["switch"]} is running {osystem}', context, True)
    order.command_synchronize(timeout=60)
    break
  else:
    i = 1
    timer = str(timeout)
    while i < 11:
      testtimer = str(10 - i)
      Orchestration.update_asynchronous_task_details(*async_update_list, 'Next test in '+testtimer+' Seconds. '+timer+' seconds spent out of 1800 max (30 minutes)')
      time.sleep(1)
      i += 1
    ret = MSA_API.process_content('WARNING', f'Cannot verify OS on {context["switch"]}', context, True)
    timeout += 10

print(ret)

# END OF FILE
