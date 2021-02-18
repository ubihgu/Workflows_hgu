from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from datetime import datetime
import json
import requests

dev_var = Variables()
dev_var.add('construction_name', var_type='String')
dev_var.add('additional_device_name', var_type='Device')
context = Variables.task_call(dev_var)

# url = context['urlpath']
# url = 'http://172.20.0.4:9200/ubilogs-2020-10-23/_doc'

dateTimeObj = datetime.now()
format = "%Y-%m-%dT%H:%M:%S+0000"
time1 = dateTimeObj.strftime(format)
format = "%Y-%m-%d"
date = dateTimeObj.strftime(format)

url = "http://msa_es:9200/ubilogs-"+date+"/_doc"

name = context['construction_name']
device_id = context['additional_device_name']

payload = {"rawlog": ""+name+" Base config input result: OK CUSTOM", "device_id": ""+device_id+"", "date": ""+time1+"", "customer_ref": "TyrellCorp", "severity": "5", "type": "NOTIFICATION", "subtype": "WF"}

headers = {'content-type': 'application/json'}

r = requests.post(url, json=payload, headers=headers)
# r = "test"

ret = MSA_API.process_content('ENDED', f'{context["construction_name"]} configured', context, True)
print(ret)