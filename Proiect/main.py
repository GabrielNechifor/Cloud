from flask import Flask, render_template, url_for, jsonify, request
import text_to_text, analytics, text_to_speech, image_to_text, spellcheck, speech_to_text, database, storage
import os, requests, uuid, json
from flask_cors import CORS
import google.oauth2.id_token
from google.auth.transport import requests

firebase_request_adapter = requests.Request()

app = Flask(__name__)
app.config['JSON_AS_ASCII'] = False
CORS(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/saved_resources_page')
def saved_resources_page():
    return render_template('savedResources.html')

@app.route('/saved_resource_page')
def saved_resource_page():
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    try:
        claims = google.oauth2.id_token.verify_firebase_token(
            id_token, firebase_request_adapter)
    except ValueError as exc:
            error_message = str(exc)
    print(claims['email'])

    email = claims['email']

    resource_name =  request.args['name']
    description, input_type, output_type, input_language, output_language = database.getAResource(email, resource_name)

    input_resource = storage.get_file(email, resource_name, "input")
    output_resource = storage.get_file(email, resource_name, "output")


    if input_type == "text": input_resource.decode('utf-8')
    if output_type == "text": output_resource.decode('utf-8')

    print(description, input_type, output_type, input_resource, output_resource)

    return render_template('savedResource.html', resource_name=resource_name, input_type=input_type, output_type=output_type,
    input_language=input_language, output_language=output_language, input_resource=input_resource, output_resource= output_resource)




@app.route('/text_to_text')
def text_to_text_handler():
    input_text = request.args['input_text']
    output_language = request.args['to']
    translated_text = text_to_text.translate(input_text, output_language)
    return translated_text


@app.route('/text_to_speech')
def text_to_speech_handler():
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    try:
        claims = google.oauth2.id_token.verify_firebase_token(
            id_token, firebase_request_adapter)
    except ValueError as exc:
            error_message = str(exc)
    print(claims['email'])

    input_text = request.args['input_text']
    output_language = request.args['to']
    translated_text = text_to_text.translate(input_text, output_language)
    audio_data = text_to_speech.translate(translated_text, output_language)
    return audio_data


@app.route('/image_to_text', methods=['POST'])
def image_to_text_handler():
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    try:
        claims = google.oauth2.id_token.verify_firebase_token(
            id_token, firebase_request_adapter)
    except ValueError as exc:
            error_message = str(exc)
    print(claims['email'])

    image_data = request.files['image_data'].read()
    output_language = request.form['to']
    text_from_image = image_to_text.get_text(image_data)
    translated_text = text_to_text.translate(text_from_image, output_language)
    return translated_text


@app.route('/image_to_speech', methods=['POST'])
def image_to_speech_handler():
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    try:
        claims = google.oauth2.id_token.verify_firebase_token(
            id_token, firebase_request_adapter)
    except ValueError as exc:
            error_message = str(exc)
    print(claims['email'])

    image_data = request.files['image_data'].read()
    output_language = request.form['to']
    text_from_image = image_to_text.get_text(image_data)
    translated_text = text_to_text.translate(text_from_image, output_language)
    audio_data = text_to_speech.translate(translated_text, output_language)
    return audio_data


@app.route('/speech_to_text', methods=['POST'])
def speech_to_text_handler():
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    try:
        claims = google.oauth2.id_token.verify_firebase_token(
            id_token, firebase_request_adapter)
    except ValueError as exc:
            error_message = str(exc)
    print(claims['email'])

    speech_data = request.files['speech_data'].read()
    input_language = request.form['from']
    output_language = request.form['to']
    text_from_speech = speech_to_text.get_text(speech_data, input_language)
    translated_text = text_to_text.translate(text_from_speech, output_language)
    return translated_text


@app.route('/speech_to_speech', methods=['POST'])
def speech_to_speech_handler():
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    try:
        claims = google.oauth2.id_token.verify_firebase_token(
            id_token, firebase_request_adapter)
    except ValueError as exc:
            error_message = str(exc)
    print(claims['email'])
    
    speech_data = request.files['speech_data'].read()
    input_language = request.form['from']
    output_language = request.form['to']
    text_from_speech = speech_to_text.get_text(speech_data, input_language)
    translated_text = text_to_text.translate(text_from_speech, output_language)
    audio_data = text_to_speech.translate(translated_text, output_language)
    return audio_data


@app.route('/save_resource', methods=['POST'])
def save_resource_handler():
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    try:
        claims = google.oauth2.id_token.verify_firebase_token(
            id_token, firebase_request_adapter)
    except ValueError as exc:
            error_message = str(exc)
    print(claims['email'])
    email = claims['email']
    

    resource_name = request.form["name"]
    description = request.form['description']
    input_type = request.form["input_type"]
    output_type = request.form["output_type"]
    input_language = request.form["input_language"]
    output_language = request.form["output_language"]
    input_resource = None
    output_resource = None

    if input_type == "text":
        input_resource = request.form["input_resource"]
    if input_type == "audio" or input_type == "image":
        input_resource = request.files['input_resource'].read()

    if output_type == "text":
        output_resource = request.form["output_resource"]
    if output_type == "audio":
        output_resource = request.files['output_resource'].read()

    database.insert_row(email, resource_name, description, input_type, output_type, input_language, output_language)
    storage.store_file(email, resource_name, "input", input_resource)
    storage.store_file(email, resource_name, "output", output_resource)

    return "Received"


@app.route('/delete_resource', methods=['POST'])
def delete_resource_handler():
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    try:
        claims = google.oauth2.id_token.verify_firebase_token(
            id_token, firebase_request_adapter)
    except ValueError as exc:
            error_message = str(exc)
    print(claims['email'])
    email = claims['email']

    json_data = request.get_json()
    name = json_data['name']
    response = database.deleteResource(email, name)
    storage.delete_file(email, name)
    if response:
        return "The resource was deleted"
    else:
        return "Something went wrong. Try again!"


@app.route('/saved_resources')
def saved_resources_handler():
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    try:
        claims = google.oauth2.id_token.verify_firebase_token(
            id_token, firebase_request_adapter)
    except ValueError as exc:
            error_message = str(exc)
    print(claims['email'])
    email = claims['email']

    resources = database.getListOfResources(email)
    return jsonify(resources)
