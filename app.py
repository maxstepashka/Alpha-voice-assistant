import os
import json
import time
import webbrowser
import logging

import pyaudio
from vosk import Model, KaldiRecognizer
import keyboard
from pathlib import Path
import speech_recognition as sr



# Загрузка сохранённых данных
with open(Path('files/config.json').resolve(), 'r', encoding='UTF-8') as data:
    config = json.load(data)
    data.close()




# Активационная фраза
if config['wakeword'] == '' or config['wakeword'] == ' ':
    wakeword = "альфа"
else:
    wakeword = tuple(config['wakeword'].lower().replace(',', '').split())

# Время приёма команд без активационной фразы
time_wait = config['time']


# Модель распознавания речи
if config['model'] == '0.22':
    model = Model('vosk-model-small-ru-0.22')
elif config['model'] == '0.4':
    model = Model('vosk-model-small-ru-0.4')

# Вариант распознавания
recognition = config['recognition']


# Массивы с ключевыми словами, которые нужно удалить из команды или изменить
to_replace = ['найди ', 'поищи', 'включи ', 'включить ', 'включил ', 'музыка ', 'музыку ', 'песня ', 'песню', 'видео ']
to_replace_write = ['напиши', 'введи']
to_replace_special = [['точка с запятой', ';'], ['запятая', ','], ['точка', '.'], ['дефис ', '-'], ['двоеточие', ':'], ['знак вопроса', '?'], ['восклицательный знак', '!']]

# Неизменяемые данные

language = 'ru'

rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

mic = sr.Microphone()

r = sr.Recognizer()

time_ = 0



# Распознавание речи
def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            com_rec = json.loads(rec.Result())
            if com_rec['text']:
                yield com_rec['text']




# Функции
def open_app(param):
    os.startfile(param)



def open_site(param):
    webbrowser.open(param)



def search(param):
    zapros = com_rec.lower()
    for i in wakeword:
        zapros = zapros.replace(i + ' ', '')
    zapros = zapros.lower().replace('найди ', '')
    webbrowser.open('https://yandex.ru/search/?text=' + zapros)



def search_song(param):
    zapros = com_rec.lower()
    for i in wakeword:
        zapros = zapros.replace(i + ' ', '')
    for i in to_replace:
        zapros = zapros.replace(i, '')
    webbrowser.open('https://music.yandex.ru/search?text=' + zapros)



def search_video(param):
    zapros = com_rec.lower()
    for i in wakeword:
        zapros = zapros.replace(i + ' ', '')
    for i in to_replace:
        zapros = zapros.replace(i, '')
    webbrowser.open('https://vkvideo.ru/?q=' + zapros)



def browser(param):
    eval(f'{param}()')



def new_tab():
    keyboard.send('ctrl+t')



def incognito_tab():
    keyboard.send('ctrl+shift+n')



def prev_tab():
    keyboard.send('ctrl+shift+tab')



def next_tab():
    keyboard.send('ctrl+tab')



def down():
    keyboard.send('pagedown')



def up():
    keyboard.send('pageup')



def end():
    keyboard.send('end')



def home():
    keyboard.send('home')



def windows(param):
    eval(f'{param}()')



def rollup():
    keyboard.send('windows+down')



def unwrap():
    keyboard.send('windows+up')



def close():
    keyboard.send('alt+f4')



def explorer():
    keyboard.send('windows+e')

def language():
    keyboard.press('alt')
    keyboard.send('shift')
    keyboard.release('alt')



def write_text(param):
    text_to_write = com_rec.lower()
    for i in wakeword:
        text_to_write = text_to_write.replace(i + ' ', '')
    for i in to_replace_write:
        text_to_write = text_to_write.replace(i + ' ', '')
    for i in to_replace_special:
        text_to_write = text_to_write.replace(' ' + i[0], i[1])
    keyboard.write(text_to_write + ' ')



def script(param):
    with open(Path('files/scripts.json').resolve(), 'r', encoding='UTF-8') as data:
        scripts = json.load(data)
        data.close()
    for i in scripts[param][0]:
        eval(i)
        time.sleep(0.1)

    



def main_func(com):
    exec = False
    global time_
    if com.startswith(wakeword) or time.time() - time_ < time_wait:
        if com.startswith(wakeword):
            time_ = time.time()
        logging.info('Распознано: ' + com)
        com = com.split()

        # Веса категорий и параметров
        with open(Path('files/weights.json').resolve(), 'r', encoding='UTF-8') as f:
            weights = json.load(f)
            f.close()

        # Определение весов
        for word in com:
            try:
                keyword_index = 0
                for keyword_index in range(len(keywords['main'][word])):
                    weights['main'][keywords['main'][word][keyword_index]['param']] += keywords['main'][word][keyword_index]['weight']
            except:
                pass

        category = max(weights['main'], key = weights['main'].get)

        for word in com:
            try:
                keyword_index = 0
                for keyword_index in range(len(keywords[category][word])):
                    weights[category][keywords[category][word][keyword_index]['param']] += keywords[category][word][keyword_index]['weight']
                exec = True
            except:
                pass


        # Исполнение команды
        if exec:
            param = max(weights[category], key = weights[category].get)
            eval(f'{category}(r"{param}")')
        else:
            pass



# Ключевые фразы
with open(Path('files/keywords.json').resolve(), 'r', encoding='UTF-8') as f:
    keywords = json.load(f)
    f.close()



# Основной цикл
with mic as source:
    if recognition == 'Google Speech Recognition':
        r.adjust_for_ambient_noise(source, duration=1)
        while True:
            com_rec = r.listen(source)
            try:
                com_rec = r.recognize_google(com_rec, language='ru-RU')
                main_func(com_rec.lower())
            except:
                pass
    else:
        for com_rec in listen():
            main_func(com_rec.lower())
