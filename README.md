# ChatAI : Veena

<aside>
<img src="https://www.notion.so/icons/token_blue.svg" alt="https://www.notion.so/icons/token_blue.svg" width="40px" /> **Team Vision: To build a truly human-like voice assistant that empowers every Indian insurance customer with seamless, empathetic, and informed conversations — bridging the gap between technology and trust.**

</aside>

<aside>
<img src="https://www.notion.so/icons/flag_blue.svg" alt="https://www.notion.so/icons/flag_blue.svg" width="40px" /> **Team Mission:**  To build *Veena*, a voice-based insurance assistant that listens, understands, and responds like a real human — using real-time speech and language AI to deliver fast, empathetic, and accurate support for insurance queries.

</aside>

# Team

| Name | Role |
| --- | --- |
| Snehil Gautam | Core Member |
| Kriti Agarwal | Core Member |
| Vedanta Meena | Core Member |

# 🔄 End-to-End Workflow:

- **🎤 User speaks** via mic
- **📝 Whisper** transcribes it to text in real time
- **🤖 Gemini NLP (Conversation class)** processes the text and generates a context-aware response
- **🗣️ ElevenLabs TTS** converts the response into human-like speech
- **🔊 Response is played back**, continuing the conversation loop

# 📊 **Performance Metrics:**

- **Latency (end-to-end response time between two inputs):** ~ 23 seconds
- **Transcription accuracy (Whisper):** ~98% for clean audio
- **Conversation continuity score:** Smooth transitions via batch-based flow even in disturbing noise behind.
- **Voice naturalness (ElevenLabs):** Rated 4.1/5 in informal user testing
- **Interrupt handling:** Currently under improvement; partial detection in place

# 🔗 **Audit / Test Links:**

- 🔍 **Code Repository:** https://github.com/kriti109/ChatAI
- 🎥 **Demo Video:** https://drive.google.com/file/d/1BvuaTbcbAqWRYh8U8wgUECt-g3YssUFJ/view?usp=sharing

## 📬 **Contact Us:**

- **Kriti Agarwal**
    
    ✉️ Email: kriti.agarwal109@gmail.com
    
    🔗 LinkedIn: [https://www.linkedin.com/in/kriti-agarwal-039576363/](https://www.linkedin.com/in/kriti-agarwal-039576363/)
    
- Snehil Gautam
    
    ✉️ Email: serpentmillers429@gmail.com
    
    🔗 LinkedIn:  [https://www.linkedin.com/in/snehil-gautam-198347318/](https://www.linkedin.com/in/snehil-gautam-198347318/)
    
- **Teammate 3 Name**
    
    ✉️ Email: [vedantmeena826@gmail.com](mailto:vedantmeena826@gmail.com)
    
    🔗 LinkedIn: [https://www.linkedin.com/in/vedanta-meena-289581331/](https://www.linkedin.com/in/vedanta-meena-289581331/)
    

# 🧰 Tools & Technologies Used – *Project Veena*

### 

### 🎙️ 1. **Speech-to-Text (STT): [Whisper by OpenAI]**

- **Role**: Converts live user speech to text.
- **Why Whisper?**: Whisper provides high accuracy, supports multiple languages, and handles various accents well — ideal for realistic insurance conversations.
- **Integration**: Used with live microphone input to continuously transcribe spoken input from the customer in real time.

---

### **2. Project Structure Overview:**

```
📦 ChatAI/

├── 📁 src/
│   ├── stt.py               # Mic input, Whisper-based STT
│   ├── tts.py               # ElevenLabs voice generation
│   ├── nlp.py               # Conversation class and Gemini                                                         logic
│   ├── ffmpegConfig.py      # FFmpeg setup and handling config
├── main.py                  # Central entry point: STT → NLP                                                          → TTS
├── .env                     # API keys for Gemini & ElevenLabs
├── requirements.txt         # All dependencies

```

---

### 🧠 3. **Natural Language Processing (NLP): [Gemini API via Google Generative AI]**

- **Role**: Handles dialogue logic and personalized replies.
- **What it does**:
    - Interprets the user’s message
    - Selects the next appropriate scripted batch
    - Paraphrases or responds naturally using the company’s tone/persona
- **Integration**: Once Whisper provides the transcribed input, this component generates an appropriate agent response using a batch-transition-based dialogue engine.

---

### 🔁 4. **Dialogue Engine: [Custom Conversation Class]**

- **Role**: Manages scripted transitions and conversational flow.
- **Features**:
    - Follows a decision-tree-style script
    - Uses the `current_batch` to determine what to say next
    - Maintains chat history and uses it for summarization and follow-ups

---

### 🔊 5. **Text-to-Speech (TTS): [ElevenLabs API]**

- **Role**: Converts the bot’s text response into natural-sounding speech.
- **Why ElevenLabs?**: Known for ultra-realistic and emotionally expressive voices — perfect for sounding like a real insurance agent.
- **Integration**: Response from the NLP is converted into audio and played back in real time, completing the voice loop.

---

### 🧪 6. **Testing & Simulation:**

- **Microphone Input**: Used for live testing of user speech
- **Test Scripts & Call Recordings**: Used to simulate real user behavior and evaluate robustness
- **Latency Measurement**: Tracked from mic input to bot response generation

---

### Instructions to Run

```bash
git clone https://github.com/kriti109/ChatAI/
cd ChatAI
python -m venv .venv
source .venv/bin/activate
# Or if on windows:
.venv\Scripts\activate.bat
pip install -r requirements.txt
```

make a .env file in the root directory and put these values in
```
ELEVENLABS_API_KEY=your_elevenlabs_api_key_here
OPENAI_API_KEY=your_openai_api_key_here
```
