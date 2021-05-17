import requests as r
import json
from datetime import datetime


SLACK_WEBHOOK_URL = '<WEBHOOK_URL_HERE>'

# r.post(SLACK_WEBHOOK_URL, '{"text":"Hello, World!"}')

headers = {"accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
"accept-encoding": "gzip, deflate, br",
"accept-language": "en-US,en-IN;q=0.9,en;q=0.8",
"cache-control": "no-cache",
# "cookie": "ext_name=ojplmecpdpgccookcobabopnaifgidhf",
"pragma": "no-cache",
"sec-ch-ua": '" Not A;Brand";v="99", "Chromium";v="90", "Google Chrome";v="90"',
"sec-ch-ua-mobile": "?0",
"sec-fetch-dest": "document",
"sec-fetch-mode": "navigate",
"sec-fetch-site": "none",
"sec-fetch-user": "?1",
"upgrade-insecure-requests": "1",
"user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36"}

now = datetime.now()

current_time = now

cowin_api = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/calendarByDistrict?district_id=199&date={now.strftime('%d-%m-%Y')}"

res = r.get(cowin_api, headers=headers)

try:
    obj = json.loads(res.content)
except:
    r.post(SLACK_WEBHOOK_URL, json.dumps({"text":'Unable to parse API data'}))


# sample = {
#           "session_id": "3fa85f64-5717-4562-b3fc-2c963f66afa6",
#           "date": "31-05-2021",
#           "available_capacity": 50,
#           "available_capacity_dose1": 25,
#           "available_capacity_dose2": 25,
#           "min_age_limit": 18,
#           "vaccine": "COVISHIELD",
#           "slots": [
#             "FORENOON",
#             "AFTERNOON"
#           ]
#         }

len(obj['centers']) == 0

# try:


try:
    if len(obj['centers']) > 0:
        msg = ''
        for center in obj['centers']:
            sessions = center['sessions']
            sess_text = ''
            for sess in sessions:
                if sess["available_capacity_dose1"] > 0:
                    sess_text = sess_text + f'`{sess["available_capacity_dose1"]}` slot(s) available AT `{center["name"]}` FOR AGE `{sess["min_age_limit"]}` FOR DATE: `{sess["date"]}`, address: `{center["address"]}` TYPE: `{sess["vaccine"]}`\n\n'
            msg = msg + sess_text
        print(current_time, ': Sending slack notif: ', msg)
        if msg != '':
            r.post(SLACK_WEBHOOK_URL, json.dumps({"text":msg}))
    else:
        print(current_time, ': No data found')
except Exception as ex:
    print(current_time, ex)
    r.post(SLACK_WEBHOOK_URL, json.dumps({"text":f'Exception while parsing vaccine data: {str(ex)}'}))