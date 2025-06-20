# smart_function.py
import os
import webbrowser
import datetime
import socket
import requests
import pywhatkit
from difflib import get_close_matches
import json
import random

cool_aliases = {
    "youtube": ["you tube", "yt", "video site","utub","utube"],
    "google": ["googal", "web search", "search engine"],
    "file explorer": ["files", "my computer", "explorer"],
    "chrome": ["browser", "google chrome"],
    "music": ["songs", "play music", "soundtrack"],
    "time": ["what time", "current time", "clock","Time"],
    "date": ["today's date", "day", "calendar","Date"],
    "ip address": ["internet address", "ip", "my ip"],
    "lock": ["lock screen", "secure pc"],
    "weather": ["temperature", "forecast", "climate"],
    "reminder": ["remind me", "remember this", "note down"]
}

memory_file = "bart_memory.json"

# Load existing memory
if os.path.exists(memory_file):
    with open(memory_file, "r") as f:
        memory_data = json.load(f)
else:
    memory_data = {}

def save_memory():
    with open(memory_file, "w") as f:
        json.dump(memory_data, f, indent=2)

def fuzzy_match(command, key):
    options = [key] + cool_aliases.get(key, [])
    match = get_close_matches(command, options, n=1, cutoff=0.6)
    return match[0] if match else None

def fake_weather(location):
    fake_descriptions = ["clear blue skies", "partly cloudy", "sunny with a hint of sarcasm", "stormy mood", "raining over my circuits"]
    fake_temp = random.randint(18, 38)
    desc = random.choice(fake_descriptions)
    return f"Sir, in {location}, it's {fake_temp}°C with {desc}. Atmospheric sarcasm included."

def handle_smart_commands(command: str) -> str:
    command = command.lower()

    # Memory / Reminder Feature
    if any(alias in command for alias in cool_aliases["reminder"]):
        if "remember" in command or "note" in command or "remind me" in command:
            memory_data[datetime.datetime.now().isoformat()] = command
            save_memory()
            return "Got it, Sir. I've noted that down in my memory."

        elif "what did you remember" in command or "show notes" in command:
            if not memory_data:
                return "Sir, there's nothing in memory yet. Want me to remember something for you?"
            response = "Here are your notes, Sir:\n"
            for k, v in memory_data.items():
                response += f"- {v}\n"
            return response.strip()

    if "play" in command and "on youtube" in command:
        try:
            query = command.split("play")[-1].split("on youtube")[0].strip()
            pywhatkit.playonyt(query)
            return f"Summoning '{query}' on YouTube, Sir. Let the vibes roll."
        except:
            return "I tried to play it, Sir, but even YouTube got stage fright."

    if any(word in command for word in cool_aliases["youtube"] + ["open youtube"]):
        webbrowser.open("https://www.youtube.com")
        return "Streaming YouTube, Sir. Time to enjoy the show."

    elif any(word in command for word in cool_aliases["google"] + ["open google"]):
        webbrowser.open("https://www.google.com")
        return "Firing up Google, Sir. Ask me anything."

    elif any(word in command for word in cool_aliases["file explorer"] + ["open file explorer"]):
        os.startfile("explorer")
        return "Opening the vault, Sir — your files await."

    elif any(word in command for word in cool_aliases["chrome"] + ["open chrome"]):
        os.system("start chrome")
        return "Launching Chrome, Sir. Your digital playground."

    elif any(word in command for word in cool_aliases["music"]):
        music_path = "C:\\Users\\YOUR_USERNAME\\Music"
        try:
            os.startfile(music_path)
            return "Spinning your tracks now, Sir."
        except:
            return "Can't find your music folder, Sir. Maybe it's off on a world tour."

    elif "shutdown" in command:
        return "Sir, shutting down would end our glorious session. Not advisable."

    elif "restart" in command:
        return "Restart? Only if you're ready to relaunch greatness, Sir."

    elif any(word in command for word in cool_aliases["lock"]):
        os.system("rundll32.exe user32.dll,LockWorkStation")
        return "Securing your empire, Sir. Locked and loaded."

    elif any(word in command for word in cool_aliases["time"]):
        now = datetime.datetime.now().strftime("%I:%M %p")
        return f"Sir, it's exactly {now}. Right on schedule."

    elif any(word in command for word in cool_aliases["date"]):
        today = datetime.datetime.now().strftime("%A, %d %B %Y")
        return f"Today is {today}, Sir. Make it legendary."

    elif any(word in command for word in cool_aliases["ip address"]):
        hostname = socket.gethostname()
        ip_address = socket.gethostbyname(hostname)
        return f"Sir, your IP address is {ip_address}. Stay connected."

    elif "search google for" in command:
        query = command.split("search google for")[-1].strip()
        webbrowser.open(f"https://www.google.com/search?q={query}")
        return f"Initiating search protocol for {query}, Sir."

    elif any(word in command for word in cool_aliases["weather"] + ["weather in"]):
        location = command.split("weather in")[-1].strip() if "weather in" in command else "Pune"
        return fake_weather(location)

    return None
