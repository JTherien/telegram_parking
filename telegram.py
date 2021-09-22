import requests
import yaml

if __name__ == '__main__':

    with open('config.yaml', 'r') as stream:

        config = yaml.safe_load(stream)


def send_message(message, config):

    bot_id = config['telegram_bot_api']
    chat_id = config['telegram_bot_chat']

    url = f'https://api.telegram.org/bot{bot_id}/sendMessage?chat_id={chat_id}&parse_mode=Markdown&text={message}'

    response = requests.get(url)

    return response.json()