# Jarvis Voice Assistant — Project Summary

## Overview
This project is a voice-activated personal assistant named **Jarvis** built using Python.  
It can listen to voice commands, respond via speech, perform tasks like playing music, fetching weather updates, browsing websites, searching Wikipedia, and more.  
It uses various APIs and libraries to deliver an interactive voice-controlled experience.

---

## ✨ Key Features
- Voice activation with a wake word (**"Jarvis"**)
- Speech synthesis (text-to-speech)
- Speech recognition (voice command input)
- Play YouTube music videos on command
- Open popular websites (YouTube, Google, Facebook)
- Provide real-time weather updates using **OpenWeatherMap API**
- Answer factual questions via Wikipedia summaries
- Control browser tabs (close tabs)
- Time announcement
- Sleep and wake modes for power management

---

## 🛠️ Main Components

### 1. Initialization
- **pygame** is initialized to handle audio playback.  
- Global mode flags:
  - `active_mode` → controls whether Jarvis listens actively.
  - `music_mode` → handles music playback state.
  - `is_speaking` → avoids conflicts between speaking and listening.

### 2. Speech Output — `speak(text)`
- Uses **gTTS** (Google Text-to-Speech) to convert text into audio.
- Saves audio temporarily as an MP3 file.
- Plays the MP3 using **pygame.mixer**.
- Safely deletes the temporary file after playback.
- Coordinates speaking/listening with `is_speaking`.

### 3. Speech Input — `listen_command(silent=False)`
- Uses **speech_recognition** library to capture microphone input.
- Adjusts for ambient noise.
- Converts speech → text via Google’s API.
- Supports silent listening mode.
- Returns recognized commands or empty string on failure.

### 4. Weather Feature
- Fetches data from **OpenWeatherMap API** for a city.
- Parses temperature, humidity, wind speed, and conditions.
- Returns descriptive weather report or error.

### 5. Command Processing & Actions
Jarvis listens for commands such as:
- **Exit/Stop** → shuts down.
- **Sleep** → goes to sleep until reactivated.
- **Play [song name]** → plays music on YouTube.
- **Close tab/song** → closes the current browser tab.
- **Open [YouTube/Google/Facebook]** → opens sites.
- **Weather in [city]** → fetches weather update.
- **Greetings** → responds conversationally.
- **Wikipedia queries** → summarizes topics.
- **What’s the time** → announces current time.
- Fallback → “Sorry, I didn’t catch that.”

### 6. Music Mode
- When playing music, Jarvis switches to **music mode**.
- Waits for wake word (“Jarvis”) to return to active mode.
- Can also close the music tab in this mode.

---

## 🔧 Supporting Functions
- `safe_delete(file_path)` → deletes temporary audio safely.  
- `extract_city(command)` → extracts city names from weather commands.  
- `close_current_tab()` → simulates `Ctrl+W` to close browser tabs.  

---

## 📚 Libraries & APIs Used
- **pygame** → audio playback
- **speech_recognition** → voice input
- **gTTS** → text-to-speech
- **pyautogui** → keyboard automation
- **requests** → HTTP requests
- **wikipedia** → Wikipedia summaries
- **webbrowser** → open URLs
- **pywhatkit** → play YouTube videos

---

## 🔄 How It Works (Flow)
1. Jarvis starts and greets the user.  
2. Waits in **sleep mode** until it hears “Jarvis.”  
3. Listens for commands.  
4. Executes commands & responds.  
5. Switches between **active** and **music mode**.  
6. Runs continuously until told to exit or sleep.  

---

## ✅ Summary
This project demonstrates integration of speech recognition, speech synthesis, APIs, web automation, and system control to build a functional, conversational AI assistant.  
It shows how Python can interact with external services and hardware to deliver a **hands-free, interactive experience**.
