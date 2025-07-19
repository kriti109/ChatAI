# this will be used for speach to text later

# import speech_recognition as sr

# def transcribe_input():
#     recognizer = sr.Recognizer()
#     with sr.Microphone() as source:
#         print("Listening...")
#         audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
#         try:
#             text = recognizer.recognize_google(audio)
#             print(f"You: {text}")
#             return text
#         except sr.UnknownValueError:
#             print("Couldn't understand")
#         except sr.RequestError as e:
#             print(f"Could not request results: {e}")


import sounddevice as sd
import numpy as np
import whisper
import tempfile
import scipy.io.wavfile
import time
import os
import google.generativeai as genai 
# import webrtcvad
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
from dotenv import load_dotenv

# Whisper model
model = whisper.load_model("medium")

# Audio settings
sample_rate = 16000  # 16 kHz for Whisper
chunk_duration = 0.5 # seconds
silence_threshold = 1352.73  # adjust this based on environment
max_silence_duration = 2.0  # seconds

def rms(audio_chunk):
    return np.sqrt(np.mean(np.square(audio_chunk.astype(np.float32))))

def record_until_silence():
    print("Start speaking... (will stop after ~2s of silence)")
    
    recorded_audio = []
    silence_start = None
    start_time = time.time()

    while True:
        chunk = sd.rec(int(chunk_duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()
        volume = rms(chunk)
        recorded_audio.append(chunk)

        if volume < silence_threshold:
            if silence_start is None:
                silence_start = time.time()
            elif time.time() - silence_start >= max_silence_duration:
                print("Silence detected. Stopping recording.")
                break
        else:
            silence_start = None

    audio = np.concatenate(recorded_audio, axis=0)
    return sample_rate, audio

# def record_with_vad(sample_rate=16000, timeout=30, silence_ms=800, pre_roll_ms=500):
#     vad = webrtcvad.Vad(2)  # Aggressiveness: 0–3
#     frame_duration = 30  # ms
#     frame_size = int(sample_rate * frame_duration / 1000)
    
#     silence_limit = int(silence_ms / frame_duration)
#     pre_roll_chunks = int(pre_roll_ms / frame_duration)

#     ring_buffer = collections.deque(maxlen=pre_roll_chunks)  # Holds pre-speech audio
#     audio_buffer = []
    
#     silence_counter = 0
#     speaking = False
#     start_time = time.time()

#     print("Listening...")

#     while True:
#         if time.time() - start_time > timeout:
#             print("⏱ Max time reached.")
#             break

#         chunk = sd.rec(frame_size, samplerate=sample_rate, channels=1, dtype='int16')
#         sd.wait()
#         frame = chunk.tobytes()

#         is_speech = vad.is_speech(frame, sample_rate)

#         if not speaking:
#             ring_buffer.append(chunk)

#         if is_speech:
#             if not speaking:
#                 print("🎙 Speech started.")
#                 speaking = True
#                 audio_buffer.extend(ring_buffer)  # Add pre-roll audio
#                 ring_buffer.clear()
#             audio_buffer.append(chunk)
#             silence_counter = 0
#         else:
#             if speaking:
#                 audio_buffer.append(chunk)
#                 silence_counter += 1
#                 if silence_counter > silence_limit:
#                     print("🤫 End of speech.")
#                     break

def record_for(duration):
    print(f"Listening...")

    total_chunks = int(duration / chunk_duration)
    recorded_audio = []

    for _ in range(total_chunks):
        chunk = sd.rec(int(chunk_duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
        sd.wait()
        recorded_audio.append(chunk)

    audio = np.concatenate(recorded_audio, axis=0)
    return sample_rate, audio



def save_to_wav(fs, audio_data):
    temp_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    scipy.io.wavfile.write(temp_file.name, fs, audio_data)
    return temp_file.name

def transcribe_audio(path):
    result = model.transcribe(path)
    return result["text"]

def measure_ambient_noise(duration=3):
    print(f"Measuring ambient noise for {duration} seconds... Stay quiet!")
    recording = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()
    volume = rms(recording)
    print(f"Ambient RMS volume: {volume:.2f}")
    return volume

def translate(text: str) -> str:
    prompt = (
        f"translate this from whatever language this is to english: {text}\nOnly return the translated text, nothing more, nothing less"
    )
    load_dotenv()
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel("gemini-2.5-flash")
    chat = model.start_chat()
    try: 
        translate = chat.send_message(prompt)
        return translate.text.strip()
    except Exception:
        return text

def record_input_for(duration):
    fs, audio = record_for(duration)
    wav_path = save_to_wav(fs, audio)
    text = transcribe_audio(wav_path)
    return text

# if __name__ == "__main__":

#     # ambient_volume = measure_ambient_noise()
#     # silence_threshold = ambient_volume * 2  # or 2.0, depending on how sensitive you want it
#     # print(f"Using silence threshold: {silence_threshold:.2f}")

#     fs, audio = record_with_vad()
#     # fs, audio = record_for(9)
#     wav_path = save_to_wav(fs, audio)
#     text = transcribe_audio(wav_path)
#     print("Transcription:", text)
#     print("\n")
#     translated = translate(text)
#     print(f"Translation: {translated}")