from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
import time

#import requests

dev_var = Variables()
dev_var.add('construction_name', var_type='String')
dev_var.add('additional_device_name', var_type='Device')
dev_var.add('urlpath', var_type='String')
context = Variables.task_call()

secondsSinceEpoch = int(round(time.time() * 1000))


#url     = 'http://example.tld'
urlpath = {context['urlpath']}

payload = {
  "rawlog": "Notification From Workflow",
  "customer_ref": "TyrellCorp",
  "timestamp": {secondsSinceEpoch},
  "device_id": {context['additional_device_name']},
  "severity": "3",
  "type": "NOTIFICATION",
  "subtype": "WF"
}
headers = {}
data = json.dumps(payload)
#res = requests.post(url, data=payload, headers=headers)

ret = MSA_API.process_content('ENDED', f'Timestamp: {secondsSinceEpoch}, URL:{urlpath}, Payload: {data}', context, True)
print(ret)
