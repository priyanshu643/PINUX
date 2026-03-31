# importing packages
import requests
import time
#Addin the API to make calls, post, patch.
# This ure is for taking the lon and lat from the user.
# the form of {'latitude' : 'xyz', 'longitude' : 'xyz'}
web_wurl = "XXX"
# This API call will get the data from the website/ web interface.
web_turl = "XXX"
# This API will inform the ESP to turn off the relay and turn on the relay.
esp_turl = "XXX"
# This API will help to update the changes on the website/ webinterface, only those changes which are updated by the python database code.
web_uurl = "XXX"
# This is to make the request and ask the user for the data of lon, lat
r = requests.get(web_wurl)
# print the hole json format data of lon
print(r.json())
# defining a function to get the weather report from the.
def weather_api(latitude, longitude):
    # This api will extract the data for weather.
    wurl = f"https://api.open-meteo.com/v1/forecast?latitude={latitude}&longitude={longitude}&current=temperature_2m,weather_code&forecast_days=1"
    # customizing the data to get the output as we want.
    weather_data = requests.get(wurl).json()
    print(weather_data)
    w_data = (weather_data['current'])
    print(w_data)
    weather_code = w_data['weather_code']
    temperature = w_data['temperature_2m']
    print(f"Temperature: {temperature}")
    print(f"Weather Code: {weather_code}")
    # ending the function by using return.
    return
# This function will take the time from the user and then customize that data and post the relay state according to it.
def tiem_check(current_time):
    # this will make the request from the API
    unpack_tiem = requests.get(web_turl)
    print(unpack_tiem.json())
    # This api will extract the data for time and after that dealy turn the rely off
    for tiem_id, tiem_data in unpack_tiem.json().items():
        print(tiem_id, tiem_data)
        if tiem_data['state'] == 'ON' and tiem_data['timer_minutes'] > 0:
            tiem = tiem_data['last_updated'].split('T')[1].split('.')[0]
            h, m, s = map(int, tiem.split(':'))
            total_seconds = h * 3600 + m * 60 + s
            relay_rest = (tiem_data['timer_minutes'] * 60)
            total_tiem = total_seconds + relay_rest
            if total_tiem <= current_time:
                #  payload is for esp to update the state
                # web_payload is for website to update it's state that the realy is turn of by the code
                payload = {f'{tiem_id}': 'OFF', }
                requests.patch(esp_turl, json=payload)
                web_payload = {f'{tiem_id}': {'state': 'OFF', 'timer_minutes': 0}}
                requests.patch(web_uurl, json=web_payload)
        else:
            payload = unpack_tiem.json()
            requests.patch(esp_turl, json=payload)
    time.sleep(1)
    return
# calling the location data from the website
r = requests.get(web_wurl)
print(r.json())
for api_id, data in r.json().items():
    while True:
        try:

            print(r.json())
            current_local = ((time.gmtime()))
            current_time = ((current_local.tm_hour * 3600) + (current_local.tm_min * 60) + current_local.tm_sec)
            print(current_time)
            if current_time % 600 == 0:
                weather_api(data['latitude'], data['longitude'])
                tiem_check(current_time)
            else:
                tiem_check(current_time)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)