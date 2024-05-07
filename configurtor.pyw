try:
    import os
    import json
    import customtkinter
except ImportError:
    print("Не все библиотеки установлены.")
    os.system("pip install customtkinter")



# Открытие сохраненных данных
with open("config_alpha.json", "r") as data:
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
app.geometry("490x300")
app.title('Конфигуратор')
app.resizable(width=False, height=False)



def add_site():
    kw = kwsite_entry.get().lower()
    ln = lnsite_entry.get()
    f = open("ALPHA_MAIN_APP.py", encoding='utf!8', mode='r')
    data = f.readlines()
    print(data)
    data[122] = f"\n            if '{kw}' in com.lower():\n                webbrowser.open(r'{ln}')\n                endword = 1\n                logging.info('Выполнена команда: открыть сайт.')\n"
    f.close

    f2 = open("ALPHA_MAIN_APP.py", encoding='utf!8', mode='w')
    f2.writelines(data)
    f2.close()




def add_app():
    kw = kwapp_entry.get().lower()
    ln = lnapp_entry.get()
    f = open("ALPHA_MAIN_APP.py", encoding='utf!8', mode='r')
    data = f.readlines()
    print(data)
    data[122] = f"\n            if '{kw}' in com.lower():\n                os.startfile(r'{ln}')\n                endword = 1\n                logging.info('Выполнена команда: открыть приложение.')\n"
    f.close

    f2 = open("ALPHA_MAIN_APP.py", encoding='utf!8', mode='w')
    f2.writelines(data)
    f2.close()

def add_cmd():
    kw = kwcmd_entry.get().lower()
    ln = lncmd_entry.get()
    f = open("ALPHA_MAIN_APP.py", encoding='utf!8', mode='r')
    data = f.readlines()
    print(data)
    data[122] = f"\n            if '{kw}' in com.lower():\n                os.system(r'start cmd /k {ln}')\n                endword = 1\n                logging.info('Выполнена команда: {ln}.')\n"
    f.close

    f2 = open("ALPHA_MAIN_APP.py", encoding='utf!8', mode='w')
    f2.writelines(data)
    f2.close()



tabview = customtkinter.CTkTabview(master=app, fg_color=colorback, segmented_button_selected_hover_color=color1, segmented_button_selected_color=color1, segmented_button_unselected_hover_color=color2)
tabview.place(relx=0.5, rely=0.45, anchor=customtkinter.CENTER)

tabview.add("Добавить веб-страницу")
tabview.add("Добавить приложение")
tabview.add("Добавить команду CMD")

label_site = customtkinter.CTkLabel(tabview.tab("Добавить веб-страницу"), text="Добавить веб-страницу", bg_color=colorback, font=("TkHeadingFont", 15.1))
label_site.place(relx=0.05, rely=0.1, anchor=customtkinter.W)

label_app = customtkinter.CTkLabel(tabview.tab("Добавить приложение"), text="Добавить приложение", bg_color=colorback, font=("TkHeadingFont", 15.1))
label_app.place(relx=0.05, rely=0.1, anchor=customtkinter.W)

label_cmd = customtkinter.CTkLabel(tabview.tab("Добавить команду CMD"), text="Добавить команду CMD", bg_color=colorback, font=("TkHeadingFont", 15.1))
label_cmd.place(relx=0.05, rely=0.1, anchor=customtkinter.W)

label_kwsite = customtkinter.CTkLabel(tabview.tab("Добавить веб-страницу"), text="Ключевая фраза:", bg_color=colorback, font=("TkHeadingFont", 14))
label_kwsite.place(relx=0.05, rely=0.3, anchor=customtkinter.W)

label_kwapp = customtkinter.CTkLabel(tabview.tab("Добавить приложение"), text="Ключевая фраза:", bg_color=colorback, font=("TkHeadingFont", 14))
label_kwapp.place(relx=0.05, rely=0.3, anchor=customtkinter.W)

label_kwcmd = customtkinter.CTkLabel(tabview.tab("Добавить команду CMD"), text="Ключевая фраза:", bg_color=colorback, font=("TkHeadingFont", 14))
label_kwcmd.place(relx=0.05, rely=0.3, anchor=customtkinter.W)

label_lnsite = customtkinter.CTkLabel(tabview.tab("Добавить веб-страницу"), text="Полная ссылка:", bg_color=colorback, font=("TkHeadingFont", 14))
label_lnsite.place(relx=0.05, rely=0.6, anchor=customtkinter.W)

label_lnapp = customtkinter.CTkLabel(tabview.tab("Добавить приложение"), text="Полный путь:", bg_color=colorback, font=("TkHeadingFont", 14))
label_lnapp.place(relx=0.05, rely=0.6, anchor=customtkinter.W)

label_lncmd = customtkinter.CTkLabel(tabview.tab("Добавить команду CMD"), text="Команда:", bg_color=colorback, font=("TkHeadingFont", 14))
label_lncmd.place(relx=0.05, rely=0.6, anchor=customtkinter.W)

kwsite_entry = customtkinter.CTkEntry(tabview.tab("Добавить веб-страницу"))
kwsite_entry.place(relx=0.95, rely=0.3, anchor=customtkinter.E)

lnsite_entry = customtkinter.CTkEntry(tabview.tab("Добавить веб-страницу"))
lnsite_entry.place(relx=0.95, rely=0.6, anchor=customtkinter.E)

kwapp_entry = customtkinter.CTkEntry(tabview.tab("Добавить приложение"))
kwapp_entry.place(relx=0.95, rely=0.3, anchor=customtkinter.E)

lnapp_entry = customtkinter.CTkEntry(tabview.tab("Добавить приложение"))
lnapp_entry.place(relx=0.95, rely=0.6, anchor=customtkinter.E)

kwcmd_entry = customtkinter.CTkEntry(tabview.tab("Добавить команду CMD"))
kwcmd_entry.place(relx=0.95, rely=0.3, anchor=customtkinter.E)

lncmd_entry = customtkinter.CTkEntry(tabview.tab("Добавить команду CMD"))
lncmd_entry.place(relx=0.95, rely=0.6, anchor=customtkinter.E)

button_1 = customtkinter.CTkButton(tabview.tab("Добавить приложение"), text="Сохранить приложение", fg_color=color1, hover_color=color2, font=("TkHeadingFont", 15), command=add_app)
button_1.place(relx=0.5, rely=0.9, anchor=customtkinter.CENTER)

button_2 = customtkinter.CTkButton(tabview.tab("Добавить веб-страницу"), text="Сохранить веб-страницу", fg_color=color1, hover_color=color2, font=("TkHeadingFont", 15), command=add_site)
button_2.place(relx=0.5, rely=0.9, anchor=customtkinter.CENTER)

button_3 = customtkinter.CTkButton(tabview.tab("Добавить команду CMD"), text="Сохранить команду CMD", fg_color=color1, hover_color=color2, font=("TkHeadingFont", 15), command=add_cmd)
button_3.place(relx=0.5, rely=0.9, anchor=customtkinter.CENTER)



app.mainloop()