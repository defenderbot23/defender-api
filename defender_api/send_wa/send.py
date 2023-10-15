import os
import json
import time

import functions_framework

from whatsapp_api_client_python import API

from common.utils import get_arg


def init_client():

    # init green api
    return API.GreenApi(os.environ['GREEN_API_INSTANCE_ID'], os.environ['GREEN_API_INSTANCE_TOKEN'])


@functions_framework.http
def send_wa(request):

    # prepare response
    response = {}

    # parse request
    request_json = request.get_json(silent=True)

    # get args
    message = get_arg(request_json, 'message')
    sleep_time = get_arg(request_json, 'sleep_time', 1)
    recipient_list = get_arg(request_json, 'recipient_list', None)   # "{phone_number}@c.us" or "{group_id}@g.us"

    # iterate recipients
    for recipient_num, recipient_id in enumerate(recipient_list):

        # send message
        green_api = init_client()
        resp = green_api.sending.sendMessage(
            chatId=recipient_id,
            message=message,
            linkPreview=False
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
