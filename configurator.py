import os
import json
import customtkinter
from pathlib import Path

# Служебные массивы и словари
choices = ["Открыть приложение", "Открыть сайт", "Новая вкладка", "Предыдущая вкладка", "Следующая вкладка", "Режим инкогнито", "Свернуть окно", "Развернуть окно", "Закрыть окно", "В конец страницы", "В начало страницы", "Пролистать вверх", "Пролистать вниз", "Подождать (сек)"]
match_process = {"Новая вкладка": "new_tab()", "Предыдущая вкладка": "prev_tab()", "Следующая вкладка": "next_tab()", "Режим инкогнито": "incognito_tab()", "Свернуть окно": "rollup()", "Развернуть окно": "unwrap()", "Закрыть окно": "close()", "В конец страницы": "end()", "В начало страницы": "home()", "Пролистать вверх": "up()", "Пролистать вниз": "down()"}
match_show = {'new_tab()': 'Новая вкладка', 'prev_tab()': 'Предыдущая вкладка', 'next_tab()': 'Следующая вкладка', 'incognito_tab()': 'Режим инкогнито', 'rollup()': 'Свернуть окно', 'unwrap()': 'Развернуть окно', 'close()': 'Закрыть окно', 'end()': 'В конец страницы', 'home()': 'В начало страницы', 'up()': 'Пролистать вверх', 'down()': 'Пролистать вниз'}

# Служебная функция, удаляюзщая элементы массива из строки
def replace_strings(string, array):
    for line in array:
        string=string.replace(line, '')
    return string

# Открытие сохраненных данных
with open(Path('files/config.json').resolve(), 'r', encoding='UTF-8') as data:
    config = json.load(data)
    
with open(Path('files/scripts.json').resolve(), 'r', encoding='UTF-8') as data:
    scripts = json.load(data)
    names = list(scripts.keys())
    

# Конфигурация интерфейса
match config['theme']:
    case 'Светлая':
        customtkinter.set_appearance_mode('light')
        colorback = '#F2F2F2'
    case 'Тёмная':
        customtkinter.set_appearance_mode('dark')
        colorback = '#1A1A1A'

match config['color']:
    case'Оранжевый':
        color1 = '#F07427'
        color2 = '#DF5900'

    case 'Зелёный':
        color1 = '#55A376'
        color2 = '#306846'

    case 'Синий':
        color1 = '#3669A0'
        color2 = '#273B4D'

    case 'Красный':
        color1 = '#EB4C42'
        color2 = '#CD443A'

    case 'Бирюзовый':
        color1 = '#1CC3BB'
        color2 = '#19AEA7'

customtkinter.set_default_color_theme('dark-blue')

# Класс окна со сценарием
class OpenScriptWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__()
        with open(Path('files/scripts.json').resolve(), 'r', encoding='UTF-8') as data:
            self.scripts = json.load(data)
            
        # Параметры и служебные переменные
        self.geometry('450x250')
        self.title(f'Сценарий "{args[1]}"')
        self.after(200, lambda: self.iconbitmap(Path('files/icon.ico').resolve()))
        script = self.scripts[args[1]][0]
        keyword = self.scripts[args[1]][1]
        self.frame=customtkinter.CTkScrollableFrame(self, width=440, height=240)
        
        # Первоначальное объявление элементов GUI
        self.label_name = customtkinter.CTkLabel(self.frame, width=430, fg_color=color1, corner_radius=5, text=args[1], font=('TkHeadingFont', 16))
        self.label_name.pack(padx=5, pady=5)

        self.label_keyword = customtkinter.CTkLabel(self.frame, width=430, fg_color=color1, corner_radius=5, text='Ключевая фраза: ' + keyword, font=('TkHeadingFont', 14))
        self.label_keyword.pack(padx=5, pady=5)

        
        for line in script:
            if line.startswith('open_app'):
                line = line + '.END'
                text = 'Открыть ' + replace_strings(line, ["open_app(r'", "').END"])
            elif line.startswith('open_site'):
                line = line + '.END'
                text = 'Открыть ' + replace_strings(line, ["open_site(r'", "').END"])
            elif line.startswith('time.sleep'):
                line = line + '.END'
                text = 'Пожождать ' + replace_strings(line, ["time.sleep(", ").END"]) + " секунд"
            else:
                text = match_show[line]
            customtkinter.CTkLabel(self.frame, width=430, fg_color="#3f3f3f", corner_radius=5, text=text, font=('TkHeadingFont', 14)).pack(padx=5, pady=5)
        self.frame.pack(padx=5, pady=5)

# Класс окна редкатирования сценария
class EditScriptWindow(customtkinter.CTkToplevel):
    def __init__(self, *args, **kwargs):
        super().__init__()
        with open(Path('files/scripts.json').resolve(), 'r', encoding='UTF-8') as data:
            self.scripts = json.load(data)
            
        # Параметры и служебные переменные
        self.geometry('480x440')
        self.name = args[1]
        self.title(f'Редкатирование сценария "{self.name}"')
        self.after(200, lambda: self.iconbitmap(Path('files/icon.ico').resolve()))
        self.fields = []
        raw_script = self.scripts[args[1]][0]
        script = []
        for line in raw_script:
            if line.startswith('open_app'):
                line = line + '.END'
                category = 'Открыть приложение'
                param = replace_strings(line, ["open_app(r'", "').END"])
            elif line.startswith('open_site'):
                line = line + '.END'
                category = 'Открыть сайт'
                param = replace_strings(line, ["open_site(r'", "').END"])
            elif line.startswith('time.sleep'):
                line = line + '.END'
                category = 'Открыть сайт'
                param = replace_strings(line, ["time.sleep(", ").END"])
            else:
                category = match_show[line]
                param=''
            script.append((category, param))


        self.frame=customtkinter.CTkScrollableFrame(self, width=430, height=420)
        self.frame.pack(padx=5, pady=5)

        for line in script:
            self.pack_show_field(line)
        
        self.button_add = customtkinter.CTkButton(self.frame, text='Добавить блок', width = 410, fg_color=color1, hover_color=color2, font=('TkHeadingFont', 15), command=self.pack_add_field)
        self.button_add.pack(padx=5, pady=5)

        self.button_save = customtkinter.CTkButton(self.frame, text='Сохранить', width = 410, fg_color=color1, hover_color=color2, font=('TkHeadingFont', 15), command=self.process)
        self.button_save.pack(padx=5, pady=5)

        self.frame.pack(padx=5, pady=5)


    
    def update(self):
        self.button_add.destroy()
        self.button_save.destroy()
        self.frame.pack_forget()
        for field_index in range(len(self.fields)):
            menu=self.fields[field_index][0]
            menu.pack_forget()
            entry=self.fields[field_index][1]
            entry.pack_forget()
            delete_button = self.fields[field_index][2]
            delete_button.pack_forget()

        for field_index in range(len(self.fields)):
            menu=self.fields[field_index][0]
            menu.pack(padx=5, pady=(15,1))
            entry=self.fields[field_index][1]
            entry.pack(padx=5, pady=2)
            delete_button = self.fields[field_index][2]
            delete_button.pack(padx=5, pady=(1,15))

    def get(self):
        result = []
        for field_index in range(len(self.fields)):
            result.append((self.fields[field_index][0].get(), self.fields[field_index][1].get()))
        return result

    def process(self):
        actions = []
        data = self.get()
        for field in data:
            match field[0]:
                case 'Открыть сайт':
                    actions.append(f"open_site(r'{field[1]}')")
                case 'Открыть приложение':
                    actions.append(f"open_app(r'{field[1]}')")
                case 'Подождать (сек)':
                    actions.append(f"time.sleep({float(field[1].replace(',', '.'))})")
                case _:
                    actions.append(match_process[field[0]])


        with open(Path('files/scripts.json').resolve(), 'r', encoding='UTF-8') as f:
            f_script = json.load(f)
            f_script[self.name][0] = actions
        

        with open(Path('files/scripts.json').resolve(), 'w', encoding='UTF-8') as f:
            json.dump(f_script, f, ensure_ascii=False, indent=2)
              


    def pack_show_field(self, line):

        menu = customtkinter.CTkOptionMenu(self.frame, values=choices, fg_color=color1, button_color=color1, button_hover_color=color2, corner_radius=5, font=('TkHeadingFont', 14), width=410)
        entry = customtkinter.CTkComboBox(self.frame, values = [line[1]], width = 410, border_color=color1, button_color=color1, button_hover_color=color2, corner_radius=5, font=('TkHeadingFont', 14))
        delete_button = customtkinter.CTkButton(self.frame, text='Удалить', fg_color="#EB4C42", hover_color='#CD443A', command=lambda: self.delete_field((menu, entry, delete_button)), width=410)

        menu.set(line[0])
        self.fields.append((menu, entry, delete_button))

        menu.pack(padx=5, pady=(15,1))
        entry.pack(padx=5, pady=2)
        delete_button.pack(padx=5, pady=(1,15))

    def pack_add_field(self):
        self.after(0, self.update())

        menu = customtkinter.CTkOptionMenu(self.frame, values=choices, fg_color=color1, button_color=color1, button_hover_color=color2, corner_radius=5, font=('TkHeadingFont', 14), width=410)
        entry = customtkinter.CTkEntry(self.frame, width = 410, placeholder_text="Параметр (при наличии)", font=('TkHeadingFont', 14))
        delete_button = customtkinter.CTkButton(self.frame, text='Удалить', fg_color="#EB4C42", hover_color='#CD443A', command=lambda: self.delete_field((menu, entry, delete_button)), width=410)

        self.fields.append((menu, entry, delete_button))

        menu.pack(padx=5, pady=(15,1))
        entry.pack(padx=5, pady=2)
        delete_button.pack(padx=5, pady=(1,15))

        self.button_add = customtkinter.CTkButton(self.frame, text='Добавить блок', width = 410, fg_color=color1, hover_color=color2, font=('TkHeadingFont', 15), command=self.pack_add_field)
        self.button_add.pack(padx=5, pady=5)

        self.button_save = customtkinter.CTkButton(self.frame, text='Сохранить', width = 410, fg_color=color1, hover_color=color2, font=('TkHeadingFont', 15), command=self.process)
        self.button_save.pack(padx=5, pady=5)

        self.frame.pack(padx=5, pady=5)
    
    def delete_field(self, object):
        self.fields.remove(object)

        menu = object[0]
        entry = object[1]
        delete_button = object[2]

        menu.destroy()
        entry.destroy()
        delete_button.destroy()
    
        self.after(0, self.update())

        self.button_add = customtkinter.CTkButton(self.frame, text='Добавить блок', width = 410, fg_color=color1, hover_color=color2, font=('TkHeadingFont', 15), command=self.pack_add_field)
        self.button_add.pack(padx=5, pady=5)

        self.button_save = customtkinter.CTkButton(self.frame, text='Сохранить', width = 410, fg_color=color1, hover_color=color2, font=('TkHeadingFont', 15), command=self.process)
        self.button_save.pack(padx=5, pady=5)

        self.frame.pack(padx=15, pady=15)

        



# Класс главного окна 
class MainOpenScriptWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # Параметры и служебные переменные
        self.geometry('480x460')
        self.title('Редактор сценариев')
        self.add_fields = []
        self.script_fields = []
        self.resizable(width=False, height=False)
        self.after(200, lambda: self.iconbitmap(Path('files/icon.ico').resolve()))
    
        # Первоначальное объявление элементов GUI
        self.open_script_window = None
        self.edit_script_window = None

        self.tabview = customtkinter.CTkTabview(master = self, fg_color=colorback, segmented_button_selected_hover_color=color1, segmented_button_selected_color=color1, segmented_button_unselected_hover_color=color2, width=450, height=440)
        self.tabview.add('Список сценариев') 
        self.tabview.add('Добавить сценарий') 
        
        self.frame_add=customtkinter.CTkScrollableFrame(master=self.tabview.tab('Добавить сценарий'), width=430, height=420)
        
        self.name_entry = customtkinter.CTkEntry(self.frame_add, width = 410, placeholder_text="Название сценария", font=('TkHeadingFont', 14))
        
        self.keyword_entry = customtkinter.CTkEntry(self.frame_add, width = 410, placeholder_text="Ключевая фраза", font=('TkHeadingFont', 14))
        
        self.button_add = customtkinter.CTkButton(self.frame_add, width = 410, fg_color=color1, hover_color=color2, text='Добавить блок', font=('TkHeadingFont', 15), command=self.pack_add_field)
        
        self.button_save = customtkinter.CTkButton(self.frame_add, width = 410, fg_color=color1, hover_color=color2, text='Сохранить', font=('TkHeadingFont', 15), command=self.process)

        self.name_entry.pack(padx=5, pady=(15, 5))
        self.keyword_entry.pack(padx=5, pady=5)
        self.button_add.pack(padx=5, pady=5)
        self.button_save.pack(padx=5, pady=(5, 15))
        self.frame_add.pack(padx=5, pady=5)
        


        self.frame_list=customtkinter.CTkScrollableFrame(master=self.tabview.tab('Список сценариев'), width=430, height=420)

        for name in names:
            self.pack_script_field(name)
            
            
        self.frame_list.pack(padx=5, pady=5)

        
        self.tabview.pack(padx=5, pady=5)

    # Отрисовка дополнительного поля ввода
    def pack_add_field(self):
        self.after(0, self.update_add())

        menu = customtkinter.CTkOptionMenu(self.frame_add, values=choices, fg_color=color1, button_color=color1, button_hover_color=color2, corner_radius=5, font=('TkHeadingFont', 14), width=410)
        entry = customtkinter.CTkEntry(self.frame_add, width = 410, placeholder_text="Параметр (при наличии)", font=('TkHeadingFont', 14))
        delete_button = customtkinter.CTkButton(self.frame_add, text='Удалить', fg_color="#EB4C42", hover_color='#CD443A', command=lambda: self.delete_add_field((menu, entry, delete_button)), width=410)

        self.add_fields.append((menu, entry, delete_button))

        menu.pack(padx=5, pady=(15,1))
        entry.pack(padx=5, pady=2)
        delete_button.pack(padx=5, pady=(1,15))

        self.button_add = customtkinter.CTkButton(self.frame_add, text='Добавить блок', width = 410, fg_color=color1, hover_color=color2, font=('TkHeadingFont', 15), command=self.pack_add_field)
        self.button_add.pack(padx=5, pady=5)

        self.button_save = customtkinter.CTkButton(self.frame_add, text='Сохранить', width = 410, fg_color=color1, hover_color=color2, font=('TkHeadingFont', 15), command=self.process)
        self.button_save.pack(padx=5, pady=(5, 15))

        self.frame_add.pack(padx=5, pady=5)

    # Удаление поля ввода
    def delete_add_field(self, object):
        self.add_fields.remove(object)

        menu = object[0]
        entry = object[1]
        delete_button = object[2]

        menu.destroy()
        entry.destroy()
        delete_button.destroy()
    
        self.after(0, self.update_add())

        self.button_add = customtkinter.CTkButton(self.frame_add, text='Добавить блок', width = 410, fg_color=color1, hover_color=color2, font=('TkHeadingFont', 15), command=self.pack_add_field)
        self.button_add.pack(padx=5, pady=5)

        self.button_save = customtkinter.CTkButton(self.frame_add, text='Сохранить', width = 410, fg_color=color1, hover_color=color2, font=('TkHeadingFont', 15), command=self.process)
        self.button_save.pack(padx=5, pady=(5, 15))

        self.frame_add.pack(padx=5, pady=5)

    # Обновление вкладки ввода
    def update_add(self):
        self.name_entry.pack_forget()
        self.keyword_entry.pack_forget()
        self.button_add.destroy()
        self.button_save.destroy()
        self.frame_add.pack_forget()
        for field_index in range(len(self.add_fields)):
            menu=self.add_fields[field_index][0]
            menu.pack_forget()
            entry=self.add_fields[field_index][1]
            entry.pack_forget()
            delete_button = self.add_fields[field_index][2]
            delete_button.pack_forget()
        
        self.name_entry.pack(padx=5, pady=(15, 5))
        self.keyword_entry.pack(padx=5, pady=5)

        for field_index in range(len(self.add_fields)):
            menu=self.add_fields[field_index][0]
            menu.pack(padx=5, pady=(15,1))
            entry=self.add_fields[field_index][1]
            entry.pack(padx=5, pady=2)
            delete_button = self.add_fields[field_index][2]
            delete_button.pack(padx=5, pady=(1,15))

    def get(self):
        result = []
        for field_index in range(len(self.add_fields)):
            result.append((self.add_fields[field_index][0].get(), self.add_fields[field_index][1].get()))
        return result
    
    def pack_script_field(self, name):
        button_open_script = customtkinter.CTkButton(self.frame_list, width = 410, fg_color=color1, hover_color=color2, text=name, font=('TkHeadingFont', 15), command=lambda: self.open_script(name))

        button_edit_script = customtkinter.CTkButton(self.frame_list, width = 410, fg_color=color1, hover_color=color2, text='Редактировать', font=('TkHeadingFont', 15), command=lambda: self.edit_script(name))

        button_delete_script = customtkinter.CTkButton(self.frame_list, text='Удалить', fg_color="#EB4C42", hover_color='#CD443A', command=lambda: self.delete_script(name, (button_open_script, button_edit_script, button_delete_script)), width=410)

        self.script_fields.append((button_open_script, button_edit_script, button_delete_script))
        button_open_script.pack(padx=5, pady=(15, 5))
        button_edit_script.pack(padx=5, pady=(5, 5))
        button_delete_script.pack(padx=5, pady=(5, 15))

    # Удаление поля сценария
    def delete_script(self, name, object):
        names.remove(name)
        with open(Path('files/scripts.json').resolve(), 'r', encoding='UTF-8') as f:
            f_script = json.load(f)
            f_script.pop(name)
        

        with open(Path('files/scripts.json').resolve(), 'w', encoding='UTF-8') as f:
            json.dump(f_script, f, ensure_ascii=False, indent=2)
          


        with open(Path('files/weights.json').resolve(), 'r', encoding='UTF-8') as f:
            f_weights = json.load(f)
            f_weights['script'].pop(name)
        

        with open(Path('files/weights.json').resolve(), 'w', encoding='UTF-8') as f:
            json.dump(f_weights, f, ensure_ascii=False, indent=2)
        

        with open(Path('files/keywords.json').resolve(), 'r', encoding='UTF-8') as f:
            f_keywords = json.load(f)
            for word in f_keywords['script']:
                items_to_delete = []
                for item in f_keywords['script'][word]:
                    if item['param'] == name:
                        items_to_delete.append(item)
                for item_to_delete in items_to_delete:
                    f_keywords['script'][word].remove(item_to_delete)
            words_to_delete = []
            for word in f_keywords['script']:
                if f_keywords['script'][word] == []:
                    words_to_delete.append(word)
            for word_to_delete in words_to_delete:
                f_keywords['script'].pop(word_to_delete)
                for item in f_keywords['main'][word_to_delete]:
                    if item['param'] == 'script':
                        f_keywords['main'][word_to_delete].remove(item)
                if f_keywords['main'][word_to_delete] == []:
                    f_keywords['main'].pop(word_to_delete)


        

        with open(Path('files/keywords.json').resolve(), 'w', encoding='UTF-8') as f:
            json.dump(f_keywords, f, ensure_ascii=False, indent=2)
        

        self.script_fields.remove(object)

        button_open_script = object[0]
        button_edit_script = object[1]
        button_delete_script = object[2]

        button_open_script.destroy()
        button_edit_script.destroy()
        button_delete_script.destroy()
    
        self.after(0, self.update_list())

        self.frame_list.pack(padx=5, pady=5)

    def open_script(self, name):
        if self.open_script_window is None or not self.open_script_window.winfo_exists():
            self.open_script_window = OpenScriptWindow(self, name)
            self.open_script_window.after(10, self.open_script_window.lift)
        elif self.open_script_window.winfo_exists():
            self.open_script_window.destroy()
            self.open_script_window = OpenScriptWindow(self, name)
            self.open_script_window.after(10, self.open_script_window.lift)
        else:
            self.open_script_window.after(10, self.open_script_window.lift)

    def edit_script(self, name):
        if self.edit_script_window is None or not self.edit_script_window.winfo_exists():
            self.edit_script_window = EditScriptWindow(self, name)
            self.edit_script_window.after(10, self.edit_script_window.lift)
        elif self.edit_script_window.winfo_exists():
            self.edit_script_window.destroy()
            self.edit_script_window = EditScriptWindow(self, name)
            self.edit_script_window.after(10, self.edit_script_window.lift)
        else:
            self.edit_script_window.after(10, self.edit_script_window.lift)

    def update_list(self):
        self.frame_list.pack_forget()
        for field_index in range(len(self.script_fields)):
            self.script_fields[field_index][0].pack_forget()
            self.script_fields[field_index][1].pack_forget()
            self.script_fields[field_index][2].pack_forget()

        for field_index in range(len(self.script_fields)):
            self.script_fields[field_index][0].pack(padx=5, pady=(15, 5))
            self.script_fields[field_index][1].pack(padx=5, pady=(5, 5))
            self.script_fields[field_index][2].pack(padx=5, pady=(5, 15))

    def update_list_for_pack(self, name):
        self.after(0, self.update_list())
        
        if name not in names:
            names.append(name)
            self.pack_script_field(name)

        self.frame_list.pack(padx=5, pady=5)            

    def process(self):
        actions = []
        data = self.get()
        name= self.name_entry.get()
        self.after(0, self.update_list_for_pack(name))
        keyword=self.keyword_entry.get()
        for field in data:
            match field[0]:
                case 'Открыть сайт':
                    actions.append(f"open_site(r'{field[1]}')")
                case 'Открыть приложение':
                    actions.append(f"open_app(r'{field[1]}')")
                case 'Подождать (сек)':
                    actions.append(f"time.sleep({float(field[1].replace(',', '.'))})")
                case _:
                    actions.append(match_process[field[0]])


        with open(Path('files/scripts.json').resolve(), 'r', encoding='UTF-8') as f:
            f_script = json.load(f)
            f_script[name] = [actions, keyword]
        

        with open(Path('files/scripts.json').resolve(), 'w', encoding='UTF-8') as f:
            json.dump(f_script, f, ensure_ascii=False, indent=2)
              

        keyword = keyword.lower().split()

        with open(Path('files/keywords.json').resolve(), 'r', encoding='UTF-8') as f:
            f_keywords = json.load(f)
            for word in keyword:
                try:
                    f_keywords['script'][word].append({'param': name, 'weight': 1/len(keyword)})
                except:
                    f_keywords['script'][word] = []
                    f_keywords['script'][word].append({'param': name, 'weight': 1/len(keyword)})

                try:
                    if {'param': 'script', 'weight': 1/len(keyword)} not in f_keywords['main'][word]:
                        f_keywords['main'][word].append({'param': 'script', 'weight': 1/len(keyword)})
                except:
                    f_keywords['main'][word] = []
                    f_keywords['main'][word].append({'param': 'script', 'weight': 1/len(keyword)})
            

        with open(Path('files/keywords.json').resolve(), 'w', encoding='UTF-8') as f:
            json.dump(f_keywords, f, ensure_ascii=False, indent=2)
            



        with open(Path('files/weights.json').resolve(), 'r', encoding='UTF-8') as f:
            f_weights = json.load(f)
            f_weights['script'][name] = 0
        

        with open(Path('files/weights.json').resolve(), 'w', encoding='UTF-8') as f:
            json.dump(f_weights, f, ensure_ascii=False, indent=2)
            



app = MainOpenScriptWindow()
app.mainloop()