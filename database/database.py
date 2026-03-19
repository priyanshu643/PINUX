# importing packages
import requests
import json
import time
web_wurl = "XXX"
web_turl = "XXX"
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
    print(f"Temperature: {w_data['temperature_2m']}")
    print(f"Weather Code: {w_data['weather_code']}")
    time.sleep(10 * 60)
    return

for api_id, data in r.json().items():

    while True:
        try:
            weather_api(data['latitude'], data['longitude'])

        except:
            print("API Error")
            time.sleep(5)