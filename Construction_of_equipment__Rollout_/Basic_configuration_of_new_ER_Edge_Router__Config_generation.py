'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk.lookup import Lookup
from msa_sdk import util

'''
List all the parameters required by the task

You can use var_name convention for your variables
They will display automaticaly as "Var Name"
The allowed types are:
  'String', 'Boolean', 'Integer', 'Password', 'IpAddress',
  'IpMask', 'Ipv6Address', 'Composite', 'OBMFRef', 'Device'

 Add as many variables as needed
'''
dev_var = Variables()
dev_var.add('construction_name', var_type='String')
dev_var.add('additional_device_name', var_type='String')
dev_var.add('additional_device_ip', var_type='String')
dev_var.add('network_prefix', var_type='Integer')
dev_var.add('adjacent_cr_name', var_type='String')
dev_var.add('adjacent_cr_ip', var_type='String')
dev_var.add('tmp_device_ip', var_type='String')
dev_var.add('tmp_cr_ip', var_type='String')
dev_var.add('tmp_prefix', var_type='Integer')
dev_var.add('prev_device_ip', var_type='String')
dev_var.add('prev_cr_ip', var_type='String')
dev_var.add('prev_prefix', var_type='Integer')
context = Variables.task_call(dev_var)

process_id = context['SERVICEINSTANCEID']
#Find device ID value second
MsaLookup = Lookup()
MsaLookup.look_list_device_ids()
devices = json.loads(MsaLookup.content)
util.log_to_process_file(process_id, context['additional_device_name'])
util.log_to_process_file(process_id, len(devices))

devicelongid = None
counter = 0

#while devicelongid is None or counter < len(devices):
while counter < len(devices):
  if devices[counter]['name'] == context['additional_device_name']:
    devicelongid = devices[counter]['id']
    break
  util.log_to_process_file(process_id, devices[counter]['name'])
  counter += 1
  util.log_to_process_file(process_id, counter)

if devicelongid == None:
  ret = MSA_API.process_content('FAILED', f'Additional device ID not found for {context["additional_device_name"]}', context, True)
  print(ret)

# read the ID of the selected managed entity
#device_id = context['additional_device_name']
# extract the database ID
#devicelongid = device_id[-3:]

device_id = context['additional_device_name']
device_ip = context['additional_device_ip']
network_prefix = context['network_prefix']
neighbor_ip = context['adjacent_cr_ip']

context['prev_device_ip'] = context['tmp_device_ip']
context['prev_cr_ip'] = context['tmp_cr_ip']
context['prev_prefix'] = context['tmp_prefix']

context['tmp_device_ip'] = device_ip
context['tmp_cr_ip'] = neighbor_ip
context['tmp_prefix'] = network_prefix

# build the Microservice JSON params for the order
micro_service_vars_array = {"object_id": device_id,
                            "device_ip": device_ip,
                            "prefix": network_prefix,
                            "neighbor": neighbor_ip
                            }

object_id = device_id

basic = {"basic_conf": {object_id: micro_service_vars_array}}

order = Order(devicelongid)
order.command_execute('UPDATE', basic)

context['tmp_prefix'] = devicelongid

if order.response.ok:
  ret = MSA_API.process_content('ENDED', f'Generated config for: {context["construction_name"]}', context, True)

else:
  ret = MSA_API.process_content('FAILED', f'Config generation for: {context["construction_name"]} failed', context, True)
print(ret)


