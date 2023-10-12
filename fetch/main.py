import os
import json

import functions_framework
import gspread
import phonenumbers

from utils import dump_to_file

# get srv acc creds
srv_acc_cred = os.environ['SRV_ACC_CRED_JSON']
print(json.dumps({"severity": "DEBUG", "message": f"CRED JSON: {srv_acc_cred}"}))
creds_file_path = dump_to_file('srv_acc_cred.json', srv_acc_cred)
print(json.dumps({"severity": "DEBUG", "message": f"Dump file: {creds_file_path}"}))

# init gsheets client
gc = gspread.service_account(filename=creds_file_path)


@functions_framework.http
def fetch(request):

    # parse request
    request_json = request.get_json(silent=True)
    request_args = request.args

    # get args
    sheet_url = get_arg(request_json, request_args, 'sheet_url',
                        'https://docs.google.com/spreadsheets/d/1sMhcaZ0fFLmoFlTDsS-uhtaemLEpFDB3PUXI5Z6BFgc')

    # get data from sheet
    sh = gc.open_by_url(sheet_url)
    all_data = sh.worksheet('Numbers').get_values()
    # text_data = sh.worksheet('Text').get_values()

    # prepare numbers
    num_list = []
    for i in range(1, len(all_data)):

        # parse and validate phone number
        parsed_number = parse_number(all_data[i][0])
        if parsed_number:
            num_list.append(
                {
                    'phone_num': parsed_number,
                    'name': all_data[i][1],
                    'category': all_data[i][2]
                }
            )
    #
    # # prepare texts
    # text_dict = {}
    # for i in range(1, len(text_data)):
    #     if text_data[i][0]:
    #         text_dict[text_data[i][0]] = text_data[i][1]

    response = {
        'numbers': num_list,
        # 'text_map': text_dict,
    }

    print(f'Response: {response}')
    return json.dumps(response), 200, {'ContentType': 'application/json'}


def get_arg(request_json, request_args, arg_name, default_value):

    if request_json and arg_name in request_json:
        arg_value = request_json[arg_name]

    elif request_args and arg_name in request_args:
        arg_value = request_args[arg_name]

    elif default_value:
        arg_value = default_value

    else:
        raise Exception(f'Argument missing: {arg_name}')

    return arg_value


def parse_number(num_str):
    parsed_number = None
    try:

        # try to parse
        parsed_number = phonenumbers.parse(num_str)

    except phonenumbers.NumberParseException as num_ex:

        # assume default "IL" region
        if num_ex.error_type == num_ex.INVALID_COUNTRY_CODE:
            parsed_number = phonenumbers.parse(num_str, "IL")

    if parsed_number:
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)[1:]
