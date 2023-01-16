#Python 2.x program for Speech Recognition

import os

from google.cloud import texttospeech
from webproject.settings import BASE_DIR
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]=os.path.join(BASE_DIR, "credentials/transdata.json")
#from playsound import playsound

# Instantiates a client

def NaturalTTS(text, filename):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
    language_code="en",
    name='en-Wavenet-C',
    ssml_gender=texttospeech.SsmlVoiceGender.FEMALE)
    audio_config = texttospeech.AudioConfig(
    audio_encoding=texttospeech.AudioEncoding.MP3)
    response = client.synthesize_speech(
    input=synthesis_input, voice=voice, audio_config=audio_config
    )
    path = os.path.join(BASE_DIR, "static/")
    filename = path+filename+".mp3"
    print(filename)
    with open(filename, 'wb') as out:
        out.write(response.audio_content)

