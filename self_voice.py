import webbrowser
import speech_recognition as sr
import pyttsx3
import os
import psutil
import pyautogui
import datetime

#text 2 speech

engine = pyttsx3.init()

#speack function
def speak(text):
    engine.say(text)
    engine.runAndWait()

#recoganize the speech

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)
    try:
        print("⏳ Recognizing...")
        command = recognizer.recognize_google(audio).lower()
        print(f"🗣 You said: {command}")
        return command
    except sr.UnknownValueError:
        print("🤖 Sorry, I didn't understand that!")
        return ""
    except sr.RequestError:
        print("⚠️ Could not request results, check your internet!")
        return ""
# clos the windows..
def close_command(site_name):
    for process in psutil.process_iter(attrs=['pid','name']):
        if process.info['name'] and ('chrome' in process.info['name'].lower()):
            try:
                os.kill(process.info['pid'],9)
                speak(f"closed {site_name}")
                return
            except Exception as e:
                 print(f"Error closing {site_name}: {e}")
                 speak(f"Could not close {site_name}")

def close_tab():
    pyautogui.hotkey("ctrl", "w")  # Closes the active tab
    speak("Closed the current tab")


#handling the commands
def command_process(command):
    if "open" in command:
        # speak("What would you like to Open?")
        site = command.replace("open","").strip()
        url = f"https://www.{site}.com"
        speak(f"Opening {site}")
        webbrowser.open(url)
    elif "hello" in command:
        speak("Hello! I am your voice assistant. How can I help you?")

    elif "search" in command:
        # speak("What would you like to search?")
        query = recognize_speech()
        if query:
            webbrowser.open(f"https://www.google.com/search?q={query}")
            speak(f"Searching for {query}")
    elif "close tab" in command:
        close_tab()
    elif "time" in command:
        time_now = datetime.datetime.now().strftime("%I:%M %p")
        speak(f"The current time is {time_now}")

    elif "date" in command:
        date_today = datetime.datetime.now().strftime("%A, %B %d, %Y")
        speak(f"Today's date is {date_today}")


    elif "exit" in command:
        speak(f"Goodbye!...")
        exit()
    else:
        speak("I'm not sure how to handle that.")
        

        #usage
if __name__ == '__main__':
    speak("Hello! I am your voice assistant. How can I help you?")
    while True:
        command = recognize_speech()
        if command:
            command_process(command)