import urllib.request as request
import urllib.parse as parse
import json
import requests

language_dict={
    'ar' : 'ar-EG',
    'bg' : 'bg-BG',
    'ca' : 'ca-ES',
    'cs' : 'cs-CZ',
    'da' : 'da-DK',
    'de' : 'de-DE',
    'el' : 'el-GR',
    'en' : 'en-US',
    'es' : 'es-ES',
    'fi' : 'fi-FI',
    'fr' : 'fr-FR',
    'he' : 'he-IL',
    'hi' : 'hi-IN',
    'hr' : 'hr-HR',
    'hu' : 'hu-HU',
    'id' : 'id-ID',
    'it' : 'it-IT',
    'ja' : 'ja-JP',
    'ko' : 'ko-KR',
    'ms' : 'ms-MY',
    'nb' : 'nb-NO',
    'nl' : 'nl-NL',
    'pl' : 'pl-PL',
    'pt' : 'pt-PT',
    'ro' : 'ro-RO',
    'ru' : 'ru-RU',
    'sk' : 'sk-SK',
    'sl' : 'sl-SI',
    'sv' : 'sv-SE',
    'ta' : 'ta-IN',
    'te' : 'te-IN',
    'th' : 'th-TH',
    'tr' : 'tr-TR',
    'vi' : 'vi-VN',
    'zh-Hans' : 'zh-CN'  
}

def spellcheck_text(text, language):
    api_key = "8262500a607e4a74a59ddb8ca0fb1cac"
    endpoint = "https://spellcheckproject.cognitiveservices.azure.com/bing/v7.0/spellcheck"
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


#print(spellcheck_text("Salu, ce ma gaci?", "ro-RO")) #fii atent la formatul limbii!