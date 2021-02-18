import json
import time
import ipaddress
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order

# List all the parameters required by the task
dev_var = Variables()
dev_var.add('lines', var_type='Integer')
context = Variables.task_call(dev_var)

# read the ID of the selected managed entity
device_id = context['device']
# extract the database ID
devicelongid = device_id[-3:]

lines =  int(context['lines'])

net4 = ipaddress.ip_network('172.42.0.0/16')
i = 0
portstart = 10000
for ip in net4.hosts(): 
  #print(i)
  #time.sleep (1)
  if i == lines:
    break
  else:
    port = i + portstart
    i += 1
    context['id'] = int(i)
    context['src_ip'] = str(ip)
    context['dst_port'] = str(port)
    micro_service_vars_array = {"object_id": context['id'],
                            "src_ip": context['src_ip'],
                            "dst_port": context['dst_port']
                            }
    object_id = i
    simple_firewall = {"simple_firewall": {object_id: micro_service_vars_array}}
    # call the CREATE for simple_firewall MS for each device
    order = Order(devicelongid)
    #order.command_execute('CREATE', simple_firewall)
    order.command_call('CREATE', 1, simple_firewall)
    # convert dict object into json
    #content = json.loads(order.content)
    #ret = MSA_API.process_content('RUNNING',
                                  #f'STATUS: {content["status"]}, \
                                   # MESSAGE: {content["message"]}',
                                  #context, True)
    #print(ret)
    #print("Hello, World!")

ret = MSA_API.process_content('ENDED',
                              f'Number of rules: {ip}',
                              context, True)
print(ret)