import yaml
import pandas as pd
from get_calendar import load_calendar
from telegram import send_message

if __name__ == '__main__':

    with open('config.yaml', 'r') as stream:

        config = yaml.safe_load(stream)

emoji = {
    'automobile':u'\U0001F697'
}

today = pd.Timestamp.now()

calendar = load_calendar(config)

event_str = [f"{emoji['automobile']} *PARKING NOTIFICATION*"]

for i, event in calendar.iterrows():

    if event['Alert Date'].date() == today.date():

        event_str.append(f"{event['Day']}: {event['Name']}")

if len(event_str) > 1:
    
    message = '\n'.join(event_str)
    
    send_message(message, config)