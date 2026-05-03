import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import urllib.parse
import pyautogui
import requests
import threading
import time
import random
from datetime import datetime

# 🔊 Voice engine
engine = pyttsx3.init()
engine.setProperty('rate', 170)

def speak(text):
    print("Jarvis:", text)
    engine.say(text)
    engine.runAndWait()

# 🎤 Listen
def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio)
        print("You:", command)
        return command.lower()
    except:
        return ""

# 🎭 Greeting
def greet():
    hour = datetime.now().hour

    if 5 <= hour < 12:
        speak(random.choice(["Good morning Irfan", "Morning boss"]))
    elif 12 <= hour < 17:
        speak("Good afternoon Irfan")
    elif 17 <= hour < 21:
        speak("Good evening Irfan")
    else:
        speak("Good night Irfan")

# 👋 Goodbye
def goodbye():
    hour = datetime.now().hour

    if 5 <= hour < 21:
        speak("Goodbye Irfan")
    else:
        speak("Good night Irfan")

# 🕌 Prayer time fetch
def get_prayer_times():
    url = "http://api.aladhan.com/v1/timingsByCity"
    params = {"city": "Kozhikode", "country": "India", "method": 5}
    data = requests.get(url, params=params).json()
    return data["data"]["timings"]

# 🔊 Adhan
def play_adhan(prayer):
    speak(f"Sir, may I remind you it's time for {prayer} prayer")
    os.system("mpg123 adhan.mp3")

# ⏰ Prayer checker
def check_prayer_times():
    timings = get_prayer_times()
    played = []

    while True:
        now = datetime.now().strftime("%H:%M")

        for prayer, t in timings.items():
            if now == t and prayer not in played:
                play_adhan(prayer)
                played.append(prayer)

        time.sleep(30)

# ⚡ MAIN CONTROL
def process(command):
    if not command:
        return

    # OPEN APPS
    if command.startswith("open"):
        app = command.replace("open", "").strip()

        if "youtube" in app:
            webbrowser.open("https://youtube.com")
        elif "google" in app:
            webbrowser.open("https://google.com")
        else:
            os.system(f"{app} &")

        speak(f"Opening {app}")

    # SEARCH
    elif "search" in command:
        query = command.replace("search", "").strip()
        url = "https://google.com/search?q=" + urllib.parse.quote(query)
        webbrowser.open(url)
        speak("Searching")

    # PLAY YOUTUBE
    elif "play" in command:
        query = command.replace("play", "").strip()
        url = "https://youtube.com/results?search_query=" + urllib.parse.quote(query)
        webbrowser.open(url)

    # VOLUME
    elif "volume up" in command:
        os.system("amixer -D pulse sset Master 10%+")
    elif "volume down" in command:
        os.system("amixer -D pulse sset Master 10%-")

    # BRIGHTNESS
    elif "brightness up" in command:
        os.system("brightnessctl set +10%")
    elif "brightness down" in command:
        os.system("brightnessctl set 10%-")

    # MOUSE
    elif "click" in command:
        pyautogui.click()
    elif "scroll down" in command:
        pyautogui.scroll(-500)
    elif "scroll up" in command:
        pyautogui.scroll(500)

    # TYPE
    elif "type" in command:
        text = command.replace("type", "").strip()
        pyautogui.write(text)

    # KEYS
    elif "press enter" in command:
        pyautogui.press("enter")
    elif "close window" in command:
        pyautogui.hotkey("alt", "f4")

    # SCREENSHOT
    elif "screenshot" in command:
        img = pyautogui.screenshot()
        img.save("screenshot.png")
        speak("Screenshot taken")

    # JOKE 😄
    elif "joke" in command:
        jokes = [
            "Why do programmers hate nature? Too many bugs.",
            "Linux users don’t die… they just get kernel panic.",
            "I am not lazy, I am on energy saving mode."
        ]
        speak(random.choice(jokes))

    # EXIT
    elif "exit" in command:
        goodbye()
        exit()

    else:
        speak("Command not recognized")

# 🚀 START
greet()

# Run prayer system in background
threading.Thread(target=check_prayer_times, daemon=True).start()

# MAIN LOOP
while True:
    cmd = listen()
    process(cmd)
