from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
import io

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


def sample_recognize(content, language_code):
    """
    Transcribe a short audio file using synchronous speech recognition

    Args:
      local_file_path Path to local audio file, e.g. /path/audio.wav
    """

    client = speech_v1p1beta1.SpeechClient()

    # local_file_path = 'resources/brooklyn_bridge.raw'

    # Sample rate in Hertz of the audio data sent
    sample_rate_hertz = 44100

    # Encoding of audio data sent. This sample sets this explicitly.
    # This field is optional for FLAC and WAV audio formats.
    encoding = enums.RecognitionConfig.AudioEncoding.ENCODING_UNSPECIFIED
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
        "audio_channel_count":2,
    }
    audio = {"content": content}

    response = client.recognize(config, audio)
    '''
    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        print(u"Transcript: {}".format(alternative.transcript))
    '''
    return response.results[0].alternatives[0].transcript

'''
with io.open("./AhCmonNowBaby.wav", "rb") as f:
        content = f.read()

print(sample_recognize(content, "en"))
'''