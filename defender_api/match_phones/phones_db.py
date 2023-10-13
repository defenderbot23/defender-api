from google.cloud.firestore_v1.base_query import FieldFilter


def chunker(seq, size):
    return (seq[pos:pos + size] for pos in range(0, len(seq), size))


def get_matching_phones(phones_col, phone_list):

    # results
    matching_phones = {}

    # iterate by chunks of 30 because of FireStore query limit for operator "whereIn"
    for phone_batch in chunker(phone_list, 30):

        # query
        print(f'Query for phone list: {phone_batch}')
        query = phones_col.where(filter=FieldFilter("phone_number", "in", phone_batch))

        # iterate results
        for phone in query.stream():

            # add result
            matching_phones[phone.get('phone_number')] = {
                'name': phone.get('name'),
                'category': phone.get('category')
            }

    return matching_phones


def get_matching_texts(texts_col, cat_list):

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
