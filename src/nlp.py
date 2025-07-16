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



import os, re, google.generativeai as genai
from dotenv import load_dotenv
from src.tts import speak

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

TRANSITIONS = {
    "1.0": {              # Greeting
        "agree_to_talk"  : "2.0",
        "busy"           : "3.0",
        "relationship"   : "2.0",  # after relation check
    },
    "2.0": {              # Policy confirmation
        "agree_pay"      : "5.0",
        "already_paid"   : "6.0",
        "no_bond"        : "4.0",
        "financial_issue": "7.0",
        "objection"      : "8.0",
    },
    "3.0": {              # Callback scheduling
        "done"           : "9.0",
    },
    "4.0": {              # Bond download
        "done"           : "9.0",
    },
    "5.0": {              # Payment follow‑up
        "done"           : "9.0",
    },
    "6.0": {              # Payment already made
        "done"           : "9.0",
    },
    "7.0": {              # Financial problem
        "done"           : "9.0",
    },
    "8.0": {              # Rebuttal
        "callback"       : "3.0",
        "done"           : "9.0",
    },
}

INTENT_LABELS = {
    "agree_to_talk"  : r"\b(yes|sure|ok|go ahead)\b",
    "busy"           : r"\b(busy|later|not now)\b",
    "relationship"   : r"\b(friend|spouse|son|daughter)\b",
    "agree_pay"      : r"\b(will pay|pay now|link|online)\b",
    "already_paid"   : r"\b(already paid|have paid)\b",
    "no_bond"        : r"\b(bond|document|lost)\b",
    "financial_issue": r"\b(no money|can.t pay|financial)\b",
    "objection"      : r"\b(not interested|cancel|stop)\b",
    "callback"       : r"\b(call back|later)\b",
    "done"           : r"\b(thanks|bye|goodbye)\b"
}

BATCHES = {
    "1.0": "Hello and good morning! May I speak with you regarding your CareSecure Insurance policy?",
    "2.0": "Your policy is in discontinuance due to non-payment. Would you like to resume it?",
    "3.0": "No problem. When would be a convenient time for me to call you back?",
    "4.0": "You can request your policy bond by sending 'BOND' via WhatsApp to 8806727272.",
    "5.0": "Would you like to pay online, via cheque, or cash collection?",
    "6.0": "Thanks for the payment! Could you share the transaction reference or payment date?",
    "7.0": "We understand financial issues. We can offer monthly payments or EMI to help continue the policy.",
    "8.0": "Discontinuing will cancel your life cover and reduce returns. Can I help you reconsider?",
    "9.0": "Thank you for your time. Feel free to reach out for help. Have a great day!"
}


# def generateResponse(text: str) -> str:
#     try:
#         convo = model.start_chat()
#         convo.send_message("You are Veena, an insurance assistant. Reply in short, friendly, easy-to-understand answers. Stay professional and helpful.")
#         reply = convo.send_message(text)
#         return reply.text.strip()
#     except Exception as e:
#         return f"Oops! Something went wrong: {e}"


class Conversation:
    def __init__(self):
        self.chat = model.start_chat()
        self.current_batch=1.0

    def classify_intent(self, user_input: str) -> str:
        user_input = user_input.lower()
        for label, pattern in INTENT_LABELS.items():
            if re.search(pattern, user_input):
                return label
        return "unknown"
    
    def paraphrase(self, text: str) -> str:
        prompt = f"Paraphrase this naturally in under 30 words:\n {text}"
        try:
            response = self.chat.send_message(prompt)
            return response.text.strip()
        except Exception as e:
            return text
        
    def start(self):
        print("ChatAI:", self.paraphrase(BATCHES["1.0"]))
        speak(self.paraphrase(BATCHES["1.0"]))

        while True:
            user=input("You: ")
            if user.lower() in {"exit", "quit"}:
                print("ChatAI: Ending the call. Take care!")
                break

            intent = self.classify_intent(user)
            next_batch = TRANSITIONS.get(self.current_batch, {}).get(intent)

            if not next_batch:
                steer = self.paraphrase("Could you please clarify so I can assists you better?")            
                print("ChatAI:", steer)
                speak(steer)
                continue

            self.current_batch = next_batch
            reply=self.paraphrase(BATCHES[next_batch])
            print("ChatAI:", reply)
            speak(reply)

            if next_batch == "9.0":
                break