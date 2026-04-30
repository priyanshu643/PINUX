# importing packages
import requests
import time
#Addin the API to make calls, post, patch.
# This ure is for taking the lon and lat from the user.
# the form of {'latitude' : 'xyz', 'longitude' : 'xyz'}
web_wurl = "https://hospital-management-syst-2aa93-default-rtdb.asia-southeast1.firebasedatabase.app/test_locations.json"
# This API call will get the data from the website/ web interface.
web_turl = "https://hospital-management-syst-2aa93-default-rtdb.asia-southeast1.firebasedatabase.app/devices.json"
# This API will inform the ESP to turn off the relay and turn on the relay.
esp_turl = "https://hospital-management-syst-2aa93-default-rtdb.asia-southeast1.firebasedatabase.app/payload.json"
# This API will help to update the changes on the website/ webinterface, only those changes which are updated by the python database code.
web_uurl = "https://hospital-management-syst-2aa93-default-rtdb.asia-southeast1.firebasedatabase.app/web_payload.json"
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
    if not unpack_tiem.json():
        return
        
    print("Checking timers for all devices...")
    
    # We will collect all changes and send them in ONE go to save the ESP32 from spam
    payload_to_send = {}
    web_payload_to_send = {}

    for tiem_id, tiem_data in unpack_tiem.json().items():
        if tiem_data['state'] == 'ON' and tiem_data['timer_minutes'] > 0:
            tiem = tiem_data['last_updated'].split('T')[1].split('.')[0]
            h, m, s = map(int, tiem.split(':'))
            total_seconds = h * 3600 + m * 60 + s
            relay_rest = (tiem_data['timer_minutes'] * 60)
            total_tiem = total_seconds + relay_rest
            
            if total_tiem <= current_time:
                print(f"Timer Finished for {tiem_id}!")
                payload_to_send[tiem_id] = 'OFF'
                web_payload_to_send[tiem_id] = {'state': 'OFF', 'timer_minutes': 0}
        else:
            # If no timer is active, just ensure the ESP matches the current state
            payload_to_send[tiem_id] = tiem_data['state']

    # Send consolidated updates only if we have data
    if payload_to_send:
        requests.patch(esp_turl, json=payload_to_send)
    if web_payload_to_send:
        requests.patch(web_uurl, json=web_payload_to_send)

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