try:
    import os
    import json
    import customtkinter
    import time
    import webbrowser
    import random
    import logging
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
    import silero
    import threading
except ImportError:
    print("Не все библиотеки установлены.")
    os.system("pip install pip install datetime py_win_keyboard_layout num2word pyaudio vosk torch sounddevice translate text2num screen_brightness_control pyautogui keyboard silero numpy customtkinter")

with open("config.json", "r") as data:
    config = json.load(data)
    data.close()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("400x340")
app.title('Голосовой ассистент "Альфа"')
app.resizable(width=False, height=False)
def start():
    try:
        alpha_th.start()
    except RuntimeError:
        pass

def save():
    wakeword = wakeword_entry.get().lower()
    voice = voice_entry.get().lower()
    ton_obsh = ton_obsh_entry.get().lower()
    theme = theme_entry.get().lower()
    config_file = open("config.json", "w")
    config_file.write('{"wakeword": "' + wakeword + '", "voice": "' + voice + '", "ton_obsh": "' + ton_obsh + '", ' + '"theme": "' + theme + '"}')
    config_file.close()

def alpha():

    with open("config.json", "r") as data:
        config = json.load(data)
        data.close()

    # Модель распознавания речи
    # Убедитесь, что модель находится в папке
    # Модели можно найти на https://alphacephei.com/vosk/models
    try:
        model = Model("vosk-model-small-ru-0.22")
    except Exception:
        print("Модель распознавания речи не установлена.")
        input()

    # Язык синтеза речи
    language = "ru"

    # Голос синтеза речи
    if config["voice"] != "kseniya" and config["voice"] != "xenia" and config["voice"] != "baya" and config[
        "voice"] != "aidar":
        speaker = "kseniya"
    else:
        speaker = config["voice"]

    # Устройство для синтеза речи
    device = torch.device("cpu")

    # Активационная фраза
    if config["wakeword"] == "" or config["wakeword"] == " ":
        wakeword = "альфа"
    else:
        wakeword = config["wakeword"]

    if config["ton_obsh"] != "стандартный" and config["ton_obsh"] != "дерзкий" and config["ton_obsh"] != "вежливый" and \
            config["ton_obsh"] != "вежливый2":
        ton_obsh = "стандартный"
    else:
        ton_obsh = config["ton_obsh"]

    model_id = "ru_v3"
    sample_rate = 48000
    put_accent = True
    put_yo = True
    rec = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()
    translator = Translator(from_lang="en", to_lang="ru")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")

    def listen():
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if (rec.AcceptWaveform(data)) and (len(data) > 0):
                com_1 = json.loads(rec.Result())
                if com_1["text"]:
                    yield com_1["text"]

    def speak(text):
        audio = model.apply_tts(text=text, speaker=speaker, sample_rate=sample_rate, put_accent=put_accent,
                                put_yo=put_yo)
        sd.play(audio, sample_rate)
        time.sleep(len(audio) / sample_rate + 1.7)
        sd.stop()

    model, _ = torch.hub.load(repo_or_dir="snakers4/silero-models", model="silero_tts", language=language,
                              speaker=model_id)
    model.to(device)

    for com_1 in listen():
        if wakeword in com_1:
            endword = 0
            com = com_1
            if wakeword in com.lower():
                com = com.lower().replace(wakeword + " ", "")
                logging.info("Распознано: " + com.lower())

                # Здесь вы можете добавлять сайты, которые ассистент сможет открывать
                if "яндекс" in com.lower() and "музык" in com.lower():
                    webbrowser.open("https://music.yandex.ru/home")
                    endword = 1
                    logging.info("Выполнена команда: открыть сайт")

                if "яндекс" in com.lower() and "почт" in com.lower():
                    webbrowser.open("https://mail.yandex.ru/")
                    endword = 1
                    logging.info("Выполнена команда: открыть сайт")

                if "яндекс" in com.lower() and "диск" in com.lower():
                    webbrowser.open("https://disk.yandex.ru/")
                    endword = 1
                    logging.info("Выполнена команда: открыть сайт")

                if "яндекс" in com.lower() and "карт" in com.lower():
                    webbrowser.open("https://yandex.ru/maps/")
                    endword = 1
                    logging.info("Выполнена команда: открыть сайт")

                if "яндекс" in com.lower() and "такс" in com.lower():
                    webbrowser.open("https://taxi.yandex.ru/")
                    endword = 1
                    logging.info("Выполнена команда: открыть сайт")

                if "яндекс" in com.lower() and "браузер" in com.lower():
                    webbrowser.open("https://ya.ru/")
                    endword = 1
                    logging.info("Выполнена команда: открыть сайт")

                if "контакте" in com.lower() and "музык" not in com.lower() and "погод" not in com.lower() and "сообщен" not in com.lower() and "сообществ" not in com.lower() and "звонк" not in com.lower() and "друз" not in com.lower() and "фото" not in com.lower() and "видео" not in com.lower():
                    webbrowser.open("https://m.vk.com")
                    endword = 1
                    logging.info("Выполнена команда: открыть сайт")

                if "контакте" in com.lower() and "погод" in com.lower():
                    webbrowser.open("https://vk.com/weather?ref=catalog_recent")
                    endword = 1
                    logging.info("Выполнена команда: открыть сайт")

                if "контакте" in com.lower() and "сообщен" in com.lower():
                    webbrowser.open("https://m.vk.com/mail")
                    endword = 1
                    logging.info("Выполнена команда: открыть сайт")

                if "контакте" in com.lower() and "звонк" in com.lower():
                    webbrowser.open("https://vk.com/calls")
                    endword = 1
                    logging.info("Выполнена команда: открыть сайт")

                if "контакте" in com.lower() and "друз" in com.lower():
                    webbrowser.open("https://vk.com/friends")
                    endword = 1
                    logging.info("Выполнена команда: открыть сайт")

                if "контакте" in com.lower() and "сообществ" in com.lower():
                    webbrowser.open("https://vk.com/groups")
                    endword = 1
                    logging.info("Выполнена команда: открыть сайт")

                if "контакте" in com.lower() and "фото" in com.lower():
                    webbrowser.open("https://m.vk.com/albums")
                    endword = 1
                    logging.info("Выполнена команда: открыть сайт")

                if "контакте" in com.lower() and "видео" in com.lower():
                    webbrowser.open("https://m.vk.com/video")
                    endword = 1
                    logging.info("Выполнена команда: открыть сайт")

                if "контакте" in com.lower() and "музык" in com.lower():
                    webbrowser.open("https://m.vk.com/audio")
                    endword = 1
                    logging.info("Выполнена команда: открыть сайт")

                if "раскладк" in com.lower() and "мен" in com.lower() or "язык" in com.lower() and "мен" in com.lower():
                    py_win_keyboard_layout.change_foreground_window_keyboard_layout()
                    logging.info("Выполнена команда: смена раскладки клавиатуры")

                if "нажм" in com.lower() or "клик" in com.lower():
                    pyautogui.click()
                    logging.info("Выполнена команда: нажатие мышью")

                if "очист" in com.lower() and "корзин" in com.lower():
                    os.system("rd /s /q %systemdrive%\$Recycle.bin")
                    endword = 1
                    logging.info("Выполнена команда: очистка корзины")

                elif "нов" in com.lower():
                    keyboard.press("ctrl")
                    keyboard.send("t")
                    keyboard.release("ctrl")
                    endword = 1
                    logging.info("Выполнена команда: открыть новую вкладку в браузере")

                elif "предыдущ" in com.lower() and "видео" not in com.lower():
                    keyboard.press("ctrl")
                    keyboard.press("shift")
                    keyboard.send("tab")
                    keyboard.release("shift")
                    keyboard.release("ctrl")
                    endword = 1
                    logging.info("Выполнена команда: открыть предыдущую вкладку в браузере")

                elif "след" in com.lower() and "видео" not in com.lower():
                    keyboard.press("ctrl")
                    keyboard.send("tab")
                    keyboard.release("ctrl")
                    endword = 1
                    logging.info("Выполнена команда: открыть следующую вкладку в браузере")

                elif "инкогнито" in com.lower():
                    keyboard.press("ctrl")
                    keyboard.press("shift")
                    keyboard.send("n")
                    keyboard.release("shift")
                    keyboard.release("ctrl")
                    endword = 1
                    logging.info("Выполнена команда: открыть новую вкладку инкогнито в браузере")

                elif "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "найди" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "поищи" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "за гугле" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "как" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "кто" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "умеешь" not in com.lower() and "что" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "времен" not in com.lower() and "сколько" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "где" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "чем" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "когда" in com.lower():
                    endword = 3
                    zapros = com.lower()
                    zapros = zapros.lower().replace("найди ", "")
                    zapros = zapros.lower().replace("поищи ", "")
                    zapros = zapros.lower().replace("за гугле ", "")
                    webbrowser.open("https://www.google.com/search?q=" + zapros)
                    logging.info("Выполнена команда: поиск")

                elif "видео" in com.lower():
                    endword = 3
                    zapros = com.lower()
                    zapros = zapros.lower().replace("найди ", "")
                    zapros = zapros.lower().replace("поищи ", "")
                    zapros = zapros.lower().replace("включи ", "")
                    zapros = zapros.lower().replace("ключи ", "")
                    zapros = zapros.lower().replace("включить ", "")
                    zapros = zapros.lower().replace("включил ", "")
                    zapros = zapros.lower().replace("видео ", "")
                    webbrowser.open("https://www.youtube.com/results?search_query=" + zapros)
                    logging.info("Выполнена команда: поиск видео")

                elif "яндекс" not in com.lower() and "контакте" not in com.lower() and "музык" in com.lower() or "яндекс" not in com.lower() and "контакте" not in com.lower() and "песн" in com.lower():
                    endword = 3
                    zapros = com.lower()
                    zapros = zapros.lower().replace("найди ", "")
                    zapros = zapros.lower().replace("поищи ", "")
                    zapros = zapros.lower().replace("включи ", "")
                    zapros = zapros.lower().replace("ключи ", "")
                    zapros = zapros.lower().replace("включить ", "")
                    zapros = zapros.lower().replace("включил ", "")
                    zapros = zapros.lower().replace("музыка ", "")
                    zapros = zapros.lower().replace("музыку ", "")
                    zapros = zapros.lower().replace("песня ", "")
                    zapros = zapros.lower().replace("песню ", "")
                    webbrowser.open("https://music.yandex.ru/search?text=" + zapros)
                    logging.info("Выполнена команда: поиск музыки")



                elif "текст" in com.lower() or "печат" in com.lower() and "голос" in com.lower():
                    endword = 0
                    speak("Запускаю режим \"Ввод текста голосом\".")
                    logging.info("Выполнена команда: Запустить режим \"Ввод текста голосом\"")

                    def listen_for_text():
                        while True:
                            data = stream.read(4000, exception_on_overflow=False)
                            if (rec.AcceptWaveform(data)) and (len(data) > 0):
                                text_to_write = json.loads(rec.Result())
                                if text_to_write["text"]:
                                    yield text_to_write["text"]

                    for text_to_write in listen_for_text():
                        logging.info("Распознано: " + text_to_write.replace(wakeword + " ", "").lower())
                        if "текст" in text_to_write.lower() and "голос" in text_to_write.lower() and "выкл" in text_to_write.lower() and wakeword in text_to_write.lower() or "печат" in text_to_write.lower() and "голос" in text_to_write.lower() and "выкл" in text_to_write.lower() and wakeword in text_to_write.lower():
                            speak("Выключаю режим \"Ввод текста голосом\".")
                            endword = 0
                            logging.info("Выполнена команда: выключить режим \"Ввод текста голосом\"")
                            break
                        else:
                            keyboard.write(text_to_write + " ")
                            logging.info("Выполнена команда: напечатать текст")



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
                    logging.info("Выполнена команда: сказать текущее время")



                elif "анекдот" in com.lower():
                    endword = 0
                    anekdoti = [
                        "- Официант, я хотел бы получить то же, что у господина за соседним столиком.\n- Нет проблем, месье. Я сейчас позову его к телефону, а вы действуйте.",
                        "Сидит баран на дереве, рубит под собой сук. Проходит человек.\n- Баран, ты упадёшь!\n- А вот и нет!\nПорубил, порубил и упал.\nВстал, посмотрел вслед человеку:\n- Однако, колдун!"]
                    anekdot = random.choice(anekdoti)
                    speak(anekdot)
                    logging.info("Comand: Выполнена команда: рассказать анекдот")



                elif "умеешь" in com.lower() or "навыки" in com.lower():
                    endword = 0
                    speak(
                        "Как голосовой ассистент, я умею: открывать определённые сайты, искать информацию, управлять браузером, менять раскладку клавиатуры, вводить сказанный вами текст и многое другое.")
                    logging.info("Comand: Выполнена команда: рассказать о навыках")



                elif "выкл" in com.lower() and "комп" in com.lower():
                    endword = 5
                    logging.info("Выполнена команда: выключить ПК")

            if endword == 1:
                endword1_type = random.randint(1, 2)
                if ton_obsh == "дерзкий":
                    if endword1_type == 1:
                        speak("Как же я от вас, людишек, устала!")
                    elif endword1_type == 2:
                        speak("Сейчас всё сделаю, подожди.")

                elif ton_obsh == "стандартный":
                    if endword1_type == 1:
                        speak("Запрос выполнен.")
                    elif endword1_type == 2:
                        speak("Сделано.")

                elif ton_obsh == "вежливый":
                    if endword1_type == 1:
                        speak("Всё для вас.")
                    elif endword1_type == 2:
                        speak("К вашим услугам.")

                elif ton_obsh == "вежливый2":
                    if endword1_type == 1:
                        speak("Запрос выполнен, сэр.")
                    elif endword1_type == 2:
                        speak("Загружаю, сэр.")

            elif endword == 2:
                if ton_obsh == "дерзкий":
                    speak("Как по вашему открыть файл, которого не существует?")

                elif ton_obsh == "стандартный":
                    speak("Файл отсутствует.")

                elif ton_obsh == "вежливый":
                    speak("Извините, не удалось найти данный файл.")

                elif ton_obsh == "вежливый2":
                    speak("Извините, сэр, не удалось найти данный файл.")

            elif endword == 3:
                if ton_obsh == "дерзкий":
                    speak("Вот тебе информация по твоему запросу.")

                elif ton_obsh == "стандартный":
                    speak("Показываю результаты поиска.")

                elif ton_obsh == "вежливый":
                    speak("Вот что мне удалось найти для вас.")

                elif ton_obsh == "вежливый2":
                    speak("Показываю результаты поиска, сэр.")


            elif endword == 5:
                if ton_obsh == "дерзкий":
                    speak("Ох, ну наконец-то.")

                elif ton_obsh == "стандартный":
                    speak("Завершаю работу и выключаю компьютер.")

                elif ton_obsh == "вежливый":
                    speak("Завершаю работу и выключаю компьютер.")

                elif ton_obsh == "вежливый2":
                    speak("Завершаю работу и выключаю компьютер, сэр.")

                os.system('shutdown /s /t 5')
                quit()

if config["theme"] != "оранжевый" and config["theme"] != "зелёный" and config["theme"] != "синий":
    color1 = "#FF7F26"
    color2 = "#DF5900"

elif config["theme"] == "оранжевый":
    color1 = "#FF7F26"
    color2 = "#DF5900"

elif config["theme"] == "зелёный":
    color1 = "#55A376"
    color2 = "#306846"

elif config["theme"] == "синий":
    color1 = "#3669A0"
    color2 = "#273B4D"

alpha_th = threading.Thread(target=alpha, daemon=True)

label_settings_assistant = customtkinter.CTkLabel(master=app, text="Настройки ассистента", bg_color="#1A1A1A", font=("TkHeadingFont", 15.1))
label_settings_assistant.place(relx=0.05, rely=0.065, anchor=customtkinter.W)

label_wakeword = customtkinter.CTkLabel(master=app, text="Активационная фраза:", bg_color="#1A1A1A", font=("TkHeadingFont", 14))
label_wakeword.place(relx=0.05, rely=0.16, anchor=customtkinter.W)

wakeword_entry = customtkinter.CTkComboBox(master=app, values=[config["wakeword"]], border_color=color1, button_color=color1, button_hover_color=color2)
wakeword_entry.set(config["wakeword"])
wakeword_entry.place(relx=0.445, rely=0.16, anchor=customtkinter.W)

label_voice = customtkinter.CTkLabel(master=app, text="Голос:", bg_color="#1A1A1A", font=("TkHeadingFont", 14))
label_voice.place(relx=0.05, rely=0.3, anchor=customtkinter.W)

voice_entry = customtkinter.CTkComboBox(master=app, values=["xenia", "kseniya", "baya"], border_color=color1, button_color=color1, button_hover_color=color2)
voice_entry.set(config["voice"])
voice_entry.place(relx=0.445, rely=0.3, anchor=customtkinter.W)

label_ton_obsh = customtkinter.CTkLabel(master=app, text="Тон общения:", bg_color="#1A1A1A", font=("TkHeadingFont", 14))
label_ton_obsh.place(relx=0.05, rely=0.44, anchor=customtkinter.W)

ton_obsh_entry = customtkinter.CTkComboBox(master=app, values=["стандартный", "вежливый", "дерзкий"], border_color=color1, button_color=color1, button_hover_color=color2)
ton_obsh_entry.set(config["ton_obsh"])
ton_obsh_entry.place(relx=0.445, rely=0.44, anchor=customtkinter.W)

label_settings_app = customtkinter.CTkLabel(master=app, text="Настройки приложения", bg_color="#1A1A1A", font=("TkHeadingFont", 15.1))
label_settings_app.place(relx=0.05, rely=0.59, anchor=customtkinter.W)

label_theme = customtkinter.CTkLabel(master=app, text="Тема:", bg_color="#1A1A1A", font=("TkHeadingFont", 14))
label_theme.place(relx=0.05, rely=0.68, anchor=customtkinter.W)

theme_entry = customtkinter.CTkComboBox(master=app, values=["оранжевый", "зелёный", "синий"], border_color=color1, button_color=color1, button_hover_color=color2)
theme_entry.set(config["theme"])
theme_entry.place(relx=0.445, rely=0.68, anchor=customtkinter.W)

button_save = customtkinter.CTkButton(master=app, text='Сохранить', command=save, fg_color=color1, hover_color=color2, font=("TkHeadingFont", 15))
button_save.place(relx=0.05, rely=0.9, anchor=customtkinter.W)

button_start = customtkinter.CTkButton(master=app, text='Запустить', command=start, fg_color=color1, hover_color=color2, font=("TkHeadingFont", 15))
button_start.place(relx=0.95, rely=0.9, anchor=customtkinter.E)

app.mainloop()
