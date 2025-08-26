import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
from gtts import gTTS
import pygame
import os

# pip install pocketsphinx

recognizer = sr.Recognizer()
engine = pyttsx3.init() 

def speak_old(text):
    engine.say(text)
    engine.runAndWait()

def speak(text):
    tts = gTTS(text)
    tts.save('temp.mp3') 

    # Initialize Pygame mixer
    pygame.mixer.init()

    # Load the MP3 file
    pygame.mixer.music.load('temp.mp3')

    # Play the MP3 file
    pygame.mixer.music.play()

    # Keep the program running until the music stops playing
    while pygame.mixer.music.get_busy():
        pygame.time.Clock().tick(10)
    
    pygame.mixer.music.unload()
    os.remove("temp.mp3") 

# Simple local fallback AI (instead of paid OpenAI API)
def aiProcess(command):
    responses = {
        "hello": "Hello! How can I help you?",
        "how are you": "I am doing great, thank you!",
        "your name": "I am Jarvis, your assistant.",
    }
    for key in responses:
        if key in command.lower():
            return responses[key]
    return "Sorry, I can't help with that right now."

def processCommand(c):
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    elif c.lower().startswith("play"):
        song = c.lower().split(" ")[1]
        if song in musicLibrary.music:
            link = musicLibrary.music[song]
            webbrowser.open(link)
        else:
            speak("Song not found in library.")
    elif "news" in c.lower():
        # Free fallback headlines (instead of paid NewsAPI)
        headlines = [
            "Today's top story: AI is helping developers build faster.",
            "Breaking: Local community launches new tech hub.",
            "Sports update: The championship finals are approaching."
        ]
        for headline in headlines:
            speak(headline)
    else:
        # Local AI
        output = aiProcess(c)
        speak(output) 

if __name__ == "__main__":
    speak("Initializing Jarvis....")
    while True:
        r = sr.Recognizer()
        print("recognizing...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=1)
            word = r.recognize_google(audio)
            if(word.lower() == "jarvis"):
                speak("Ya")
                # Listen for command
                with sr.Microphone() as source:
                    print("Jarvis Active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("Error; {0}".format(e))
