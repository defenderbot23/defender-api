import json
import requests
from datetime import datetime


def get_timed_messages():

    # prepare URL
    url = "https://europe-west1-fair-alliance-401708.cloudfunctions.net/defender-api-fetch_gsheet"

    # build request
    payload = json.dumps({
      "url": "https://docs.google.com/spreadsheets/d/1p9n-XSeNRaHt_CkK5aff3rYoApZwvBKixSJCAr6YRxU",
      "worksheet": "Broadcast",
      "start_row": 1,
      "fields": [
        {
          "name": "time",
          "column": 0
        },
        {
          "name": "message",
          "column": 1
        }
      ]
    })
    headers = {
      'Content-Type': 'application/json'
    }

    resp = requests.request("POST", url, headers=headers, data=payload)
    resp.raise_for_status()

    # filter empty
    messages = resp.json()
    messages = [msg for msg in messages if msg['message'] and msg['time']]

    # return
    return messages


def fix_times(timed_messages):

    # iterate times
    for tm in timed_messages:

        # parse
        parsed_time = datetime.strptime(tm['time'], '%H:%M').time()

        # combine
        tm['time'] = datetime.combine(datetime.now(), parsed_time)


def get_current_message():

    # get all times messages
    timed_messages = get_timed_messages()
    fix_times(timed_messages)

    # find current
    current_tm = next((tm for tm in reversed(timed_messages) if datetime.now().time() > tm['time'].time()), None)

    # return
    return current_tm
