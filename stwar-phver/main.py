import json
import functions_framework

from phones_db import get_matching_phones, get_matching_texts


@functions_framework.http
def match_phones(request):

    # parse request
    request_json = request.get_json(silent=True)
    query_phone_list = request_json.get('phone_list')
    print(f'Query phones: {query_phone_list}')

    # get matches
    matching_phones = get_matching_phones(query_phone_list)
    print(f'Matching phones: {matching_phones}')

    # get texts for categories
    matched_categories = {m['category'] for m in matching_phones.values()}
    match_texts = get_matching_texts(matched_categories)
    print(f'Matching texts: {match_texts}')

    # prepare response
    response = {
        'texts': match_texts,
        'phone_numbers': matching_phones
    }

    print(f'Response: {response}')
    return json.dumps(response), 200, {'ContentType': 'application/json'}
