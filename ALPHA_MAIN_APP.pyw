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
except ImportError:
    print("Не все библиотеки установлены.")
    os.system("pip install pip install datetime py_win_keyboard_layout num2word pyaudio vosk torch sounddevice translate text2num screen_brightness_control pyautogui keyboard silero numpy customtkinter")

with open("config.json", "r") as data:
    config = json.load(data)
    data.close()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("400x320")
app.title('Альфа')
app.resizable(width=False, height=False)
def start():
    os.startfile(r"Alpha.py")

def quit():
    app.destroy()

def save():
    wakeword = wakeword_entry.get().lower()
    voice = voice_entry.get().lower()
    ton_obsh = ton_obsh_entry.get().lower()
    theme = theme_entry.get().lower()
    config_file = open("config.json", "w")
    config_file.write('{"wakeword": "' + wakeword + '", "voice": "' + voice + '", "ton_obsh": "' + ton_obsh + '", ' + '"theme": "' + theme + '"}')
    config_file.close()

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
button_save.place(relx=0.1, rely=0.9, anchor=customtkinter.W)

button_start = customtkinter.CTkButton(master=app, text='Запустить', command=start, fg_color=color1, hover_color=color2, font=("TkHeadingFont", 15))
button_start.place(relx=0.9, rely=0.9, anchor=customtkinter.E)


app.mainloop()
