from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from datetime import datetime
import json
import requests

dev_var = Variables()
context = Variables.task_call()

dateTimeObj = datetime.now()
format = "%Y-%m-%dT%H:%M:%S+0000"
time1 = dateTimeObj.strftime(format)
format = "%Y-%m-%d"
date = dateTimeObj.strftime(format)

url = "http://msa_es:9200/ubilogs-"+date+"/_doc"

ce_list = context['ce_list']
er_list = context['er_list']
  
for i in range(len(ce_list)):
  payload = {"rawlog": " VPN "+context['vpn_id']+" configured between "+ce_list[i]['id']+" and "+er_list[i]['id']+"", "device_id": ""+ce_list[i]['id']+"", "date": ""+time1+"", "customer_ref": "TyrellCorp", "severity": "5", "type": "NOTIFICATION", "subtype": "VPN WF"}
  headers = {'content-type': 'application/json'}
  r = requests.post(url, json=payload, headers=headers)

if context['warning'] == 1:
  ret = MSA_API.process_content('WARNING', f'VPN {context["vpn_id"]} Rollback completed, Error on some devices', context, True)
  print(ret)
else:
  ret = MSA_API.process_content('ENDED', f'VPN {context["vpn_id"]} Rollback completed', context, True)
  print(ret)