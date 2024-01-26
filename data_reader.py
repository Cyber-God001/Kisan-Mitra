import pandas as pd


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


if __name__ == '__main__':
    data = retrieve_data()
    reply = get_reply(data, "Mujhe kuch Fertiliser Dealers ke list batao")
    if reply is None:
        print('Send to gpt')
    print(reply['text'])
    print('opening website ' + reply['link'])
