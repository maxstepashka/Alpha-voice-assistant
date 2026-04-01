import os
import json
import time
import webbrowser
import sys
from pathlib import Path
import pyaudio
import vosk
import keyboard
import speech_recognition
from termcolor import colored

vosk.SetLogLevel(-1)

with open(Path('config/config.json').resolve(), 'r', encoding='UTF-8') as data:
    config = json.load(data)
    data.close()


if config['wakeword'] == '' or config['wakeword'] == ' ':
    wakeword = "альфа"
else:
    wakeword = tuple(config['wakeword'].lower().replace(',', '').split())

time_wait = float(config['accept_time'])

match config['search_system']:
    case 'Яндекс':
        search_url = 'https://yandex.ru/search/?text='
    case 'Google':
        search_url = 'https://www.google.com/search?q='
    case 'Bing':
        search_url = 'https://www.bing.com/search?q='
    case 'DuckDuckGo':
        search_url = 'https://duckduckgo.com/?q='

match config['music_search_system']:
    case 'Яндекс Музыка':
        music_search_url = 'https://music.yandex.ru/search?text='
    case 'Звук':
        music_search_url = 'https://zvuk.com/search?query='

match config['video_search_system']:
    case 'ВК Видео':
        video_search_url = 'https://vkvideo.ru/?q='
    case 'Rutube':
        video_search_url = 'https://rutube.ru/search/?query='
    

model = vosk.Model(f'vosk-model-small-ru-{config["vosk_version"]}')

recognition = config['recognition_type']


to_replace = ['найди ', 'поищи', 'включи ', 'включить ', 'включил ', 'музыка ', 'музыку ', 'песня ', 'песню', 'видео ']
to_replace_write = ['напиши', 'введи']
to_replace_special = [['точка с запятой', ';'], ['запятая', ','], ['точка', '.'], ['дефис ', '-'], ['двоеточие', ':'], ['знак вопроса', '?'], ['восклицательный знак', '!']]


recognizer_vosk = vosk.KaldiRecognizer(model, 16000)

audio = pyaudio.PyAudio()

stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


microphone = speech_recognition.Microphone()

recognizer_sr = speech_recognition.Recognizer()

time_ = 0


def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (recognizer_vosk.AcceptWaveform(data)) and (len(data) > 0):
            cmd_recognized = json.loads(recognizer_vosk.Result())
            if cmd_recognized['text']:
                yield cmd_recognized['text']


def open_app(parameter):
    os.startfile(parameter)

def open_site(parameter):
    webbrowser.open(parameter)

def python(parameter):
    eval(parameter)

def command_line(parameter):
    os.system(parameter)


def search(parameter):
    query = cmd_recognized.lower()
    for i in wakeword:
        query = query.replace(i + ' ', '')
    query = query.lower().replace('найди ', '')
    webbrowser.open(search_url + query)

def search_song(parameter):
    query = cmd_recognized.lower()
    for i in wakeword:
        query = query.replace(i + ' ', '')
    for i in to_replace:
        query = query.replace(i, '')
    webbrowser.open(music_search_url + query)

def search_video(parameter):
    query = cmd_recognized.lower()
    for i in wakeword:
        query = query.replace(i + ' ', '')
    for i in to_replace:
        query = query.replace(i, '')
    webbrowser.open(video_search_url + query)


def browser(parameter):
    eval(f'{parameter}()')

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



def windows(parameter):
    eval(f'{parameter}()')

def rollup():
    keyboard.send('windows+down')

def unwrap():
    keyboard.send('windows+up')

def close():
    keyboard.send('alt+f4')

def explorer():
    os.startfile("explorer.exe")

def calculator():
    os.startfile("calc.exe")

def notepad():
    os.startfile("notepad.exe")

def language():
    keyboard.press('alt')
    keyboard.send('shift')
    keyboard.release('alt')


def write_text(parameter):
    text_to_write = cmd_recognized.lower()
    for i in wakeword:
        text_to_write = text_to_write.replace(i + ' ', '')
    for i in to_replace_write:
        text_to_write = text_to_write.replace(i + ' ', '')
    for i in to_replace_special:
        text_to_write = text_to_write.replace(' ' + i[0], i[1])
    keyboard.write(text_to_write + ' ')


def script(parameter):
    with open(Path('config/scripts.json').resolve(), 'r', encoding='UTF-8') as data:
        scripts = json.load(data)
        data.close()
    for i in scripts[parameter]['actions']:
        eval(i)
        time.sleep(0.1)


def process(cmd):
    exec = False
    global time_
    if cmd.startswith(wakeword) or time.time() - time_ < time_wait:
        if cmd.startswith(wakeword):
            time_ = time.time()
        print(colored('Распознано:' , color='white', on_color=(255,95,0), attrs=['bold']), end=' ')
        print(cmd)
        cmd = cmd.split()

        
        with open(Path('config/weights.json').resolve(), 'r', encoding='UTF-8') as f:
            weights = json.load(f)
            f.close()


        for word in cmd:
            try:
                keyword_index = 0
                for keyword_index in range(len(keywords['main'][word])):
                    weights['main'][keywords['main'][word][keyword_index]['parameter']] += keywords['main'][word][keyword_index]['weight']
            except:
                pass

        category = max(weights['main'], key = weights['main'].get)

        for word in cmd:
            try:
                keyword_index = 0
                for keyword_index in range(len(keywords[category][word])):
                    weights[category][keywords[category][word][keyword_index]['parameter']] += keywords[category][word][keyword_index]['weight']
                exec = True
            except:
                pass


        if exec:
            parameter = max(weights[category], key = weights[category].get)
            eval(f'{category}(r"{parameter}")')
        else:
            pass


with open(Path('config/keywords.json').resolve(), 'r', encoding='UTF-8') as f:
    keywords = json.load(f)
    f.close()


with microphone as source:
    if recognition == 'Speech Recognition':
        recognizer_sr.adjust_for_ambient_noise(source, duration=1)
        print(colored('Информация:' , color='white', on_color=(255,95,0), attrs=['bold']), end=' ')
        print('Голосовой ассистент готов к использованию.')
        while True:
            cmd_recognized = recognizer_sr.listen(source)
            try:
                cmd_recognized = recognizer_sr.recognize_google(cmd_recognized, language='ru-RU')
                process(cmd_recognized.lower())
            except:
                pass
    else:
        print(colored('Информация:' , color='white', on_color=(255,95,0), attrs=['bold']), end=' ')
        print('Голосовой ассистент готов к использованию.')
        for cmd_recognized in listen():
            process(cmd_recognized.lower())