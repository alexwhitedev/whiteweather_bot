# eb5881c20443bfd4f79d94615136837a
import requests


app_id = 'eb5881c20443bfd4f79d94615136837a'


def check_city(text):
    try:
        #check city in openweathermap data
        res = requests.get("http://api.openweathermap.org/data/2.5/find",
                     params={'q': text,
                             'type': 'like',
                             'units': 'metric',
                             'APPID': app_id})
        print(res)
        data = res.json()
        cities = ['{} ([])'.format(d['name'], d['sys']['country'])
                  for d in data['list']]
        print('city:', cities)
        city_id = data['list'][0]['id']
        print('city_id=', city_id)
        return city_id
    except Exception as e:
        print('Exception (find):', e)
        return 'Wrong city entered'
        pass


def current_forecast(user_cityID):
    try:
        #get current weather with city id
        res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                           params={'id': user_cityID,
                                   'type': 'like',
                                   'units': 'metric',
                                   'lang': 'ru',
                                   'APPID': app_id})
        print(res)
        data = res.json()
        
        print("conditions:", data['weather'][0]['description'])
        print("temp:", data['main']['temp'])
        print("temp_min:", data['main']['temp_min'])
        print("temp_max:", data['main']['temp_max'])
    except Exception as e:
        print("Exception (weather):", e)
        pass

    return data


def week_forecast(user_cityID):
    try:
        #get weather forecast for 5 days
        res = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                           params={'id': user_cityID, 'units': 'metric', 'lang': 'ru', 'APPID': app_id})
        data = res.json()
    except Exception as e:
        print("Exception (forecast):", e)
        pass

    return data
