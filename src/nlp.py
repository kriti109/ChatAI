import os, datetime, google.generativeai as genai
from dotenv import load_dotenv
from src.tts import speak

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

os.makedirs("call_logs", exist_ok=True)

class Conversation:
    def __init__(self):
        self.chat = model.start_chat(history=[])
        self.current_batch = "1.0"
        self.history = []
        self.customer_name = "Alex"
        self.system_persona = (
            "You are Veena, an empathetic and professional insurance assistant calling on behalf of CareSecure Insurance. "
            "You speak in a warm, concise, easy-to-understand manner. Stay polite, helpful, and gently persuasive when needed. "
            "Always maintain professionalism and encourage the customer to stay informed about and continue their policy. "
            f"You're calling {self.customer_name} to discuss why they didn't pay and if something could be done about it"
        )
        self.TRANSITIONS = {
            "1.0": ["2.0", "3.0"],
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
            "1.0": (
                  "Hello and very Good Morning Sir, May I speak with Alex?\n"
                  "My name is Veena and I am an Executive calling on behalf of ValuEnable Life Insurance Co. Ltd. "
                  "This is a service call with regards to your life insurance policy. "
                "Is this the right time to speak to you regarding the renewal of your policy?"
             ),
              "2.0": (
                  "Let me start by confirming your policy details. Your policy is ValuEnable Life Secure Plan, insurance policy number 65892147, started on 25th September 2019, and you've paid ₹4,00,000 so far."
                  "The premium of ₹1,00,000 due on 25th September 2024 is still pending, and your policy is currently in “Discontinuance” status, with no life insurance cover. Could you please let me know why you haven’t been able to pay the premium?"
             ),
                   
             "2.1": (
                  "I would like to inform you that the due date for renewal premium payment for your policy was on 25th September 2024. The grace period is over due to non-payment of the regular premium and you are losing the benefit of your plan. "
                  "Would you like to know what your policy's benefits you could get if you resume paying premiums?"
             ),
             "3.0": (
                  "When would be a convenient time to call you again to provide the information about your policy with us? Please can you give a time and date?Thank you sir/ma’am, I will arrange your call back at the given time."
                  
             ),
             "4.0": (
                 "You can download the policy bond through WhatsApp. "
                   "Please send a message from your registered mobile number on 8806727272 and you will be able to download the policy bond."
             ),
             "5.0": (
                 "May I know how you plan to make the payment? Will it be via cash, cheque, or online?\n"
                 "If you wish, you can pay online now. We’ll send you a link, or you can visit our website. "
                 "You can use Debit card, Credit card, Net banking, PhonePe, WhatsApp or Google Pay to make the payment.\n"
                  "You can conveniently pay the premium from home without visiting the branch. I’m here to assist you with the digital payment process.\n"
                 "I’m noting your preference. I’ll send you a payment link for easy processing.\n"
                 "As confirmed, you’ll pay the premium on 25th September 2024 at 10:00 AM via online transfer. "
                 "Please ensure timely payment to maintain your policy benefits. We’ll call to confirm the payment status."
             ),
             "6.0": (
                  "Thank you for making the payment. May I know when you made the payment?\n"
                  "May I know where you made the payment (e.g., online, cheque, or cash)?\n"
                 "Could you please provide the transaction ID or reference ID? For cheque payments, we’ll need the cheque number. "
                 "I can assist with further tracking if needed."
             ),
             "7.0": (
                 "I understand your concern. To achieve your financial goals, staying invested is key. "
                 "You can pay via credit card, EMI, or change your payment mode to monthly. "
                 "Can you arrange the premium to continue benefits?"
             ),
             "7.1": (
                 "Would it help if I explain the flexible payment options again or tell you when we can follow up next?"
             ),
             "8.0": (
                 "You can opt for the Partial Withdrawal option after completing 5 years of the policy i.e., lock-in period. "
                 "If premiums stop before the lock-in ends, the policy will discontinue and growth will be limited to 4–4.5% returns. "
                   "You will lose your life cover of ₹10,00,000. If you continue with this policy till maturity, you will receive ₹5,53,089. "
                  "Would you be willing to pay your premium now?"
             ),
             "8.1": (
                 "I’ll update the details in our CRM."
             ),
             "9.0": (
                 "For any further assistance with your policy, feel free to call our helpline at 1800 209 7272, "
                 "message us on WhatsApp at 8806 727272, mail us, or visit our website. "
                 "Thank you for your valuable time. Have a great day ahead."
             )
         }


    def paraphrase(self, text: str) -> str:
        prompt = (
            f"System persona: {self.system_persona}\n"
            f"Paraphrase the following in whatever language the user prefers:\n\n{text}"
        )
        try:
            response = self.chat.send_message(prompt)
            return response.text.strip()
        except Exception:
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
        except Exception:
            return script_line

    def get_next_batch(self, user_input: str) -> str:
        options = self.TRANSITIONS.get(self.current_batch, [])
        if not options:
            return "9.0"
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
            conclusion_prompt = f"Based on this call, what decision did the agent and the customer come to? Keep it short. \n{conversation}"
            summary = model.generate_content(summary_prompt).text.strip()
            conclusion = model.generate_content(conclusion_prompt).text.strip()
            return summary, conclusion
        except Exception:
            return "Summary not available.", "Conclusion not available."

        '''def save_logs(self):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        file_path = f"call_logs/call_log_{timestamp}.txt"
        summary, conclusion = self.summarize_call()

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(f"Summary:\n{summary}\n\n")
            f.write(f"Conclusion:\n{conclusion}\n\n")
            f.write(f"Chat History:\n")
            for line in self.history:
                f.write(line + "\n")
        print(f"\nLog saved: {file_path}")'''

    def start(self):
        if self.current_batch == "1.0":
            opening = f"Hello and very Good Morning Sir, May I speak with {self.customer_name}?"
        else:
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

            # Check if someone else is speaking
            if "not alex" in user.lower():
                user_lower = user.lower()
                if any(word in user_lower for word in ["son", "daughter", "kid", "child", "i am his son", "i am his daughter", "this is his kid"]):
                    response = "Hi there! Could you tell me when would be a good time to speak with your father?"
                    self.history.append(f"ChatAI: {response}")
                    print("ChatAI:", response)
                    speak(response)
        
                    user = input("You: ")
                    self.history.append(f"Customer: {user}")
        
                    # Close the call
                    closing = self.BATCHES["9.0"]
                    self.history.append(f"ChatAI: {closing}")
                    print("ChatAI:", closing)
                    speak(closing)
                    break

                else:
                    response = "Oh, are you available to talk about the policy?"
                    self.history.append(f"ChatAI: {response}")
                    print("ChatAI:", response)
                    speak(response)

                    # Transition directly to payment batch
                    self.current_batch = "5.0"
                    payment_msg = self.converse_naturally(user, self.BATCHES["5.0"])
                    self.history.append(f"ChatAI: {payment_msg}")
                    print("ChatAI:", payment_msg)
                    speak(payment_msg)
                    continue

            next_batch = self.get_next_batch(user)
            if next_batch == self.current_batch:
                steer = self.converse_naturally(user, "Could you help me understand better?")
                self.history.append(f"ChatAI: {steer}")
                print("ChatAI: ", steer)
                speak(steer)
                continue

            self.current_batch = next_batch
            reply = self.converse_naturally(user, self.BATCHES[next_batch])
            self.history.append(f"ChatAI: {reply}")
            print("ChatAI:", reply)
            speak(reply)

            if next_batch == "9.0":
                break

        'self.save_logs()'  

'''
import os, datetime, google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel("gemini-2.5-flash")

os.makedirs("call_logs", exist_ok=True)

class Conversation:
    def __init__(self):
        self.chat = model.start_chat(history=[])
        self.current_batch = "1.0"
        self.history = []
        self.customer_name = "Alex"
        self.system_persona = (
            "You are Veena, an empathetic and professional insurance assistant calling on behalf of CareSecure Insurance. "
            "You speak in a warm, concise, easy-to-understand manner. Stay polite, helpful, and gently persuasive when needed. "
            "Always maintain professionalism and encourage the customer to stay informed about and continue their policy. "
            f"You're calling {self.customer_name} to discuss why they didn't pay and if something could be done about it"
        )
        self.TRANSITIONS = {
            "1.0": ["2.0", "3.0"],
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
            "1.0": (
                "Hello and very Good Morning Sir, May I speak with Alex?\n"
                "My name is Veena and I am an Executive calling on behalf of ValuEnable Life Insurance Co. Ltd. "
                "This is a service call with regards to your life insurance policy. "
                "Is this the right time to speak to you regarding the renewal of your policy?"
            ),
            "2.0": (
                "Let me start by confirming your policy details. Your policy is ValuEnable Life Secure Plan, insurance policy number 65892147, "
                "started on 25th September 2019, and you've paid ₹4,00,000 so far. "
                "The premium of ₹1,00,000 due on 25th September 2024 is still pending, and your policy is currently in “Discontinuance” status, "
                "with no life insurance cover. Could you please let me know why you haven’t been able to pay the premium?"
            ),
            "2.1": (
                "I would like to inform you that the due date for renewal premium payment for your policy was on 25th September 2024. "
                "The grace period is over due to non-payment of the regular premium and you are losing the benefit of your plan. "
                "Would you like to know what your policy's benefits you could get if you resume paying premiums?"
            ),
            "3.0": (
                "When would be a convenient time to call you again to provide the information about your policy with us? "
                "Please can you give a time and date? Thank you sir/ma’am, I will arrange your call back at the given time."
            ),
            "4.0": (
                "You can download the policy bond through WhatsApp. "
                "Please send a message from your registered mobile number on 8806727272 and you will be able to download the policy bond."
            ),
            "5.0": (
                "May I know how you plan to make the payment? Will it be via cash, cheque, or online?\n"
                "If you wish, you can pay online now. We’ll send you a link, or you can visit our website. "
                "You can use Debit card, Credit card, Net banking, PhonePe, WhatsApp or Google Pay to make the payment.\n"
                "You can conveniently pay the premium from home without visiting the branch. I’m here to assist you with the digital payment process.\n"
                "I’m noting your preference. I’ll send you a payment link for easy processing.\n"
                "As confirmed, you’ll pay the premium on 25th September 2024 at 10:00 AM via online transfer. "
                "Please ensure timely payment to maintain your policy benefits. We’ll call to confirm the payment status."
            ),
            "6.0": (
                "Thank you for making the payment. May I know when you made the payment?\n"
                "May I know where you made the payment (e.g., online, cheque, or cash)?\n"
                "Could you please provide the transaction ID or reference ID? For cheque payments, we’ll need the cheque number. "
                "I can assist with further tracking if needed."
            ),
            "7.0": (
                "I understand your concern. To achieve your financial goals, staying invested is key. "
                "You can pay via credit card, EMI, or change your payment mode to monthly. "
                "Can you arrange the premium to continue benefits?"
            ),
            "7.1": (
                "Would it help if I explain the flexible payment options again or tell you when we can follow up next?"
            ),
            "8.0": (
                "You can opt for the Partial Withdrawal option after completing 5 years of the policy i.e., lock-in period. "
                "If premiums stop before the lock-in ends, the policy will discontinue and growth will be limited to 4–4.5% returns. "
                "You will lose your life cover of ₹10,00,000. If you continue with this policy till maturity, you will receive ₹5,53,089. "
                "Would you be willing to pay your premium now?"
            ),
            "8.1": (
                "I’ll update the details in our CRM."
            ),
            "9.0": (
                "For any further assistance with your policy, feel free to call our helpline at 1800 209 7272, "
                "message us on WhatsApp at 8806 727272, mail us, or visit our website. "
                "Thank you for your valuable time. Have a great day ahead."
            )
        }

    def paraphrase(self, text: str) -> str:
        prompt = (
            f"System persona: {self.system_persona}\n"
            f"Paraphrase the following in whatever language the user prefers:\n\n{text}"
        )
        try:
            response = self.chat.send_message(prompt)
            return response.text.strip()
        except Exception:
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
        except Exception:
            return script_line

    def get_next_batch(self, user_input: str) -> str:
        options = self.TRANSITIONS.get(self.current_batch, [])
        if not options:
            return "9.0"
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
            conclusion_prompt = f"Based on this call, what decision did the agent and the customer come to? Keep it short. \n{conversation}"
            summary = model.generate_content(summary_prompt).text.strip()
            conclusion = model.generate_content(conclusion_prompt).text.strip()
            return summary, conclusion
        except Exception:
            return "Summary not available.", "Conclusion not available."

    def start(self):
        if self.current_batch == "1.0":
            opening = f"Hello and very Good Morning Sir, May I speak with {self.customer_name}?"
        else:
            opening = self.paraphrase(self.BATCHES[self.current_batch])
        self.history.append(f"ChatAI: {opening}")
        print("ChatAI:", opening)

        while True:
            user = input("You: ")
            self.history.append(f"Customer: {user}")

            if user.lower() in {"exit", "quit"}:
                print("ChatAI: Ending the call. Take care!")
                break

            # ✅ Fixed Child Detection Block
            if "not alex" in user.lower():
                user_lower = user.lower()
                if any(word in user_lower for word in ["son", "daughter", "kid", "child", "i am his son", "i am his daughter", "this is his kid"]):
                    response = (
                        "Thank you. Could you please tell your father this is Veena from CareSecure Insurance? "
                        "His premium is pending and his policy is in discontinuance. I’ll call back later."
                    )
                    self.history.append(f"ChatAI: {response}")
                    print("ChatAI:", response)

                    closing = self.BATCHES["9.0"]
                    self.history.append(f"ChatAI: {closing}")
                    print("ChatAI:", closing)
                    break
                else:
                    response = "Oh, are you available to talk about the policy?"
                    self.history.append(f"ChatAI: {response}")
                    print("ChatAI:", response)

                    self.current_batch = "5.0"
                    payment_msg = self.converse_naturally(user, self.BATCHES["5.0"])
                    self.history.append(f"ChatAI: {payment_msg}")
                    print("ChatAI:", payment_msg)
                    continue

            next_batch = self.get_next_batch(user)
            if next_batch == self.current_batch:
                steer = self.converse_naturally(user, "Could you help me understand better?")
                self.history.append(f"ChatAI: {steer}")
                print("ChatAI: ", steer)
                continue

            self.current_batch = next_batch
            reply = self.converse_naturally(user, self.BATCHES[next_batch])
            self.history.append(f"ChatAI: {reply}")
            print("ChatAI:", reply)

            if next_batch == "9.0":
                break'''
