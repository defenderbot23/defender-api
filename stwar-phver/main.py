import json
import functions_framework

import gspread
import phonenumbers
from phonenumbers import NumberParseException

from auth import init_auth

# try to get secret
try:
    secret_value = init_auth()
    print(f'Secret: {secret_value}')

except Exception as ex:
    print(ex)

# init gsheets client
gc = gspread.service_account(filename='/workspace/srv_acc.json')


@functions_framework.http
def insert_row(request):

    # parse request
    request_json = request.get_json(silent=True)
    request_args = request.args

    # get args
    sheet_url = get_arg(request_json, request_args, 'sheet_url',
                        'https://docs.google.com/spreadsheets/d/1sMhcaZ0fFLmoFlTDsS-uhtaemLEpFDB3PUXI5Z6BFgc')

    # get data from sheet
    sh = gc.open_by_url(sheet_url)
    all_data = sh.worksheet('Numbers').get_values()
    text_data = sh.worksheet('Text').get_values()

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

    # prepare texts
    text_dict = {}
    for i in range(1, len(text_data)):
        if text_data[i][0]:
            text_dict[text_data[i][0]] = text_data[i][1]

    response = {
        'text_map': text_dict,
        'numbers': num_list
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

    return arg_value


def parse_number(num_str):
    parsed_number = None
    try:

        # try to parse
        parsed_number = phonenumbers.parse(num_str)

    except NumberParseException as num_ex:

        # assume default "IL" region
        if num_ex.error_type == num_ex.INVALID_COUNTRY_CODE:
            parsed_number = phonenumbers.parse(num_str, "IL")

    if parsed_number:
        return phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164)[1:]
