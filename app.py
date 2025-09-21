import os
import json
import time
import webbrowser
import logging
import sys
import pyaudio
from vosk import Model, KaldiRecognizer
import keyboard
from pathlib import Path
import speech_recognition as sr


with open(Path('files/config.json').resolve(), 'r', encoding='UTF-8') as data:
    config = json.load(data)
    data.close()


if config['wakeword'] == '' or config['wakeword'] == ' ':
    wakeword = "альфа"
else:
    wakeword = tuple(config['wakeword'].lower().replace(',', '').split())

time_wait = config['time']

match config['search']:
    case 'Яндекс':
        search_url = 'https://yandex.ru/search/?text='
    case 'Google':
        search_url = 'https://www.google.com/search?q='
    case 'Bing':
        search_url = 'https://www.bing.com/search?q='
    case 'DuckDuckGo':
        search_url = 'https://duckduckgo.com/?q='

match config['music_search']:
    case 'Яндекс Музыка':
        music_search_url = 'https://music.yandex.ru/search?text='
    case 'Звук':
        music_search_url = 'https://zvuk.com/search?query='

match config['video_search']:
    case 'ВК Видео':
        video_search_url = 'https://vkvideo.ru/?q='
    case 'Rutube':
        video_search_url = 'https://rutube.ru/search/?query='
    

if config['model'] == '0.22':
    model = Model('vosk-model-small-ru-0.22')
elif config['model'] == '0.4':
    model = Model('vosk-model-small-ru-0.4')

recognition = config['recognition']


to_replace = ['найди ', 'поищи', 'включи ', 'включить ', 'включил ', 'музыка ', 'музыку ', 'песня ', 'песню', 'видео ']
to_replace_write = ['напиши', 'введи']
to_replace_special = [['точка с запятой', ';'], ['запятая', ','], ['точка', '.'], ['дефис ', '-'], ['двоеточие', ':'], ['знак вопроса', '?'], ['восклицательный знак', '!']]


rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(message)s')

mic = sr.Microphone()

r = sr.Recognizer()

time_ = 0


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            cmd_recognized = json.loads(rec.Result())
            if cmd_recognized['text']:
                yield cmd_recognized['text']


def open_app(param):
    os.startfile(param)

def open_site(param):
    webbrowser.open(param)

def python(param):
    eval(param)

def command_line(param):
    os.system(param)


def search(param):
    zapros = cmd_recognized.lower()
    for i in wakeword:
        zapros = zapros.replace(i + ' ', '')
    zapros = zapros.lower().replace('найди ', '')
    webbrowser.open(search_url + zapros)

def search_song(param):
    zapros = cmd_recognized.lower()
    for i in wakeword:
        zapros = zapros.replace(i + ' ', '')
    for i in to_replace:
        zapros = zapros.replace(i, '')
    webbrowser.open(music_search_url + zapros)

def search_video(param):
    zapros = cmd_recognized.lower()
    for i in wakeword:
        zapros = zapros.replace(i + ' ', '')
    for i in to_replace:
        zapros = zapros.replace(i, '')
    webbrowser.open(video_search_url + zapros)


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
    text_to_write = cmd_recognized.lower()
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


def process(cmd):
    exec = False
    global time_
    if cmd.startswith(wakeword) or time.time() - time_ < time_wait:
        if cmd.startswith(wakeword):
            time_ = time.time()
        logging.info('Распознано: ' + cmd)
        cmd = cmd.split()

        
        with open(Path('files/weights.json').resolve(), 'r', encoding='UTF-8') as f:
            weights = json.load(f)
            f.close()


        for word in cmd:
            try:
                keyword_index = 0
                for keyword_index in range(len(keywords['main'][word])):
                    weights['main'][keywords['main'][word][keyword_index]['param']] += keywords['main'][word][keyword_index]['weight']
            except:
                pass

        category = max(weights['main'], key = weights['main'].get)

        for word in cmd:
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


with open(Path('files/keywords.json').resolve(), 'r', encoding='UTF-8') as f:
    keywords = json.load(f)
    f.close()


with mic as source:
    if recognition == 'Speech Recognition':
        r.adjust_for_ambient_noise(source, duration=1)
        while True:
            cmd_recognized = r.listen(source)
            try:
                cmd_recognized = r.recognize_google(cmd_recognized, language='ru-RU')
                process(cmd_recognized.lower())
            except:
                pass
    else:
        for cmd_recognized in listen():
            process(cmd_recognized.lower())
