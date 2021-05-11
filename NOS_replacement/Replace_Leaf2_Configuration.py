from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

dev_var = Variables()
dev_var.add('leaf2_if', var_type='String')
context = Variables.task_call(dev_var)

# build the Microservice JSON params for the order
micro_service_vars_array = {"object_id": context["leaf2_if"],
                           "state": "ADMDN"
                           }

object_id = context["leaf2_if"]

cumulus_port = {"Port__Cumulus_": {object_id: micro_service_vars_array}}

melongid = context['leaf2'][-3:]

# call the UPDATE MS method
order = Order(melongid)
order.command_execute('UPDATE', cumulus_port)

if order.response.ok:
  order.command_synchronize(timeout=60)
  ret = MSA_API.process_content('ENDED', f'Port update: {context["leaf2_if"]} on Leaf2 successful', context, True)
else:
  ret = MSA_API.process_content('FAILED', f'Port update: {context["leaf2_if"]} on Leaf2 failed', context, True)

print(ret)