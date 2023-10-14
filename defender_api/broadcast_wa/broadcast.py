import os
import json
import time

from whatsapp_api_client_python import API

from broadcast_wa.timed_messages import get_current_message


def init_wa_client():

    # init green api
    return API.GreenApi(os.environ['GREEN_API_INSTANCE_ID'], os.environ['GREEN_API_INSTANCE_TOKEN'])


def get_groups(api):

    all_contacts = api.serviceMethods.getContacts()
    groups = {g['id']: g for g in all_contacts.data if g['type'] == 'group'}
    return groups


def broadcast(event):

    # collect executed actions
    response = {
        'message': None,
        'groups': []
    }

    # fetch current message
    current_tm = get_current_message()
    if current_tm:

        # add message
        print(f'Current message is {current_tm["message"]}')
        response['message'] = current_tm['message']

        # get all groups in contacts
        gapi = init_wa_client()
        groups = get_groups(gapi)

        # iterate recipients
        for group_idx, group in enumerate(groups):

            # send message
            print(f'Sending message to: {group}')
            # resp = gapi.sending.sendMessage(
            #     chatId=group['id'],
            #     message=current_tm
            # )

            # register send
            # if resp.code == 200:
            response['groups'].append(group)

            # sleep only if there's more to send
            if group_idx < len(groups) - 1:
                time.sleep(0.1)

    # return
    return json.dumps(response), 200, {'ContentType': 'application/json'}
