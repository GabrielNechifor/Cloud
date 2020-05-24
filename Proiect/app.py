from flask import Flask, render_template, url_for, jsonify, request
import text_to_text, analytics, text_to_speech, image_to_text, spellcheck, speech_to_text
import os, requests, uuid, json

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/text_to_text')
def text_to_text_handler():
    input_text = request.args['input_text']
    output_language = request.args['to']
    translated_text = text_to_text.translate(input_text, output_language)
    return translated_text


@app.route('/text_to_speech')
def text_to_speech_handler():
    input_text = request.args['input_text']
    output_language = request.args['to']
    translated_text = text_to_text.translate(input_text, output_language)
    audio_data = text_to_speech.translate(translated_text, output_language)
    return audio_data


@app.route('/image_to_text', methods=['POST'])
def image_to_text_handler():
    image_data = request.files['image_data'].read()
    output_language = request.form['to']
    text_from_image = image_to_text.get_text(image_data)
    translated_text = text_to_text.translate(text_from_image, output_language)
    return translated_text


@app.route('/image_to_speech', methods=['POST'])
def image_to_speech_handler():
    image_data = request.files['image_data'].read()
    output_language = request.form['to']
    text_from_image = image_to_text.get_text(image_data)
    translated_text = text_to_text.translate(text_from_image, output_language)
    audio_data = text_to_speech.translate(translated_text, output_language)
    return audio_data


@app.route('/speech_to_text', methods=['POST'])
def speech_to_text_handler():
    speech_data = request.files['speech_data'].read()
    input_language = request.form['from']
    output_language = request.form['to']
    text_from_speech = speech_to_text.get_text(speech_data, input_language)
    translated_text = text_to_text.translate(text_from_speech, output_language)
    return translated_text


@app.route('/speech_to_speech', methods=['POST'])
def speech_to_speech_handler():
    speech_data = request.files['speech_data'].read()
    input_language = request.form['from']
    output_language = request.form['to']
    text_from_speech = speech_to_text.get_text(speech_data, input_language)
    translated_text = text_to_text.translate(text_from_speech, output_language)
    audio_data = text_to_speech.translate(translated_text, output_language)
    return audio_data


