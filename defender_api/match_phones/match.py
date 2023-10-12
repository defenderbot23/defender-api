import json
import functions_framework
from google.cloud import firestore

from phones_db import get_matching_phones, get_matching_texts


@functions_framework.http
def match_phones(request):

    # parse request
    request_json = request.get_json(silent=True)
    query_phone_list = [int(num) for num in request_json.get('phone_list')]

    # init firestore client
    db = firestore.Client()

    # get matches
    phones_col = db.collection("phones")
    matching_phones = get_matching_phones(phones_col, query_phone_list)

    # get texts
    match_texts = {}
    if matching_phones:
        matched_categories = {m['category'] for m in matching_phones.values()}
        texts_col = db.collection("texts")
        match_texts = get_matching_texts(texts_col, matched_categories)

    # prepare response
    response = {
        'texts': match_texts,
        'phone_numbers': matching_phones
    }

    return json.dumps(response), 200, {'ContentType': 'application/json'}
