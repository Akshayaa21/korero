import requests
from decouple import config

ELEVEN_LABS_API_KEY = config("ELEVEN_LABS_API_KEY")


def convert_text_to_speech(message):

    # Define data that we are gonna send 
    body ={
        "text": message,
        "voice_settings": {
            "stability": 0,
            "similarity_boost": 0,
            "style":0.5,
            "use_speaker_boost": True
        }
    }

    voice_hannah = "Ql8tESJYh1rsV2fuE0NO"

    # Constructing Headers and Endpoint 
    headers = {"xi-api-key": ELEVEN_LABS_API_KEY, "Content-Type":"application/json", "accept":"audio/mpeg"}
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_hannah}"

    # Send request 
    try:
        response = requests.post(url, json=body, headers=headers)
    except Exception as e:
        return

    # Handle response
    if response.status_code == 200:
        return response.content
    else:
        return 