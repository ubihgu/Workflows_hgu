from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk import util
import json

dev_var = Variables()
context = Variables.task_call(dev_var)

for device in context['matched_devices']:
  if device == context['additional_device'][-3:]:
    micro_service_vars_array = {"object_id": context['additional_version']}
  else:
    micro_service_vars_array = {"object_id": context['version']}
  apache = {"Apache_Version": {"null": micro_service_vars_array}}
  # call the CREATE method
  order = Order(device)
  order.command_execute('CREATE', apache)

ret = MSA_API.process_content('ENDED', 'Apache updated on {}.'.format(context['matched_devices']), context, True)
print(ret)
