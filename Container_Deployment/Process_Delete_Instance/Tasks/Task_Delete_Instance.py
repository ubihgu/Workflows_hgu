'''
Visit http://[YOUR_MSA_URL]/msa_sdk/ to see what you can import.
'''
from msa_sdk.variables import Variables
from msa_sdk.msa_api import MSA_API

ret = MSA_API.process_content('Instance Deleted', 'Task OK', True)
print(ret)

