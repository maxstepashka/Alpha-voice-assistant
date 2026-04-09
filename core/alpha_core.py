import os
import json
import time
import webbrowser
import sys
import copy
from pathlib import Path
import pyaudio
import vosk
import keyboard
from termcolor import colored

vosk.SetLogLevel(-1)

with open(Path('config/config.json').resolve(), 'r', encoding='UTF-8') as config_file:
    config = json.load(config_file)

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


to_replace = ['найди ', 'поищи', 'включи ', 'включить ', 'включил ', 'музыка ', 'музыку ', 'песня ', 'песню', 'видео ']
to_replace_write = ['напиши', 'введи']
to_replace_special = [['точка с запятой', ';'], ['запятая', ','], ['точка', '.'], ['дефис ', '-'], ['двоеточие', ':'], ['знак вопроса', '?'], ['восклицательный знак', '!']]


recognizer_vosk = vosk.KaldiRecognizer(model, 16000)

audio = pyaudio.PyAudio()

stream = audio.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()


time_of_execution = 0


def listen():
    while True:
        data = stream.read(num_frames=4000, exception_on_overflow=False)
        if (recognizer_vosk.AcceptWaveform(data)) and (len(data) > 0):
            text = json.loads(recognizer_vosk.Result())
            if text['text']:
                yield text['text']


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
    for i in scripts[parameter]['actions']:
        eval(i)
        time.sleep(0.1)


def process(cmd):
    execute = False

    global time_of_execution
    if cmd.startswith(wakeword) or time.time() - time_of_execution < time_wait:
        if cmd.startswith(wakeword):
            time_of_execution = time.time()
        print(colored('Распознано:' , color='white', on_color=(255,95,0), attrs=['bold']), end=' ')
        print(cmd)
        for word in wakeword:
            cmd = cmd.replace(word, '')

        cmd = cmd.split()

        weights = copy.deepcopy(weights_template)

        words_to_remove = []
        # Перебор команды для определения категории
        for word in cmd:
            # try ... except для проверки наличия ключа в словаре
            try:
                for keyword_index in range(len(keywords['main'][word])):
                    # Повышение общего веса категории
                    weights['main'][keywords['main'][word][keyword_index]['parameter']] += keywords['main'][word][keyword_index]['weight']
            except KeyError:
                words_to_remove.append(word)

        # Удаление слов, которые не влияют на результат
        for word in words_to_remove:
            cmd.remove(word)

        # Определение категории с максимальным весом
        category = max(weights['main'], key = weights['main'].get)

        # Перебор команды для определения параметра
        for word in cmd:
            # try ... except для проверки наличия ключа в словаре
            try:
                for keyword_index in range(len(keywords[category][word])):
                    # Повышение общего веса параметра
                    weights[category][keywords[category][word][keyword_index]['parameter']] += keywords[category][word][keyword_index]['weight']
                # Если хоть одно слово, ссылающееся на параметр есть в словаре, команда может быть исполнена
                execute = True
            except KeyError:
                pass

        if execute:
            # Вычисление максимального веса, т. е. веса кандидата
            candidates_weight = weights[category][max(weights[category], key = weights[category].get)]
            # Подсчёт количества кандидатов
            candidates_count = sum(1 for value in weights[category] if weights[category][value] == candidates_weight)

            # Если кандидатов больше 1, произошло противоречие
            if candidates_count > 1:
                parameter = solve_conflicts(cmd=cmd, weights_sector=copy.deepcopy(weights[category]), conflict_category=category, max_weight=candidates_weight)
            else:
                # Определение параметра с максимальным весом
                parameter = max(weights[category], key = weights[category].get)
            eval(f'{category}(r"{parameter}")')
        else:
            pass

# Функция решения противоречий
def solve_conflicts(cmd, weights_sector, conflict_category, max_weight):
    conflict_keys = [key for key, value in weights_sector.items() if value == max_weight]
    words_to_remove = []

    # Подсчёт числа слов, иницирующих противоречие
    for word in cmd:
        links_count = 0
        for value in keywords[conflict_category][word]:
            if value['parameter'] in conflict_keys:
                links_count += 1
        if links_count > 1:
            words_to_remove.append(word)

    # Удаление слов, инициирующих противоречие
    for word in words_to_remove:
        cmd.remove(word)

    if cmd:
        # Если команда валидна, в ней должно остаться только одно слово, указывающее на решение конфликта
        for value in keywords[conflict_category][cmd[0]]:
            weights_sector[value['parameter']] += value['weight']
        return max(weights_sector, key = weights_sector.get)
    else:
        # Случай, при котором команда невалидна
        return max(weights_sector, key = weights_sector.get)


with open(Path('config/keywords.json').resolve(), 'r', encoding='UTF-8') as keywords_file:
    keywords = json.load(keywords_file)

with open(Path('config/weights.json').resolve(), 'r', encoding='UTF-8') as weights_file:
    weights_template = json.load(weights_file)

with open(Path('config/scripts.json').resolve(), 'r', encoding='UTF-8') as scripts_file:
    scripts = json.load(scripts_file)

print(colored(text='Информация:', color='white', on_color=(255, 95, 0), attrs=['bold']), end=' ')
print('Голосовой ассистент готов к использованию.')
for cmd_recognized in listen():
    process(cmd_recognized.lower())
