import os
import json
import customtkinter
from pathlib import Path



# Открытие сохраненных данных
with open(Path('files/config.json').resolve(), 'r', encoding = 'UTF-8') as data:
    config = json.load(data)
    data.close()

# Конфигурация интерфейса
match config['theme']:
    case 'Светлая':
        customtkinter.set_appearance_mode('light')
        color_background = '#F2F2F2'
        color_label = "#979DA2"
    case 'Тёмная':
        customtkinter.set_appearance_mode('dark')
        color_background = '#1A1A1A'
        color_label = '#3F3F3F'

match config['color']:
    case 'Оранжевый':
        color_main = '#F07427'
        color_hover = '#DF5900'

    case 'Зелёный':
        color_main = '#55A376'
        color_hover = '#306846'

    case 'Синий':
        color_main = '#3669A0'
        color_hover = '#273B4D'

    case 'Красный':
        color_main = '#EB4C42'
        color_hover = '#CD443A'

    case 'Бирюзовый':
        color_main = '#1CC3BB'
        color_hover = '#19AEA7'

customtkinter.set_default_color_theme('dark-blue')

class MainWindow(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        
        self.geometry('540x370')
        self.title('Голосовой ассистент "Альфа"')
        self.resizable(width=False, height=False)
        self.after(225, lambda :self.iconbitmap(Path('files/icon.ico').resolve()))

        self.tabview = customtkinter.CTkTabview(master=self, fg_color=color_background, segmented_button_selected_hover_color=color_main, segmented_button_selected_color=color_main, segmented_button_unselected_hover_color=color_hover)
        self.tabview.pack(padx=5, pady=5)
        
        

        self.tabview.add('Настройки ассистента')
        self.tabview.add('Конфигурация ассистента')
        self.tabview.add('Настройки приложения')

        self.frame_buttons = self.frame_settings_app = customtkinter.CTkFrame(master=self, width=510, height=160)


        self.button_save = customtkinter.CTkButton(master=self.frame_buttons, text='Сохранить', width = 490, fg_color=color_main, hover_color=color_hover, font=('TkHeadingFont', 15), corner_radius=5, command=self.save)
        self.button_save.pack(padx=5, pady=5)

        self.button_start = customtkinter.CTkButton(master=self.frame_buttons, text='Запустить', width = 235, fg_color=color_main, hover_color=color_hover, font=('TkHeadingFont', 15), corner_radius=5, command=self.start)
        self.button_start.pack(padx=(5, 0), pady=5, side='left')
        self.button_command = customtkinter.CTkButton(master=self.frame_buttons, text='Редактор команд', width = 235, fg_color=color_main, hover_color=color_hover, font=('TkHeadingFont', 15), corner_radius=5, command=self.command)
        self.button_command.pack(padx=(0, 5), pady=5, side='right')




        self.frame_buttons.pack(padx=5, pady=(0, 15))

        self.frame_settings_assistant = customtkinter.CTkScrollableFrame(master=self.tabview.tab('Настройки ассистента'), width=530, height=160)


        self.frame_wakeword = customtkinter.CTkFrame(self.frame_settings_assistant, width=530)

        self.label_wakeword = customtkinter.CTkLabel(self.frame_wakeword, width=235, fg_color=color_label, corner_radius=5, text='Активационная фраза', font=('TkHeadingFont', 14))
        self.label_wakeword.pack(padx=5, pady=5, side='left')

        self.wakeword_entry = customtkinter.CTkComboBox(self.frame_wakeword, width = 225, values=[config['wakeword']], border_color=color_main, button_color=color_main, button_hover_color=color_hover, corner_radius=5, font=('TkHeadingFont', 14))
        self.wakeword_entry.set(config['wakeword'])
        self.wakeword_entry.pack(padx=5, pady=5, side='right')

        self.frame_wakeword.pack(fill='x', pady=5)


        self.frame_time = customtkinter.CTkFrame(self.frame_settings_assistant, width=530)

        self.label_time = customtkinter.CTkLabel(self.frame_time, width=235, fg_color=color_label, corner_radius=5, text='Прием команд без акт. фразы, с', font=('TkHeadingFont', 14))
        self.label_time.pack(padx=5, pady=5, side='left')
        
        self.time_entry = customtkinter.CTkComboBox(self.frame_time, width = 225, values=[str(config['time'])], border_color=color_main, button_color=color_main, button_hover_color=color_hover, corner_radius=5, font=('TkHeadingFont', 14))
        self.time_entry.set(config['time'])
        self.time_entry.pack(padx=5, pady=5, side='right')

        self.frame_time.pack(fill='x', pady=5)

        
        self.frame_search = customtkinter.CTkFrame(self.frame_settings_assistant, width=530)

        self.label_search = customtkinter.CTkLabel(self.frame_search, width=235, fg_color=color_label, corner_radius=5, text='Поисковая система', font=('TkHeadingFont', 14))
        self.label_search.pack(padx=5, pady=5, side='left')
        
        self.search_entry = customtkinter.CTkOptionMenu(self.frame_search, width = 225, values=['Яндекс', 'Bing', 'DuckDuckGo'], fg_color=color_main, button_color=color_main, button_hover_color=color_hover, corner_radius=5, font=('TkHeadingFont', 14))
        self.search_entry.set(config['search'])
        self.search_entry.pack(padx=5, pady=5, side='right')
        
        self.frame_search.pack(fill='x', pady=5)


        self.frame_music_search = customtkinter.CTkFrame(self.frame_settings_assistant, width=530)

        self.label_music_search = customtkinter.CTkLabel(self.frame_music_search, width=235, fg_color=color_label, corner_radius=5, text='Поиск музыки', font=('TkHeadingFont', 14))
        self.label_music_search.pack(padx=5, pady=5, side='left')
        
        self.music_search_entry = customtkinter.CTkOptionMenu(self.frame_music_search, width = 225, values=['Яндекс Музыка', 'Звук'], fg_color=color_main, button_color=color_main, button_hover_color=color_hover, corner_radius=5, font=('TkHeadingFont', 14))
        self.music_search_entry.set(config['music_search'])
        self.music_search_entry.pack(padx=5, pady=5, side='right')
        
        self.frame_music_search.pack(fill='x', pady=5)


        self.frame_video_search = customtkinter.CTkFrame(self.frame_settings_assistant, width=530)

        self.label_video_search = customtkinter.CTkLabel(self.frame_video_search, width=235, fg_color=color_label, corner_radius=5, text='Поиск видео', font=('TkHeadingFont', 14))
        self.label_video_search.pack(padx=5, pady=5, side='left')
        
        self.video_search_entry = customtkinter.CTkOptionMenu(self.frame_video_search, width = 225, values=['ВК Видео', 'Rutube'], fg_color=color_main, button_color=color_main, button_hover_color=color_hover, corner_radius=5, font=('TkHeadingFont', 14))
        self.video_search_entry.set(config['video_search'])
        self.video_search_entry.pack(padx=5, pady=5, side='right')
        
        self.frame_video_search.pack(fill='x', pady=5)



        self.frame_config_assistant = customtkinter.CTkScrollableFrame(master=self.tabview.tab('Конфигурация ассистента'), width=530, height=160)

        self.frame_recognition = customtkinter.CTkFrame(self.frame_config_assistant, width=530)

        self.label_recognition = customtkinter.CTkLabel(self.frame_recognition, width=235, fg_color=color_label, corner_radius=5, text='Вариант распознавания', font=('TkHeadingFont', 14))
        self.label_recognition.pack(padx=5, pady=5, side='left')

        self.recognition_entry = customtkinter.CTkOptionMenu(self.frame_recognition, width = 225, values=['Vosk', 'Speech Recognition'], fg_color=color_main, button_color=color_main, button_hover_color=color_hover, corner_radius=5, font=('TkHeadingFont', 14))
        self.recognition_entry.set(config['recognition'])
        self.recognition_entry.pack(padx=5, pady=5, side='right')

        self.frame_recognition.pack(fill='x', pady=5)


        self.frame_model = customtkinter.CTkFrame(self.frame_config_assistant, width=530)

        self.label_model = customtkinter.CTkLabel(self.frame_model, width=235, fg_color=color_label, corner_radius=5, text='Версия модели Vosk', font=('TkHeadingFont', 14))
        self.label_model.pack(padx=5, pady=5, side='left')

        self.model_entry = customtkinter.CTkOptionMenu(self.frame_model, width = 225, values=['0.22', '0.4'], fg_color=color_main, button_color=color_main, button_hover_color=color_hover, corner_radius=5, font=('TkHeadingFont', 14))
        self.model_entry.set(config['model'])
        self.model_entry.pack(padx=5, pady=5, side='right')

        self.frame_model.pack(fill='x', pady=5)



        self.frame_settings_app = customtkinter.CTkScrollableFrame(master=self.tabview.tab('Настройки приложения'), width=530, height=160)
        

        self.frame_theme = customtkinter.CTkFrame(self.frame_settings_app, width=530)

        self.label_theme = customtkinter.CTkLabel(self.frame_theme, width=235, fg_color=color_label, corner_radius=5, text='Тема приложения', font=('TkHeadingFont', 14))
        self.label_theme.pack(padx=5, pady=5, side='left')

        self.theme_entry = customtkinter.CTkOptionMenu(self.frame_theme, width = 225, values=['Светлая', 'Тёмная'], fg_color=color_main, button_color=color_main, button_hover_color=color_hover, corner_radius=5, font=('TkHeadingFont', 14))
        self.theme_entry.set(config['theme'])
        self.theme_entry.pack(padx=5, pady=5, side='right')

        self.frame_theme.pack(fill='x', pady=5)


        self.frame_color = customtkinter.CTkFrame(self.frame_settings_app, width=530)

        self.label_color = customtkinter.CTkLabel(self.frame_color, width=235, fg_color=color_label, corner_radius=5, text='Акцентный цвет', font=('TkHeadingFont', 14))
        self.label_color.pack(padx=5, pady=5, side='left')

        self.color_entry = customtkinter.CTkOptionMenu(self.frame_color, width = 225, values=['Оранжевый', 'Зелёный', 'Синий', 'Красный', 'Бирюзовый'], fg_color=color_main, button_color=color_main, button_hover_color=color_hover, corner_radius=5, font=('TkHeadingFont', 14))
        self.color_entry.set(config['color'])
        self.color_entry.pack(padx=5, pady=5, side='right')

        self.frame_color.pack(fill='x', pady=5)



        self.frame_settings_assistant.pack(padx=5, pady=5)
        self.frame_config_assistant.pack(padx=5, pady=5)
        self.frame_settings_app.pack(padx=5, pady=5)
        

    def save(self):
        config['wakeword'] = self.wakeword_entry.get().lower()
        config['time'] = int(self.time_entry.get())
        config['search'] = self.search_entry.get()
        config['music_search'] = self.music_search_entry.get()
        config['video_search'] = self.video_search_entry.get()
        config['recognition'] = self.recognition_entry.get()
        config['model'] = self.model_entry.get()
        config['theme'] = self.theme_entry.get()
        config['color'] = self.color_entry.get()
        
        with open(Path('files/config.json').resolve(), 'w', encoding='UTF-8') as config_file:
            json.dump(config, config_file, ensure_ascii=False, indent=2)
            config_file.close()

    def start(self):
        self.save()
        os.startfile('app.exe')

    def command(self):
        os.startfile('configurator.exe')

app = MainWindow()
app.mainloop()