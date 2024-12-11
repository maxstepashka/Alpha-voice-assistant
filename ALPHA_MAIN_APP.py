# Загрузка библиотек
try:
    import os
    import json
    import customtkinter
    import time
    import webbrowser
    import logging
    from num2word import word
    import pyaudio
    from vosk import Model, KaldiRecognizer, SetLogLevel
    import torch
    import sounddevice as sd
    import keyboard
    import numpy
    import silero
    import threading
    from gigachat import GigaChat
    from transliterate import translit
    import re
    from num2words import num2words
    from pathlib import Path
    import speech_recognition as sr
    import codecs
except ImportError:
    print('Не все библиотеки установлены.')
    os.system('pip install num2word pyaudio vosk torch sounddevice keyboard silero numpy customtkinter gigachat transliterate num2words pathlib SpeechRecognition')



# Загрузка сохранённых данных
with codecs.open(Path('files/config_alpha.json').resolve(), 'r', 'utf-8') as data:
    config = json.load(data)
    data.close()




# Активационная фраза
if config['wakeword'] == '' or config['wakeword'] == ' ':
    wakeword = "альфа"
else:
    wakeword = tuple(config['wakeword'].lower().replace(',', '').split())
# Голос синтеза речи
speaker = config['voice']

# Время приёма команд без активационной фразы
time_wait = config['time']

# Модель синтеза речи
model_id = config['sintez']

# Модель распознавания речи
if config['rasp'] == '0.22':
    model = Model('vosk-model-small-ru-0.22')
elif config['rasp'] == '0.4':
    model = Model('vosk-model-small-ru-0.4')

# Вариант распознавания
recognition = config['rasp_type']

# API GigaChat
gc_api = config['gc_api']

# Массивы с ключевыми словами, которые нужно удалить из команды или изменить
to_replace = ['найди ', 'поищи', 'включи ', 'включить ', 'включил ', 'музыка ', 'музыку ', 'песня ', 'песню', 'видео ']
to_replace_write = ['напиши', 'введи']
to_replace_special = [['точка с запятой', ';'], ['запятая', ','], ['точка', '.'], ['дефис ', '-'], ['двоеточие', ':'], ['знак вопроса', '?'], ['восклицательный знак', '!']]

# Неизменяемые данные
sample_rate = 48000

language = 'ru'

device = torch.device('cpu')

put_accent = True

put_yo = True

rec = KaldiRecognizer(model, 16000)

p = pyaudio.PyAudio()

stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()

giga = GigaChat(credentials=gc_api, scope='GIGACHAT_API_PERS', verify_ssl_certs=False)

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



# Синтез речи
def speak(text):
    logging.info('Асссистент: ' + text)
    text=translit(text.replace('c', 'к'), 'ru').lower().replace('w', 'в').replace('x', 'кс')
    num = re.findall(r'-?\d+\+?', text)
    if num != []:
        for i in num:
            numt = num2words(int(i), lang = 'ru')
            text = text.replace(i, numt)
    audio = model.apply_tts(text, speaker=speaker, sample_rate=sample_rate, put_accent=put_accent, put_yo=put_yo)
    sd.play(audio, sample_rate)
    time.sleep(len(audio) / sample_rate + 1.7)
    sd.stop()



# Функции
def open_(param):
    try:
        os.startfile(param)
    except:
        webbrowser.open(param)



def search(param):
    zapros = com_rec.lower()
    for i in wakeword:
        zapros = zapros.replace(i + ' ', '')
    zapros = zapros.lower().replace('найди ', '')
    webbrowser.open('https://www.google.com/search?q=' + zapros)



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
    webbrowser.open('https://www.youtube.com/results?search_query=' + zapros)



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



def tell(param):
      zapros = com_rec.lower()
      for i in wakeword:
        zapros = zapros.replace(i + ' ', '')
      response = giga.chat(zapros + '. Ответ должен быть очень кратким')
      speak(response.choices[0].message.content)

def write_text(param):
    text_to_write = com_rec.lower()
    for i in wakeword:
        text_to_write = text_to_write.replace(i + ' ', '')
    for i in to_replace_write:
        text_to_write = text_to_write.replace(i + ' ', '')
    for i in to_replace_special:
        text_to_write = text_to_write.replace(' ' + i[0], i[1])
    keyboard.write(text_to_write + ' ')




def main_func(com):
    exec = False
    global time_
    if com.startswith(wakeword) or time.time() - time_ < time_wait:
        if com.startswith(wakeword):
            time_ = time.time()
        logging.info('Распознано: ' + com)
        com = com.split()

        # Веса категорий и параметров
        with codecs.open(Path('files/we.json').resolve(), 'r', 'utf-8') as data_we:
            we = json.load(data_we)
            data_we.close()

        # Определение весов
        for i in com:
            try:
                ind_kw = 0
                for ind_kw in range(len(kw['main'][i])):
                    we['main'][kw['main'][i][ind_kw]['param']] += kw['main'][i][ind_kw]['weight']
            except:
                pass

        ca = max(we['main'], key = we['main'].get)

        for i in com:
            try:
                ind_kw = 0
                for ind_kw in range(len(kw[ca][i])):
                    we[ca][kw[ca][i][ind_kw]['param']] += kw[ca][i][ind_kw]['weight']
                exec = True
            except:
                pass


        # Исполнение команды
        if exec:
            pa = max(we[ca], key = we[ca].get)
            eval(f'{ca}(r"{pa}")')
        else:
            pass



# Ключевые фразы
with codecs.open(Path('files/kw.json').resolve(), 'r', 'utf-8') as data_kw:
    kw = json.load(data_kw)
    data_kw.close()



# Загрузка модели синтеза речи
model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models', model='silero_tts', language=language, speaker=model_id)
model.to(device)



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
