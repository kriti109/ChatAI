from elevenlabs import generate, save, play, set_api_key
import os
from dotenv import load_dotenv

load_dotenv()
set_api_key(os.getenv("ELEVENLABS_API_KEY"))

audio = generate(
    text="Hello from Veena. This is a voice test.",
    voice="Rachel"
)

save(audio, "veena_test.mp3")
play(audio)  # or use playsound if you want

