# ============================================================
#   assistant.py - Voice Assistant Core
#   QSkill Internship | Python Development | Slab 2
# ============================================================

import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import json
import threading
import time
import requests
import random
import wikipedia
import subprocess

# ============================================================
#   SETUP ENGINE
# ============================================================

engine = pyttsx3.init()

def set_voice():
    voices = engine.getProperty('voices')
    engine.setProperty('rate',   175)
    engine.setProperty('volume', 1.0)
    # Try to set female voice
    for v in voices:
        if 'female' in v.name.lower() or 'zira' in v.name.lower():
            engine.setProperty('voice', v.id)
            break

set_voice()

# ============================================================
#   SPEAK & LISTEN
# ============================================================

def speak(text):
    """Convert text to speech."""
    print(f"🤖 Assistant: {text}")
    engine.say(text)
    engine.runAndWait()


def listen():
    """Listen to microphone and return text."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source, duration=0.5)
        try:
            audio = r.listen(source, timeout=5, phrase_time_limit=10)
        except sr.WaitTimeoutError:
            return ""
    try:
        print("🔍 Recognizing...")
        query = r.recognize_google(audio, language='en-in')
        print(f"👤 You said: {query}")
        return query.lower()
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Please try again.")
        return ""
    except sr.RequestError:
        speak("Speech service is unavailable. Check your internet.")
        return ""


# ============================================================
#   REMINDERS
# ============================================================

reminders = []

def set_reminder(message, seconds):
    """Set a reminder after given seconds."""
    def reminder_thread():
        time.sleep(seconds)
        speak(f"Reminder: {message}")
        print(f"⏰ REMINDER: {message}")
    t = threading.Thread(target=reminder_thread, daemon=True)
    t.start()
    reminders.append({'message': message, 'seconds': seconds,
                       'time': datetime.datetime.now().strftime('%H:%M:%S')})


# ============================================================
#   WEATHER
# ============================================================

def get_weather(city="Hyderabad"):
    """Get weather using Open-Meteo (free, no API key needed)."""
    try:
        # Get coordinates
        geo_url = f"https://geocoding-api.open-meteo.com/v1/search?name={city}&count=1"
        geo     = requests.get(geo_url, timeout=5).json()
        if not geo.get('results'):
            return f"Sorry, I couldn't find weather for {city}."
        lat  = geo['results'][0]['latitude']
        lon  = geo['results'][0]['longitude']

        # Get weather
        w_url = (f"https://api.open-meteo.com/v1/forecast?"
                 f"latitude={lat}&longitude={lon}"
                 f"&current=temperature_2m,weathercode,windspeed_10m"
                 f"&temperature_unit=celsius")
        w = requests.get(w_url, timeout=5).json()['current']

        temp      = w['temperature_2m']
        windspeed = w['windspeed_10m']
        code      = w['weathercode']

        conditions = {
            0: 'Clear sky', 1: 'Mainly clear', 2: 'Partly cloudy',
            3: 'Overcast', 45: 'Foggy', 61: 'Light rain',
            63: 'Moderate rain', 80: 'Rain showers', 95: 'Thunderstorm'
        }
        condition = conditions.get(code, 'Variable conditions')

        result = (f"Weather in {city}: {condition}. "
                  f"Temperature is {temp}°C with wind speed {windspeed} km/h.")
        return result
    except Exception as e:
        return f"Sorry, I couldn't fetch weather right now."


# ============================================================
#   NEWS
# ============================================================

def get_news():
    """Get top headlines using RSS (no API key needed)."""
    try:
        url  = "https://feeds.bbci.co.uk/news/rss.xml"
        res  = requests.get(url, timeout=5)
        import xml.etree.ElementTree as ET
        root = ET.fromstring(res.content)
        items = root.findall('.//item')[:5]
        headlines = []
        for item in items:
            title = item.find('title')
            if title is not None:
                headlines.append(title.text)
        if headlines:
            news_text = "Here are today's top headlines. " + ". ".join(headlines[:3])
            return news_text
        return "Sorry, couldn't fetch news right now."
    except:
        return "Sorry, news service is unavailable."


# ============================================================
#   WIKIPEDIA
# ============================================================

def search_wikipedia(query):
    try:
        result = wikipedia.summary(query, sentences=2)
        return result
    except wikipedia.exceptions.DisambiguationError as e:
        return f"Multiple results found. Please be more specific."
    except:
        return f"Sorry, I couldn't find information about {query}."


# ============================================================
#   JOKES
# ============================================================

jokes = [
    "Why do programmers prefer dark mode? Because light attracts bugs!",
    "Why did the Python programmer wear glasses? Because they couldn't C!",
    "How many programmers does it take to change a light bulb? None, that's a hardware problem!",
    "Why do Java developers wear glasses? Because they don't C sharp!",
    "What is a computer's favorite snack? Microchips!"
]

def tell_joke():
    return random.choice(jokes)


# ============================================================
#   COMMAND PROCESSOR
# ============================================================

def process_command(query):
    """Process voice command and return response."""
    query = query.lower().strip()

    if not query:
        return "I didn't hear anything. Please try again."

    # ── Greetings ────────────────────────────────────────────
    if any(w in query for w in ['hello', 'hi', 'hey', 'good morning', 'good evening']):
        hour = datetime.datetime.now().hour
        if hour < 12:   greeting = "Good morning"
        elif hour < 17: greeting = "Good afternoon"
        else:           greeting = "Good evening"
        response = f"{greeting}! I'm your personal assistant. How can I help you?"

    # ── Time ─────────────────────────────────────────────────
    elif 'time' in query:
        now = datetime.datetime.now().strftime('%I:%M %p')
        response = f"The current time is {now}."

    # ── Date ─────────────────────────────────────────────────
    elif 'date' in query or 'today' in query:
        today = datetime.datetime.now().strftime('%A, %B %d, %Y')
        response = f"Today is {today}."

    # ── Weather ──────────────────────────────────────────────
    elif 'weather' in query:
        city = 'Hyderabad'
        for word in ['in', 'at', 'for']:
            if word in query:
                parts = query.split(word)
                if len(parts) > 1:
                    city = parts[-1].strip().title()
                    break
        response = get_weather(city)

    # ── News ─────────────────────────────────────────────────
    elif 'news' in query or 'headlines' in query:
        response = get_news()

    # ── Reminder ─────────────────────────────────────────────
    elif 'remind' in query or 'reminder' in query:
        try:
            # e.g. "remind me to drink water in 10 seconds"
            parts = query.split('in')
            msg   = parts[0].replace('remind me to', '').replace('set reminder', '').strip()
            time_part = parts[-1].strip()
            secs  = 60  # default 1 minute
            if 'second' in time_part:
                secs = int(''.join(filter(str.isdigit, time_part)) or 10)
            elif 'minute' in time_part:
                mins = int(''.join(filter(str.isdigit, time_part)) or 1)
                secs = mins * 60
            elif 'hour' in time_part:
                hrs  = int(''.join(filter(str.isdigit, time_part)) or 1)
                secs = hrs * 3600
            set_reminder(msg or "Task reminder", secs)
            response = f"Reminder set for {msg} in {secs} seconds!"
        except:
            response = "Sorry, I couldn't set the reminder. Try: remind me to drink water in 1 minute."

    # ── Wikipedia ────────────────────────────────────────────
    elif 'who is' in query or 'what is' in query or 'tell me about' in query:
        search_query = (query.replace('who is', '')
                             .replace('what is', '')
                             .replace('tell me about', '').strip())
        response = search_wikipedia(search_query)

    # ── Open websites ────────────────────────────────────────
    elif 'open youtube' in query:
        webbrowser.open('https://youtube.com')
        response = "Opening YouTube!"

    elif 'open google' in query:
        webbrowser.open('https://google.com')
        response = "Opening Google!"

    elif 'search' in query:
        search_query = query.replace('search', '').strip()
        webbrowser.open(f'https://www.google.com/search?q={search_query}')
        response = f"Searching for {search_query} on Google!"

    # ── Joke ─────────────────────────────────────────────────
    elif 'joke' in query or 'funny' in query:
        response = tell_joke()

    # ── Name ─────────────────────────────────────────────────
    elif 'your name' in query or 'who are you' in query:
        response = "I am Jarvis, your personal Python voice assistant built for QSkill internship!"

    # ── Thanks ───────────────────────────────────────────────
    elif 'thank' in query:
        response = "You're welcome! Is there anything else I can help you with?"

    # ── Stop ─────────────────────────────────────────────────
    elif any(w in query for w in ['bye', 'exit', 'quit', 'stop', 'goodbye']):
        response = "Goodbye! Have a great day!"

    # ── Default ──────────────────────────────────────────────
    else:
        webbrowser.open(f'https://www.google.com/search?q={query}')
        response = f"I searched Google for: {query}"

    return response


# ============================================================
#   MAIN LOOP (Terminal Mode)
# ============================================================

if __name__ == "__main__":
    print("=" * 55)
    print("  🤖 JARVIS - Voice Assistant")
    print("  QSkill Internship | Python Development")
    print("=" * 55)
    speak("Hello! I am Jarvis, your personal assistant. How can I help you?")

    while True:
        query = listen()
        if not query:
            continue
        response = process_command(query)
        speak(response)
        if any(w in query for w in ['bye', 'exit', 'quit', 'stop', 'goodbye']):
            break
