from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
dev_var = Variables()
dev_var.add('switch', var_type='Device')
dev_var.add('leaf1', var_type='Device')
dev_var.add('leaf2', var_type='Device')

context = Variables.task_call(dev_var)
ret = MSA_API.process_content('ENDED',
                              f'Workflow Instance Created. Managed Entity: {context["switch"]}',
                              context, True)
print(ret)