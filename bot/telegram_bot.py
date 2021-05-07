import telebot
import requests
import config
from telebot import types
import database
from geopy.geocoders import Nominatim
import json

class Bot:
    bot = telebot.TeleBot(config.API_TOKEN)
    API_KEY_FOR_WEATHER = 'f205cd59a0ce301860a67739db7d51e6'
    base = database.SQL('users.db')

    @staticmethod
    @bot.message_handler(commands=['start'])
    def welcome(message):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        first = types.KeyboardButton('Узнать погоду')
        markup.add(first)
        Bot.bot.send_message(message.chat.id,
                             "Добро пожаловать, {0.first_name}!".format(message.from_user,
                                                                        Bot.bot.get_me()), reply_markup=markup)

    @staticmethod
    @bot.message_handler(content_types=['text'])
    def echo(message):
        if message.chat.type == 'private':
            if message.text == 'Узнать погоду':
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
                if Bot.base.checkuser(message.chat.id):
                    markup.add(types.KeyboardButton(Bot.base.getcity(message.chat.id)))
                markup.add(types.KeyboardButton('Ввести город'))
                Bot.bot.send_message(message.chat.id, "Выберите желаемое", Bot.bot.get_me(), reply_markup=markup)
            elif message.text == 'Ввести город':
                Bot.bot.send_message(message.chat.id, "Введите город:")
                Bot.bot.register_next_step_handler(message, Bot.get_city)
            else:
                Bot.get_the_forecast(message.chat.id, message.text)

    @staticmethod
    def get_city(message):
        Bot.get_the_forecast(message.chat.id, message.text)

    @staticmethod
    def get_the_forecast(chat_id, text):
        try:
            print(text)
            geolocator = Nominatim(user_agent='bot')
            location = geolocator.geocode(text)
            lat = location.latitude
            long = location.longitude
            weather_req = requests.get(
                'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&appid={}'.format(lat, long, Bot.API_KEY_FOR_WEATHER))
            current_weather = json.loads(weather_req.text)['current']
            temp = round(current_weather['temp'] - 273.15)
            feels_like = round(current_weather['feels_like'] - 273.15)
            clouds = current_weather['clouds']
            wind_speed = current_weather['wind_speed']
            print(json.loads(weather_req.text))
            Bot.base.add(chat_id, text)
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
            markup.add(types.KeyboardButton('Узнать погоду'))
            Bot.bot.send_message(chat_id, 'Текущая температура воздуха: {} °C, '
                                          'ощущается как {} °C, скорость ветра - {} м/с'.format(str(temp), str(feels_like), str(wind_speed)), Bot.bot.get_me(), reply_markup=markup)
        except:
            Bot.bot.send_message(chat_id, 'Неправильный город, попробуйте ещё раз')