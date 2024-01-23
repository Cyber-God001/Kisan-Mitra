import json
from openai import OpenAI


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
    client = OpenAI(
        api_key='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')
    start_talk(client)
    while (True):
        me = input("ME > ")
        if me == "exit":
            break
        append_message({
            "role": "user",
            "content": me
        })
        gpt = start_talk(client)
        print("\nGPT > " + gpt + "\n")
