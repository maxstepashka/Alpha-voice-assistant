# Убедитесь, что все библиотеки установлены!
try:
    # Эти библиотеки уже установлены
    import os
    import json
    import time
    import webbrowser
    import random
    from sound import Sound

    # Следующие библиотеки нужно установить вручную
    # Для этого введите в консоль Windows следующую команду: pip install + название библиотеки
    # Пример: pip install vosk - эта команда устанавливает библиотеку vosk
    from datetime import datetime
    import py_win_keyboard_layout
    from num2word import word
    import pyaudio
    from vosk import Model, KaldiRecognizer
    import torch
    import sounddevice as sd
    from translate import Translator
    from text_to_num import text2num
    import screen_brightness_control as sbc
    import pyautogui
    import keyboard
    import numpy
except ImportError:
    print("Не все библиотеки установлены.")
    os.system("pip install datetime py_win_keyboard_layout num2word pyaudio vosk torch sounddevice translate text2num screen_brightness_control pyautogui keyboard silero numpy")

# Модель распознавания речи
# Убедитесь, что модель находится в папке
# Модели можно найти на https://alphacephei.com/vosk/models
try:
    model = Model("vosk-model-small-ru-0.4")
except Exception:
    print("Модель распознавания речи не установлена.")
    input()
# Язык синтеза речи
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
    audio = model.apply_tts(text=text, speaker=speaker, sample_rate=sample_rate, put_accent=put_accent,
                            put_yo=put_yo)
    sd.play(audio, sample_rate)
    time.sleep(len(audio) / sample_rate + 1.7)
    sd.stop()


model, _ = torch.hub.load(repo_or_dir="snakers4/silero-models", model="silero_tts", language=language, speaker=model_id)
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

            # Здесь вы можете добавлять свои программы, которые ассистент сможет открывать
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

            if "яндекс" in com.lower() and "музык" in com.lower():
                webbrowser.open("https://music.yandex.ru/home")
                endword = 1

            if "яндекс" in com.lower() and "почт" in com.lower():
                webbrowser.open("https://mail.yandex.ru/")
                endword = 1

            if "яндекс" in com.lower() and "диск" in com.lower():
                webbrowser.open("https://disk.yandex.ru/")
                endword = 1

            if "яндекс" in com.lower() and "карт" in com.lower():
                webbrowser.open("https://yandex.ru/maps/")
                endword = 1

            if "яндекс" in com.lower() and "такс" in com.lower():
                webbrowser.open("https://taxi.yandex.ru/")
                endword = 1

            if "яндекс" in com.lower() and "браузер" in com.lower():
                webbrowser.open("https://ya.ru/")
                endword = 1

            if "контакте" in com.lower() and "музык" not in com.lower() and "погод" not in com.lower() and "сообщен" not in com.lower() and "сообществ" not in com.lower() and "звонк" not in com.lower() and "друз" not in com.lower() and "фото" not in com.lower() and "видео" not in com.lower():
                webbrowser.open("https://m.vk.com")
                endword = 1

            if "контакте" in com.lower() and "погод" in com.lower():
                webbrowser.open("https://vk.com/weather?ref=catalog_recent")
                endword = 1

            if "контакте" in com.lower() and "сообщен" in com.lower():
                webbrowser.open("https://m.vk.com/mail")
                endword = 1

            if "контакте" in com.lower() and "звонк" in com.lower():
                webbrowser.open("https://vk.com/calls")
                endword = 1

            if "контакте" in com.lower() and "друз" in com.lower():
                webbrowser.open("https://vk.com/friends")
                endword = 1

            if "контакте" in com.lower() and "сообществ" in com.lower():
                webbrowser.open("https://vk.com/groups")
                endword = 1

            if "контакте" in com.lower() and "фото" in com.lower():
                webbrowser.open("https://m.vk.com/albums")
                endword = 1

            if "контакте" in com.lower() and "видео" in com.lower():
                webbrowser.open("https://m.vk.com/video")
                endword = 1

            if "контакте" in com.lower() and "музык" in com.lower():
                webbrowser.open("https://m.vk.com/audio")
                endword = 1

            elif "найди" in com.lower() or "поищи" in com.lower() or "за гугле" in com.lower():
                zapros = com.lower()
                zapros = zapros.lower().replace("найди ", "")
                zapros = zapros.lower().replace("поищи ", "")
                zapros = zapros.lower().replace("за гугле ", "")
                webbrowser.open("https://www.google.com/search?q=" + zapros)


            elif "громк" in com.lower() or "звук" in com.lower():
                vol = com.lower()
                vol = vol.lower().replace("громкость ", "")
                vol = vol.lower().replace("громко ", "")
                vol = vol.lower().replace("громкой ", "")
                vol = vol.lower().replace("громкий ", "")
                vol = vol.lower().replace("громких ", "")
                vol = vol.lower().replace("на ", "")
                vol = vol.lower().replace("но ", "")
                vol = vol.lower().replace("поставь ", "")
                vol = vol.lower().replace("поставить ", "")
                vol = vol.lower().replace("поставили ", "")
                vol = vol.lower().replace("звук ", "")
                vol = vol.lower().replace("установи ", "")
                vol = vol.lower().replace("установить ", "")
                vol = vol.lower().replace("установили ", "")
                try:
                    vol = text2num(vol, "ru")
                    setvol = 1
                except ValueError:
                    setvol = 0
                    speak("Неизвестное значение громкости.")
                if setvol == 1:
                    Sound.volume_set(int(vol))


            elif "ярк" in com.lower():
                br = com.lower()
                br = br.lower().replace("яркость", "")
                br = br.lower().replace("яркой ", "")
                br = br.lower().replace("яркий ", "")
                br = br.lower().replace("ярких ", "")
                br = br.lower().replace("на ", "")
                br = br.lower().replace("но ", "")
                br = br.lower().replace("поставь ", "")
                br = br.lower().replace("поставить ", "")
                br = br.lower().replace("поставили ", "")
                br = br.lower().replace("установи ", "")
                br = br.lower().replace("установить ", "")
                br = br.lower().replace("установили ", "")
                try:
                    br = text2num(br, "ru")
                    setbr = 1
                except ValueError:
                    setbr = 0
                    speak("Неизвестное значение яркости.")
                if setbr == 1:
                    sbc.set_brightness(int(br))




            elif "раскладк" in com.lower() or "язык" in com.lower() and "мен" in com.lower():
                py_win_keyboard_layout.change_foreground_window_keyboard_layout()



            elif "нажм" in com.lower() or "клик" in com.lower():
                pyautogui.click()



            elif "очист" in com.lower() and "корзин" in com.lower():
                os.system("rd /s /q %systemdrive%\$Recycle.bin")
                endword = 1


            elif "текст" in com.lower() or "печат" in com.lower() and "голос" in com.lower():
                endword = 0
                speak("Запускаю режим \"Ввод текста голосом\".")


                def listen_for_text():
                    while True:
                        data = stream.read(4000, exception_on_overflow=False)
                        if (rec.AcceptWaveform(data)) and (len(data) > 0):
                            text_to_write = json.loads(rec.Result())
                            if text_to_write["text"]:
                                yield text_to_write["text"]


                for text_to_write in listen_for_text():
                    print(text_to_write)
                    if "текст" in text_to_write.lower() or "печат" in text_to_write.lower() and "голос" in text_to_write.lower() and "выкл" in text_to_write.lower():
                        speak("Выключаю режим \"Ввод текста голосом\".")
                        endword = 0
                        break
                    else:
                        keyboard.write(text_to_write + " ")



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
                audio = model.apply_tts(text=text, speaker=speaker, sample_rate=sample_rate, put_accent=put_accent,
                                        put_yo=put_yo)
                sd.play(audio, sample_rate)
                time.sleep(len(audio) / sample_rate + 1.7)
                sd.stop()



            elif "анекдот" in com.lower():
                anekdoti = [
                    "- Официант, я хотел бы получить то же, что у господина за соседним столиком.\n- Нет проблем, месье. Я сейчас позову его к телефону, а вы действуйте.",
                    "Сидит баран на дереве, рубит под собой сук. Проходит человек.\n- Баран, ты упадёшь!\n- Однако, вряд ли!\nПорубил, порубил и упал.\nВстал, посмотрел вслед человеку:\n- Колдун, однако!"]
                anekdot = random.choice(anekdoti)
                speak(anekdot)



            elif "умеешь" in com.lower() or "навыки" in com.lower():
                speak(
                    "Как голосовой ассистент, я умею: открывать программы и сайты, искать информацию в браузере, управлять громкостью и яркостью, менять раскладку клавиатуры, говорить, который час и многое другое.")



            elif com.lower() == "выключи компьютер":
                os.system('shutdown -s')



            elif "заверши" in com.lower() and "работу" in com.lower():
                endword = 0
                break

        if endword == 1:
            speak("Запрос выполнен.")
        elif endword == 2:
            speak("Приложение отсутствует.")
