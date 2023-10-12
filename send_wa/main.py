import os
import json

import functions_framework

from whatsapp_api_client_python import API

from common.utils import get_arg

# init green api
green_api = API.GreenApi(os.environ['GREEN_API_INSTANCE_ID'], os.environ['GREEN_API_INSTANCE_TOKEN'])


@functions_framework.http
def send(request):

    # parse request
    request_json = request.get_json(silent=True)

    # get args
    chat_id = get_arg(request_json, 'chat_id')  # f'{phone_number}@c.us'
    message = get_arg(request_json, 'message')

    # send message
    resp = green_api.sending.sendMessage(
        chatId=chat_id,
        message=message
    )

    # return
    return json.dumps(resp), 200, {'ContentType': 'application/json'}
