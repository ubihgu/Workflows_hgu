from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API
from msa_sdk.orchestration import Orchestration
import time

dev_var = Variables()
dev_var.add('message', var_type='String')
context = Variables.task_call(dev_var)

Orchestration = Orchestration(context['UBIQUBEID'])
async_update_list = (context['PROCESSINSTANCEID'], context['TASKID'], context['EXECNUMBER'])

Orchestration.update_asynchronous_task_details(*async_update_list, 'Process started')

time.sleep(10)

Orchestration.update_asynchronous_task_details(*async_update_list, 'Processing '+context["message"]+'')

time.sleep(10)

ret = MSA_API.process_content('ENDED', f'{context["message"]} updated', context, True)
print(ret)

# END OF FILE