import json
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('id', var_type='Integer')
dev_var.add('dst_port', var_type='Integer')
dev_var.add('prev_device_ip', var_type='String')
dev_var.add('prev_cr_ip', var_type='String')
dev_var.add('prev_prefix', var_type='Integer')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['additional_device_name']
# extract the database ID
#devicelongid = device_id[-3:]
devicelongid = context['tmp_prefix'] 

# build the Microservice JSON params for the order 
micro_service_vars_array = {"object_id": device_id,
                            "device_ip": context['prev_device_ip'],
                            "prefix": context['prev_prefix'],
                            "neighbor": context['prev_cr_ip']
                            }

object_id = device_id

basic = {"basic_conf": {object_id: micro_service_vars_array}}

order = Order(devicelongid)
order.command_execute('DELETE', basic)

# build the Microservice JSON params for firewall
micro_service_vars_array = {"object_id": context['id'],
                            "src_ip": context['adjacent_cr_ip'],
                            "dst_port": context['dst_port']
                            }

object_id = context['id']

simple_firewall = {"simple_firewall": {object_id: micro_service_vars_array}}

# call the CREATE for simple_firewall MS for each device
order = Order(devicelongid)
order.command_execute('DELETE', simple_firewall)



# convert dict object into json
content = json.loads(order.content)

# check if the response is OK
if order.response.ok:

    if 'rules' in context.keys():
        num = len(context['rules'])
    else:
        context['rules'] = {}
        num = 0

    context['rules'][num] = {}
    context['rules'][num]['delete'] = False
    context['rules'][num]['id'] = context['id']
    context['rules'][num]['src_ip'] = context['adjacent_cr_ip']
    context['rules'][num]['dst_port'] = context['dst_port']

    ret = MSA_API.process_content('ENDED',
                                  f'STATUS: {content["status"]}, \
                                    MESSAGE: {content["message"]}',
                                  context, True)
else:
    ret = MSA_API.process_content('FAILED',
                                  f'Policy update failed \
                                  - {order.content}',
                                  context, True)


print(ret)
