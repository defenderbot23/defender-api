import os
import json
import time

import functions_framework

from whatsapp_api_client_python import API

from common.utils import get_arg
from broadcast.timed_messages import get_current_message


def init_wa_client():

    # init green api
    return API.GreenApi(os.environ['GREEN_API_INSTANCE_ID'], os.environ['GREEN_API_INSTANCE_TOKEN'])


@functions_framework.http
def broadcast(request):

    # fetch current message
    current_tm = get_current_message()

    # prepare response
    response = {}

    # parse request
    request_json = request.get_json(silent=True)

    # get args
    sheet_url = get_arg(request_json, 'sheet_url')
    message = get_arg(request_json, 'message')
    sleep_time = get_arg(request_json, 'sleep_time', 1)
    recipient_list = get_arg(request_json, 'recipient_list', None)   # "{phone_number}@c.us" or "{group_id}@g.us"

    # iterate recipients
    for recipient_num, recipient_id in enumerate(recipient_list):

        # send message
        green_api = init_wa_client()
        resp = green_api.sending.sendMessage(
            chatId=recipient_id,
            message=message
        )

        response[recipient_id] = {
            'code': resp.code,
            'data': resp.data,
            'error': resp.error
        }

        # sleep only if there's more to send
        if recipient_num < len(recipient_list) - 1:
            time.sleep(sleep_time)

    # return
    return json.dumps(response), 200, {'ContentType': 'application/json'}
