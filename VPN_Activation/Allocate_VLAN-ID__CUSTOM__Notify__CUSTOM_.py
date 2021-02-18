from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from datetime import datetime
import json
import requests

dev_var = Variables()
dev_var.add('vpn_name', var_type='String')
dev_var.add('vlan-id', var_type='Integer')
context = Variables.task_call(dev_var)

dateTimeObj = datetime.now()
format = "%Y-%m-%dT%H:%M:%S+0000"
time1 = dateTimeObj.strftime(format)
format = "%Y-%m-%d"
date = dateTimeObj.strftime(format)

url = "http://msa_es:9200/ubilogs-"+date+"/_doc"

name = context['vpn_name']
vlan_id = context['vlan_id']

device_id = name

payload = {"rawlog": " VLAN "+vlan_id+" reserved for VPN "+name+": OK", "device_id": ""+device_id+"", "date": ""+time1+"", "customer_ref": "TyrellCorp", "severity": "5", "type": "NOTIFICATION", "subtype": "WF"}

headers = {'content-type': 'application/json'}

r = requests.post(url, json=payload, headers=headers)

ret = MSA_API.process_content('ENDED', f'VLAN {context["vlan_id"]} reserved for {context["vpn_name"]} configured', context, True)
print(ret)