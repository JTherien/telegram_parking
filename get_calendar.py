import os
import yaml
import requests
from icalendar import Calendar
import pandas as pd

def pull_calendar(config):

    CALENDAR_ID = config['calendar_id']
    URL = config['calendar_url']
    payload = {'client_id':CALENDAR_ID}

    return requests.get(URL, json=payload).text

def load_calendar(config):

    this_week = pd.Timestamp.now().to_period('W')
    this_week_file = f"{this_week.strftime('%Y-%m-%d')} calendar.csv"

    if os.path.exists(f'data/{this_week_file}'):

        events_this_week = pd.read_csv(f'data/{this_week_file}', parse_dates=['Date', 'Alert Date'])

    else:

        calendar = Calendar.from_ical(pull_calendar(config))

        events_this_week_lst = []

        for event in calendar.walk():
            
            if event.get('summary') != None:

                event_week = (
                    pd.to_datetime(event.get('dtstart').dt)
                    .to_period('W')
                    .start_time
                )

                if event_week == this_week.start_time:

                    events_this_week_lst.append(
                        [event.get('summary'), 
                        pd.to_datetime(event.get('dtstart').dt)]
                    )

        events_this_week = pd.DataFrame(events_this_week_lst, columns=['Name', 'Date'])
        events_this_week['Alert Date'] = events_this_week['Date'] - pd.Timedelta(1, 'D')
        events_this_week['Day'] = events_this_week['Date'].dt.day_name()

        events_this_week.to_csv(f'data/{this_week_file}', index=False)

    return events_this_week

if __name__ == '__main__':

    with open('config.yaml', 'r') as stream:

        config = yaml.safe_load(stream)

    load_calendar(config)