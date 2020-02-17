# -*- coding: utf-8 -*-
ANSIBLE_METADATA = {
    'metadata_version': '1.3',
    'status': ['preview'],
    'supported_by': 'Ping Xiao'
}

DOCUMENTATION = '''
---
module: zos_operator_outstanding_action
short_description: display outstanding messages requiring operator action
description:
    - Get list of outstanding messages requiring operator action given one or more conditions
author: "Ping Xiao (@xiaoping)"
deprecated: []
options:
  request_number_list:
    description:
      - Parameter to specify question number or list of numbers.
    type: list
    required: False
    default: ['all']
  system:
    description:
      - Filter messages for a system. If the system name is not specified, all system messages in SYSPLEX will be returned. Wild cards are not supported.
    type: str
    required: False
    default: False
  message_id:
    description:
      - The message identifier for the action message awaiting a reply
    type: str
    required: False
    default: False
  jobname:
    description:
      - The name of the job which issued the action message
    type: str
    required: False
    default: False
seealso: [zos_operator]
notes:
  - check_mode is supported but in the case of this module, it never changs the system state so always return False
'''

EXAMPLES = '''
# Task(s) is a call to an ansible module, basically an action needing to be accomplished
- name: Get all outstanding messages requiring operator action
  zos_operator_outstanding_action:
    request_number_list: 
        - all
- Sample result('requests' field):
[
    {
        'number': '001', 
        'type': 'R', 
        'system': 'MV27', 
        'job_id': 'STC01537', 
        'message_text': '*399 HWSC0000I *IMS CONNECT READY* IM5HCONN', 
        'jobname': 'IM5HCONN', 
        'message_id': 'HWSC0000I'
    },
    {
        'number': '002', 
        'type': 'R', 
        'system': 'MV27', 
        'job_id': 'STC01533', 
        'message_text': '*400 DFS3139I IMS INITIALIZED, AUTOMATIC RESTART PROCEEDING IM5H', 
        'jobname': 'IM5HCTRL', 
        'message_id': 'DFS3139I'
    }
    ...
]
- name: Get outstanding messages given the question number
  zos_operator_outstanding_action:
    request_number_list:
        - 010
        - 008
        - 009
- Sample result('requests' field):
[
    {
        'number': '010',
        'type': 'R',
        'system': 'MV2I',
        'job_id': 'STC15833',
        'message_text': '*133 VAMP 0670 : ENTER COMMAND FOR IYCIZVMP', 
        'jobname': 'VAMP',
        'message_id': 'VAMP'
    }, 
    {
        'number': '008',
        'type': 'R',
        'system': 'MV2H',
        'job_id': 'STC15768',
        'message_text': '*116 VAMP 0670 : ENTER COMMAND FOR IYDCZVMP',
        'jobname': 'VAMP',
        'message_id': 'VAMP'
    }, 
    {
        'number': '009',
        'type': 'R',
        'system': 'MV2I',
        'message_text': '*130 DSI802A IYCIN    REPLY WITH VALID NCCF SYSTEM OPERATOR COMMAND',
        'jobname': 'NETVIEW',
        'message_id': 'DSI802A'
    }
- name: To display all outstanding messages issued on system MV2H
  zos_operator_outstanding_action:
      system: mv2h
- Sample result('requests' field):
[
   {
        'number': '101',
        'type': 'R', 
        'system': 'MV2H',
        'job_id': 'STC15413',
        'message_text': '*101 VAMP 0670 : ENTER COMMAND FOR IYDBZVMP',
        'jobname': 'VAMP',
        'message_id': 'VAMP'
    }, 
    {
        'number': '113',
        'type': 'R', 
        'system': 'MV2H',
        'message_text': '*113 DSI802A IYDCN    REPLY WITH VALID NCCF SYSTEM OPERATOR COMMAND', 
        'jobname': 'NETVIEW',
        'message_id': 'DSI802A'
    }
]
- name: To display all outstanding messages whose job name begin with im5 
  zos_operator_outstanding_action:
      jobname: im5*
- Sample result('requests' field):
[
    {
        'number': '088',
        'type': 'R',
        'system': 'MV2D',
        'job_id': 'STC15113',
        'message_text': '*088 DFS3139I IMS INITIALIZED, AUTOMATIC RESTART PROCEEDING IM5F', 
        'jobname': 'IM5FCTRL',
        'message_id': 'DFS3139I
    }, 
    {
        'number': '087',
        'type': 'R', 
        'system': 'MV2D',
        'job_id': 'STC15175',
        'message_text': '*087 HWSC0000I *IMS CONNECT READY* IM5FCONN',
        'jobname': 'IM5FCONN',
        'message_id': 'HWSC0000I'
    }
]
- name: To display the outstanding messages whose message id begin with dsi*
  zos_operator_outstanding_action:
      message_id: dsi*
- Sample result('requests' field):
[
    {
        'number': '086',
        'type': 'R', 'system':
        'MV2D', 'job_id':
        'STC15120', 'message_text':
        '*086 DSI802A IYM2D    REPLY WITH VALID NCCF SYSTEM OPERATOR COMMAND',
        'jobname': 'MQNVIEW', 
        'message_id': 'DSI802A'
    }, 
    {
        'number': '070',
        'type': 'R',
        'system': 'MV29',
        'job_id': 'STC14852',
        'message_text': '*070 DSI802A IYM29    REPLY WITH VALID NCCF SYSTEM OPERATOR COMMAND',
        'jobname': 'MQNVIEW', 
        'message_id': 'DSI802A'
    }
]
- name: Get outstanding messages given the various conditions
  zos_operator_outstanding_action:
    jobname: mq*
    message_id: dsi*
    system: mv29
- Sample result('requests' field):
[
    {
        'number': '070',
        'type': 'R',
        'system': 'MV29',
        'job_id': 'STC14852',
        'message_text': '*070 DSI802A IYM29    REPLY WITH VALID NCCF SYSTEM OPERATOR COMMAND',
        'jobname': 'MQNVIEW', 
        'message_id': 'DSI802A'
    }
]
'''
RETURN = '''
changed:
    description: True if the state was changed, otherwise False
    returned: always
    type: bool
failed:
    description: True if run operator command failed, othewise False
    returned: always
    type: bool
message:
    description: Return if the operator command been issued successfully
    type: str
requests_count:
    description: The count of the outstanding messages
    type: int
requests:
    description: The list of the outstanding messages
    type: list[dict]
    sample:
    [
        {
            'number': '009', //the open question numbers
            'type': 'R', //The type of the request, default is 'R'
            'system': 'MV2C', //The system name
            'job_id': 'STC13367', //The job identifier
            'message_text': '*009 DFS3139I IMS INITIALIZED, AUTOMATIC RESTART PROCEEDING IM4A', //The mssage text for the request
            'jobname': 'IM4ACTRL', //The name of the job which issued the action message
            'message_id': 'DFS3139I' //The message identifier for the action message awaiting a reply
        }, 
        {
            'number': '010', 
            'type': 'R', 
            'system': 'MV2C', 
            'job_id': 'STC13369', 
            'message_text': '*010 DFS3139I IMS INITIALIZED, AUTOMATIC RESTART PROCEEDING IM5A', 
            'jobname': 'IM5ACTRL', 
            'message_id': 'DFS3139I'
        }
        ...
    ]
'''


from ansible.module_utils.basic import AnsibleModule
import argparse
import re
from traceback import format_exc
from ansible_collections.ibm.ibm_zos_core.plugins.module_utils.better_arg_parser import BetterArgParser
from zoautil_py import OperatorCmd

def run_module():
    module_args = dict(
        request_number_list=dict(type='list', required=False,default=['all']),
        system=dict(type='str',required=False),
        message_id=dict(type='str',required=False),
        jobname=dict(type='str',required=False)
    )
    
    arg_defs=dict(
        request_number_list = dict(
            arg_type=request_number_list_type,
            required=False,
            default=['all']
        ),
        system=dict(
            arg_type=system_type,
            required=False
        ),
        message_id=dict(
            arg_type=message_id_type,
            required=False
        ),
        jobname=dict(
            arg_type=jobname_type,
            required=False
        )
    )

    result = dict(
        changed=False,
        original_message='',
        message=''
    )

    module = AnsibleModule(
        argument_spec=module_args,
        supports_check_mode=True
    )

    result['original_message'] = module.params
    if module.check_mode:
        return result
    try:
        parser = BetterArgParser(arg_defs)
        new_params = parser.parse_args(module.params)
        requests = find_required_request(new_params)
        if requests:
            result['requests_count'] = len(requests)
    except Error as e:
        module.fail_json(msg=e.msg, **result)
    except Exception as e:
        trace = format_exc()
        module.fail_json(msg='An unexpected error occurred: {0}'.format(trace), **result)
    result['message'] = {'stdout': 'The operator command has been issued succeessfully.', 'stderr': ''}
    result['requests'] = requests
    module.exit_json(**result)

def request_number_list_type(arg_val, params):
    for value in arg_val:
        if value and value !='all':
            validate_parameters_based_on_regex(value,'^[0-9]{2,}$')

def system_type(arg_val, params):
    if arg_val and arg_val!='*':
        arg_val = arg_val.strip('*')
    value=arg_val
    regex='^[a-zA-Z0-9]{1,8}$'
    validate_parameters_based_on_regex(value,regex)

def message_id_type(arg_val, params):
    if arg_val and arg_val!='*':
        arg_val = arg_val.strip('*')
    value=arg_val
    regex='^[a-zA-Z0-9]{1,8}$'
    validate_parameters_based_on_regex(value,regex)

def jobname_type(arg_val, params):
    if arg_val and arg_val!='*':
        arg_val = arg_val.strip('*')
    value=arg_val
    regex='^[a-zA-Z0-9]{1,8}$'
    validate_parameters_based_on_regex(value,regex)


def validate_parameters_based_on_regex(value,regex):
    pattern = re.compile(regex)
    if pattern.search(value):
        return true
    else:
        raise ValidationError(str(value))



def find_required_request(params):
    merged_list = create_merge_list()
    requests = filter_requests(merged_list,params)
    if requests:
        pass
    else:
        message='There is no such request given the condition, check your command or update your filter'
        raise OperatorCmdError(message)
    return requests

def create_merge_list():
    operator_cmd_a = 'd r,a,s'
    operator_cmd_b = 'd r,a,jn'
    message_a = execute_command(operator_cmd_a)
    message_b = execute_command(operator_cmd_b)
    list_a = parse_result_a(message_a)
    list_b = parse_result_b(message_b)
    merged_list = merge_list(list_a,list_b)
    return merged_list

def filter_requests(merged_list,params):
    request_number_list = params.get('request_number_list')
    system = params.get('system')
    message_id = params.get('message_id')
    jobname = params.get('jobname')
    newlist=[]
    if 'all'.lower() not in [(str(request)).lower() for request in request_number_list]:
        for number in request_number_list:
            for dict in merged_list:
                if dict.get('number') == str(number):
                    newlist.append(dict)
                    break
    else:
        newlist = merged_list
    if system:
        newlist = handle_conditions(newlist,'system',system.upper().strip('*'))
    if jobname:
        newlist = handle_conditions(newlist,'jobname',jobname.upper().strip('*'))
    if message_id:
        newlist = handle_conditions(newlist,'message_id',message_id.upper().strip('*'))
    return newlist

def handle_conditions(list,condition_type,condition_values):
    regex = re.compile(condition_values)
    newlist = []
    for dict in list:
        exist = regex.search(dict.get(condition_type))
        if exist:
            newlist.append(dict)
    return newlist

def execute_command(operator_cmd):
    rc_message = OperatorCmd.execute(operator_cmd)
    rc = rc_message.get('rc')
    message = rc_message.get('message')
    if rc > 0:
        raise OperatorCmdError(message)
    return message

def parse_result_a(result):
    dict_temp = {}
    list = []
    request_temp=''
    end_flag = False
    lines = result.split('\n')
    regex = re.compile(r'\s+')

    for index,line in enumerate(lines):
        line = line.strip()
        pattern_without_job_id = re.compile(r'\s*[0-9]{2,}\s[A-Z]{1}\s[a-zA-Z0-9]{1,8}')
        pattern_with_job_id = re.compile(r'\s*[0-9]{2,}\s[A-Z]{1}\s[A-Z0-9]{1,8}\s+[A-Z0-9]{1,8}\s')
        m = pattern_without_job_id.search(line)
        n = pattern_with_job_id.search(line)

        if index == (len(lines)-1):
            endflag = True
        if n or m or end_flag:
            if request_temp:
                dict_temp['message_text']=request_temp
                list.append(dict_temp)
                request_temp=''
                dict_temp = {}
            if n:
                elements = regex.split(line,4)
                dict_temp = {'number':elements[0],'type':elements[1],'system':elements[2],'job_id':elements[3]}
                request_temp = elements[4].strip()
                continue
            if m:
                elements = line.split(' ',3)
                dict_temp = {'number':elements[0],'type':elements[1],'system':elements[2]}
                request_temp = elements[3].strip()
                continue
        else:
            if request_temp:
                request_temp = request_temp +' '+line
    return list


def parse_result_b(result):
    # using d r,a,jn
    dict_temp = {}
    list = []    
    lines = result.split('\n')
    regex = re.compile(r'\s+')
    for index,line in enumerate(lines):
        line = line.strip()
        pattern_with_jobname = re.compile(r'\s*[0-9]{2,}\s[A-Z]{1}\s[A-Z0-9]{1,8}\s+')
        m = pattern_with_jobname.search(line)
        if m:
            elements = regex.split(line,5)
            # 215 R IM5GCONN *215 HWSC0000I *IMS CONNECT READY*  IM5GCONN
            dict_temp = {'number':elements[0],'jobname':elements[2],'message_id':elements[4]}
            list.append(dict_temp)
            continue
    return list

def merge_list(list_a,list_b):
    merged_list = []
    for dict_a in list_a:
        for dict_b in list_b:
            if dict_a.get('number') == dict_b.get('number'):
                dict_z = dict_a.copy()
                dict_z.update(dict_b)
                merged_list.append(dict_z)
    return merged_list
     

class Error(Exception):
    pass

class ValidationError(Error):
    def __init__(self, message):
        self.msg = 'An error occurred during validate the input parameters: "{0}"'.format(message)

class OperatorCmdError(Error):
    def __init__(self, message):
        self.msg = 'An error occurred during issue the operator command, the response is "{0}"'.format(message)


def main():
    run_module()

if __name__ == '__main__':
    main()