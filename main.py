import os
import tempfile
import pygame
import speech_recognition as sr
from gtts import gTTS
import pyautogui
import time
import requests
import wikipedia
import webbrowser

# Initialize pygame mixer
pygame.init()
pygame.mixer.init()

# Modes
active_mode = False
music_mode = False
is_speaking = False  # Added global flag

# Safe delete temp file
def safe_delete(file_path, retries=5, delay=0.1):
    for _ in range(retries):
        try:
            os.remove(file_path)
            return
        except PermissionError:
            time.sleep(delay)
    print(f"Warning: Could not delete {file_path}. File may still be in use.")  

# Speak function
def speak(text):
    global is_speaking
    is_speaking = True

    print(f"Jarvis: {text}")
    tts = gTTS(text=text, lang='en')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        temp_path = fp.name
        tts.save(temp_path)

    pygame.mixer.music.load(temp_path)
    pygame.mixer.music.play()

    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)

    safe_delete(temp_path)
    is_speaking = False

# Listen for command
def listen_command(silent=False):
    recognizer = sr.Recognizer()
    global is_speaking

    while is_speaking:
        time.sleep(0.1)

    with sr.Microphone() as source:
        if not silent:
            print("Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio)
        print(f"User said: {command}")
        return command.lower()
    except sr.UnknownValueError:
        if not silent:
            pass
        return ""
    except sr.RequestError:
        if not silent:
            pass
        return ""

# Weather API
def get_weather(city):
    api_key = "14bc15184646ec7cd67eb46bf47d79dc"  # Replace with your OpenWeatherMap API key
    base_url = "http://api.openweathermap.org/data/2.5/weather?"
    complete_url = f"{base_url}appid={api_key}&q={city}&units=metric"
    
    response = requests.get(complete_url)
    data = response.json()
    
    if str(data.get("cod")) == "200":
        main = data["main"]
        weather_desc = data["weather"][0]["description"]
        temp = main["temp"]
        humidity = main["humidity"]
        wind_speed = data["wind"]["speed"]
        country = data["sys"]["country"]
        city_name = data["name"]
        
        weather_report = (f"Current temperature in {city_name}, {country} is {temp}°C with {weather_desc}. "
                          f"Humidity is {humidity} percent and wind speed is {wind_speed} meters per second.")
        return weather_report
    else:
        return f"Sorry, I couldn't find the weather for that location."

# Extract city name
def extract_city(command):
    if "weather in" in command:
        return command.split("weather in", 1)[1].strip()
    elif "in" in command:
        return command.split("in", 1)[1].strip()
    return ""

# Close current tab
def close_current_tab():
    speak("Okay, closing the current tab.")
    while is_speaking:
        time.sleep(0.1)
    pyautogui.hotkey("ctrl", "w")
    speak("Closed the current tab.")

# MAIN FUNCTION
def main():
    global active_mode, music_mode

    speak("Initializing Jarvis")
    speak("Hello, how are you? Say 'Jarvis' to activate me.")
    time.sleep(2)
    active_mode = True
    music_mode = False

    while True:
        if not active_mode and not music_mode:
            print("Sleeping... Say 'Jarvis' to wake me.")
            wake_word = listen_command(silent=True)

            if "exit" in wake_word or "stop" in wake_word:
                speak("Goodbye!")
                break

            if "jarvis" in wake_word:
                active_mode = True
                speak("Yes, I am online now.")
            continue

        if active_mode:
            command = listen_command()

            if "exit" in command or "stop" in command:
                speak("Going offline. Goodbye!")
                break

            elif "sleep" in command or "go to sleep" in command:
                speak("Going to sleep. Say 'Jarvis' to wake me.")
                active_mode = False
                continue

            elif "play" in command:
                song = command.replace("play", "").strip()
                if song:
                    speak(f"Playing {song}")
                    import pywhatkit  # Keep this only for YouTube playback
                    pywhatkit.playonyt(song)
                    active_mode = False
                    music_mode = True
                else:
                    speak("Please tell me the song name.")

            elif "close song" in command or "close tab" in command:
                close_current_tab()

            elif "open" in command:
                if "youtube" in command:
                    speak("Opening YouTube.")
                    webbrowser.open("https://www.youtube.com")
                elif "google" in command:
                    speak("Opening Google.")
                    webbrowser.open("https://www.google.com")
                elif "facebook" in command:
                    speak("Opening Facebook.")
                    webbrowser.open("https://www.facebook.com")
                else:
                    speak("I can only open known websites like YouTube, Google, or Facebook.")
    
            elif "weather" in command:
                city = extract_city(command)
                if city:
                    speak(get_weather(city))
                else:
                    speak("Please tell me the city name.")
                    
            elif any(greet in command for greet in ["how are you","how r u","how are u","whats up"]):
                speak("I am doing great! how can i help you?")        

            elif any(q in command for q in ["who", "what", "when", "where", "why", "how"]) and not any(skip in command for skip in ["time", "weather", "play", "song"]):
                try:
                    speak("Let me check that for you.")
                    summary = wikipedia.summary(command, sentences=2)
                    speak(summary)
                except wikipedia.exceptions.DisambiguationError as e:
                    speak(f"Your query is too broad. Did you mean {e.options[0]}?")
                except wikipedia.exceptions.PageError:
                    speak("Sorry, I couldn't find any matching article.")
                except Exception:
                    speak("Sorry, something went wrong while searching Wikipedia.")
    
            elif "what's the time" in command or "what is the time" in command:
                current_time = time.strftime("%I:%M %p")
                speak(f"The current time is {current_time}")

            elif "jarvis" in command:
                speak("Yes?")    

            else:
                speak("Sorry, I didn't catch that.")

        if music_mode:
            print("Music mode active... Say 'Jarvis' to give me new commands.")
            wake_word = listen_command(silent=True)

            if "jarvis" in wake_word:
                music_mode = False
                active_mode = True
                speak("Yes, I am online now.")

            elif "close song" in wake_word or "close tab" in wake_word:
                close_current_tab()
                music_mode = False
                active_mode = True

if __name__ == "__main__":
    main()
