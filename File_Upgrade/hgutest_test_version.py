from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk import util
import json

dev_var = Variables()
dev_var.add('name', var_type='String')
dev_var.add('device.0.target', var_type='Device')
dev_var.add('version', var_type='String')
dev_var.add('additional_device', var_type='String')
dev_var.add('additional_version', var_type='String')
context = Variables.task_call(dev_var)

process_id = context['SERVICEINSTANCEID']
context['matched_devices'] = dict()
error_devices = dict()

j = 1
# GET the list of Devices that needs be updated (ie versionc an be imported and not the same as the target version)
devices = context['device']
for i in range(len(devices)):
#  util.log_to_process_file(process_id, devices[i]['target'])
  devicelongid = devices[i]['target'][-3:]
  order = Order(devicelongid)
  order.command_execute('IMPORT', {"Apache_Version":"0"})
  order.command_objects_instances("Apache_Version")
  if json.loads(order.content):
    version = json.loads(order.content)[0]
    order.command_objects_instances_by_id("Apache_Version", version)
    ver = json.loads(order.content)['Apache_Version'][version]['object_id']
#    util.log_to_process_file(process_id, ver)
    if ver == "7.0.106":
      context['matched_devices'][devicelongid] = list()
      context['matched_devices'][devicelongid].append({'id': devicelongid})
      j = j + 1
    else:
      error_devices[devicelongid] = list()
      error_devices[devicelongid].append({'id': devicelongid})
      ret = MSA_API.process_content('FAILED', f'{error_devices} run Tomcat {ver} instead of 7.0.106 ', context, True)
      print(ret)
  else:
    version = "NULL"
    error_devices[devicelongid] = list()
    error_devices[devicelongid].append({'id': devicelongid})
    ret = MSA_API.process_content('FAILED', f'{error_devices} run Tomcat {ver} instead of 7.0.106 ', context, True)
    print(ret)
#  util.log_to_process_file(process_id, version)

if context['additional_device']:
  devicelongid = context['additional_device'][-3:]
  order = Order(devicelongid)
  order.command_execute('IMPORT', {"Apache_Version":"0"})
  order.command_objects_instances("Apache_Version")
  if json.loads(order.content):
    version = json.loads(order.content)[0]
    order.command_objects_instances_by_id("Apache_Version", version)
    ver = json.loads(order.content)['Apache_Version'][version]['object_id']
#    util.log_to_process_file(process_id, ver)
    if ver == "7.0.106":
      context['matched_devices'][devicelongid] = list()
      context['matched_devices'][devicelongid].append({'id': devicelongid})
    else:
      error_devices[devicelongid] = list()
      error_devices[devicelongid].append({'id': devicelongid})
      ret = MSA_API.process_content('FAILED', f'{error_devices} run Tomcat {ver} instead of 7.0.106 ', context, True)
      print(ret)
  else:
    version = "NULL"
    error_devices[devicelongid] = list()
    error_devices[devicelongid].append({'id': devicelongid})
    ret = MSA_API.process_content('FAILED', f'{error_devices} run Tomcat {ver} instead of 7.0.106 ', context, True)
    print(ret)
#  util.log_to_process_file(process_id, version) 

ret = MSA_API.process_content('ENDED', 'Apache will be updated on {}. Errors happened on {}'.format(context['matched_devices'], error_devices), context, True)
print(ret)