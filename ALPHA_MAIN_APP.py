# Загрузка библиотек
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
    os.system("pip install datetime py_win_keyboard_layout num2word pyaudio vosk torch sounddevice translate text2num screen_brightness_control pyautogui keyboard silero numpy customtkinter")



# Открытие сохраненных данных
with open("config.json", "r") as data:
    config = json.load(data)
    data.close()



# Конфигурация интерфейса
if config["theme2"] == "светлая":
    customtkinter.set_appearance_mode("light")
    colorback = "#F2F2F2"
elif config["theme2"] == "тёмная":
    customtkinter.set_appearance_mode("dark")
    colorback = "#1A1A1A"


if config["theme"] == "оранжевый":
    color1 = "#FF7F26"
    color2 = "#DF5900"

elif config["theme"] == "зелёный":
    color1 = "#55A376"
    color2 = "#306846"

elif config["theme"] == "синий":
    color1 = "#3669A0"
    color2 = "#273B4D"

elif config["theme"] == "красный":
    color1 = "#EB4C42"
    color2 = "#CD443A"

elif config["theme"] == "бирюзовый":
    color1 = "#1CC3BB"
    color2 = "#19AEA7"



customtkinter.set_default_color_theme("dark-blue")
app = customtkinter.CTk()
app.geometry("530x370")
app.title('Голосовой ассистент "Альфа"')
app.resizable(width=False, height=False)



# Функции
def start():
    try:
        alpha_th.start()
    except RuntimeError:
        pass


# Сохранение данных
def save():
    wakeword = wakeword_entry.get().lower()
    voice = voice_entry.get().lower()
    ton_obsh = ton_obsh_entry.get().lower()
    theme = theme_entry.get().lower()
    theme2 = theme2_entry.get().lower()
    rasp = vosk_entry.get().lower()
    sintez = silero_entry.get().lower()
    config_file = open("config.json", "w")
    config_file.write('{"wakeword": "' + wakeword + '", "voice": "' + voice + '", "ton_obsh": "' + ton_obsh + '", "vosk": "' + rasp + '", "silero": "' + sintez + '", "theme2": "' + theme2 + '", "theme": "' + theme + '"}')
    config_file.close()



# Главный поток
def alpha():
    # Загрузка сохранённых данных
    with open("config.json", "r") as data:
        config = json.load(data)
        data.close()



    # Модель распознавания речи
    if config["vosk"] == "0.22":
        model = Model("vosk-model-small-ru-0.22")
    elif config["vosk"] == "0.4":
        model = Model("vosk-model-small-ru-0.4")
    # Язык синтеза речи
    language = "ru"
    # Голос синтеза речи
    speaker = config["voice"]
    # Устройство для синтеза речи
    device = torch.device("cpu")
    # Активационная фраза
    if config["wakeword"] == "" or config["wakeword"] == " ":
        wakeword = "альфа"
    else:
        wakeword = config["wakeword"]
    ton_obsh = config["ton_obsh"]
    model_id = config["silero"]



    # Неизменяемые данные
    sample_rate = 48000
    put_accent = True
    put_yo = True
    rec = KaldiRecognizer(model, 16000)
    p = pyaudio.PyAudio()
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    stream.start_stream()
    translator = Translator(from_lang="en", to_lang="ru")
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(message)s")



    # Распознавание речи
    def listen():
        while True:
            data = stream.read(4000, exception_on_overflow=False)
            if (rec.AcceptWaveform(data)) and (len(data) > 0):
                com_1 = json.loads(rec.Result())
                if com_1["text"]:
                    yield com_1["text"]



    # Синтез речи
    def speak(text):
        audio = model.apply_tts(text=text, speaker=speaker, sample_rate=sample_rate, put_accent=put_accent,
                                put_yo=put_yo)
        sd.play(audio, sample_rate)
        time.sleep(len(audio) / sample_rate + 1.7)
        sd.stop()



    # Загрузка модели синтеза речи
    model, _ = torch.hub.load(repo_or_dir="snakers4/silero-models", model="silero_tts", language=language, speaker=model_id)
    model.to(device)



    for com_1 in listen():
        if wakeword in com_1:
            endword = 0
            com = com_1
            if wakeword in com.lower():
                com = com.lower().replace(wakeword + " ", "")
                logging.info("Распознано: " + com.lower())



                # Сайты
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



                # Раскладка клавиатуры
                if "раскладк" in com.lower() and "мен" in com.lower() or "язык" in com.lower() and "мен" in com.lower():
                    py_win_keyboard_layout.change_foreground_window_keyboard_layout()
                    logging.info("Выполнена команда: смена раскладки клавиатуры")



                # Нажатие мышью
                if "нажм" in com.lower() or "клик" in com.lower():
                    pyautogui.click()
                    logging.info("Выполнена команда: нажатие мышью")



                # Очистка корзины
                if "чист" in com.lower() and "корзин" in com.lower():
                    os.system("rd /s /q %systemdrive%\$Recycle.bin")
                    endword = 1
                    logging.info("Выполнена команда: очистка корзины")



                # Новая вкладка
                elif "нов" in com.lower():
                    keyboard.press("ctrl")
                    keyboard.send("t")
                    keyboard.release("ctrl")
                    endword = 1
                    logging.info("Выполнена команда: открыть новую вкладку в браузере")



                # Предыдущая вкладка
                elif "предыдущ" in com.lower() and "видео" not in com.lower():
                    keyboard.press("ctrl")
                    keyboard.press("shift")
                    keyboard.send("tab")
                    keyboard.release("shift")
                    keyboard.release("ctrl")
                    endword = 1
                    logging.info("Выполнена команда: открыть предыдущую вкладку в браузере")



                # Следующая вкладка
                elif "след" in com.lower() and "видео" not in com.lower():
                    keyboard.press("ctrl")
                    keyboard.send("tab")
                    keyboard.release("ctrl")
                    endword = 1
                    logging.info("Выполнена команда: открыть следующую вкладку в браузере")



                # Режим инкогнито
                elif "инкогнито" in com.lower():
                    keyboard.press("ctrl")
                    keyboard.press("shift")
                    keyboard.send("n")
                    keyboard.release("shift")
                    keyboard.release("ctrl")
                    endword = 1
                    logging.info("Выполнена команда: открыть новую вкладку инкогнито в браузере")



                # Вверх
                elif "верх" in com.lower():
                    keyboard.send("pageup")
                    endword = 1
                    logging.info("Выполнена команда: пролистать вверх")

                # Вниз
                elif "низ" in com.lower():
                    keyboard.send("pagedown")
                    endword = 1
                    logging.info("Выполнена команда: пролистать вниз")

                # В начало страницы
                elif "нача" in com.lower():
                    keyboard.send("home")
                    endword = 1
                    logging.info("Выполнена команда: пролистать в начало страницы")


                # В конец страницы
                elif "коне" in com.lower() or "конц" in com.lower():
                    keyboard.send("end")
                    endword = 1
                    logging.info("Выполнена команда: пролистать в конец страницы")


                # Поиск информации
                elif "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "найди" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "поищи" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "за гугле" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "как" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "кто" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "умеешь" not in com.lower() and "что" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "времен" not in com.lower() and "сколько" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "где" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "чем" in com.lower() or "видео" not in com.lower() and "музык" not in com.lower() and "песн" not in com.lower() and "когда" in com.lower():
                    endword = 3
                    zapros = com.lower()
                    zapros = zapros.lower().replace("найди ", "")
                    zapros = zapros.lower().replace("поищи ", "")
                    zapros = zapros.lower().replace("за гугле ", "")
                    webbrowser.open("https://www.google.com/search?q=" + zapros)
                    logging.info("Выполнена команда: поиск")



                # Поиск видео
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



                # Поиск музыки
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



                # Печать текста голосом
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



                # Текущее время
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



                # Анекдоты
                elif "анекдот" in com.lower() or "смеш" in com.lower():
                    endword = 0
                    anekdoti = [
                        "- Официант, я хотел бы получить то же, что у господина за соседним столиком.\n- Нет проблем, месье. Я сейчас позову его к телефону, а вы действуйте.",
                        "Сидит баран на дереве, рубит под собой сук. Проходит человек.\n- Баран, ты упадёшь!\n- А вот и нет!\nПорубил, порубил и упал.\nВстал, посмотрел вслед человеку:\n- Однако, колдун!"]
                    anekdot = random.choice(anekdoti)
                    speak(anekdot)
                    logging.info("Comand: Выполнена команда: рассказать анекдот")



                # Навыки
                elif "умеешь" in com.lower() or "навыки" in com.lower() or "умени" in com.lower():
                    endword = 0
                    speak(
                        "Как голосовой ассистент, я умею: открывать определённые сайты, искать информацию, управлять браузером, менять раскладку клавиатуры, вводить сказанный вами текст и многое другое.")
                    logging.info("Comand: Выполнена команда: рассказать о навыках")



                # Выключение ПК
                elif "выкл" in com.lower() and "комп" in com.lower():
                    endword = 5
                    logging.info("Выполнена команда: выключить ПК")



            # Ответная фраза
            if endword == 1:
                endword1_type = random.randint(1, 3)
                if ton_obsh == "дерзкий":
                    if endword1_type == 1:
                        speak("Как же я от вас, людишек, устала!")
                    elif endword1_type == 2:
                        speak("Сейчас всё сделаю, подожди.")
                    elif endword1_type == 3:
                        speak("Да подожди ты, сейчас всё будет.")

                elif ton_obsh == "стандартный":
                    if endword1_type == 1:
                        speak("Запрос выполнен.")
                    elif endword1_type == 2:
                        speak("Сделано.")
                    elif endword1_type == 3:
                        speak("Готово.")

                elif ton_obsh == "вежливый":
                    if endword1_type == 1:
                        speak("Как пожелаете.")
                    elif endword1_type == 2:
                        speak("К вашим услугам.")
                    elif endword1_type == 3:
                        speak("Конечно, уже готово.")


            elif endword == 2:
                if ton_obsh == "дерзкий":
                    speak("Как по вашему открыть файл, которого не существует?")

                elif ton_obsh == "стандартный":
                    speak("Файл отсутствует.")

                elif ton_obsh == "вежливый":
                    speak("Извините, не удалось найти данный файл.")


            elif endword == 3:
                if ton_obsh == "дерзкий":
                    speak("Вот тебе информация по твоему запросу.")

                elif ton_obsh == "стандартный":
                    speak("Показываю результаты поиска.")

                elif ton_obsh == "вежливый":
                    speak("Вот что мне удалось найти для вас.")


            elif endword == 5:
                if ton_obsh == "дерзкий":
                    speak("Ох, ну наконец-то.")

                elif ton_obsh == "стандартный":
                    speak("Завершаю работу и выключаю компьютер.")

                elif ton_obsh == "вежливый":
                    speak("Завершаю работу и выключаю компьютер.")

                os.system('shutdown /s /t 5')

                quit()



# Инициализация главного потока 
alpha_th = threading.Thread(target=alpha, daemon=True)



# Разметка интерфейса
tabview = customtkinter.CTkTabview(master=app, fg_color=colorback, segmented_button_selected_hover_color=color1, segmented_button_selected_color=color1, segmented_button_unselected_hover_color=color2)
tabview.place(relx=0.5, rely=0.35, anchor=customtkinter.CENTER)



tabview.add("Настройки ассистента")
tabview.add("Конфигурация ассистента")
tabview.add("Настройки приложения")



label_settings_assistant = customtkinter.CTkLabel(tabview.tab("Настройки ассистента"), text="Настройки ассистента", bg_color=colorback, font=("TkHeadingFont", 15.1))
label_settings_assistant.place(relx=0.05, rely=0.1, anchor=customtkinter.W)



label_config_assistant = customtkinter.CTkLabel(tabview.tab("Конфигурация ассистента"), text="Конфигурация ассистента", bg_color=colorback, font=("TkHeadingFont", 15.1))
label_config_assistant.place(relx=0.05, rely=0.1, anchor=customtkinter.W)



label_settings_app = customtkinter.CTkLabel(tabview.tab("Настройки приложения"), text="Настройки приложения", bg_color=colorback, font=("TkHeadingFont", 15.1))
label_settings_app.place(relx=0.05, rely=0.1, anchor=customtkinter.W)



label_wakeword = customtkinter.CTkLabel(tabview.tab("Настройки ассистента"), text="Активационная фраза:", bg_color=colorback, font=("TkHeadingFont", 14))
label_wakeword.place(relx=0.05, rely=0.3, anchor=customtkinter.W)



wakeword_entry = customtkinter.CTkComboBox(tabview.tab("Настройки ассистента"), values=[config["wakeword"]], border_color=color1, button_color=color1, button_hover_color=color2)
wakeword_entry.set(config["wakeword"])
wakeword_entry.place(relx=0.95, rely=0.3, anchor=customtkinter.E)



label_voice = customtkinter.CTkLabel(tabview.tab("Настройки ассистента"), text="Голос:", bg_color=colorback, font=("TkHeadingFont", 14))
label_voice.place(relx=0.05, rely=0.6, anchor=customtkinter.W)



voice_entry = customtkinter.CTkOptionMenu(tabview.tab("Настройки ассистента"), values=["xenia", "kseniya", "baya", "aidar"], fg_color=color1, button_color=color1, button_hover_color=color2)
voice_entry.set(config["voice"])
voice_entry.place(relx=0.95, rely=0.6, anchor=customtkinter.E)



label_ton_obsh = customtkinter.CTkLabel(tabview.tab("Настройки ассистента"), text="Тон общения:", bg_color=colorback, font=("TkHeadingFont", 14))
label_ton_obsh.place(relx=0.05, rely=0.9, anchor=customtkinter.W)



ton_obsh_entry = customtkinter.CTkOptionMenu(tabview.tab("Настройки ассистента"), values=["стандартный", "вежливый", "дерзкий"], fg_color=color1, button_color=color1, button_hover_color=color2)
ton_obsh_entry.set(config["ton_obsh"])
ton_obsh_entry.place(relx=0.95, rely=0.9, anchor=customtkinter.E)



label_vosk= customtkinter.CTkLabel(tabview.tab("Конфигурация ассистента"), text="Распознавание речи:", bg_color=colorback, font=("TkHeadingFont", 14))
label_vosk.place(relx=0.05, rely=0.3, anchor=customtkinter.W)



vosk_entry = customtkinter.CTkOptionMenu(tabview.tab("Конфигурация ассистента"), values=["0.22", "0.4"], fg_color=color1, button_color=color1, button_hover_color=color2)
vosk_entry.set(config["vosk"])
vosk_entry.place(relx=0.95, rely=0.3, anchor=customtkinter.E)



label_silero= customtkinter.CTkLabel(tabview.tab("Конфигурация ассистента"), text="Синтез речи:", bg_color=colorback, font=("TkHeadingFont", 14))
label_silero.place(relx=0.05, rely=0.6, anchor=customtkinter.W)



silero_entry = customtkinter.CTkOptionMenu(tabview.tab("Конфигурация ассистента"), values=["ru_v3", "v3_1_ru"], fg_color=color1, button_color=color1, button_hover_color=color2)
silero_entry.set(config["silero"])
silero_entry.place(relx=0.95, rely=0.6, anchor=customtkinter.E)



label_theme2 = customtkinter.CTkLabel(tabview.tab("Настройки приложения"), text="Тема:", bg_color=colorback, font=("TkHeadingFont", 14))
label_theme2.place(relx=0.05, rely=0.3, anchor=customtkinter.W)



theme2_entry = customtkinter.CTkOptionMenu(tabview.tab("Настройки приложения"), values=["светлая", "тёмная"], fg_color=color1, button_color=color1, button_hover_color=color2)
theme2_entry.set(config["theme2"])
theme2_entry.place(relx=0.95, rely=0.3, anchor=customtkinter.E)



label_theme = customtkinter.CTkLabel(tabview.tab("Настройки приложения"), text="Акцентный цвет:", bg_color=colorback, font=("TkHeadingFont", 14))
label_theme.place(relx=0.05, rely=0.6, anchor=customtkinter.W)



theme_entry = customtkinter.CTkOptionMenu(tabview.tab("Настройки приложения"), values=["оранжевый", "зелёный", "синий", "красный", "бирюзовый"], fg_color=color1, button_color=color1, button_hover_color=color2)
theme_entry.set(config["theme"])
theme_entry.place(relx=0.95, rely=0.6, anchor=customtkinter.E)



button_1 = customtkinter.CTkButton(master=app, text="Сохранить", fg_color=color1, hover_color=color2, font=("TkHeadingFont", 15), command=save)
button_1.place(relx=0.075, rely=0.9, anchor=customtkinter.W)



button_2 = customtkinter.CTkButton(master=app, text="Запустить", fg_color=color1, hover_color=color2, font=("TkHeadingFont", 15), command=start)
button_2.place(relx=0.925, rely=0.9, anchor=customtkinter.E)



# Запуск интерфейса
app.mainloop()