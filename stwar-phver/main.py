import json
import functions_framework

from phones_db import get_matching_phones, get_matching_texts


@functions_framework.http
def match_phones(request):
    # Request structure: <Command> <input1> <input2> <input3> ...

    # Parse request
    request_list = request.data.decode('utf-8').split(' ')
    
    # Get command
    command = request_list[0]
    
    # Get input
    input_list = request_list[1:]
    
    print(f'Command: {command}')
    print(f'Input: {input_list}')
    