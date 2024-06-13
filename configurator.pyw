try:
    import os
    import json
    import customtkinter
    from pathlib import Path
except ImportError:
    print("Не все библиотеки установлены.")
    os.system("pip install customtkinter pathlib")



# Открытие сохраненных данных
with open(Path("files/config_alpha.json").resolve(), "r") as data:
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
    color1 = "#F07427"
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
app.geometry("430x330")
app.title('Редактор сценариев')
app.resizable(width=False, height=False)
app.after(201, lambda :app.iconbitmap(Path("files/Untitled.ico").resolve()))

def add():
    tp = tp_entry.get()
    kw = kw_entry.get().lower()
    ln = ln_entry.get()
    an = an_entry.get()
    if tp == "Открыть файл":
        f = open("ALPHA_MAIN_APP.py", encoding='utf!8', mode='r')
        data = f.readlines()
        data[116] = f"\n        if '{kw}' in com.lower():\n            os.startfile(r'{ln}')\n            speak('{an}')\n            custom_endword = True\n            logging.info('Выполнена команда: открыть приложение.')\n"
        f.close

        f2 = open("ALPHA_MAIN_APP.py", encoding='utf!8', mode='w')
        f2.writelines(data)
        f2.close()

    elif tp == "Выполнить команду CMD":
        f = open("ALPHA_MAIN_APP.py", encoding='utf!8', mode='r')
        data = f.readlines()
        data[116] = f"\n        if '{kw}' in com.lower():\n            os.system(r'start cmd /k {ln}')\n            speak('{an}')\n            custom_endword = True\n            logging.info('Выполнена команда: {ln}.')\n"
        f.close
    
        f2 = open("ALPHA_MAIN_APP.py", encoding='utf!8', mode='w')
        f2.writelines(data)
        f2.close()
        
    elif tp == "Открыть веб-страницу":
        f = open("ALPHA_MAIN_APP.py", encoding='utf!8', mode='r')
        data = f.readlines()
        data[116] = f"\n        if '{kw}' in com.lower():\n            webbrowser.open(r'{ln}')\n            speak('{an}')\n            custom_endword = True\n            logging.info('Выполнена команда: открыть сайт.')\n"
        f.close
    
        f2 = open("ALPHA_MAIN_APP.py", encoding='utf!8', mode='w')
        f2.writelines(data)
        f2.close()
        
    elif tp == "Нажать сочетание клавиш":
        f = open("ALPHA_MAIN_APP.py", encoding='utf!8', mode='r')
        data = f.readlines()
        data[116] = f"\n        if '{kw}' in com.lower():\n            keyboard.send(r'{ln}')\n            speak('{an}')\n            custom_endword = True\n            logging.info('Выполнена команда: нажать сочетание \"{ln}\".')\n"
        f.close
    
        f2 = open("ALPHA_MAIN_APP.py", encoding='utf!8', mode='w')
        f2.writelines(data)
        f2.close()

    elif tp == "Ввести текст":
        f = open("ALPHA_MAIN_APP.py", encoding='utf!8', mode='r')
        data = f.readlines()
        data[116] = f"\n        if '{kw}' in com.lower():\n            keyboard.write(r'{ln}')\n            speak('{an}')\n            custom_endword = True\n            logging.info('Выполнена команда: ввести текст.')\n"
        f.close

        f2 = open("ALPHA_MAIN_APP.py", encoding='utf!8', mode='w')
        f2.writelines(data)
        f2.close()
        

label_main = customtkinter.CTkLabel(master=app, text="Редактор сценариев", bg_color=colorback, font=("TkHeadingFont", 15.1))
label_main.place(relx=0.05, rely=0.1, anchor=customtkinter.W)

label_kw = customtkinter.CTkLabel(master=app, text="Ключевая фраза:", bg_color=colorback, font=("TkHeadingFont", 14))
label_kw.place(relx=0.05, rely=0.2, anchor=customtkinter.W)

label_tp = customtkinter.CTkLabel(master=app, text="Тип команды:", bg_color=colorback, font=("TkHeadingFont", 14))
label_tp.place(relx=0.05, rely=0.35, anchor=customtkinter.W)

label_ln = customtkinter.CTkLabel(master=app, text="Данные команды:", bg_color=colorback, font=("TkHeadingFont", 14))
label_ln.place(relx=0.05, rely=0.5, anchor=customtkinter.W)

label_an = customtkinter.CTkLabel(master=app, text="Ответная фраза:", bg_color=colorback, font=("TkHeadingFont", 14))
label_an.place(relx=0.05, rely=0.65, anchor=customtkinter.W)

kw_entry = customtkinter.CTkEntry(master = app, width = 230, font=("TkHeadingFont", 14))
kw_entry.place(relx=0.95, rely=0.2, anchor=customtkinter.E)

tp_entry = customtkinter.CTkOptionMenu(master=app, values=["Открыть файл", "Открыть веб-страницу", "Выполнить команду CMD", "Нажать сочетание клавиш", "Ввести текст"], width = 230, fg_color=color1, button_color=color1, button_hover_color=color2, font=("TkHeadingFont", 14))
tp_entry.set("Открыть файл")
tp_entry.place(relx=0.95, rely=0.35, anchor=customtkinter.E)

ln_entry = customtkinter.CTkEntry(master=app, width = 230, placeholder_text="Cочетание (alt + f4 и т. д.), команда и т. д.", font=("TkHeadingFont", 14))
ln_entry.place(relx=0.95, rely=0.5, anchor=customtkinter.E)

an_entry = customtkinter.CTkEntry(master=app, width = 230, font=("TkHeadingFont", 14))
an_entry.place(relx=0.95, rely=0.65, anchor=customtkinter.E)

button_1 = customtkinter.CTkButton(master=app, text="Сохранить команду", width = 230, fg_color=color1, hover_color=color2, font=("TkHeadingFont", 15), command=add)
button_1.place(relx=0.5, rely=0.85, anchor=customtkinter.CENTER)

app.mainloop()