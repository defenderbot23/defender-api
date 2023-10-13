import phonenumbers


def get_arg(request_json, arg_name, default_value=None):

    if request_json and arg_name in request_json:
        arg_value = request_json[arg_name]

    elif default_value:
        arg_value = default_value

    else:
        raise Exception(f'Argument missing: {arg_name}')

    return arg_value


def dump_to_tmp(filename, content):

    # prepare name
    file_path = f'/tmp/{filename}'

    # write to file
    with open(file_path, 'w') as f:
        f.write(content)

    return file_path


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
