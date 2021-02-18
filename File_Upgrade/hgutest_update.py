from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk import util
import json

dev_var = Variables()
context = Variables.task_call(dev_var)

for device in context['matched_devices']:
  i = 0

ret = MSA_API.process_content('ENDED', 'Apache will be updated on {} starting with {}.'.format(context['matched_devices'], device), context, True)
print(ret)
