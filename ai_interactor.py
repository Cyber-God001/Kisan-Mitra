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
        me = input("ME > ")
        if me == "exit":
            break
        me_hindi = translate_to_hindi(me)
        print("TRANS > " + me_hindi)
        append_message({
            "role": "user",
            "content": me_hindi
        })
        gpt = start_talk(client)
        print("\nGPT > " + gpt + "\n")
