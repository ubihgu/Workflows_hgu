from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
context = Variables.task_call()

ret = MSA_API.process_content('WARNING', f'CHECK IS STILL WORK IN PROGRESS', context, True)
print(ret)