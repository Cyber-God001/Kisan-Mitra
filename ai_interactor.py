import uuid
import requests as rq
import json
from dotenv import dotenv_values


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
    env = dotenv_values(".env")
    base_url = env["BASE_URL"]
    organization_id = env["ORGANIZATION_ID"]
    cookie = env["COOKIE"]
    print(base_url)
    request_headers = generate_headers(cookie, "")
    request_body = {
        "uuid": new_chat_id,
        "name": "Mitr"
    }

    create_chat_response = rq.post(
        base_url + "/organizations/" + organization_id + "/chat_conversations", headers=request_headers, json=request_body)
    if create_chat_response.status_code == 201:
        return new_chat_id

    raise ConnectionRefusedError("Cookie Expire hogya change karlo")


def send_chat(message: str, chatId: str):
    env = dotenv_values(".env")
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
    env = dotenv_values(".env")
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


if __name__ == '__main__':
    chatId = create_chat()
    while (True):
        message = str(input("Me: "))
        if message == "exit":
            break
        print("\n")
        send_chat(message, chatId)
        reply = get_reply(chatId)
        print("Claude: " + reply)
        print("\n")
    exit(0)
