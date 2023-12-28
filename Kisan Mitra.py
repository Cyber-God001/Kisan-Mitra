""" KISAN MITRA : AI Assistant robot with Arduino and Python

author: Sachin Kumar
mail: cyber.pvtlogin@proton.me
Last Edit: Nov 2023

License: Copyright (c) Sachin Kumar
General Public License (GPL3+)
"""


import speech_recognition as sr   # voice recognition library
import random                     # to choose random words from list
import pyttsx3                    # offline Text to Speech
import datetime  as dt            # to get date and time
import webbrowser                 # to open and perform web tasks
import serial                     # for serial communication
import pywhatkit                  # for more web automation
from   wikipedia import *         # wikipedia library
import requests                   # MODULES FOR
from bs4 import BeautifulSoup     # WEATHER

# Declare robot name (Wake-Up word)
robot_name = 'mitra'

# random words list
hi_words = ['hi', 'hello', 'jai shree ram']
bye_words = ['bye', 'tata']
r_u_there = ['are you there', 'you there']

# initilize things
engine = pyttsx3.init()                    # init text to speech engine
voices = engine.getProperty('voices')      # check for voices
engine.setProperty('voice', voices[2].id)  # indian voice
engine.setProperty('rate', 180)            # To ensure robot speaks slow enough
listener = sr.Recognizer()                 # initialize speech recognition API
set_lang('hi')                             # setting the language of wiki library to hindi

# connect with motor driver board over serial communication
try:
    port = serial.Serial("COM11", 9600)
    print("Phycial body, connected.")
except:
    print("Unable to connect to my physical body")


def listen():
    """ listen to what user says"""
    try:
        with sr.Microphone() as source:                         # get input from mic
            print("Talk>>")
            voice = listener.listen(source)                     # listen from microphone
            command = listener.recognize_google(voice).lower()  # use google API
            # all words lowercase- so that we can process easily
            #command = command.lower()         
            print(command)

            # look for wake up word in the beginning
            if (command.split(' ')[0] == robot_name):
                # if wake up word found....
                print("[wake-up word found]")
                process(command)                 # call process funtion to take action
    except:
        pass

def process(words):
    """ process what user says and take actions """
    print(words) # check if it received any command

    # break words in
    word_list = words.split(' ')[1:]                        # split by space and ignore the wake-up word

    if (len(word_list)==1):
        if (word_list[0] == robot_name):
            talk("How Can I help you?")
            #.write(b'l')
            return

    if word_list[0] == 'play':
        """if command for playing things, play from youtube"""
        talk("Okay sir")
        extension = ' '.join(word_list[1:])                    # Playing from Youtube
        port.write(b'u')
        pywhatkit.playonyt(extension)   
        port.write(b'l')          
        return

    elif word_list[0] == 'search':
        """if command for google search"""
        port.write(b'u')
        talk("जी सर, आपको कह गए वर्ड का मतलब ढूंढा जा रहा है")
        port.write(b'l')                                          # Google search
        extension = ' '.join(word_list[1:])
        pywhatkit.search(extension)
        return


    elif word_list[0] == 'open':
        """if command for opening URLs"""
        port.write(b'l')
        talk("जी सर, ये रहे आपके नतीजे")
        url = f"http://{''.join(word_list[1:])}"                    # For opening custom links
        webbrowser.open(url)
        return
    
    elif "website" in word_list:
        talk("किसान के लिए सरकार की सहायक वेबसाइट खोली जा रही है")
        port.write(b'h')                                        # For opening government website
        port.write(b'l')
        url = f"https://farmer.gov.in/"   
        webbrowser.open(url)
        return
    
    
    elif "developers" in word_list:
        talk("मेरे डेवलपर, सचिन कुमार और प्रद्युम्न राज हैं")    # Intro to the devs
        port.write(b'u')
        return
    
    elif "thank" in word_list:
        """if command for saying thanks"""
        talk(" धन्यवाद , मैं आशा करता हूं आपको हमारा प्रदर्शन पसंद आया")
        port.write(b'h')                                               # For saying thank you
        return
    
    if word_list[0] == 'jay':
        """if command for opening URLs"""
        talk("Jay Shree Raam")                                    # Fun Activity
        port.write(b'u')
        return
    
    elif word_list[0] == 'namaste':
        """if command for opening URLs"""
        talk("नमस्कार, मैं किसान मित्र हूं, मुझे बताएं मैं आपकी कैसे मदद कर सकता हूं")
        port.write(b'h')                                       # For greeting the guests
        return
    
    elif "judges" in word_list:
        """if command for opening URLs"""
        talk("नमस्कार वैज्ञानिक महोदय, मैं किसान मित्र हूं, बताइये मैं आपकी क्या सहायता कर सकता हूं")
        port.write(b'h')                                       # For greeting the guests
        return
    
    elif "organic" in word_list:
        talk("जरूर सर, कृपया प्रतीक्षा करें, आपके परिणाम खोजे जा रहे हैं")
        port.write(b'u') 
        port.write(b'l')
        url=f"https://krushidukan.bharatagri.com/collections/all-organic-bio-fertilizers-online-shop"
        webbrowser.open(url)
        return
    
    
    elif "khad" in word_list:
        talk("जरूर सर, कृपया प्रतीक्षा करें, आपके परिणाम खोजे जा रहे हैं") 
        port.write(b'u') 
        port.write(b'l')
        url=f"https://krushidukan.bharatagri.com/"
        webbrowser.open(url)
        return


    elif word_list[0] == 'mujhe':
        talk("ये रहे आस पास के डीलर के नाम और संपर्क विवरण")
        url= f"file:///G:/Downloads/SeedReport.html"
        port.write(b'l')
        webbrowser.open(url)
        return
    
    
    
    
    

    
    elif word_list[0] == 'dance':
        port.write(b'U')

    elif word_list[0] == 'smash':
        port.write(b's')

    elif word_list[0] == 'punch':
        port.write(b'p')

    # now check for matches
    for word in word_list:
        if word in hi_words:
            """ if user says hi/hello greet him accordingly"""
            port.write(b'h')               # send command to wave hand
            talk(random.choice(hi_words))

        elif word in bye_words:
            """ if user says bye etc"""
            talk(random.choice(bye_words))


def talk(sentence):
    """ talk / respond to the user """
    engine.say(sentence)
    engine.runAndWait()

# run the app
while True:
    listen()  # runs listen one time