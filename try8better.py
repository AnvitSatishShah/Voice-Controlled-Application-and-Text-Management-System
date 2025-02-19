# conda activate <environment_name>
# python file.py
import speech_recognition as sr
import subprocess
import pyautogui
import time
from googletrans import Translator
from textblob import TextBlob  # For sentiment analysis
import os

# Create a recognizer object
r = sr.Recognizer()
translator = Translator()

def open_application(app_name):
    try:
        # Check if the app_name is a PDF or text file
        if app_name.endswith(".pdf") and os.path.isfile(app_name):
            print(f"Attempting to open PDF file: {app_name}...")
            subprocess.run(["open", app_name])
            return True
        elif app_name.endswith(".txt") and os.path.isfile(app_name):
            print(f"Attempting to open text file: {app_name}...")
            subprocess.run(["open", app_name])
            return True
        
        app_commands = {
            "notes": "Notes",
            "app store": "App Store",
            "find my": "Find My",
            "settings": "System Preferences",
            "reminders": "Reminders",
            "contacts": "Contacts",
            "calendar": "Calendar",
            "photos": "Photos",
            "maps": "Maps",
            "mail": "Mail",
            "messages": "Messages",
            "safari": "Safari",
            "finder": "Finder"
        }
        
        if app_name in app_commands:
            print(f"Attempting to open {app_commands[app_name]}...")
            subprocess.run(["open", "-a", app_commands[app_name]])
            time.sleep(5)  # Wait for the application to open

            if app_name == "notes":
                time.sleep(2)  # Ensure the app is active
                pyautogui.hotkey('command', 'n')  # Create a new note
                time.sleep(1)  # Wait for the new note to be created
                return True
        else:
            print(f"Application '{app_name}' not recognized.")
    except Exception as e:
        print(f"Error opening application: {e}")

def type_text(text):
    time.sleep(1)  # Wait for the note to be ready
    print(f"Typing text: {text}")  # Debug output
    pyautogui.typewrite(text, interval=0.1)  # Type the provided text
    print(f"Typed: {text}")

def translate_text(text, dest_language):
    try:
        # Ensure the translation request uses the correct destination language
        translation = translator.translate(text, dest=dest_language)
        return translation.text  # Should return text in local script
    except Exception as e:
        print(f"Error translating text: {e}")
        return None

def analyze_sentiment(text):
    try:
        blob = TextBlob(text)
        return blob.sentiment
    except Exception as e:
        print(f"Error analyzing sentiment: {e}")
        return None

def sentiment_to_string(sentiment):
    if sentiment.polarity > 0:
        return "Positive"
    elif sentiment.polarity < 0:
        return "Negative"
    else:
        return "Neutral"

def replace_keywords(command):
    # Replace specific words
    replacements = {
        "hai": "hi"
    }
    for old, new in replacements.items():
        command = command.replace(old, new)
    return command

def handle_voice_command(command):
    command = command.lower()
    command = replace_keywords(command)  # Replace specific keywords
    print(f"Received command: {command}")  # Debug output

    if "open notes and write" in command:
        content = command.split("open notes and write", 1)[1].strip()
        if open_application("notes"):
            type_text(content)
    elif "translate to marathi" in command:
        text = command.split("translate to marathi", 1)[1].strip()
        translated = translate_text(text, "mr")  # Ensure correct language code
        if translated:
            print(f"Translated text: {translated}")
    elif "translate to hindi" in command:
        text = command.split("translate to hindi", 1)[1].strip()
        translated = translate_text(text, "hi")  # Ensure correct language code
        if translated:
            print(f"Translated text: {translated}")
    elif "open pdf file" in command:
        pdf_file = command.split("open pdf file", 1)[1].strip()
        pdf_file = pdf_file.replace("hi", "hi.pdf")  # Adjusting for your specific case
        open_application(pdf_file)  # Try to open the specified PDF file
    elif "open text file" in command:
        text_file = command.split("open text file", 1)[1].strip()
        text_file = text_file.replace("hi", "hi.txt")  # Adjusting for your specific case
        open_application(text_file)  # Try to open the specified text file
    elif "open" in command:
        app_name = command.split("open", 1)[1].strip()
        open_application(app_name)  # Try to open the specified app

# Use the default microphone as the audio source
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)

# Attempt to recognize the speech
try:
    text = r.recognize_google(audio, language='en-IN')  # Adjusting for Indian accent recognition
    print("You said: " + text)

    # Analyze sentiment
    sentiment = analyze_sentiment(text)
    if sentiment:
        sentiment_description = sentiment_to_string(sentiment)
        print(f"Sentiment: {sentiment_description}")

    # Handle the voice command
    handle_voice_command(text)

except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))