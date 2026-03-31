# importing packages
import requests
import json
import time
from datetime import datetime, timedelta
web_wurl = "XXX"
web_turl = "XXX"
esp_turl = "XXX"
web_uurl = "XXX"
r = requests.get(web_wurl)
print(r.json())
def weather_api(latitude, longitude):
    wurl = f"https://api.open-meteo.com/v1/forecast?latitude={data['latitude']}&longitude={data['longitude']}&current=temperature_2m,weather_code&forecast_days=1"
    weather_data = requests.get(wurl).json()
    print(weather_data)
    w_data = (weather_data['current'])
    print(w_data)
    weather_code = w_data['weather_code']
    temperature = w_data['temperature_2m']
    print(f"Temperature: {temperature}")
    print(f"Weather Code: {weather_code}")

    return
def tiem_check():
    unpack_tiem = requests.get(web_turl)
    print(unpack_tiem.json())
    for tiem_id, tiem_data in unpack_tiem.json().items():
        print(tiem_id, tiem_data)
        if tiem_data['timer_minutes'] > 0:
            tiem = tiem_data['last_updated'].split('T')[1].split('.')[0]
            h, m, s = map(int, tiem.split(':'))
            total_seconds = h * 3600 + m * 60 + s
            relay_rest = (tiem_data['timer_minutes'] * 60)
            total_tiem = total_seconds + relay_rest
            if total_tiem <= current_time:
                payload = {f'{tiem_id}': 'OFF', }
                requests.patch(esp_turl, json=payload)
                web_payload = {f'{tiem_id}': {'state': 'OFF', 'timer_minutes': 0}}
                requests.patch(web_uurl, json=web_payload)
    time.sleep(1)
    return

for api_id, data in r.json().items():
    while True:
        try:
            current_local = ((time.localtime()))
            current_time = ((current_local.tm_hour * 3600) + (current_local.tm_min * 60) + current_local.tm_sec)
            print(current_time)
            if current_time % 600 == 0:
                weather_api(data['latitude'], data['longitude'])
                tiem_check()
            else:
                tiem_check()
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)