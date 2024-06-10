import requests
from dotenv import load_dotenv
import os
from twilio.rest import Client

load_dotenv()
account_sid = os.environ['TWILIO_ACCOUNT_SID']
auth_token = os.environ['TWILIO_AUTH_TOKEN']
txt_out_no = os.environ['TXT_OUT']
txt_in_no = os.environ['TXT_IN']

api_endpoint = "https://api.openweathermap.org/data/2.5/forecast"
owm_api_key = os.environ['OWM_API_KEY']

params = {
    "lat": -33.9258,
    "lon": 18.4232,
    "appid": owm_api_key,
    "cnt": 4,
}

r = requests.get(url=api_endpoint, params=params)
r.raise_for_status()
print(f"Status code: {r.status_code}")

data = r.json()
wx_list = [i["weather"][0]["id"] for i in data["list"]]

if any(i < 700 for i in wx_list):
    client = Client(account_sid, auth_token)
    message = client.messages \
                    .create(
                         body="Rain is forecast for today - bring an umbrella ☂️",
                         from_=txt_out_no,
                         to=txt_in_no,
                     )

    print(message.status)
