# Убедитесь, что все библиотеки установлены!
import os
import random
from datetime import datetime
import webbrowser
from num2word import word
import json
import pyaudio
from vosk import Model, KaldiRecognizer
import torch
import sounddevice as sd
import time
from translate import Translator
from sound import Sound
from text_to_num import text2num



# Эти параметры можно настраивать

# Язык синтеза речи
# Модель распознавания речи
# Убедитесь, что модель находится в папке
# Модели можно найти на https://alphacephei.com/vosk/models
model = Model("vosk-model-small-ru-0.4")
language = "ru"
# Голос синтеза речи
speaker = "xenia"
# Устройство для синтеза речи
device = torch.device("cpu")
# Активационная фраза
wakeword = "альфа"



model_id = "ru_v3"
sample_rate = 48000
put_accent = True
put_yo = True
rec = KaldiRecognizer(model, 16000)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
stream.start_stream()
translator = Translator(from_lang="en", to_lang="ru")



def listen():
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if (rec.AcceptWaveform(data)) and (len(data) > 0):
            com_1 = json.loads(rec.Result())
            if com_1["text"]:
                yield com_1["text"]



def speak(text):
    print(text)
    audio = model.apply_tts(text=text, speaker=speaker, sample_rate=sample_rate, put_accent=put_accent, put_yo=put_yo)
    sd.play(audio, sample_rate)
    time.sleep(len(audio) / sample_rate + 1.7)
    sd.stop()



model, _ = torch.hub.load(repo_or_dir="snakers4/silero-models", model = "silero_tts", language=language, speaker = model_id)
model.to(device)



for com_1 in listen():
    if wakeword in com_1:
         endword = 0
         vol = 0
         setvol = 0
         com = com_1
         if wakeword in com.lower():
             com = com.lower().replace(wakeword + " ", "")
             print("Распознано: " + com.lower())


            # Здесь вы можете добавлять свои программы, которые голосовой ассистент сможет открывать
             if "терминал" in com.lower():
                 try:
                     os.startfile(r'C:\Windows\system32\cmd.exe')
                     endword = 1
                 except FileNotFoundError:
                     endword = 2


             
             if "блокнот" in com.lower():
                 try:
                     os.startfile(r'C:\Windows\system32\notepad.exe')
                     endword = 1
                 except FileNotFoundError:
                     endword = 2



             elif "найди" in com.lower() or "поищи" in com.lower() or "загугли" in com.lower():
                 zapros = com.lower()
                 if "найди" in zapros.lower():
                     zapros = zapros.lower().replace("найди ", "")
                 if "поищи" in zapros.lower():
                     zapros = zapros.lower().replace("поищи ", "")
                 if "загугли" in zapros.lower():
                     zapros = zapros.lower().replace("загугли ", "")
                 webbrowser.open_new_tab('https://www.google.com/search?q=' + zapros)
                 endword = 1



             elif "громкость" in com.lower() or "звук" in com.lower() or "установи" in com.lower() or "":
                 vol = com.lower()
                 if "громкость" in vol.lower():
                     vol = vol.lower().replace("громкость", "")
                 if "на" in vol.lower():
                     vol = vol.lower().replace("на ", "")
                 if "поставь" in vol.lower():
                     vol = vol.lower().replace("поставь ", "")
                 if "звук" in vol.lower():
                     vol = vol.lower().replace("звук ", "")
                 if "установи" in vol.lower():
                     vol = vol.lower().replace("установи ", "")
                 try:
                     vol = text2num(vol, "ru")
                     setvol = 1
                 except ValueError:
                     setvol = 0
                     speak("Неизвестное значение громкости.")
                 if setvol == 1:
                     Sound.volume_set(int(vol))



             elif com.lower() == "выключи компьютер":
                 os.system('shutdown -s')



             elif "сколько времени" in com.lower() or "который час" in com.lower():
                 endword = 0
                 current_time = datetime.now()
                 h = str(current_time.hour)
                 m = str(current_time.minute)
                 if len(str(current_time.hour)) == 1:
                     h = "0" + str(h)
                 if len(str(current_time.minute)) == 1:
                     m = "0" + str(m)
                 print(h + ":" + m)
                 h = translator.translate((word(current_time.hour)))
                 m = translator.translate((word(current_time.minute)))
                 text = h + " " + m
                 audio = model.apply_tts(text=text, speaker=speaker, sample_rate=sample_rate, put_accent=put_accent, put_yo=put_yo)
                 sd.play(audio, sample_rate)
                 time.sleep(len(audio) / sample_rate + 1.7)
                 sd.stop()



             elif "анекдот" in com.lower():
                 anekdoti = ["- Официант, я хотел бы получить то же, что у господина за соседним столиком.\n- Нет проблем, месье. Я сейчас позову его к телефону, а вы действуйте.",
                             "Сидит Чукча на дереве, рубит под собой сук. Проходит человек.\n- Чукча, Вы упадете!\n- Однако, вряд ли!\nПорубил, порубил и упал.\nВстал, посмотрел вслед человеку:\n- Колдун, однако!"]
                 anekdot = random.choice(anekdoti)
                 speak(anekdot)



             elif "умеешь" in com.lower() or "навыки" in com.lower():
                 speak("Как голосовой ассистент, я умею: открывать программы, искать информацию в браузере, управлять громкостью компьютера, говорить, который час и рассказывать анекдоты.")



             elif "заверши" in com.lower() and "работу" in com.lower():
                 endword = 0
                 break



         if endword == 1:
             speak("Запрос выполнен.")
         elif endword == 2:
             speak("Приложение отсутствует.")