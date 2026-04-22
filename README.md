# 🎤 Voice Activated Personal Assistant - JARVIS
### QSkill Internship | Python Development | Slab 2

A professional voice-activated personal assistant built with Python, Flask, SpeechRecognition and pyttsx3. Features a beautiful dark-themed web interface.

---

## 🎯 Project Overview
JARVIS is a voice-activated personal assistant that can answer questions, tell jokes, check weather, read news, set reminders, and search the web — all through voice commands or text input.

---

## 📁 Project Structure
```
voice_assistant/
├── app.py              ← Flask web server
├── assistant.py        ← Core assistant logic
├── requirements.txt    ← Dependencies
├── README.md           ← Documentation
└── templates/
    └── index.html      ← Beautiful dark UI
```

---

## 🚀 How to Run

### 1. Install Dependencies
```bash
pip install flask speechrecognition pyttsx3 requests wikipedia pyaudio
```

### 2. Run the App
```bash
python app.py
```

### 3. Open Browser
```
http://127.0.0.1:5000
```

---

## ✨ Features
- 🎤 Voice Recognition (SpeechRecognition)
- 🔊 Text to Speech (pyttsx3)
- ⏰ Set Reminders (threading)
- 🌤️ Real-time Weather (Open-Meteo API)
- 📰 Latest News Headlines (BBC RSS)
- 📚 Wikipedia Search
- 🌐 Open Websites (YouTube, Google)
- 😂 Tell Jokes
- 💬 Command History
- 🌐 Beautiful Flask Web Interface

---

## 🧠 Technologies Used
| Tool | Purpose |
|---|---|
| Python | Core language |
| Flask | Web framework |
| SpeechRecognition | Voice input |
| pyttsx3 | Text to speech |
| requests | API calls |
| wikipedia | Knowledge search |
| threading | Reminders |
| PyAudio | Microphone access |

---

## 🗣️ Example Commands
- "What is the time?"
- "Tell me the news"
- "What is the weather in Hyderabad?"
- "Tell me a joke"
- "Who is Elon Musk?"
- "Set reminder to drink water in 1 minute"
- "Open YouTube"
- "Search Python tutorials"

---

*QSkill Internship | Python Development Domain | April–May 2026*
