import urllib.request as request
import urllib.parse as parse
import json
import requests


def spellcheck_text(text, language):
    api_key = "09129496065c485d81a8bc76bc242d2a"
    endpoint = "https://tema4spellcheck.cognitiveservices.azure.com/bing/v7.0/spellcheck"
    data = {'text': text}
    params = {
    'mkt': language,
    'mode':'proof'
    }
    headers = {
    'Content-Type': 'application/x-www-form-urlencoded',
    'Ocp-Apim-Subscription-Key': api_key,
    }
    response = requests.post(endpoint, headers=headers, params=params, data=data)
    json_response = response.json()
    '''
    data = {'text': text,
            'mkt': language,
            'mode': 'proof'}

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded',
        'Ocp-Apim-Subscription-Key': api_key,
    }

    data = parse.urlencode(data).encode('utf-8')
    response = request.Request(endpoint, headers=headers, data = data)
    json_response = request.urlopen(response)
    '''
    result = json_response
    aditional_replacing_offset = 0

    for corrections in result['flaggedTokens']:
        offset = corrections['offset'] + aditional_replacing_offset
        bad_word = corrections['token']
        correct_word = corrections['suggestions'][0]['suggestion'] #most likely word
        text = text[:offset] + correct_word + text[offset+len(bad_word):]
        aditional_replacing_offset += len(correct_word) - len(bad_word)
    
    return text


#print(spellcheck_text("Salu, ce ma gaci?", "ro-RO")) #fii atent la formatul limbii !