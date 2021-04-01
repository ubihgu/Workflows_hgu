<?php

/**
 * This file is necessary to include to use all the in-built libraries of /opt/fmc_repository/Reference/Common
 */
require_once '/opt/fmc_repository/Process/Reference/Common/common.php';

/**
 * List all the parameters required by the task
 */
function list_args()
{
  /**
   * You can use var_name convention for your variables
   * They will display automaticaly as "Var Name"
   * The allowed types are:
   *    'String', 'Boolean', 'Integer', 'Password', 'IpAddress',
   *    'IpMask', 'Ipv6Address', 'Composite', 'OBMFRef', 'Device'
   *
   * Add as many variables as needed
   */
  
}
  $verb  = "JSSMSEXEC";
  $param = "show logging";
  $device_id = '138';
  $rawlogs_json = _secengine_perform_verb_on_device($device_id, $verb, $param);
  $rawlogs = json_decode($rawlogs_json, true);
logToFile("---sh logging---\n". var_export($rawlogs, true));
task_exit( ENDED, $context['SERVICEINSTANCEID']);
?>