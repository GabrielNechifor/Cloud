# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
from datetime import datetime
import logging
import os
import io

from flask import Flask, redirect, render_template, request

from google.cloud import datastore
from google.cloud import storage
from google.cloud import vision
from google.cloud.vision import types
from google.cloud import translate_v2 as translate
from google.auth.transport import requests
import google.oauth2.id_token


CLOUD_STORAGE_BUCKET = "imgs_ocr"
vision_client = vision.ImageAnnotatorClient()
storage_client = storage.Client()
translate_client = translate.Client()


firebase_request_adapter = requests.Request()


datastore_client = datastore.Client()

app = Flask(__name__)

def store_time(email, dt):
    entity = datastore.Entity(key=datastore_client.key('User', email, 'visit'))
    entity.update({
        'timestamp': dt
    })

    datastore_client.put(entity)


def fetch_times(email, limit):
    ancestor = datastore_client.key('User', email)
    query = datastore_client.query(kind='visit', ancestor=ancestor)
    query.order = ['-timestamp']

    times = query.fetch(limit=limit)

    return times


# [START gae_python37_auth_verify_token]
@app.route('/', methods=['GET', 'POST'])
def root():
    # Verify Firebase auth.
    id_token = request.cookies.get("token")
    error_message = None
    claims = None
    times = None
    full_texts = None
    image = None

    if id_token:
        try:
            claims = google.oauth2.id_token.verify_firebase_token(
                id_token, firebase_request_adapter)

            store_time(claims['email'], datetime.now())

        except ValueError as exc:
            error_message = str(exc)

    return render_template(
        'index.html',
        user_data=claims, error_message=error_message, image_entity=image,
    full_texts=full_texts)
# [END gae_python37_auth_verify_token]



@app.route('/upload_photo', methods=['GET', 'POST'])
def upload_photo():
    id_token = request.cookies.get("token")
    claims = None
    error_message = None
    try:
        claims = google.oauth2.id_token.verify_firebase_token(
            id_token, firebase_request_adapter)
    except ValueError as exc:
            error_message = str(exc)


    photo = request.files['file']

    # Create a Cloud Storage client.
    storage_client = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = storage_client.get_bucket(CLOUD_STORAGE_BUCKET)

    # Create a new blob and upload the file's content.
    blob = bucket.blob(photo.filename)
    blob.upload_from_string(
            photo.read(), content_type=photo.content_type)

    # Make the blob publicly viewable.
    blob.make_public()

    # Create a Cloud Vision client.
    # vision_client = vision.ImageAnnotatorClient()

    # Use the Cloud Vision client to detect a face for our image.
    source_uri = 'gs://{}/{}'.format(CLOUD_STORAGE_BUCKET, blob.name)
    image = vision.types.Image(
        source=vision.types.ImageSource(gcs_image_uri=source_uri))

    # If a face is detected, save to Datastore the likelihood that the face
    # displays 'joy,' as determined by Google's Machine Learning algorithm.
        
        # image = vision.types.Image()
        # image.source.image_uri = source_uri
    print("URL +" + str(image.source.image_uri))
    #Text detection
    response = vision_client.text_detection(image=image)
    texts = response.text_annotations
    print('Texts:')
    full_texts=[]
    for text in texts:
        
        vertices = (['({},{})'.format(vertex.x, vertex.y)
                    for vertex in text.bounding_poly.vertices])

        ###Translation part
        result = translate_client.translate(
            text.description, target_language='ro')

        # print(u'Detected source language: {}'.format(
            # result['detectedSourceLanguage']))
        full_texts.append({'before':result['input'],'after':result['translatedText']})

    if response.error.message:
        raise Exception(
        '{}\nFor more info on error messages, check: https://cloud.google.com/apis/design/errors'.format(
            response.error.message))

    # Redirect to the home page.
    return render_template('photo-uploaded.html',user_data=claims, error_message=error_message, image_entity=image,
    full_texts=full_texts)



if __name__ == '__main__':
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host='127.0.0.1', port=8080, debug=True)
