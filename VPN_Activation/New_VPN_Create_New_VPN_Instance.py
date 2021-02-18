from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

dev_var = Variables()
dev_var.add('vpn_name', var_type='String')
context = Variables.task_call(dev_var)

ret = MSA_API.process_content('ENDED', f'Workflow instance created', context, True)
print(ret)

# END OF FILE