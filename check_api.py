import os
from elevenlabs import ElevenLabs
from dotenv import load_dotenv
from elevenlabs.core.api_error import ApiError

load_dotenv()
api_key = os.getenv("ELEVENLABS_API_KEY")

client = ElevenLabs(api_key=api_key)

try:
    voices_response = client.voices.get_all()
    print("API Key is valid! Voices available:")
    for voice in voices_response.voices:
        print(f"- {voice.name} (ID: {voice.voice_id})")
except ApiError as e:
    print(f"API Key error or request failed: {e}")
