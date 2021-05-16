
import telegram_send

import requests

import time

import smtplib
import pprint
import pandas as pd
from requests.api import head

from requests.sessions import session
print = pprint.PrettyPrinter()

url_states = "https://cdn-api.co-vin.in/api/v2/admin/location/states"

url_districts = "https://cdn-api.co-vin.in/api/v2/admin/location/districts/15"

url_for_findbydist = f"https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/findByDistrict"



headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
            "Authorization": "auth_bear"
            ,"Accept-Language": "en_US"}

def send_mail(date):
    with requests.session() as session:
        fin_end_point = url_for_findbydist+f"?district_id={district_id}&date={date}"
        response = session.get(url = fin_end_point,headers=headers)

        response = response.json()

        for session in response['sessions']:

            #For Age not equal to 45 and capacity is above zero
            if (session['min_age_limit'] != 45) & (session['available_capacity'] > 0):
                message_string=f"Subject:  Alert'!! \n\n Available - {session['available_capacity']} in {session['name']} on {session['date']} for the age {session['min_age_limit']} and link https://www.cowin.gov.in/home "

                telegram_send.send(messages=[message_string])






res = requests.get(url_districts,headers=headers)
district = "Ranchi"

today = time.strftime("%d-%m-%Y")

datelist = pd.date_range(today, periods=7).tolist()



re = res.json()

a=re['districts']
rp = pd.DataFrame.from_dict(a)

ind = rp['district_name'].loc[lambda x: x=='Ranchi'].index
district_id= int(rp.loc[ind]["district_id"])

print.pprint(district_id)

# import daemon

# with daemon.DaemonContext():
while True:

    with requests.session() as session:

        for date in datelist:
            date = date.strftime("%d-%m-%Y")
            send_mail(date)

    time.sleep(1000)

