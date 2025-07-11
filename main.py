#from src.stt import transcribeAudio
from src.nlp import generateResponse
from src.tts import speak
#from src.ffmpegConfig import configureFfmpeg

print("ChatAI: Hello! This is Veena from CareSecure Insurance. How can I assist you today?")
speak("Hello! This is Veena from CareSecure Insurance. How can I assist you today?")
while True:
    #only for now it's text, we'll test all connections 
    # and add stt layer over it

    userInput = input("You: ")
    if userInput.lower() in ["exit", "quit"]:
        break
    response = generateResponse(userInput)
    print("ChatAI: ", response)
    speak(response)