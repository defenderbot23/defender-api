from google.cloud import firestore
from google.cloud.firestore_v1.base_query import FieldFilter

db = firestore.Client()
phones_col = db.collection("phones")
texts_col = db.collection("text")


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def get_matching_phones(phone_list):

    # results
    matching_phones = {}

    for phone_batch in chunker(phone_list, 30):

        # query
        query = phones_col.where(filter=FieldFilter("phone_number", "in", phone_batch))

        # iterate results
        for phone in query.stream():

            # add result
            matching_phones[phone.get('phone_number')] = {
                'name': phone.get('name'),
                'category': phone.get('category')
            }

    return matching_phones


def get_matching_texts(cat_list):

    # results
    matching_texts = {}

    # query
    query = texts_col.where(filter=FieldFilter("category", "in", cat_list))

    # iterate results
    for text in query.stream():

        # add result
        matching_texts[text.get('category')] = {
            'text': text.get('text')
        }

    return matching_texts
