import json, uuid
import requests
from flask_babel import _
from flask import current_app

def translate(text, dest_language):
    if 'MS_TRANSLATOR_KEY' not in current_app.config or \
            not current_app.config['MS_TRANSLATOR_KEY']:
        return _('Error: the translation service is not configured.')
    auth = current_app.config['MS_TRANSLATOR_KEY']
    base_url = 'https://api.cognitive.microsofttranslator.com'
    path = '/translate?api-version=3.0'
    params = '&to=' + dest_language
    constructed_url = base_url + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': auth,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4()),
        'Ocp-Apim-Subscription-Region': 'westeurope'
    }

    body = [{'text' : text}]
    r = requests.post(constructed_url, headers=headers, json=body)
    if r.status_code != 200:
        return _('Error: the translation service failed.')
    return json.loads(r.content.decode('utf-8-sig'))[0]['translations'][0]['text']
