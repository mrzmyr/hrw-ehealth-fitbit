import fitbit
import gather_keys_oauth2 as Oauth2
import datetime
import json
import numpy as np
import pandas as pd
from terminaltables import AsciiTable

def to_csv_format(data):
    table = [['time', 'value']]
    steps_arr = steps['activities-steps-intraday']['dataset']
    for v in steps_arr[0:20]:
        table.append([v['time'], v['value']])
    return table

def print_as_table(data):
    print(AsciiTable(data).table)

def save_csv(path, data):
    df = pd.DataFrame(data)
    df.to_csv(path)

def save_json(path, data):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)

CLIENT_ID = '22D9HB'
CLIENT_SECRET = '11d2d00eb64f1647fb6ee92adc6c6e64'

server = Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])

authd_client = fitbit.Fitbit(
    CLIENT_ID,
    CLIENT_SECRET,
    oauth2=True,
    access_token=ACCESS_TOKEN,
    refresh_token=REFRESH_TOKEN
)

y = str((datetime.datetime.now() - datetime.timedelta(days=14)).strftime("%Y-%m-%d"))
steps = authd_client.intraday_time_series('activities/steps', base_date=y)
heart = authd_client.intraday_time_series('activities/heart', base_date=y)
profile = authd_client.user_profile_get()

steps_csv = to_csv_format(steps)
heart_csv = to_csv_format(heart)

save_csv('./dist/steps.csv', steps_csv)
save_csv('./dist/heart.csv', heart_csv)

save_json('./dist/steps.json', steps)
save_json('./dist/heart.json', heart)
save_json('./dist/profile.json', profile)

print('Steps:')
print('-'*20)
print_as_table(steps_csv)

print('Heart:')
print('-'*20)
print_as_table(heart_csv)

authd_client.sleep()
