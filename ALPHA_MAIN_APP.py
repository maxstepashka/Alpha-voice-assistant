import os
try:
    import customtkinter
except ImportError:
    print("Не все библиотеки установлены.")
    os.system("pip install customtkinter")


customtkinter.set_appearance_mode("dark")  # Modes: system (default), light, dark
customtkinter.set_default_color_theme("dark-blue")  # Themes: blue (default), dark-blue, green

app = customtkinter.CTk()  # create CTk window like you do with the Tk window
app.geometry("240x240")
app.title('Альфа')
app.resizable(width=False, height=False)
def button_function():
    os.startfile(r"Alpha.py")

# Use CTkButton instead of tkinter Button
frame = customtkinter.CTkFrame(master=app)
frame.pack(expand=True)


button = customtkinter.CTkButton(master=app, text='Запустить "Альфу"', command=button_function, fg_color="#F07427", hover_color="#FF6027")
button.place(relx=0.5, rely=0.2, anchor=customtkinter.CENTER)

button2 = customtkinter.CTkButton(master=app, text='Выход', command=app.destroy, fg_color="#F07427", hover_color="#FF6027")
button2.place(relx=0.5, rely=0.45, anchor=customtkinter.S)

label = customtkinter.CTkLabel(master=app, text="Github создателя:\ngithub.com/maxstepashka", bg_color="#212121")
label.place(relx=0.5, rely=0.65, anchor=customtkinter.S)

label = customtkinter.CTkLabel(master=app, text="Email создателя:\nstepanovmax9@yandex.ru", bg_color="#212121")
label.place(relx=0.5, rely=0.85, anchor=customtkinter.S)

app.mainloop()