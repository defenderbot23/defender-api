import functions_framework

import send_wa.send as send
import fetch_gsheet.fetch as fetch
import match_phones.match as match
import broadcast_wa.broadcast as broadcast


@functions_framework.http
def match_phones(request):
    return match.match_phones(request)


@functions_framework.http
def send_wa(request):
    return send.send_wa(request)


@functions_framework.http
def fetch_gsheet(request):
    return fetch.fetch_gsheet(request)


@functions_framework.cloud_event
def broadcast_wa(event):
    return broadcast.broadcast_wa(event)
