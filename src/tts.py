#later will be used for text to speech
import os
from dotenv import load_dotenv
from elevenlabs.client import ElevenLabs
from elevenlabs import play

load_dotenv()
elevenlabs = ElevenLabs(
  api_key=os.getenv("ELEVENLABS_API_KEY"),
)

def speak(text):
    audio = elevenlabs.text_to_speech.convert(
    text=text,
    voice_id="cgSgspJ2msm6clMCkdW9",
    model_id="eleven_multilingual_v2",
    output_format="mp3_44100_128",
    )
    play(audio)
 