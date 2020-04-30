# -*- coding: utf-8 -*-
import os, requests, uuid, json


subscription_key = "02cf146dde3a48eb99210c08270d089b"

endpoint = "https://api.cognitive.microsofttranslator.com/"

def translate_text(input_text, output_language):
    path = 'translate?api-version=3.0'
    params = '&to=' + output_language
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': 'westeurope',
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': input_text
    }]

    request = requests.post(constructed_url, headers=headers, json=body)
    response = request.json()
    return response
 
#print(translate_text("hi","ro"))
