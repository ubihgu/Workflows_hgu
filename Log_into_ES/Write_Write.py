from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from datetime import datetime
import time
import json
import requests

dev_var = Variables()
dev_var.add('message', var_type='String')
dev_var.add('device', var_type='Device')
dev_var.add('severity', var_type='integer')
dev_var.add('type', var_type='String')
context = Variables.task_call(dev_var)

dateTimeObj = datetime.now()
format = "%Y-%m-%dT%H:%M:%S+0000"
time1 = dateTimeObj.strftime(format)
format = "%Y-%m-%d"
date = dateTimeObj.strftime(format)

url = "http://172.20.0.4:9200/ubilogs-"+date+"/_doc"

message = context['message']
device_id = context['device']
severity = context['severity']
type_id = context['type']

payload = {"rawlog": ""+message+"", "device_id": ""+device_id+"", "date": ""+time1+"", "customer_ref": "TyrellCorp", "severity": ""+severity+"", "type": ""+type_id+"", "subtype": "WF"}

headers = {'content-type': 'application/json'}

r = requests.post(url, json=payload, headers=headers)

ret = MSA_API.process_content('ENDED', f'Post Result: {r}, url: {url}', context, True)
