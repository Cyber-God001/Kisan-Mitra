"""Ai Interaction"""

import speech_recognition as sr   # voice recognition library
import pyttsx3                    # offline Text to Speech
import datetime as dt            # to get date and time
import webbrowser                 # to open and perform web tasks
import serial                     # for serial communication
import pywhatkit                  # for more web automation
import uuid
import requests as rq
import json
from openai import OpenAI
import pandas as pd


def init_bot():
    # initilize things
    engine = pyttsx3.init()                    # init text to speech engine
    voices = engine.getProperty('voices')      # check for voices
    engine.setProperty('voice', voices[2].id)  # indian voice
    # To ensure robot speaks slow enough
    engine.setProperty('rate', 180)
    listener = sr.Recognizer()
    gpt_client = OpenAI(
        api_key='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')
    database = retrieve_data()
    return {
        'engine': engine,
        'listener': listener,
        'gpt_client': gpt_client,
        'database': database
    }


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


def retrieve_data():
    db = pd.read_excel("database.xlsx")
    triggers = []
    replies = []
    links = []
    for i in db['triggers'].to_list():
        triggers.append(str.lower(i))

    for i in db['replies'].to_list():
        replies.append(i)

    for i in db['links'].to_list():
        links.append(i)
    return {
        'triggers': triggers,
        'replies': replies,
        'links': links
    }


def get_reply(data, reply):
    reply = str.lower(reply)
    for i in range(len(data['triggers'])):
        if data['triggers'][i] in reply:
            return {
                'text': data['replies'][i],
                'link': data['links'][i]
            }
    return None


def talk(sentence, engine):
    """ talk / respond to the user """
    engine.say(sentence)
    engine.runAndWait()


def listen(listener):
    try:
        with sr.Microphone() as source:
            print("Talk>>")
            voice = listener.listen(source)
            command = listener.recognize_google(voice).lower()
            return command
    except:
        pass


def translate_to_hindi(message, client):
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
    providers = init_bot()
    ctr = 0
    threshold = 10
    while (True):
        try:
            me = listen(providers['listener'])
            print("\nME > " + me + "\n")
        except TypeError:
            ctr = ctr + 1
            if ctr > threshold:
                break
            continue
        reply = get_reply(providers['database'], me)
        if reply is None:
            me_hindi = translate_to_hindi(me, providers['gpt_client'])
            print("TRANS > " + me_hindi)
            append_message({
                "role": "user",
                "content": me_hindi
            })
            gpt_reply = start_talk(providers['gpt_client'])
            print("\nGPT > " + gpt_reply + "\n")
            talk(gpt_reply, providers['engine'])
        else:
            print("\nGPT > " + reply['text'] + "\n")
            talk(reply['text'])
            webbrowser.open(reply['link'])
