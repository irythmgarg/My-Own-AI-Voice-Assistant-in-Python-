import speech_recognition as sr
import pyttsx3
import pywhatkit
import wikipedia
import pyaudio
import datetime
import webbrowser
import psutil
from plyer import battery as plyer_battery  # Renamed to avoid conflict with psutil's battery check
import requests

# Initialize the recognizer
r = sr.Recognizer()

# Set Wikipedia language to English
wikipedia.set_lang("en")

# Function to speak the text aloud
def speak(text):
    engine = pyttsx3.init()  # Initialize pyttsx3 text-to-speech engine
    engine.say(text)  # Convert text to speech
    engine.runAndWait()  # Wait for the speech to finish

# Function to listen to the user's voice command
def listen_command():
    try:
        with sr.Microphone() as source:
            # Adjust the recognizer to the ambient noise
            r.adjust_for_ambient_noise(source)
            print("Say something!")
            # Listen for the audio
            audio = r.listen(source)
            # Recognize the speech using Google's recognizer
            my_text = r.recognize_google(audio)
            my_text = my_text.lower()  # Convert the speech to lowercase
            print("User said: " + my_text)

            # Check if the user asked about the battery percentage
            if 'battery' in my_text:
                battery_info = psutil.sensors_battery()  # Get battery status using psutil
                speak(f"Battery is at {battery_info.percent} percent")  # Speak the battery status
                return None

            # If the user says thank you or goodbye, exit the loop
            elif any(word in my_text for word in ['thank', 'thanks', 'bye', 'byee']):
                return 'thank you'

            # If the user wants to play a song
            elif 'play' in my_text:
                song = my_text.replace('play', '').strip()  # Extract the song name
                if song:
                    speak("Playing " + song)  # Speak the song being played
                    pywhatkit.playonyt(song)  # Play the song on YouTube
                    return 'thank you'
                else:
                    speak("Please say the song name after 'play'.")  # Ask for song name
                return None

            # If the user asks for the current date
            elif 'date' in my_text:
                today_date = datetime.date.today()  # Get today's date
                speak(f"Today's date is {str(today_date)}")  # Speak the date
                return None

            # If the user asks for the current time
            elif 'time' in my_text:
                today_time = datetime.datetime.now().strftime('%H:%M')  # Get the current time
                speak(f"Current time is {str(today_time)}")  # Speak the time
                return None

            # If the user wants to open a specific website
            elif 'open' in my_text:
                # Define a dictionary of common websites
                sites = {
                    "youtube": "https://www.youtube.com",
                    "google": "https://www.google.com",
                    "github": "https://www.github.com",
                    "thapar": "https://www.thapar.edu",
                    "gmail": "https://mail.google.com",
                    "stackoverflow": "https://stackoverflow.com",
                    "webkiosk": "https://webkiosk.thapar.edu/",
                    "lms": "https://lms.thapar.edu/moodle/",
                    "marks": "https://webkiosk.thapar.edu/",
                    "moodle": "https://lms.thapar.edu/moodle/",
                    "chat gpt": "https://chatgpt.com/"
                }

                # Loop through the dictionary to check if the website is in the command
                for site in sites:
                    if site in my_text:
                        speak(f"Opening {site}")  # Speak the website being opened
                        webbrowser.open(sites[site])  # Open the website in the default browser
                        return None

                # If no matching website is found
                speak("Sorry, I don't know that website.")
                return None

            # If the user asks for information from Wikipedia
            else:
                # Define triggers for various types of information
                triggers = [
                    'who is', 'where is', 'who was', 'where was',
                    'what is', 'what was',
                    'tell me about', 'define',
                    'give me information about', 'give information about',
                    'information about'
                ]
                # Check if the user's command starts with any trigger
                for trigger in triggers:
                    if my_text.startswith(trigger):
                        query = my_text.replace(trigger, '').strip()  # Extract the query
                        print(f"Searching Wikipedia for: '{query}'")  # Debug print
                        try:
                            # Fetch the summary from Wikipedia
                            info = wikipedia.summary(query, 1)
                            print(info)
                            speak(info)  # Speak the information
                            return info
                        except wikipedia.exceptions.DisambiguationError as e:
                            # Handle ambiguity in the search term
                            speak("The term is too ambiguous. Please be more specific.")
                            print(f"DisambiguationError: {e}")
                        except wikipedia.exceptions.PageError as e:
                            # Handle case where page is not found
                            speak("Sorry, I couldn't find any information on that.")
                            print(f"PageError: {e}")
                        except Exception as e:
                            # Catch any other errors
                            speak("Something went wrong while searching Wikipedia.")
                            print(f"General Error: {e}")
                        return None

            return None
    except sr.UnknownValueError:
        # Handle case where speech is not recognized
        print("Sorry, I did not understand that.")
        speak("Sorry, I did not understand that.")
        return None
    except sr.RequestError:
        # Handle case where speech recognition service is down
        print("Speech recognition service is down.")
        speak("Speech recognition service is down.")
        return None

# Main loop
while True:
    # Listen for commands
    returned = listen_command()
    if returned == "thank you":  # If the user says "thank you", exit the loop
        speak("Thanks, Have a good time")
        break
