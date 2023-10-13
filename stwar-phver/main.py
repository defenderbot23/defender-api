import json
import functions_framework

from admins_db import check_by_mail, get_admin_details, get_admin_group

AVAILABLE_COMMANDS = {
    "check_by_mail": check_by_mail,
    "get_admin_details": get_admin_details,
    "get_admin_group": get_admin_group
}

@functions_framework.http
def match_phones(request):
    # Request structure:
    # {
    #  "command": "<command",
    #  "input": ["<input1>", "<input2>", ...]
    # }
    
    # Parse request
    request_json = request.get_json()
    
    # Get command
    command = request_json['command']
    
    # Get input
    input_list = request_json['input']
    
    print(f'Command: {command}')
    print(f'Input: {input_list}')
    
    if command not in AVAILABLE_COMMANDS.keys():
        response = {
            "status": "error",
            "message": f"Command: '{command}' not found"
        }
        
    else:
        response = AVAILABLE_COMMANDS[command](*input_list)
    
    return json.dumps(response), 200, {'Content-Type': 'application/json'}