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


def generate_headers(cookie: str, chatId: str):
    headers = {
        'Origin': 'https://claude.ai',
        'Content-Type': 'application/json',
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Cookie': cookie
    }

    if chatId != "":
        headers['Referer'] = 'https://claude.ai/chat/' + chatId

    return headers




def create_chat():
    new_chat_id = str(uuid.uuid4())
    env = load_env()
    print (env.keys())
    base_url = env["BASE_URL"]
    organization_id = env["ORGANIZATION_ID"]
    cookie = env["COOKIE"]
    print(base_url)
    request_headers = generate_headers(cookie, "")
    request_body = {
        "uuid": new_chat_id,
        "name": "Mitra"
    }

    create_chat_response = rq.post(
        base_url + "/organizations/" + organization_id + "/chat_conversations", headers=request_headers, json=request_body)
    if create_chat_response.status_code == 201:
        return new_chat_id

    raise ConnectionRefusedError("Cookie Expire hogya change karlo")


def send_chat(message: str, chatId: str):
    env = load_env()
    base_url = env["BASE_URL"]
    organization_id = env["ORGANIZATION_ID"]
    cookie = env["COOKIE"]

    request_headers = generate_headers(cookie, chatId)
    request_body = {
        "completion": {
            "prompt": message,
            "timezone": "Asia/Calcutta",
            "model": "claude-2.1"
        },
        "organization_uuid": organization_id,
        "conversation_uuid": chatId,
        "text": message,
        "attachments": []
    }

    chat_response = rq.post(base_url + "/append_message",
                            headers=request_headers, json=request_body)

    if chat_response.status_code != 200:
        raise ConnectionRefusedError("Cookie Expire hogya change karlo")


def get_reply(chatId: str):
    env = load_env()
    base_url = env["BASE_URL"]
    organization_id = env["ORGANIZATION_ID"]
    cookie = env["COOKIE"]

    request_headers = generate_headers(cookie, chatId)
    reply_response = rq.get(base_url + "/organizations/" + organization_id +
                            "/chat_conversations/" + chatId, headers=request_headers)

    if reply_response.status_code != 200:
        raise ConnectionRefusedError("Cookie Expire hogya change karlo")

    data = json.loads(reply_response.text)
    gi = -1
    for message in data['chat_messages']:
        if message['index'] > gi:
            gi = message['index']

    for message in data['chat_messages']:
        if message['index'] == gi:
            return message['text']


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
        return # now check for matches
    
    else:
        talk(response)
  



def talk(sentence):
    """ talk / respond to the user """
    engine.say(sentence)
    engine.runAndWait()

def speechtotext():
    try:
        with sr.Microphone() as source:                         # get input from mic
            print("Talk>>")
            voice = listener.listen(source)                     # listen from microphone
            command = listener.recognize_google(voice).lower()  # use google API
            # all words lowercase- so that we can process easily
            #command = command.lower()         
            return command
    except:
        pass   
    
def load_env():
    env= {
        'COOKIE':"sessionKey=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; activitySessionId=22376e33-673a-4d7f-8fda-d89e5246f6f5; __cf_bm=8cYXjxdSnhVlLtKJ.D8BK1azBzfV.sX_ZCKtD.vV4Jw-1705763659-1-AVv9AgL/jEHduQctAZuG+QSjCpquryiijyp1IV95k8ndUfmOKbzg444tN9cw2O74s5o0kjrz4fuJdrwaarISUuE=; cf_clearance=vWhvFVvDV9_bCC90q7f8xHnQlwRp6BiT3Bv0j7DB8dw-1705763660-1-AZN1F6jzSybNo3K3QeXRpUKUMKY9CPZ1LuuybLOAKPK+sfSSl4gzI0/v8b6959YIkw1/UZpBg/YmZJCDiYbRPXk=; __ssid=68137bedde1bae01937e7fc03cd95b5; intercom-session-lupk8zyo=L0RoVTZPWXp5NExOZCsyZExVdTVLN3dEMEFqSkt6cXZabm1SNFFQcVQwRmNxaytnb0E0MkhFYVZpVWFVRFZPdi0tZUpyR2pieHVCR0xqR0xqRDJyLzY5Zz09--217281583efc36d09524de47d7602628e1e9d1d2; intercom-device-id-lupk8zyo=e6524229-b1a6-4ac7-97b4-21c15cb54c51; __stripe_mid=ebd03d84-3220-4603-96bb-18d6554b8285dbcf5c; __stripe_sid=03babdd9-1698-493f-9ee4-9b9c66c97552a1540b",
        'ORGANIZATION_ID':"cd4e0be6-3ea7-487c-8b59-658a3ea1e092",
        'BASE_URL':"https://claude.ai/api"
    }
    return env

if __name__ == '__main__':
    chat_id=create_chat()
    while True:
        user=speechtotext()
        send_chat(user, chat_id)
        bot=get_reply(chat_id)
        talk(bot)



    


                    

