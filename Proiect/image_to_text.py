from flask import Flask, render_template, request
import json
import azure.cognitiveservices.speech as speechsdk
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os, requests, uuid, json
import io

def get_text(image_data):
    subscription_key = "c92ca35ff7354fa985474ed1630e52a8"
    endpoint = 'https://textfromimageproject.cognitiveservices.azure.com/'
	
    ocr_url = endpoint + "vision/v2.1/ocr"

    headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
    params = {'language': 'en', 'detectOrientation': 'true'}
    response = requests.post(ocr_url, headers=headers, params=params, data = image_data)
    
    analysis = response.json()
    response = ''
    for region in analysis['regions']:
        for line in region['lines']:
            for word in line['words']:
                response += word['text'] + ' '
	
    return response



'''
with io.open("D:\Facultate\CC\Cloud\Tema3\Image\Kamina quote.jpg", "rb") as f:
        content = f.read()

print(get_text(content))
'''