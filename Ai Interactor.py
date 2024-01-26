"""Ai Interaction"""

import speech_recognition as sr   # voice recognition library
import pyttsx3                    # offline Text to Speech
import datetime  as dt            # to get date and time
import webbrowser                 # to open and perform web tasks
import serial                     # for serial communication
import pywhatkit                  # for more web automation
import uuid
import requests as rq
import json
from openai import OpenAI



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
listener = sr.Recognizer() 

def listen():
    """ listen to what user says"""
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
    


def start_talk(client):
    with open("messages.json") as file:
        messages = json.load(file)
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    append_message({
        "role": response.choices[0].message.role,
        "content": response.choices[0].message.content
    })

    return response.choices[0].message.content


def append_message(message):
    with open("messages.json") as file:
        messages = json.load(file)
    messages.append(message)

    with open("messages.json", "w") as file_out:
        json.dump(messages, file_out)








def process(words):
    """ process what user says and take actions """
    print(words) # check if it received any command

    # break words in
    word_list = words.split(' ')[1:]                        # split by space and ignore the wake-up word

    if (len(word_list)==1):
        if (word_list[0] == robot_name):
            talk("How Can I help you?")
            return

    if word_list[0] == 'play':
        """if command for playing things, play from youtube"""
        talk("Okay sir")
        extension = ' '.join(word_list[1:])                    # Playing from Youtube
        pywhatkit.playonyt(extension)            
        return

    elif word_list[0] == 'search':
        """if command for google search"""
        talk("जी सर, आपको कह गए वर्ड का मतलब ढूंढा जा रहा है")                                          # Google search
        extension = ' '.join(word_list[1:])
        pywhatkit.search(extension)
        return


    elif word_list[0] == 'open':
        """if command for opening URLs"""
        talk("जी सर, ये रहे आपके नतीजे")
        url = f"http://{''.join(word_list[1:])}"                    # For opening custom links
        webbrowser.open(url)
        return
    
    elif "website" in word_list:
        talk("किसान के लिए सरकार की सहायक वेबसाइट खोली जा रही है")
        url = f"https://farmer.gov.in/"   
        webbrowser.open(url)
        return
    
    
    elif "developers" in word_list:
        talk("मेरे डेवलपर, सचिन कुमार और प्रद्युम्न राज हैं")    # Intro to the devs
        return
    
    elif "thank" in word_list:
        """if command for saying thanks"""
        talk(" धन्यवाद , मैं आशा करता हूं आपको हमारा प्रदर्शन पसंद आया")                                               # For saying thank you
        return
    
    if word_list[0] == 'jay':
        """if command for opening URLs"""
        talk("Jay Shree Raam")                                    # Fun Activity
        return
    
    elif word_list[0] == 'namaste':
        """if command for Greeting Guests"""
        talk("नमस्कार, मैं किसान मित्र हूं, मुझे बताएं मैं आपकी कैसे मदद कर सकता हूं")                                       # For greeting the guests
        return
    
    elif "judges" in word_list:
        """if command for greeting judges"""
        talk("नमस्कार वैज्ञानिक महोदय, मैं किसान मित्र हूं, बताइये मैं आपकी क्या सहायता कर सकता हूं")                                     # For greeting the judges
        return
    
    elif "organic" in word_list:
        talk("जरूर सर, कृपया प्रतीक्षा करें, आपके परिणाम खोजे जा रहे हैं")
        url=f"https://krushidukan.bharatagri.com/collections/all-organic-bio-fertilizers-online-shop"
        webbrowser.open(url)
        return
    
    
    elif "khad" in word_list:
        talk("जरूर सर, कृपया प्रतीक्षा करें, आपके परिणाम खोजे जा रहे हैं") 
        url=f"https://krushidukan.bharatagri.com/"
        webbrowser.open(url)
        return


    elif word_list[0] == 'mujhe':
        talk("ये रहे आस पास के डीलर के नाम और संपर्क विवरण")
        url= f"file:///G:/Downloads/SeedReport.html"
        webbrowser.open(url)
        return 
    
    else:
        talk(response)
  



def talk(sentence):
    """ talk / respond to the user """
    engine.say(sentence)
    engine.runAndWait()

def speechtotext():
    try:
        with sr.Microphone() as source:
            print("Talk>>")
            voice = listener.listen(source)                     
            command = listener.recognize_google(voice).lower()  
            return command
    except:
        pass
    
def translate_to_hindi(message):
    with open("translator.json") as file:
        prompt = json.load(file)
    prompt.append({
        "role": "user",
        "content": message
    })
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=prompt
    )
    return response.choices[0].message.content


           
    


if __name__ == '__main__':
    client = OpenAI(
        api_key='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')
    while (True):
        me = speechtotext()
        print("\nME > " + me + "\n")
        me_hindi = translate_to_hindi(me)
        print("TRANS > " + me_hindi)
        append_message({
            "role": "user",
            "content": me_hindi
        })
        reply = start_talk(client)
        print("\nGPT > " + reply + "\n")
        talk(reply)


    


                    

