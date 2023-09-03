import os
import json
try:
    import customtkinter
except ImportError:
    print("Не все библиотеки установлены.")
    os.system("pip install customtkinter")

with open("config.json", "r") as data:
    config = json.load(data)
    data.close()

customtkinter.set_appearance_mode("dark")
customtkinter.set_default_color_theme("dark-blue")

app = customtkinter.CTk()
app.geometry("260x293")
app.title('Альфа')
app.resizable(width=False, height=False)
def start():
    os.startfile(r"Alpha.py")

def save():
    wakeword = wakeword_entry.get().lower()
    voice = voice_entry.get().lower()
    ton_obsh = ton_obsh_entry.get().lower()
    config_file = open("config.json", "w")
    config_file.write('{"wakeword": "' + wakeword + '", "voice": "' + voice + '", "ton_obsh": "' + ton_obsh + '"}')
    config_file.close()


label_wakeword = customtkinter.CTkLabel(master=app, text="Активационная фраза", bg_color="#1A1A1A", font=("TkHeadingFont", 14))
label_wakeword.place(relx=0.5, rely=0.1, anchor=customtkinter.CENTER)

wakeword_entry = customtkinter.CTkEntry(master=app, placeholder_text=config["wakeword"])
wakeword_entry.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)

label_voice = customtkinter.CTkLabel(master=app, text="Голос (xenia, kseniya, baya)", bg_color="#1A1A1A", font=("TkHeadingFont", 14))
label_voice.place(relx=0.5, rely=0.3, anchor=customtkinter.CENTER)

voice_entry = customtkinter.CTkEntry(master=app, placeholder_text=config["voice"])
voice_entry.place(relx=0.5, rely=0.4, anchor=customtkinter.CENTER)

label_ton_obsh = customtkinter.CTkLabel(master=app, text="Тон общения \n(стандартный, вежливый, дерзкий)", bg_color="#1A1A1A", font=("TkHeadingFont", 14))
label_ton_obsh.place(relx=0.5, rely=0.52, anchor=customtkinter.CENTER)

ton_obsh_entry = customtkinter.CTkEntry(master=app, placeholder_text=config["ton_obsh"])
ton_obsh_entry.place(relx=0.5, rely=0.64, anchor=customtkinter.CENTER)

button_save = customtkinter.CTkButton(master=app, text='Сохранить', command=save, fg_color="#F07427", hover_color="#FF6027", font=("TkHeadingFont", 14))
button_save.place(relx=0.5, rely=0.77, anchor=customtkinter.CENTER)

button_start = customtkinter.CTkButton(master=app, text='Запустить', command=start, fg_color="#F07427", hover_color="#FF6027", font=("TkHeadingFont", 14))
button_start.place(relx=0.5, rely=0.9, anchor=customtkinter.CENTER)

app.mainloop()