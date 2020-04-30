from flask import Flask, render_template, url_for, jsonify, request
import translate, analytics, textToSpeech, textFromImage, spellcheck
import requests
import azure.cognitiveservices.speech as speechsdk
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os, requests, uuid, json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return render_template('index.html', audio='false')

@app.route('/sentiment-text', methods=['POST'])
def sentiment_text():
    data = request.get_json()
    input_text = data['text']
    response = analytics.sentiment_analysis_example(input_text)
    return jsonify(response)

@app.route('/translate-text', methods=['POST'])
def translate_text():
    data = request.get_json()
    input_text = data['text']
    output_language = data['to']
    response = translate.translate_text(input_text, output_language)
    return jsonify(response)

language="en"
input_text="Type text fpor translate"

@app.route("/audio.mp3")
def get_audio():
    global language
    global input_text
    translated_text = translate.translate_text(input_text, language)
    result = textToSpeech.get_voice(translated_text[0]['translations'][0]['text'], language)

    return result



@app.route("/set_language_and_text")
def set_language_and_text():
    global language
    global input_text
    language = request.args['output_language']
    input_text = request.args['input_text']


    return render_template('index.html',audio='true')


@app.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():

    image_data = request.files['file'].read()

    result = textFromImage.text_from_image(image_data)

    return render_template('index.html',audio='true', result=result)

@app.route('/spellcheck')
def spellcheck_text():
    language = request.args['spellcheck_language']
    input_text = request.args['spellcheck_text']
    response = spellcheck.spellcheck_text(input_text, language)
    #response = spellcheck.spellcheck_text('Salu, ce ma gaci?', 'ro-RO')
    return render_template('index.html',audio='true', response=response)


