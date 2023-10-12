import os
import json

import functions_framework
import gspread
import phonenumbers

from utils import dump_to_tmp

# get srv acc creds
srv_acc_cred = os.environ['SRV_ACC_CRED_JSON']
creds_file_path = dump_to_tmp('srv_acc_cred.json', srv_acc_cred)

# init gsheets client
gc = gspread.service_account(filename=creds_file_path)


@functions_framework.http
def fetch(request):

    # parse request
    request_json = request.get_json(silent=True)

    # get args
    url = get_arg(request_json, 'url')
    worksheet = get_arg(request_json, 'worksheet')
    start_row = get_arg(request_json, 'start_row', 0)
    fields = get_arg(request_json, 'fields')

    # get data from sheet
    sheet = gc.open_by_url(url)
    all_data = sheet.worksheet(worksheet).get_values()

    # init response
    resp = []

    # iterate rows
    for row_index in range(start_row, len(all_data)):

        # init row resp
        row_resp = {}

        # parse fields
        for f in fields:

            # get data
            row_resp[f['name']] = all_data[row_index][f['column']]

            # format
            if f.get('format') == 'phone':
                row_resp[f['name']] = parse_number(row_resp[f['name']])

        # append to response
        resp.append(row_resp)

    # return
    return json.dumps(resp), 200, {'ContentType': 'application/json'}


def get_arg(request_json, arg_name, default_value=None):

    if request_json and arg_name in request_json:
        arg_value = request_json[arg_name]

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
