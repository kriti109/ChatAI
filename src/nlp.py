# def generateResponse(text):
#     #only for testing so no actual integration for now
#     if "cupcake" in text.lower():
#         return "I love cupcakes too! They're delicious and fun to decorate."
#     elif "weather" in text.lower():
#         return "The weather is always changing, isn't it? Do you prefer sunny days or rainy ones?"
#     elif "music" in text.lower():
#         return "Music is a universal language! What genre do you enjoy the most?"
#     elif "movies" in text.lower():
#         return "Movies are a great way to tell stories. Do you have a favorite genre or director?"
#     elif "hello" in text.lower():
#         return "Hello! This is Veena from CareSecure Insurance. How can I assist you today?"
#     else:
#         return "I'm not sure how to respond to that. Can you tell me more about what you're interested in?"

# import os
# from openai import OpenAI
# from dotenv import load_dotenv

# load_dotenv()
# client=OpenAI(
#     api_key = os.getenv("OPENAI_API_KEY")
# )

# def generateResponse(text: str) -> str:
#     try:
#         response = client.responses.create(
#             model="gpt-4o", 
#             messages=[
#                 {"role": "system", "content": "You are Veena, an insurance assistant. Reply in short, friendly, easy-to-understand answers. Stay professional and helpful."},
#                 {"role": "user", "content": text}
#             ],
#             max_tokens=100
#         )
#         return response.choices[0].message.content.strip()
#     except Exception as e:
#         return f"Oops! Something went wrong: {e}"

import os
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

model = genai.GenerativeModel("gemini-2.5-flash")

def generateResponse(text: str) -> str:
    try:
        convo = model.start_chat()
        convo.send_message("You are Veena, an insurance assistant. Reply in short, friendly, easy-to-understand answers. Stay professional and helpful.")
        reply = convo.send_message(text)
        return reply.text.strip()
    except Exception as e:
        return f"Oops! Something went wrong: {e}"