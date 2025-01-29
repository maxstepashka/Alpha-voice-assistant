try:
    import os
    import json
    import customtkinter
    from pathlib import Path
    import codecs
except ImportError:
    print('Не все библиотеки установлены.')
    os.system('pip install customtkinter pathlib')


choices = ["-", "Открыть сайт", "Создать новую вкладку", "Предыдущая вкладка", "Следующая вкладка", "Включить режим инкогнито", "Свернуть окно", "Развернуть окно", "Закрыть окно", "Переместить в конец страницы", "Переместить в начало страницы", "Пролистать вверх", "Пролистать вниз", "Подождать (сек)", "Сказать фразу"]
sootv = {"Создать новую вкладку": "new_tab()", "Предыдущая вкладка": "prev_tab()", "Следующая вкладка": "next_tab()", "Включить режим инкогнито": "incognito_tab()", "Свернуть окно": "rollup()", "Развернуть окно": "unwrap()", "Закрыть окно": "close()", "Переместить в конец страницы": "end()", "Переместить в начало страницы": "home()", "Пролистать вверх": "up()", "Пролистать вниз": "down()"}

# Открытие сохраненных данных
with codecs.open(Path('files/config_alpha.json').resolve(), 'r', 'utf-8') as data:
    config = json.load(data)
    data.close()

with codecs.open(Path('files/com_list.txt').resolve(), 'r', 'utf-8') as data:
    com_list = data.read()
    data.close()



# Конфигурация интерфейса
if config['theme2'] == 'светлая':
    customtkinter.set_appearance_mode('light')
    colorback = '#F2F2F2'

elif config['theme2'] == 'тёмная':
    customtkinter.set_appearance_mode('dark')
    colorback = '#1A1A1A'

if config['theme'] == 'оранжевый':
    color1 = '#F07427'
    color2 = '#DF5900'

elif config['theme'] == 'зелёный':
    color1 = '#55A376'
    color2 = '#306846'

elif config['theme'] == 'синий':
    color1 = '#3669A0'
    color2 = '#273B4D'

elif config['theme'] == 'красный':
    color1 = '#EB4C42'
    color2 = '#CD443A'

elif config['theme'] == 'бирюзовый':
    color1 = '#1CC3BB'
    color2 = '#19AEA7'



customtkinter.set_default_color_theme('dark-blue')
app = customtkinter.CTk()
app.geometry('430x450')
app.title('Редактор сценариев')
app.resizable(width=False, height=False)
app.after(201, lambda :app.iconbitmap(Path('files/Untitled.ico').resolve()))

def add():
    do = []
    kw = kw_entry_.get().lower().split()

    if do_entry_1.get() != '-':
        if do_entry_1.get() == 'Открыть сайт':
            do.append(f"open_site('{ln_entry_1.get()}')")
        elif do_entry_1.get() == 'Подождать (сек)':
            do.append(f"time.sleep({float(ln_entry_1.get())})")
        elif do_entry_1.get() == 'Сказать фразу':
            do.append(f"speak('{ln_entry_1.get()}')")
        else:
            do.append(sootv[do_entry_1.get()])

    if do_entry_2.get() != '-':
        if do_entry_2.get() == 'Открыть сайт':
            do.append(f"open_site('{ln_entry_2.get()}')")
        elif do_entry_2.get() == 'Подождать (сек)':
            do.append(f"time.sleep({float(ln_entry_2.get())})")
        elif do_entry_2.get() == 'Сказать фразу':
            do.append(f"speak('{ln_entry_2.get()}')")
        else:
            do.append(sootv[do_entry_2.get()])

    if do_entry_3.get() != '-':
        if do_entry_3.get() == 'Открыть сайт':
            do.append(f"open_site('{ln_entry_3.get()}')")
        elif do_entry_3.get() == 'Подождать (сек)':
            do.append(f"time.sleep({float(ln_entry_3.get())})")
        elif do_entry_3.get() == 'Сказать фразу':
            do.append(f"speak('{ln_entry_3.get()}')")
        else:
            do.append(sootv[do_entry_3.get()])
    
    if do_entry_4.get() != '-':
        if do_entry_4.get() == 'Открыть сайт':
            do.append(f"open_site('{ln_entry_4.get()}')")
        elif do_entry_4.get() == 'Подождать (сек)':
            do.append(f"time.sleep({float(ln_entry_4.get())})")
        elif do_entry_4.get() == 'Сказать фразу':
            do.append(f"speak('{ln_entry_4.get()}')")
        else:
            do.append(sootv[do_entry_4.get()])

    with codecs.open(Path('files/protocol.json').resolve(), 'r', 'utf-8') as f:
        f_pr = json.load(f)
        ma = str(max(list(map(int, f_pr.keys()))) + 1)
        f_pr[ma] = do
    f.close()

    with codecs.open(Path('files/protocol.json').resolve(), 'w', 'utf-8') as f:
        json.dump(f_pr, f, ensure_ascii=False)
        f.close()  



    ln = ln_entry_1.get()
    with codecs.open(Path('files/kw.json').resolve(), 'r', 'utf-8') as f:
        f_kw = json.load(f)
        for i in kw:
            try:
                f_kw['protocol'][i].append({'param': ma, 'weight': 1/len(kw)})
            except:
                f_kw['protocol'][i] = []
                f_kw['protocol'][i].append({'param': ma, 'weight': 1/len(kw)})

            try:
                f_kw['main'][i].append({'param': 'protocol', 'weight': 1/len(kw)})
            except:
                f_kw['main'][i] = []
                f_kw['main'][i].append({'param': 'protocol', 'weight': 1/len(kw)})
        f.close()

    with codecs.open(Path('files/kw.json').resolve(), 'w', 'utf-8') as f:
        json.dump(f_kw, f, ensure_ascii=False)
        f.close()



    with codecs.open(Path('files/we.json').resolve(), 'r', 'utf-8') as f:
        f_we = json.load(f)
        f_we['protocol'][ma] = 0
        f.close()

    with codecs.open(Path('files/we.json').resolve(), 'w', 'utf-8') as f:
        json.dump(f_we, f, ensure_ascii=False)
        f.close()    
tabview = customtkinter.CTkTabview(master = app, fg_color=colorback, segmented_button_selected_hover_color=color1, segmented_button_selected_color=color1, segmented_button_unselected_hover_color=color2, width=420, height = 420)
tabview.place(relx=0.5, rely=0.46, anchor=customtkinter.CENTER)



tabview.add('Добавить сценарий')
tabview.add('Ключевые фразы')  

label_com_list = customtkinter.CTkLabel(tabview.tab('Ключевые фразы'), text='Список команд', bg_color=colorback, font=('TkHeadingFont', 15.1))
label_com_list.place(relx=0.05, rely=0.05, anchor=customtkinter.W)


textbox = customtkinter.CTkTextbox(tabview.tab('Ключевые фразы'), width= 369, height = 340)
textbox.place(relx = 0.05, rely = 0.6, anchor=customtkinter.W)
textbox.insert('0.0', com_list)
textbox.configure(state = 'disabled')






kw_entry_ = customtkinter.CTkEntry(tabview.tab('Добавить сценарий'), width = 230, placeholder_text="Ключевая фраза", font=('TkHeadingFont', 14))
kw_entry_.place(relx=0.05, rely=0.06, anchor=customtkinter.W)

do_entry_1 = customtkinter.CTkOptionMenu(tabview.tab('Добавить сценарий'), width = 230, values=choices, fg_color=color1, button_color=color1, button_hover_color=color2, corner_radius=5, font=('TkHeadingFont', 14))
do_entry_1.place(relx=0.05, rely=0.15, anchor=customtkinter.W)

ln_entry_1 = customtkinter.CTkEntry(tabview.tab('Добавить сценарий'), width = 230, placeholder_text="Параметр (Ссылка, путь и т. д.)", font=('TkHeadingFont', 14))
ln_entry_1.place(relx=0.05, rely=0.24, anchor=customtkinter.W)


do_entry_2 = customtkinter.CTkOptionMenu(tabview.tab('Добавить сценарий'), width = 230, values=choices, fg_color=color1, button_color=color1, button_hover_color=color2, corner_radius=5, font=('TkHeadingFont', 14))
do_entry_2.place(relx=0.05, rely=0.35, anchor=customtkinter.W)

ln_entry_2 = customtkinter.CTkEntry(tabview.tab('Добавить сценарий'), width = 230, placeholder_text="Параметр (Ссылка, путь и т. д.)", font=('TkHeadingFont', 14))
ln_entry_2.place(relx=0.05, rely=0.44, anchor=customtkinter.W)


do_entry_3 = customtkinter.CTkOptionMenu(tabview.tab('Добавить сценарий'), width = 230, values=choices, fg_color=color1, button_color=color1, button_hover_color=color2, corner_radius=5, font=('TkHeadingFont', 14))
do_entry_3.place(relx=0.05, rely=0.55, anchor=customtkinter.W)

ln_entry_3 = customtkinter.CTkEntry(tabview.tab('Добавить сценарий'), width = 230, placeholder_text="Параметр (Ссылка, путь и т. д.)", font=('TkHeadingFont', 14))
ln_entry_3.place(relx=0.05, rely=0.64, anchor=customtkinter.W)


do_entry_4 = customtkinter.CTkOptionMenu(tabview.tab('Добавить сценарий'), width = 230, values=choices, fg_color=color1, button_color=color1, button_hover_color=color2, corner_radius=5, font=('TkHeadingFont', 14))
do_entry_4.place(relx=0.05, rely=0.75, anchor=customtkinter.W)

ln_entry_4 = customtkinter.CTkEntry(tabview.tab('Добавить сценарий'), width = 230, placeholder_text="Параметр (Ссылка, путь и т. д.)", font=('TkHeadingFont', 14))
ln_entry_4.place(relx=0.05, rely=0.84, anchor=customtkinter.W)

button_1 = customtkinter.CTkButton(tabview.tab('Добавить сценарий'), text='Сохранить', width = 370, fg_color=color1, hover_color=color2, font=('TkHeadingFont', 15), command=add)
button_1.place(relx=0.5, rely=0.94, anchor=customtkinter.CENTER)

app.mainloop()