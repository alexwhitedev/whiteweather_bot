import telebot
# import requests
# import re
import json
import weather
import schedule
import time
from multiprocessing import Process
import datetime


pattern = r'[^\,a-z]'


bot = telebot.TeleBot('857408920:AAGS34mfcLMRVsQsW17CMGM3n01QGXB2H-0')

keyboard1 = telebot.types.ReplyKeyboardMarkup(True)
keyboard2 = telebot.types.ReplyKeyboardRemove(True)
keyboard1.row('Current', 'Today', 'Week', 'Change city')


# def schedule_message():
    # bot.send_message(344900233, "wake up!")


# schedule.every(0.2).minutes.do(schedule_message)


# while True:
#     schedule.run_pending()
#     time.sleep(1)

def schedule_message():
    while True:
        print(str(datetime.datetime.now())[11:16])
        if str(datetime.datetime.now())[11:16] == "07:00":
            try:
                with open('data.json') as file:
                    data = json.load(file)
            except Exception as e:
                print("Exception:", e)
                data = []
            print(data)
            for i in data:
                print(data)
                for key in i:
                    # print(key)
                    user_city_id = i[key]["city_ID"]
                    user_city = i[key]["city"]
                    data1 = weather.week_forecast(user_city_id)
                    send_message = "city: " + user_city + "; Today\n"
                    bot.send_message(str(key), send_message)
                    print(data1['list'])
                    send_message = data1['list'][0]['dt_txt'].split(' ')[0] + '\n'
                    tmp = data1['list'][0]['dt_txt'].split(' ')[0]
                    for с in data1['list']:
                        if tmp == str(с['dt_txt'].split(' ')[0]):
                            send_message += str(с['dt_txt'].split(' ')[1]) + '\n\t{0:+3.0f}'.format(
                                с['main']['temp']) + ', ' + \
                                            str(с['weather'][0]['description']) + '\n'
                        else:
                            bot.send_message(str(key), send_message, reply_markup=keyboard1)
                            break

        time.sleep(60)


p1 = Process(target=schedule_message, args=())
p1.start()


def read_json(id, col):
    try:
        data = json.load(open('data.json'))
    except Exception as e:
        print("Exception:", e)
        data = []

    for i in data:
        if i[str(id)]:
            return i[str(id)][col]
        else:
            print('Not id in data')


def write_json(id, user_city, user_city_ID):
    try:
        with open('data.json', 'r') as file:
            data = json.load('data.json')
    except Exception as e:
        print("Exception:", e)
        data = []

    if id not in data:
        data.append({
            id: {
                "city": user_city,
                "city_ID": user_city_ID
            }
        })

    with open('data.json', 'w') as file:
        json.dump(data, file, indent=2, ensure_ascii=False)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, '''Привет, я бот, помогающий тебе следить за погодой.
                                      \nВведи город и страну в формате \n[город],[сокращенное название страны]\
                                      \nНа англ языке
                                      \nНапример, Kyiv,UA''',
                     reply_markup=keyboard2)


@bot.message_handler(content_types=['text'])
def send_text(message):
    user_city_id = read_json(message.chat.id, "city_ID")
    user_city = read_json(message.chat.id, "city")

    if message.text == 'Current':
        data = weather.current_forecast(user_city_id)
        send_message = ''
        send_message += "city: " + user_city + "; Current\n"
        bot.send_message(message.chat.id, send_message, reply_markup=keyboard1)
        send_message = str(data['main']['temp']) + ', ' + str(data['weather'][0]['description'])
        bot.send_message(message.chat.id, send_message, reply_markup=keyboard1)

    elif message.text == 'Today':
        data = weather.week_forecast(user_city_id)
        send_message = ''
        send_message += "city: " + user_city + "; Today\n"
        bot.send_message(message.chat.id, send_message)
        send_message = data['list'][0]['dt_txt'].split(' ')[0] + '\n'
        tmp = data['list'][0]['dt_txt'].split(' ')[0]
        for i in data['list']:
            if tmp == str(i['dt_txt'].split(' ')[0]):
                send_message += str(i['dt_txt'].split(' ')[1]) + '\n\t{0:+3.0f}'.format(i['main']['temp']) + ', ' + \
                                str(i['weather'][0]['description']) + '\n'
            else:
                bot.send_message(message.chat.id, send_message, reply_markup=keyboard1)
                break

    elif message.text == 'Week':
        data = weather.week_forecast(user_city_id)
        send_message = ''
        send_message += "city: " + user_city + "; Week\n"
        bot.send_message(message.chat.id, send_message)
        send_message = data['list'][0]['dt_txt'].split(' ')[0] + '\n'
        tmp = data['list'][0]['dt_txt'].split(' ')[0]
        for i in data['list']:
            if tmp == str(i['dt_txt'].split(' ')[0]):
                send_message += str(i['dt_txt'].split(' ')[1]) + '\n\t{0:+3.0f}'.format(i['main']['temp']) + ', ' + \
                                str(i['weather'][0]['description']) + '\n'
            else:
                bot.send_message(message.chat.id, send_message, reply_markup=keyboard1)
                send_message = str(i['dt_txt'].split(' ')[0]) + '\n'
                tmp = str(i['dt_txt'].split(' ')[0])


    elif message.text == 'Change city':
        bot.send_message(message.chat.id, '\nВведи город и страну в формате\n[город],[сокращенное название страны]\n\
                                 Например, Kyiv,UA', reply_markup = keyboard2)

    else:
        write_json(message.chat.id, message.text, weather.check_city(message.text))
        bot.send_message(message.chat.id, '\nВыберите один из пунтктов меню', reply_markup=keyboard1)


bot.polling()

