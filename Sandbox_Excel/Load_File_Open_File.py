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
dev_var.add('sheet_id', var_type='integer')
dev_var.add('row', var_type='integer')
dev_var.add('column', var_type='integer')

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
sheet_id = int(context['sheet_id'])
column = int(context['column'])
row = int(context['row'])

wb = xlrd.open_workbook(file) 
sheet = wb.sheet_by_index(sheet_id) 
  
# For row 0 and column 0 
cell = sheet.cell_value(row, column)


ret = MSA_API.process_content('ENDED',
                                  f'STATUS: OK, \
                                    MESSAGE: Cell value: {cell}, {sheet.nrows} rows, {sheet.ncols} cols, {sheet.row_values(row)}',
                                  context, True)

print(ret)

