import logging
import pyttsx3
import requests
import speech_recognition as sr
import keyboard
import os
import subprocess as sp
import imdb
import wolframalpha
import pyautogui
import webbrowser
import time
import os

from datetime import datetime
from decouple import config
from random import choice
from const import random_text
from utils import find_my_ip, send_whatsapp_message, search_on_google, search_on_wikipedia, youtube, send_email, get_news, weather_forecast
import google.generativeai as genai

GEMINI_API_KEY=os.environ.get("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

engine = pyttsx3.init()
engine.setProperty('volume', 1.0)
engine.setProperty('rate', 220)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[1].id)

logging.getLogger("comtypes").setLevel(logging.WARNING)

USER = config('USER')
HOSTNAME = config('BOT')


def speak(text):
    engine.say(text)
    engine.runAndWait()


def greet_me():
    hour = datetime.now().hour
    if (hour >= 6) and (hour < 12):
        speak(f"Good morning {USER}")
    elif (hour >= 12) and (hour <= 16):
        speak(f"Good afternoon {USER}")
    elif (hour >= 16) and (hour < 19):
        speak(f"Good evening {USER}")
    speak(f"I am {HOSTNAME}. How may i assist you? {USER}")


listening = False


def start_listening():
    global listening
    listening = True
    print("started listening ")


def pause_listening():
    global listening
    listening = False
    print("stopped listening")


keyboard.add_hotkey('ctrl+alt+k', start_listening)
keyboard.add_hotkey('ctrl+alt+p', pause_listening)


# Take Voice Command
def take_command():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 1
        audio = r.listen(source)

    try:
        print("Recognizing...")
        query = r.recognize_google(audio, language='en-in').lower()
        print(query)

        if 'stop' in query or 'exit' in query:
            speak("Goodbye! Have a great day.")
            exit()

        speak(choice(random_text))
        return query

    except Exception:
        speak("Sorry, I couldn't understand. Can you repeat?")
        return "None"

# Gemini AI Response
def get_gemini_response(query):
    try:
        response = model.generate_content(query)
        return response.text if response and hasattr(response, 'text') else "I'm sorry, I couldn't process that request."
    except Exception as e:
        print(f"Error getting Gemini response: {e}")
        return "I'm sorry, I couldn't process that request."

if __name__ == '__main__':
    greet_me()
    while True:
        if listening:
            query = take_command().lower()
            if "how are you" in query:
                speak("I am absolutely fine sir. What about you")
            
            elif "what is your name" in query:
                speak("My name is SIBEL sir")

            elif "I am fine" in query:
                speak("That's great to hear sir. How can I help you?")

            elif "open command prompt" in query:
                speak("Opening command prompt")
                os.system('start cmd')

            elif "open camera" in query:
                speak("Opening camera sir")
                sp.run('start microsoft.windows.camera:', shell=True)

            elif "open notepad" in query:
                speak("Opening Notepad for you sir")
                notepad_path = "C:\\Users\\user\\AppData\\Local\\Microsoft\\WindowsApps\\notepad.exe"
                os.startfile(notepad_path)

            elif "open discord" in query:
                speak("Opening Discord for you sir")
                discord_path = "C:\\Users\\user\\AppData\\Local\\Discord\\app-1.0.9175\\Discord.exe"
                os.startfile(discord_path)

            # elif "open gta" in query:
            #     speak("Opening Gta for you sir")
            #     gta_path = "D:\\Tanishq\\GTA\\Launcher.exe"
            #     os.startfile(gta_path)

            elif "open chrome" in query:
                speak("Opening Chrome for you sir")
                chrome_path = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
                os.startfile(chrome_path)

            elif 'ip address' in query:
                ip_address = find_my_ip()
                speak(
                    f'Your IP Address is {ip_address}.\n For your convenience, I am printing it on the screen sir.')
                print(f'Your IP Address is {ip_address}')

            elif "open youtube" in query:
                speak("What do you want to play on youtube sir?")
                video = take_command().lower()
                youtube(video)

            elif "open google" in query:
                speak(f"What do you want to search on google {USER}")
                query = take_command().lower()
                search_on_google(query)

            elif "wikipedia" in query:
                speak("what do you want to search on wikipedia sir?")
                search = take_command().lower()
                results = search_on_wikipedia(search)
                speak(f"According to wikipedia,{results}")
                speak("I am printing in on terminal")
                print(results)


            elif "send an email" in query:
                speak("On what email address do you want to send sir?. Please enter in the terminal")
                receiver_add = input("Email address:")
                speak("What should be the subject sir?")
                subject = take_command().capitalize()
                speak("What is the message ?")
                message = take_command().capitalize()
                if send_email(receiver_add, subject, message):
                    speak("I have sent the email sir")
                    print("I have sent the email sir")
                else:
                    speak("something went wrong Please check the error log")

            elif "send whatsapp message" in query:
                speak(
                    'On what number should I send the message sir? Please enter in the console: ')
                number = input("Enter the number: ")
                speak("What is the message sir?")
                message = take_command().lower()
                send_whatsapp_message(number, message)
                speak("I've sent the message sir.")

            elif "give me news" in query:
                speak(f"I am reading out the latest headline of today,sir")
                speak(get_news())
                speak("I am printing it on screen sir")
                print(*get_news(), sep='\n')

            elif 'weather' in query:
                ip_address = find_my_ip()
                speak("tell me the name of your city")
                city = input("Enter name of your city")
                speak(f"Getting weather report for your city {city}")
                weather, temp, feels_like = weather_forecast(city)
                speak(f"The current temperature is {temp}, but it feels like {feels_like}")
                speak(f"Also, the weather report talks about {weather}")
                speak("For your convenience, I am printing it on the screen sir.")
                print(f"Description: {weather}\nTemperature: {temp}\nFeels like: {feels_like}")

            elif "movie" in query:
                movies_db = imdb.IMDb()
                speak("Please tell me the movie name:")
                text = take_command()
                movies = movies_db.search_movie(text)
                speak("searching for" + text)
                speak("I found these")
                for movie in movies:
                    title = movie["title"]
                    year = movie["year"]
                    speak(f"{title}-{year}")
                    info = movie.getID()
                    movie_info = movies_db.get_movie(info)
                    rating = movie_info["rating"]
                    cast = movie_info["cast"]
                    actor = cast[0:5]
                    plot = movie_info.get('plot outline', 'plot summary not available')
                    speak(f"{title} was released in {year} has imdb ratings of {rating}.It has a cast of {actor}. "
                          f"The plot summary of movie is {plot}")

                    print(f"{title} was released in {year} has imdb ratings of {rating}.\n It has a cast of {actor}. \n"
                          f"The plot summary of movie is {plot}")


            elif "calculate" in query:
                app_id = "9A23TV-H7KL7E2VTK"
                client = wolframalpha.Client(app_id)
                ind = query.lower().split().index("calculate")
                text = query.split()[ind + 1:]
                result = client.query(" ".join(text))
                try:
                    ans = next(result.results).text
                    speak("The answer is " + ans)
                    print("The answer is " + ans)
                except StopIteration:
                    speak("I couldn't find that . Please try again")


            elif 'what is' in query or 'who is' in query or 'which is' in query:
                app_id = "9A23TV-H7KL7E2VTK"
                client = wolframalpha.Client(app_id)
                try:

                    ind = query.lower().index('what is') if 'what is' in query.lower() else \
                        query.lower().index('who is') if 'who is' in query.lower() else \
                            query.lower().index('which is') if 'which is' in query.lower() else None

                    if ind is not None:
                        text = query.split()[ind + 2:]
                        res = client.query(" ".join(text))
                        ans = next(res.results).text
                        speak("The answer is " + ans)
                        print("The answer is " + ans)
                    else:
                        speak("I couldn't find that. Please try again.")
                except StopIteration:
                    speak("I couldn't find that. Please try again.")

            elif 'tell me about' in query:
                try:
                    gemini_response = model.generate_content(query).text
                    speak(gemini_response)
                    print(gemini_response)
                except Exception as e:
                    print(f"Error in Gemini query: {e}")
                    speak("I'm sorry, I couldn't find an answer to that.")

            elif 'subscribe' in query:
                speak(
                    "Everyone who are watching this video, Please subscribe for more amazing content from CodeWithArhan "
                    "I will show you how to do this")
                speak("Firstly Go to youtube")
                webbrowser.open("https://www.youtube.com/")
                speak("click on the search bar")
                pyautogui.moveTo(806, 125, 1)
                pyautogui.click(x=806, y=125, clicks=1, interval=0, button='left')
                speak("CodeWithArhan")
                pyautogui.typewrite("CodeWithArhan", 0.1)
                time.sleep(1)
                speak("press enter")
                pyautogui.press('enter')
                pyautogui.moveTo(971, 314, 1)
                speak("Here you will see our channel")
                pyautogui.moveTo(1688, 314, 1)
                speak("click here to subscribe our channel")
                pyautogui.click(x=1688, y=314, clicks=1, interval=0, button='left')
                speak("And also Don't forget to press the bell icon")
                pyautogui.moveTo(1750, 314, 1)
                pyautogui.click(x=1750, y=314, clicks=1, interval=0, button='left')
                speak("turn on all notifications")
                pyautogui.click(x=1750, y=320, clicks=1, interval=0, button='left')

            else:
                try:
                    gemini_response =get_gemini_response(query)
                    gemini_response = gemini_response.replace("*","")
                    if gemini_response and gemini_response != "I'm sorry, I couldn't process that request.":
                        speak(gemini_response)
                        print(gemini_response)
                except Exception as e:
                    print(f"Error in Gemini query: {e}")
                    speak("I'm sorry, I couldn't find an answer to that.")