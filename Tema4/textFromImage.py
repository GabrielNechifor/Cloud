from flask import Flask, render_template, request
import azure.cognitiveservices.speech as speechsdk
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os, requests, uuid, json

def text_from_image(image_data):
    subscription_key = "88484c62b82b4e93a2b57864db5c014a"
    endpoint = 'https://extracttextfromimage.cognitiveservices.azure.com/'
	
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
