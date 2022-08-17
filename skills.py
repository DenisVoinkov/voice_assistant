import os
import webbrowser
import sys
import subprocess
import requests
import pyttsx3
import voice
import random


def browser():
    '''
    open browser with url link
    '''

    webbrowser.open('https://www.google.com', new=2)


def weather():
    '''
    info about weather
    '''

    try:
        params = {'q': 'Prague', 'units': 'metric', 'lang': 'ru', 'appid': '853b717c60d81964623ff98fc524a816'}
        response = requests.get(f'https://api.openweathermap.org/data/2.5/weather', params=params)

        if not response:
            raise

        w = response.json()
        voice.speaker(f"На улице {w['weather'][0]['description']} {round(w['main']['temp'])} градусов")

    except:
        voice.speaker('Произошла ошибка при попытке запроса к ресурсу API, проверть код')


def passive():
    '''
    функция заглушки при простом разговоре с ботом
    '''
    pass


def play_greetings():

    greetings = [
        'Здравствуйте, чем могу быть полезна?',
        'Приветствую, как я могу помочь?',
        'Добрый день, буду рада вам помочь',
        'Привет, готова помогать',
    ]

    voice.speaker(greetings[random.randint(0, len(greetings) - 1)])


def play_bye():

    bye = [
        'Прощайте',
        'До свидания',
        'Завершаю работу',
        'Прекращаю работу',
    ]

    voice.speaker(bye[random.randint(0, len(bye) - 1)])
    print('Моргана завершила работу...')
    sys.exit()
