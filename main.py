import os
from src.nlp import Conversation
#from src.ffmpegConfig import configureFfmpeg

# print("ChatAI: Hello! This is Veena from CareSecure Insurance. How can I assist you today?")
# speak("Hello! This is Veena from CareSecure Insurance. How can I assist you today?")

# while True:
    #only for now it's text, we'll test all connections 
    # hopefully this works 
    # and add stt layer over it

    # userInput = input("You: ")
    # if userInput.lower() in ["exit", "quit"]:
    #     break
    # response = generateResponse(userInput)
    # print("ChatAI: ", response)
    # speak(response)

os.environ["ALSA_LOGLEVEL"] = "none"

def chat():
    session = Conversation()
    session.start()

if __name__ == "__main__":
    chat()
