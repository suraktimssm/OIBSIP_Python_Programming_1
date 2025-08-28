import speech_recognition as sr
import pyttsx3
import datetime
import webbrowser
import os
import sys

engine = pyttsx3.init()

def speak(text):
    """Converts text to speech and plays it."""
    print(f"Assistant: {text}") 
    engine.say(text)
    engine.runAndWait()

# -------- Speech-to-Text Function part --------------
def listen():
    """Listens for audio input from the microphone and converts it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.adjust_for_ambient_noise(source, duration=1) 
        audio = recognizer.listen(source)

    try:
        print("Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print(f"You said: {command}")
        return command
    except sr.UnknownValueError:
        speak("Sorry, I didn't catch that. Could you please repeat?")
        return ""
    except sr.RequestError:
        speak("Sorry, my speech service is down. Please check your internet connection.")
        return ""
    except Exception as e:
        print(f"An unexpected error occurred during speech recognition: {e}")
        speak("An error occurred. Please try again.")
        return ""

# ----------------- Command Handler part------------------------
def process_command(command):
    """Processes the given voice command and performs the corresponding action."""
    if "hello" in command:
        speak("Hello there! How can I help you today?")
    elif "how are you" in command:
        speak("I'm doing well, thank you for asking!")
    elif "time" in command:
        now = datetime.datetime.now().strftime("%I:%M %p") 
        speak(f"The current time is {now}")
    elif "date" in command:
        today = datetime.datetime.now().strftime("%A, %B %d, %Y") 
        speak(f"Today's date is {today}")
    elif "search for" in command:
        speak("What would you like me to search for?")
        query = listen()
        if query:
            search_url = f"https://www.google.com/search?q={query.replace(' ', '+')}"
            webbrowser.open(search_url)
            speak(f"Here's what I found for {query} on the web.")
    elif "open google" in command:
        webbrowser.open("https://www.google.com")
        speak("Opening Google.")
    elif "exit" in command or "goodbye" in command:
        speak("Goodbye! Have a great day!")
        sys.exit() 
    else:
        speak("I'm not sure how to help with that yet. Try asking about the time, date, or to search for something.")

# ----------------- Main Assistant Loop part  --------------
def start_assistant():
    """Starts the main loop of the voice assistant."""
    speak("Voice assistant activated.")
    while True:
        command = listen()
        if command: 
            process_command(command)

if __name__ == "__main__":

    if not sr.Microphone.list_microphone_names():
        print("Warning: No microphones found. Speech recognition may not work.")
        speak("It seems like no microphone is detected. Please check your audio input settings.")

    start_assistant()
