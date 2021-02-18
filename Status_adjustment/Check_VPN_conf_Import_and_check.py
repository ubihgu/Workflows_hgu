from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.order import Order
from msa_sdk import util
import json
import requests
from datetime import datetime
from msa_sdk.orchestration import Orchestration
from msa_sdk.device import Device
 
dev_var = Variables()
dev_var.add('device', var_type='Device')
context = Variables.task_call(dev_var)

process_id = context['SERVICEINSTANCEID']
Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])

conf_ok = list()
conf_error = list()

devicelongid = context['device'][-3:]
new_device = Device(device_id=devicelongid)
status = new_device.status()
util.log_to_process_file(process_id, status)


order = Order(devicelongid)
order.command_synchronize(timeout=60)
order.command_execute('IMPORT', {"vpn_conf":"0"})
order.command_objects_instances("vpn_conf")
vpns = json.loads(order.content)

for vpn in vpns:
  order.command_objects_instances_by_id("vpn_conf", vpn)
  sla = json.loads(order.content)['vpn_conf'][vpn]['sla']
  bandwidth = json.loads(order.content)['vpn_conf'][vpn]['bandwidth']
  Orchestration.update_asynchronous_task_details(*async_update_list, 'Processing '+vpn+' sla:'+sla+' bandwidth:'+bandwidth+'')
  util.log_to_process_file(process_id, vpn)
  util.log_to_process_file(process_id, sla)
  util.log_to_process_file(process_id, bandwidth)
  if sla == "middle" and int(bandwidth) > 1000:
    conf_error.append({vpn})
  else:
    conf_ok.append({vpn})

if len(conf_error) == 0:
    ret = MSA_API.process_content('ENDED', '{} VPN parameters are correct (bandwidth<1000 if sla = middle)'.format(context['device']), context, True)
    print(ret)
else:
  dateTimeObj = datetime.now()
  format = "%Y-%m-%dT%H:%M:%S+0000"
  time1 = dateTimeObj.strftime(format)
  format = "%Y-%m-%d"
  date = dateTimeObj.strftime(format)
  url = "http://msa_es:9200/ubilogs-"+date+"/_doc"
  error_list = str(conf_error)
  context['error_list'] = error_list
  payload = {"rawlog": ""+context['device']+" VPN config parameter error for "+error_list+" bandwidth too high for sla", "device_id": ""+context['device']+"", "date": ""+time1+"", "customer_ref": "NextGen IP NW", "severity": "0", "type": "ALARM", "subtype": "VPN"}
  headers = {'content-type': 'application/json'}
  r = requests.post(url, json=payload, headers=headers)
  ret = MSA_API.process_content('FAILED', '{} VPN parameters error for {} '.format(context['device'], conf_error), context, True)
  print(ret)