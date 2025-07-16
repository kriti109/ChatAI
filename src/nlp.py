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



import os, datetime, google.generativeai as genai
from dotenv import load_dotenv
from src.tts import speak

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

os.makedirs("call_logs", exist_ok=True)

# TRANSITIONS = {
# "1.0": ["2.0", "3.0"],
# "2.0": ["2.1", "2.2", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0"],
# "2.1": ["5.0", "7.0", "8.0"],
# "2.2": ["5.0", "7.0", "8.0"],
# "3.0": ["9.0"],
# "4.0": ["9.0"],
# "5.0": ["5.1", "6.0", "9.0"],
# "5.1": ["6.0", "9.0"],
# "6.0": ["6.1", "9.0"],
# "6.1": ["9.0"],
# "7.0": ["7.1", "7.2", "5.0", "8.0", "9.0"],
# "7.1": ["5.0", "3.0", "9.0"],
# "7.2": ["5.0", "8.0", "9.0"],
# "8.0": ["8.1", "8.2", "3.0", "9.0"],
# "8.1": ["5.0", "7.0", "3.0", "9.0"],
# "8.2": ["5.0", "7.0", "3.0", "9.0"],
# "9.0": []
# }

# BATCHES = {
# "1.0": f"Good morning! This is Veena from CareSecure Insurance. Am I speaking to {self.customer_name}, or is someone else available to talk about the policy?",
# "2.0": "Your policy is in discontinuance due to non-payment. Would you like to resume it?",
# "2.1": "Is there a reason you're unsure about continuing? I'm happy to clarify anything before we proceed.",
# "2.2": "Would it help if I explained what restarting your policy would provide?",
# "3.0": "No problem. When would be a convenient time for me to call you back?",
# "4.0": "You can request your policy bond by sending 'BOND' via WhatsApp to 8806727272.",
# "5.0": "Would you like to pay online, via cheque, or request a cash collection?",
# "5.1": "I can send you the payment link on WhatsApp or SMS if that makes it easier.",
# "6.0": "Thanks for the payment! Could you please share the transaction reference or payment date?",
# "6.1": "Great, I'll just verify it. Is there anything else you'd like to check in the meantime?",
# "7.0": "We understand financial issues. We can offer monthly payments or EMI to help continue the policy.",
# "7.1": "Would it help if I paused the policy temporarily instead of canceling it outright?",
# "7.2": "Is there someone in your family who might assist with continuing the plan temporarily?",
# "8.0": "Discontinuing will cancel your life cover and reduce returns. Can I help you reconsider?",
# "8.1": "Would it help if I gave you a quick comparison of benefits if you continue versus discontinue?",
# "8.2": "It is your decision — but you have already built up value. I would love to help you keep that secure.",
# "9.0": "Thank you for your time. Feel free to reach out for help. Have a great day!"
# }

class Conversation:
    def __init__(self):
        self.chat = model.start_chat(history=[])
        self.current_batch = "1.0"
        self.history = []
        self.customer_name = "Alex"     # We can later make this dynamic using certain command arguments or another directory storing names
        self.system_persona = (
            "You are Veena, an empathetic and professional insurance assistant calling on behalf of CareSecure Insurance. "
            "You speak in a warm, concise, easy-to-understand manner. Stay polite, helpful, and gently persuasive when needed. "
            "Always maintain professionalism and encourage the customer to stay informed about their policy. "
            f"You're calling {self.customer_name} to discuss why they didn't pay and if something could be done about it"
        )
        self.TRANSITIONS = {
            """
            Logic branching for how to proceed after taking in the user input, added scenarios so that the conversation is guided
            """
            "1.0": ["2.0", "3.0"], # Proceed or reschedule
            "2.0": ["2.1", "4.0", "5.0", "6.0", "7.0", "8.0", "9.0"],
            "2.1": ["5.0", "7.0", "8.0"],
            "3.0": ["9.0"],
            "4.0": ["9.0"],
            "5.0": ["6.0", "9.0"],
            "6.0": ["9.0"],
            "7.0": ["7.1", "5.0", "9.0"],
            "7.1": ["5.0", "3.0", "9.0"],
            "8.0": ["8.1", "3.0", "9.0"],
            "8.1": ["5.0", "7.0", "3.0", "9.0"],
            "9.0": []
            }

        self.BATCHES = {
            "1.0": f"Good morning! This is Veena from CareSecure Insurance. Am I speaking to {self.customer_name}, or is someone else available to talk about the policy?",
            "2.0": "Your policy is in discontinuance due to non-payment. Would you like to resume it?",
            "2.1": "I understand this might come as a surprise. Are there any concerns you'd like to clarify before we proceed?",
            "3.0": "No problem. When would be a convenient time for me to call you back?",
            "4.0": "You can request your policy bond by sending 'BOND' via WhatsApp to 8806727272.",
            "5.0": "Would you like to pay online, via cheque, or schedule a cash collection?",
            "6.0": "Thanks for the payment! Could you share the transaction reference or payment date for our records?",
            "7.0": "We understand financial challenges. If it helps, we can arrange smaller monthly payments or an EMI option. Would that work for you?",
            "7.1": "We're here to support you. Is there a timeline by which you'd be comfortable resuming the policy?",
            "8.0": "Discontinuing the policy will cancel your life cover and reduce returns. Would you like to reconsider or talk through alternatives?",
            "8.1": "I appreciate your openness. To help you make a better decision, I can explain the benefits again or suggest flexible payment options.",
            "9.0": "Thank you for your time. Feel free to reach out for help anytime. Have a great day!"
        }
    
    def paraphrase(self, text: str) -> str:
        prompt = (
            f"System persona: {self.system_persona}\n"
            f"Paraphrase the following in under 25 words, natural tone:\n\n{text}"
        )
        try:
            response = self.chat.send_message(prompt)
            return response.text.strip()
        except Exception as e:
            return text
    
    def converse_naturally(self, user_input: str, script_line: str) -> str:
        prompt = (
            f"System persona: {self.system_persona}\n"
            f"Current script reply: {script_line}\n"
            f"User just said: {user_input}\n"
            "Reply without deviating from the script reply in a natural, polite, friendly tone — keep the intent the same and tailor it to feel like a smooth continuation of the conversation. Limit to under 30 words."
        )
        try:
            response = self.chat.send_message(prompt)
            return response.text.strip()
        except Exception as e:
            return script_line
        
    def get_next_batch(self, user_input: str) -> str:
        options = self.TRANSITIONS.get(self.current_batch, [])
        if not options:
            "9.0"

        prompt = (
            f"System persona: {self.system_persona}\n"
            f"Current batch: {self.current_batch}\n"
            f"Current context: {self.BATCHES[self.current_batch]}\n"
            f"Possible next batches: {options}\n"
            f"User said: {user_input}\n\n"
            f"Which batch should follow? Reply ONLY with one of: {options}"
        )
        try:
            res = self.chat.send_message(prompt)
            for option in options:
                if option in res.text:
                    return option
        except:
            pass
        return self.current_batch
    
    def summarize_call(self) -> tuple[str, str]:
        conversation = "\n".join(self.history)
        try:
            summary_prompt = f"Summarize the following call transcript in 3 sentences:\n{conversation}"
            conclusion_prompt = f"Based on this call, what decision did the agent and the customer cme to? Keep it short. \n{conversation}"
            summary = model.generate_content(summary_prompt).text.strip()
            conclusion = model.generate_content(conclusion_prompt).text.strip()
            return summary, conclusion
        except Exception:
            return "Summary not available.", "Conclusion not available."
    
    def save_logs(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"call_logs/call_log_{timestamp}.txt"
        summary, conclusion = self.summarize_call()

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"Summary:\n{summary}\n\n")
            f.write(f"Conclusion:\n{conclusion}\n\n")
            f.write(f"Chat History:\n")
            for line in self.history:
                f.write(line + "\n")
        print(f"\n Log saved: {file_path}")

    def start(self):
        opening = self.paraphrase(self.BATCHES[self.current_batch])
        self.history.append(f"ChatAI: {opening}")
        print("ChatAI:", opening)
        speak(opening)

        while True:
            user = input("You: ")
            self.history.append(f"Customer: {user}")
            if user.lower() in {"exit", "quit"}:
                print("ChatAI: Ending the call. Take care!")
                break

            next_batch = self.get_next_batch(user)
            if next_batch == self.current_batch:
                steer = self.converse_naturally(user ,"Could you help me understand better?")
                self.history.append(f"ChatAI: {steer}")
                print("ChatAI: ", steer)
                speak(steer)
                continue
            
            self.current_batch = next_batch
            reply = self.converse_naturally(user ,self.BATCHES[next_batch])
            self.history.append(f"ChatAI: {reply}")
            print("ChatAI:", reply)
            speak(reply)

            if next_batch == "9.0":
                break
        self.save_logs()
