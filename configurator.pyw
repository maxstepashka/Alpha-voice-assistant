try:
    import os
    import json
    import customtkinter
    from pathlib import Path
    import codecs
except ImportError:
    print("Не все библиотеки установлены.")
    os.system("pip install customtkinter pathlib")



# Открытие сохраненных данных
with codecs.open(Path("files/config_alpha.json").resolve(), "r", 'utf-8') as data:
    config = json.load(data)
    data.close()

with codecs.open(Path("files/com_list.txt").resolve(), "r", 'utf-8') as data:
    com_list = data.read()
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
app.geometry("430x410")
app.title('Команды')
app.resizable(width=False, height=False)
app.after(201, lambda :app.iconbitmap(Path("files/Untitled.ico").resolve()))

def add():
    kw = kw_entry.get().lower().split()
    ln = ln_entry.get()
    with codecs.open(Path("files/kw.json").resolve(), "r", 'utf-8') as f:
        f_kw = json.load(f)
        for i in kw:
            try:
                f_kw['open_'][i].append({"param": ln, "weight": 1/len(kw)})
            except:
                f_kw['open_'][i] = []
                f_kw['open_'][i].append({"param": ln, "weight": 1/len(kw)})
        f.close()

    with codecs.open(Path("files/kw.json").resolve(), "w", 'utf-8') as f:
        json.dump(f_kw, f, ensure_ascii=False)
        f.close()



    with codecs.open(Path("files/we.json").resolve(), "r", 'utf-8') as f:
        f_we = json.load(f)
        f_we['open_'][ln] = 0
        f.close()

    with codecs.open(Path("files/we.json").resolve(), "w", 'utf-8') as f:
        json.dump(f_we, f, ensure_ascii=False)
        f.close()        

label_com_list = customtkinter.CTkLabel(master=app, text="Список команд", bg_color=colorback, font=("TkHeadingFont", 15.1))
label_com_list.place(relx=0.05, rely=0.045, anchor=customtkinter.W)

textbox = customtkinter.CTkTextbox(app, width= 400, height = 190)
textbox.place(relx = 0.05, rely = 0.33, anchor=customtkinter.W)
textbox.insert("0.0", com_list)
textbox.configure(state = "disabled")

label_add_com = customtkinter.CTkLabel(master=app, text="Добавить сайт/файл", bg_color=colorback, font=("TkHeadingFont", 15.1))
label_add_com.place(relx=0.05, rely=0.619, anchor=customtkinter.W)

label_kw = customtkinter.CTkLabel(master=app, text="Ключевая фраза:", bg_color=colorback, font=("TkHeadingFont", 14))
label_kw.place(relx=0.05, rely=0.71, anchor=customtkinter.W)

label_ln = customtkinter.CTkLabel(master=app, text="Ссылка/путь:", bg_color=colorback, font=("TkHeadingFont", 14))
label_ln.place(relx=0.05, rely=0.82, anchor=customtkinter.W)

kw_entry = customtkinter.CTkEntry(master = app, width = 230, font=("TkHeadingFont", 14))
kw_entry.place(relx=0.95, rely=0.71, anchor=customtkinter.E)

ln_entry = customtkinter.CTkEntry(master=app, width = 230, font=("TkHeadingFont", 14))
ln_entry.place(relx=0.95, rely=0.82, anchor=customtkinter.E)

button_1 = customtkinter.CTkButton(master=app, text="Сохранить", width = 230, fg_color=color1, hover_color=color2, font=("TkHeadingFont", 15), command=add)
button_1.place(relx=0.5, rely=0.918, anchor=customtkinter.CENTER)

app.mainloop()