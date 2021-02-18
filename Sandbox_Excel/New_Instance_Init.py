'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
import xlrd 
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

'''
List all the parameters required by the task

You can use var_name convention for your variables
They will display automaticaly as "Var Name"
The allowed types are:
  'String', 'Boolean', 'Integer', 'Password', 'IpAddress',
  'IpMask', 'Ipv6Address', 'Composite', 'OBMFRef', 'Device'

 Add as many variables as needed
'''
dev_var = Variables()
dev_var.add('file', var_type='String')

'''
context => Service Context variable per Service Instance
All the user-inputs of Tasks are automatically stored in context
Also, any new variables should be stored in context which are used across Service Instance
The variables stored in context can be used across all the Tasks and Processes of a particular Service
Update context array [add/update/delete variables] as per requirement

ENTER YOUR CODE HERE
'''
context = Variables.task_call(dev_var)
file = context['file']

ret = MSA_API.process_content('ENDED', 'Task OK', context, True)
print(ret)

