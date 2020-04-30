from flask import Flask, render_template, request
import azure.cognitiveservices.speech as speechsdk
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
import os, requests, uuid, json

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

def get_voice(text, language):
    # Creates an instance of a speech config with specified subscription key and service region.
    # Replace with your own subscription key and service region (e.g., "westus").
    speech_key, service_region = "e965286e589c468f9aeb7c5f03b03cb4", "westeurope"
    language = language_dict[language]
    speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)
    speech_config.set_property(speechsdk.PropertyId.SpeechServiceConnection_SynthLanguage, language)
    speech_config.set_speech_synthesis_output_format(speechsdk.SpeechSynthesisOutputFormat.Audio16Khz128KBitRateMonoMp3)

    # Creates a speech synthesizer using the default speaker as audio output.
    speech_synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)

    # Synthesizes the received text to speech.
    # The synthesized speech is expected to be heard on the speaker with this line executed.
    result = speech_synthesizer.speak_text_async(text).get()

    # Checks result.
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        print("Speech synthesized to speaker for text [{}]".format(text))
    elif result.reason == speechsdk.ResultReason.Canceled:
        cancellation_details = result.cancellation_details
        print("Speech synthesis canceled: {}".format(cancellation_details.reason))
        if cancellation_details.reason == speechsdk.CancellationReason.Error:
            if cancellation_details.error_details:
                print("Error details: {}".format(cancellation_details.error_details))
        print("Did you update the subscription info?")
    result = result.audio_data
    return result
