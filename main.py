import flet as ft
import os
import json
from pathlib import Path
import webbrowser
from typing import Optional

def main(page: ft.Page):
    page.window.height=630
    page.window.width=950
    page.theme_mode=ft.ThemeMode.DARK
    page.theme=ft.Theme(color_scheme_seed='#FF8800')

    CHOICES = ['Открыть приложение', 'Открыть сайт', 'Подождать (сек)', 'Выполнить команду CMD', 'Выполнить команду Python', 'Новая вкладка', 'Предыдущая вкладка', 'Следующая вкладка', 'Режим инкогнито', 'Свернуть окно', 'Развернуть окно', 'Закрыть окно', 'В конец страницы', 'В начало страницы', 'Пролистать вверх', 'Пролистать вниз']
    MATCH_PROCESS = {'Новая вкладка': 'new_tab()', 'Предыдущая вкладка': 'prev_tab()', 'Следующая вкладка': 'next_tab()', 'Режим инкогнито': 'incognito_tab()', 'Свернуть окно': 'rollup()', 'Развернуть окно': 'unwrap()', 'Закрыть окно': 'close()', 'В конец страницы': 'end()', 'В начало страницы': 'home()', 'Пролистать вверх': 'up()', 'Пролистать вниз': 'down()'}
    MATCH_SHOW = {'new_tab()': 'Новая вкладка', 'prev_tab()': 'Предыдущая вкладка', 'next_tab()': 'Следующая вкладка', 'incognito_tab()': 'Режим инкогнито', 'rollup()': 'Свернуть окно', 'unwrap()': 'Развернуть окно', 'close()': 'Закрыть окно', 'end()': 'В конец страницы', 'home()': 'В начало страницы', 'up()': 'Пролистать вверх', 'down()': 'Пролистать вниз'}
    PAREMETER_COMMANDS=['Открыть приложение', 'Открыть сайт', 'Подождать (сек)', 'Выполнить команду CMD', 'Выполнить команду Python']
    CHOICES_DROPDOWN_OPTIONS=list(map(lambda x: ft.DropdownOption(x), CHOICES))

    # Служебная функция, удаляюзщая элементы массива из строки
    def replace_strings(string, array):
        for line in array:
            string=string.replace(line, '')
        return string
    
    def open_new_page(route):
        global previous
        previous=page.route
        page.go(route)
        
    with open(Path('files/config.json').resolve(), 'r', encoding = 'UTF-8') as config_json_file:
        config_json = json.load(config_json_file)

    with open(Path('docs/about_app.md').resolve(), 'r', encoding = 'UTF-8') as about_app_markdown_file:
        about_app_markdown_text = about_app_markdown_file.read()

    with open(Path('docs/settings.md').resolve(), 'r', encoding = 'UTF-8') as settings_markdown_file:
        settings_markdown_text = settings_markdown_file.read()

    with open(Path('docs/scripts.md').resolve(), 'r', encoding = 'UTF-8') as scripts_markdown_file:
        scripts_markdown_text = scripts_markdown_file.read()

    with open(Path('docs/functions.md').resolve(), 'r', encoding = 'UTF-8') as functions_markdown_file:
        functions_markdown_text = functions_markdown_file.read()

    with open(Path('docs/keywords.md').resolve(), 'r', encoding = 'UTF-8') as keywords_markdown_file:
        keywords_markdown_text = keywords_markdown_file.read()
    
    appbar=ft.AppBar(title=ft.Text('Голосовой ассистент «Альфа»', weight=ft.FontWeight.BOLD), elevation=2, automatically_imply_leading=False, elevation_on_scroll=False)
    

    side_panel_label = ft.Container(ft.Text('Управление', size=24, weight=ft.FontWeight.BOLD), padding=ft.padding.only(left=5))
    
    home_page_button=ft.TextButton(content=ft.Container(content=ft.Text('Главная', size=24, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center_left, padding=ft.padding.only(left=5)),
            width=170,
            height=50,
            on_click=lambda e: page.go('/')
    )

    settings_page_button=ft.TextButton(content=ft.Container(content=ft.Text('Настройки', size=24, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center_left, padding=ft.padding.only(left=5)),
            width=170,
            height=50,
            on_click=lambda e: page.go('/settings')
    )

    scripts_page_button=ft.TextButton(content=ft.Container(content=ft.Text('Сценарии', size=24, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center_left, padding=ft.padding.only(left=5)),
            width=170,
            height=50,
            on_click=lambda e: page.go('/scripts')
        )
    
    docs_page_button=ft.TextButton(content=ft.Container(content=ft.Text('Справка', size=24, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center_left, padding=ft.padding.only(left=5)),
            width=170,
            height=50,
            on_click=lambda e: open_new_page('/docs')
        )
    
    run_assistant_button=ft.ElevatedButton(content=ft.Container(content=ft.Text('Запустить', size=24, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center_left, padding=ft.padding.only(left=5)),
            width=170,
            height=50,
            on_click=lambda e: os.startfile('app.exe')
        )

    side_column = ft.Column(controls=[side_panel_label, run_assistant_button, home_page_button, settings_page_button, scripts_page_button, docs_page_button])


    
    docs_card=ft.Container(ft.Card(content=ft.Container(ft.Column(controls=[
        ft.Container(content=ft.Text('Документация', weight=ft.FontWeight.BOLD, size=19), alignment=ft.alignment.top_left, padding=ft.padding.only(left=10, right=10, top=7, bottom=1)), 
        ft.Container(content=ft.Text('Подробная инструкция', weight=ft.FontWeight.BOLD, size=14.5), alignment=ft.alignment.center_left, padding=ft.padding.only(left=10, right=10, top=1, bottom=1)), 
        ft.Container(content=ft.TextButton(content=ft.Container(content=ft.Text('Изучить', size=15, weight=ft.FontWeight.BOLD)), on_click=lambda e: open_new_page('/docs')), alignment=ft.alignment.bottom_right, padding=ft.padding.only(left=7, right=7, top=1, bottom=7))], 
        expand=True), expand=True), expand=True), width=220, height=130)
    
    github_card=ft.Container(ft.Card(content=ft.Container(ft.Column(controls=[
        ft.Container(content=ft.Text('GitHub проекта', weight=ft.FontWeight.BOLD, size=19), alignment=ft.alignment.top_left, padding=ft.padding.only(left=10, right=10, top=7, bottom=1)), 
        ft.Container(content=ft.Text('Репозиторий', weight=ft.FontWeight.BOLD, size=14.5), alignment=ft.alignment.center_left, padding=ft.padding.only(left=10, right=10, top=1, bottom=1)), 
        ft.Container(content=ft.TextButton(content=ft.Container(content=ft.Text('Перейти', size=15, weight=ft.FontWeight.BOLD)), on_click=lambda e: webbrowser.open('https://github.com/maxstepashka/Alpha-voice-assistant')), alignment=ft.alignment.bottom_right, padding=ft.padding.only(left=7, right=7, top=1, bottom=7))], 
        expand=True), expand=True), expand=True), width=220, height=130)

    logo=ft.Container(content=ft.Row([ft.Image(src='alpha.png', width=80, height=80), ft.Container(ft.Text('Голосовой ассистент «Альфа»', size=30, weight=ft.FontWeight.BOLD), padding=ft.padding.only(left=5))]), padding=ft.padding.only(left=5))

    home_column=ft.Container(content=ft.Column(controls=[logo, ft.Row(controls=[docs_card, github_card])], alignment=ft.MainAxisAlignment.CENTER), expand=True)




    assistant_settings_label=ft.Text('Настройки ассистента', size=24, weight=ft.FontWeight.BOLD) 

    assistant_settings_main_label=ft.Container(ft.Text('Основные', size=22, weight=ft.FontWeight.BOLD))

    activation_phrase_label=ft.Container(ft.Text('Активационная фраза', size=18, weight=ft.FontWeight.BOLD, color='#FFB781'))

    activation_phrase_field=ft.TextField(value=config_json['wakeword'], hint_text='Активационная фраза', width=330)
    
    time_accept_label=ft.Container(ft.Text('Прием команд без активационной фразы, с', size=18, weight=ft.FontWeight.BOLD, color='#FFB781'), padding=ft.padding.only(top=6))

    time_accept_field=ft.TextField(value=config_json['time'], hint_text='Время в секундах', width=330)


    assistant_settings_search_systems_label=ft.Container(ft.Text('Поисковые системы', size=22, weight=ft.FontWeight.BOLD), padding=ft.padding.only(top=10))

    search_system_label=ft.Container(ft.Text('Поиск информации', size=18, weight=ft.FontWeight.BOLD, color='#FFB781'), padding=ft.padding.only(top=6))

    search_system_field=ft.Dropdown(value=config_json['search'], options=[ft.DropdownOption('Яндекс'), ft.DropdownOption('Bing'), ft.DropdownOption('DuckDuckGo')], width=330)

    music_search_system_label=ft.Container(ft.Text('Поиск музыки', size=18, weight=ft.FontWeight.BOLD, color='#FFB781'), padding=ft.padding.only(top=6))

    music_search_system_field=ft.Dropdown(value=config_json['music_search'], options=[ft.DropdownOption('Яндекс Музыка'), ft.DropdownOption('Звук')], width=330)

    video_search_system_label=ft.Container(ft.Text('Поиск видео', size=18, weight=ft.FontWeight.BOLD, color='#FFB781'), padding=ft.padding.only(top=6))

    video_search_system_field=ft.Dropdown(value=config_json['video_search'], options=[ft.DropdownOption('ВК Видео'), ft.DropdownOption('Rutube')], width=330)


    assistant_settings_config_label=ft.Container(ft.Text('Конфигурация ассистента', size=22, weight=ft.FontWeight.BOLD), padding=ft.padding.only(top=10))

    recognition_type_label=ft.Container(ft.Text('Распознавание речи', size=18, weight=ft.FontWeight.BOLD, color='#FFB781'), padding=ft.padding.only(top=6))

    recognition_type_field=ft.Dropdown(value=config_json['recognition'], options=[ft.DropdownOption('Vosk'), ft.DropdownOption('Speech Recognition')], width=330)

    vosk_version_label=ft.Container(ft.Text('Версия модели Vosk', size=18, weight=ft.FontWeight.BOLD, color='#FFB781'), padding=ft.padding.only(top=6))

    vosk_version_field=ft.Dropdown(value=config_json['vosk_model'], options=[ft.DropdownOption('0.22'), ft.DropdownOption('0.4')], width=330)


    settings_save_button=ft.ElevatedButton(text='Сохранить', icon=ft.Icons.SAVE, on_click=lambda e: save_settings())

    settings_column=ft.Container(ft.Column(controls=[
        assistant_settings_label, assistant_settings_main_label, activation_phrase_label, activation_phrase_field, time_accept_label, time_accept_field, ft.Divider(), assistant_settings_search_systems_label, search_system_label, search_system_field, music_search_system_label, music_search_system_field, video_search_system_label, video_search_system_field, ft.Divider(), assistant_settings_config_label, recognition_type_label, recognition_type_field, vosk_version_label, vosk_version_field 
    ], scroll=True, alignment=ft.MainAxisAlignment.START), expand=True, padding=ft.padding.only(left=5, top=7), alignment=ft.alignment.top_left)


    def save_settings():
        config_json={}
        config_json['wakeword']=activation_phrase_field.value
        config_json['time']=time_accept_field.value
        config_json['search']=search_system_field.value
        config_json['music_search']=music_search_system_field.value
        config_json['video_search']=video_search_system_field.value
        config_json['recognition']=recognition_type_field.value
        config_json['vosk_model']=vosk_version_field.value

        with open(Path('files/config.json').resolve(), 'w', encoding='UTF-8') as scripts_json_file:
            json.dump(config_json, scripts_json_file, ensure_ascii=False, indent=2)
        
        page.open(ft.SnackBar(content=ft.Text('Настройки сохранены.'), show_close_icon=True, bgcolor=ft.Colors.PRIMARY))
    



    scripts_label=ft.Text('Сценарии', size=24, weight=ft.FontWeight.BOLD) 

    scripts_search_field=ft.TextField(hint_text='Запрос', width=490)

    scripts_search_button=ft.ElevatedButton(icon=ft.Icons.SEARCH, text='Найти', on_click=lambda e: scripts_search())

    scripts_clear_button=ft.ElevatedButton(icon=ft.Icons.CLEAR, text='Очистить', on_click=lambda e: scripts_search_clear())

    add_script_button=ft.ElevatedButton(icon=ft.Icons.ADD, text='Добавить', on_click=lambda e: open_new_page('/add_script'))

    import_scripts_button=ft.ElevatedButton(icon=ft.Icons.UPLOAD, text='Загрузить из файла', on_click=lambda e: scripts_import_file_dialog.pick_files(allow_multiple=False))

    export_scripts_button=ft.ElevatedButton(icon=ft.Icons.DOWNLOAD, text='Сохранить в файл', on_click=lambda e: scripts_export_file_dialog.pick_files(allow_multiple=False))

    add_script_name_field=ft.TextField(hint_text='Имя', width=330)

    add_script_keyword_field=ft.TextField(hint_text='Ключевая фраза', width=330)

    add_script_insert_button=ft.ElevatedButton('Добавить поле', icon=ft.Icons.ADD, on_click=lambda e: add_script_block_column_insert())

    add_script_save_button=ft.ElevatedButton('Сохранить', icon=ft.Icons.SAVE, on_click=lambda e: add_script())
    

    def pick_scripts_import_file(e: ft.FilePickerResultEvent):
        scripts_import_file_name = (
            "".join(map(lambda f: f.path, e.files)) if e.files else None
        )
        import_scripts(scripts_import_file_name)

    scripts_import_file_dialog = ft.FilePicker(on_result=pick_scripts_import_file)
    page.overlay.append(scripts_import_file_dialog)


    def pick_scripts_export_file(e: ft.FilePickerResultEvent):
        scripts_export_file_name = (
            "".join(map(lambda f: f.path, e.files)) if e.files else None
        )
        export_scripts(scripts_export_file_name)

    scripts_export_file_dialog = ft.FilePicker(on_result=pick_scripts_export_file)
    page.overlay.append(scripts_export_file_dialog)




    def make_scripts_blocks(scripts_json: Optional[dict]):
        if scripts_json==None:
            with open(Path('files/scripts.json').resolve(), 'r', encoding='UTF-8') as scripts_json_file:
                scripts_json=json.loads(scripts_json_file.read())
        global scripts_listview
        scripts_listview=ft.ListView(divider_thickness=0.1, controls=[ft.Column([scripts_label, ft.Row([scripts_search_field, scripts_search_button, scripts_clear_button]), ft.Divider(), ft.Row([add_script_button, import_scripts_button, export_scripts_button]), ft.Divider()])], padding=ft.padding.only(left=5, top=7))
        for name in scripts_json:
            block_raw = {'name': ft.Text(name, weight=ft.FontWeight.BOLD, size=23), 'keyword': ft.Text('Ключевая фраза: ' + scripts_json[name][1], weight=ft.FontWeight.BOLD, size=19), 'lines': []}
            script=scripts_json[name][0]
            for line in script:
                if line.startswith('open_app'):
                    line = line + '.END'
                    text = 'Открыть ' + replace_strings(line, ["open_app(r'", "').END"])
                elif line.startswith('open_site'):
                    line = line + '.END'
                    text = 'Открыть ' + replace_strings(line, ["open_site(r'", "').END"])
                elif line.startswith('time.sleep'):
                    line = line + '.END'
                    text = 'Подождать ' + replace_strings(line, ["time.sleep(", ").END"]) + ' секунд'
                elif line.startswith('command_line'):
                    line = line + '.END'
                    text = 'Выполнить команду CMD: ' + replace_strings(line, ["command_line(r'", "').END"])
                elif line.startswith('python'):
                    line = line + '.END'
                    text = 'Выполнить команду Python: ' + replace_strings(line, ["python(r'", "').END"])
                else:
                    text = MATCH_SHOW[line]
                block_raw['lines'].append(ft.Container(ft.Text(text, weight=ft.FontWeight.BOLD, size=18, color='#FFB781')))
            block=ft.Column([block_raw['name'], block_raw['keyword']])
            block.controls.extend(block_raw['lines'])

            block.controls.extend([ft.Row([ft.ElevatedButton('Изменить', icon=ft.Icons.EDIT, on_click=lambda e: init_edit_script(e.control.data), data=name), ft.ElevatedButton('Удалить', icon=ft.Icons.DELETE, color=ft.Colors.RED_500, on_click=lambda e: delete_script(e.control.data), data=name)]), ft.Divider()])
            scripts_listview.controls.append(block)


    def scripts_search():
        to_remove=[]
        with open(Path('files/scripts.json').resolve(), 'r', encoding='UTF-8') as scripts_json_file:
            scripts_json=json.loads(scripts_json_file.read())
        for name in scripts_json:
            if scripts_search_field.value.lower() not in name.lower():
                to_remove.append(name)
        for name in to_remove:
            scripts_json.pop(name)
        make_scripts_blocks(scripts_json)
        page.views.clear()
        page.views.append(
            ft.View(
                '/scripts',
                [
                    appbar, ft.Row(expand=True, controls=[ft.Container(alignment=ft.alignment.center, content=side_column, padding=7, expand=False), ft.VerticalDivider(width=0.1, color=ft.Colors.GREY_800), ft.Container(scripts_listview, expand=True)])
                ],
            )
        )
        page.update()

    def scripts_search_clear():  
        make_scripts_blocks(None)
        page.views.clear()
        scripts_search_field.value=None
        page.views.append(
            ft.View(
                '/scripts',
                [
                    appbar, ft.Row(expand=True, controls=[ft.Container(alignment=ft.alignment.center, content=side_column, padding=7, expand=False), ft.VerticalDivider(width=0.1, color=ft.Colors.GREY_800), ft.Container(scripts_listview, expand=True)])
                ],
            )
        )
        page.update()

    def delete_script(name):
        with open(Path('files/scripts.json').resolve(), 'r', encoding='UTF-8') as scripts_json_file:
            scripts_json = json.load(scripts_json_file)
            scripts_json.pop(name)
        

        with open(Path('files/scripts.json').resolve(), 'w', encoding='UTF-8') as scripts_json_file:
            json.dump(scripts_json, scripts_json_file, ensure_ascii=False, indent=2)
          


        with open(Path('files/weights.json').resolve(), 'r', encoding='UTF-8') as weights_json_file:
            weights_json = json.load(weights_json_file)
            weights_json['script'].pop(name)
        

        with open(Path('files/weights.json').resolve(), 'w', encoding='UTF-8') as weights_json_file:
            json.dump(weights_json, weights_json_file, ensure_ascii=False, indent=2)
        

        with open(Path('files/keywords.json').resolve(), 'r', encoding='UTF-8') as keywords_json_file:
            keywords_json = json.load(keywords_json_file)
            for word in keywords_json['script']:
                items_to_delete = []
                for item in keywords_json['script'][word]:
                    if item['param'] == name:
                        items_to_delete.append(item)
                for item_to_delete in items_to_delete:
                    keywords_json['script'][word].remove(item_to_delete)
            words_to_delete = []
            for word in keywords_json['script']:
                if keywords_json['script'][word] == []:
                    words_to_delete.append(word)
            for word_to_delete in words_to_delete:
                keywords_json['script'].pop(word_to_delete)
                for item in keywords_json['main'][word_to_delete]:
                    if item['param'] == 'script':
                        keywords_json['main'][word_to_delete].remove(item)
                if keywords_json['main'][word_to_delete] == []:
                    keywords_json['main'].pop(word_to_delete)

        page.views.clear()
        make_scripts_blocks(None)
        appbar.leading=None
        page.views.append(
            ft.View(
                '/scripts',
                [
                    appbar, ft.Row(expand=True, controls=[ft.Container(alignment=ft.alignment.center, content=side_column, padding=7, expand=False), ft.VerticalDivider(width=0.1, color=ft.Colors.GREY_800), ft.Container(scripts_listview, expand=True)])
                ],
            )
        )
        page.update()
        

        with open(Path('files/keywords.json').resolve(), 'w', encoding='UTF-8') as keywords_json_file:
            json.dump(keywords_json, keywords_json_file, ensure_ascii=False, indent=2)

    def init_add_script_column():
        global add_script_block_index
        global add_script_column
        global add_script_block_column

        add_script_block_index=0
        add_script_block_column=ft.Column([
            ft.Column([
                ft.Dropdown(value='Открыть приложение', options=CHOICES_DROPDOWN_OPTIONS, width=330, data=add_script_block_index, on_change=lambda e: add_script_param_field_validate(e.control.data)), 
                ft.TextField(hint_text='Путь', width=330), 
                ft.ElevatedButton('Удалить', icon=ft.Icons.DELETE, color=ft.Colors.RED_500, data=add_script_block_index, on_click=lambda e: add_script_delete_field(e.control.data)), 
                ft.Divider()
            ], data=add_script_block_index), 
            ft.Column([add_script_insert_button, add_script_save_button])
        ])

        add_script_column=ft.ListView([
            ft.Column([
                ft.Container(ft.Text('Добавление', weight=ft.FontWeight.BOLD, size=23), padding=ft.padding.only(top=5, bottom=5)), 
                ft.Container(ft.Text('Имя', weight=ft.FontWeight.BOLD, size=18), padding=ft.padding.only(top=5, bottom=5)), 
                add_script_name_field, 
                ft.Container(ft.Text('Ключевая фраза', weight=ft.FontWeight.BOLD, size=18), padding=ft.padding.only(top=5, bottom=5)), 
                add_script_keyword_field, 
                ft.Divider(),
                ft.Container(ft.Text('Действия', weight=ft.FontWeight.BOLD, size=18), padding=ft.padding.only(top=5, bottom=5))
            ]), 
            add_script_block_column
        ], expand=True, padding=ft.padding.only(left=5, top=2))



    def add_script_block_column_insert():
        global add_script_block_index
        global add_script_block_column
        add_script_block_index+=1
        add_script_block_column.controls[-1]=ft.Column([
            ft.Dropdown(value='Открыть приложение', options=CHOICES_DROPDOWN_OPTIONS, width=330, data=add_script_block_index, on_change=lambda e: add_script_param_field_validate(e.control.data)), 
            ft.TextField(hint_text='Путь', width=330), 
            ft.ElevatedButton('Удалить', icon=ft.Icons.DELETE, color=ft.Colors.RED_500, data=add_script_block_index, on_click=lambda e: add_script_delete_field(e.control.data)), 
            ft.Divider()
            ], data=add_script_block_index)
        add_script_block_column.controls.append(ft.Column([add_script_insert_button, add_script_save_button]))
        page.update()


    def add_script_param_field_validate(block_index):
        for block in add_script_block_column.controls:
            if block.data==block_index:
                if block.controls[0].value in PAREMETER_COMMANDS:
                    match block.controls[0].value:
                        case 'Открыть приложение':
                            block.controls[1].hint_text='Путь'
                        case 'Открыть сайт':
                            block.controls[1].hint_text='Ссылка'
                        case 'Подождать (сек)':
                            block.controls[1].hint_text='Время в секундах'
                        case 'Выполнить команду CMD':
                            block.controls[1].hint_text='Команда CMD'
                        case 'Выполнить команду Python':
                            block.controls[1].hint_text='Команда Python'
                    block.controls[1].visible=True
                else: 
                    block.controls[1].visible=False
        page.update()
        

    def add_script_delete_field(block_index):
        for block in add_script_block_column.controls:
            if block.data==block_index:
                add_script_block_column.controls.remove(block)
        page.views.clear()
        page.views.append(
            ft.View(
                '/add_script',
                [
                    appbar, add_script_column
                ],
            )
        )
        page.update()


    def add_script():
        actions=[]
        name=add_script_name_field.value
        keyword=add_script_keyword_field.value
        for block in add_script_block_column.controls[:-1]:
            match block.controls[0].value:
                case 'Открыть сайт':
                    actions.append(f"open_site(r'{block.controls[1].value}')")
                case 'Открыть приложение':
                    actions.append(f"open_app(r'{block.controls[1].value}')")
                case 'Открыть приложение':
                    actions.append(f"open_app(r'{block.controls[1].value}')")
                case 'Подождать (сек)':
                    actions.append(f"time.sleep({float(block.controls[1].value.replace(',', '.'))})")
                case 'Выполнить команду CMD':
                    actions.append(f"command_line(r'{block.controls[1].value}')")
                case 'Выполнить команду Python':
                    actions.append(f"python(r'{block.controls[1].value}')")
                case _:
                    actions.append(MATCH_PROCESS[block.controls[0].value])

        with open(Path('files/scripts.json').resolve(), 'r', encoding='UTF-8') as scripts_json_file:
            scripts_json = json.load(scripts_json_file)
            scripts_json={name: [actions, keyword]} | scripts_json
        
        with open(Path('files/scripts.json').resolve(), 'w', encoding='UTF-8') as scripts_json_file:
            json.dump(scripts_json, scripts_json_file, ensure_ascii=False, indent=2)
        

        with open(Path('files/weights.json').resolve(), 'r', encoding='UTF-8') as weights_json_file:
            weights_json = json.load(weights_json_file)
            weights_json['script'][name] = 0
        

        with open(Path('files/weights.json').resolve(), 'w', encoding='UTF-8') as weights_json_file:
            json.dump(weights_json, weights_json_file, ensure_ascii=False, indent=2)


        keyword=keyword.replace(',', '')
        keyword = keyword.lower().split()

        with open(Path('files/keywords.json').resolve(), 'r', encoding='UTF-8') as keywords_json_file:
            keywords_json = json.load(keywords_json_file)
            for word in keyword:
                try:
                    keywords_json['script'][word].append({'param': name, 'weight': 1/len(keyword)})
                except:
                    keywords_json['script'][word] = []
                    keywords_json['script'][word].append({'param': name, 'weight': 1/len(keyword)})

                try:
                    if {'param': 'script', 'weight': 1/len(keyword)} not in keywords_json['main'][word]:
                        keywords_json['main'][word].append({'param': 'script', 'weight': 1/len(keyword)})
                except:
                    keywords_json['main'][word] = []
                    keywords_json['main'][word].append({'param': 'script', 'weight': 1/len(keyword)})
            

        with open(Path('files/keywords.json').resolve(), 'w', encoding='UTF-8') as keywords_json_file:
            json.dump(keywords_json, keywords_json_file, ensure_ascii=False, indent=2)

        page.go("/scripts")
        

    edit_script_insert_button=ft.ElevatedButton('Добавить поле', icon=ft.Icons.ADD, on_click=lambda e: edit_script_block_column_insert())

    edit_script_save_button=ft.ElevatedButton('Сохранить', icon=ft.Icons.SAVE, on_click=lambda e: edit_script(e.control.data))

    def init_edit_script(name):
        edit_script_save_button.data=name
        global edit_script_block_index
        global edit_script_column
        global edit_script_block_column
        global editing_script

        with open(Path('files/scripts.json').resolve(), 'r', encoding='UTF-8') as scripts_json_file:
            scripts_json=json.loads(scripts_json_file.read())
        
        editing_script=scripts_json[name][0]
        
        edit_script_block_index=-1
        edit_script_block_column=ft.Column([
            edit_script_insert_button
        ])

        for line in editing_script:
            if line.startswith('open_app'):
                line = line + '.END'
                category="Открыть приложение"
                param = replace_strings(line, ["open_app(r'", "').END"])
            elif line.startswith('open_site'):
                line = line + '.END'
                category="Открыть сайт"
                param = replace_strings(line, ["open_site(r'", "').END"])
            elif line.startswith('time.sleep'):
                line = line + '.END'
                category="Подождать (сек)"
                param = replace_strings(line, ["time.sleep(", ").END"])
            elif line.startswith('command_line'):
                line = line + '.END'
                category="Выполнить команду CMD"
                param = replace_strings(line, ["command_line(r'", "').END"])
            elif line.startswith('python'):
                line = line + '.END'
                category="Выполнить команду Python"
                param = replace_strings(line, ["python(r'", "').END"])
            else:
                category = MATCH_SHOW[line]
                param=None
            edit_script_block_index+=1
            edit_script_block_column.controls[-1]=ft.Column([
                ft.Dropdown(value=category, options=CHOICES_DROPDOWN_OPTIONS, width=330, data=edit_script_block_index, on_change=lambda e: edit_script_param_field_validate(e.control.data)), 
                ft.TextField(value=param, width=330, visible=True if category in PAREMETER_COMMANDS else False), 
                ft.ElevatedButton('Удалить', icon=ft.Icons.DELETE, color=ft.Colors.RED_500, data=edit_script_block_index, on_click=lambda e: edit_script_delete_field(e.control.data)), 
                ft.Divider()
            ], data=edit_script_block_index)
            edit_script_block_column.controls.append(ft.Column([edit_script_insert_button, edit_script_save_button]))

        edit_script_column=ft.ListView([
            ft.Column([
                ft.Container(ft.Text(f'Редактирование сценария «{name}»', weight=ft.FontWeight.BOLD, size=23), padding=ft.padding.only(top=5, bottom=5)), 
                ft.Divider(),
                ft.Container(ft.Text('Действия', weight=ft.FontWeight.BOLD, size=18), padding=ft.padding.only(top=5, bottom=5))
            ]), 
            edit_script_block_column
        ], expand=True, padding=ft.padding.only(left=5, top=2))

        open_new_page('/edit_script')

    def edit_script_block_column_insert():
        global edit_script_block_index
        global edit_script_block_column
        edit_script_block_index+=1
        edit_script_block_column.controls[-1]=ft.Column([
            ft.Dropdown(value='Открыть приложение', options=CHOICES_DROPDOWN_OPTIONS, width=330, data=edit_script_block_index, on_change=lambda e: edit_script_param_field_validate(e.control.data)), 
            ft.TextField(hint_text='Путь', width=330), 
            ft.ElevatedButton('Удалить', icon=ft.Icons.DELETE, color=ft.Colors.RED_500, data=edit_script_block_index, on_click=lambda e: edit_script_delete_field(e.control.data)), 
            ft.Divider()
            ], data=edit_script_block_index)
        edit_script_block_column.controls.append(ft.Column([edit_script_insert_button, edit_script_save_button]))
        page.update()

    def edit_script_param_field_validate(block_index):
        for block in edit_script_block_column.controls:
            if block.data==block_index:
                if block.controls[0].value in PAREMETER_COMMANDS:
                    match block.controls[0].value:
                        case 'Открыть приложение':
                            block.controls[1].hint_text='Путь'
                        case 'Открыть сайт':
                            block.controls[1].hint_text='Ссылка'
                        case 'Подождать (сек)':
                            block.controls[1].hint_text='Время в секундах'
                        case 'Выполнить команду CMD':
                            block.controls[1].hint_text='Команда CMD'
                        case 'Выполнить команду Python':
                            block.controls[1].hint_text='Команда Python'
                    block.controls[1].visible=True
                else: 
                    block.controls[1].visible=False
                block.controls[1].value=None
        page.update()
        

    def edit_script_delete_field(block_index):
        for block in edit_script_block_column.controls:
            if block.data==block_index:
                edit_script_block_column.controls.remove(block)
        page.views.clear()
        page.views.append(
            ft.View(
                '/edit_script',
                [
                    appbar, edit_script_column
                ],
            )
        )
        page.update()


    def edit_script(name):
        actions=[]
        for block in edit_script_block_column.controls[:-1]:
            match block.controls[0].value:
                case 'Открыть сайт':
                    actions.append(f"open_site(r'{block.controls[1].value}')")
                case 'Открыть приложение':
                    actions.append(f"open_app(r'{block.controls[1].value}')")
                case 'Открыть приложение':
                    actions.append(f"open_app(r'{block.controls[1].value}')")
                case 'Подождать (сек)':
                    actions.append(f"time.sleep({float(block.controls[1].value.replace(',', '.'))})")
                case 'Выполнить команду CMD':
                    actions.append(f"command_line(r'{block.controls[1].value}')")
                case 'Выполнить команду Python':
                    actions.append(f"python(r'{block.controls[1].value}')")
                case _:
                    actions.append(MATCH_PROCESS[block.controls[0].value])

        with open(Path('files/scripts.json').resolve(), 'r', encoding='UTF-8') as scripts_json_file:
            scripts_json = json.load(scripts_json_file)
            scripts_json[name][0]=actions
        
        with open(Path('files/scripts.json').resolve(), 'w', encoding='UTF-8') as scripts_json_file:
            json.dump(scripts_json, scripts_json_file, ensure_ascii=False, indent=2)

        page.go('/scripts')


    def import_scripts(file_name):
        with open(file_name, 'r', encoding='UTF-8') as apf_json_file:
            apf_json = json.load(apf_json_file)
            keywords_json = apf_json['keywords']
            weights_json = apf_json['weights']
            scripts_json = apf_json['scripts']

        with open(Path('files/keywords.json').resolve(), 'w', encoding='UTF-8') as keywords_json_file:
            json.dump(keywords_json, keywords_json_file, ensure_ascii=False, indent=2)

        with open(Path('files/weights.json').resolve(), 'w', encoding='UTF-8') as weights_json_file:
            json.dump(weights_json, weights_json_file, ensure_ascii=False, indent=2)

        with open(Path('files/scripts.json').resolve(), 'w', encoding='UTF-8') as scripts_json_file:
            json.dump(scripts_json, scripts_json_file, ensure_ascii=False, indent=2)

        make_scripts_blocks(None)
        page.views.clear()
        page.views.append(
            ft.View(
                '/scripts',
                [
                    appbar, ft.Row(expand=True, controls=[ft.Container(alignment=ft.alignment.center, content=side_column, padding=7, expand=False), ft.VerticalDivider(width=0.1, color=ft.Colors.GREY_800), ft.Container(scripts_listview, expand=True)])
                ],
            )
        )
        page.update()
        

    def export_scripts(file_name):
        with open(Path('files/keywords.json').resolve(), 'r', encoding='UTF-8') as keywords_json_file:
            keywords_json = json.load(keywords_json_file)

        with open(Path('files/weights.json').resolve(), 'r', encoding='UTF-8') as weights_json_file:
            weights_json = json.load(weights_json_file)

        with open(Path('files/scripts.json').resolve(), 'r', encoding='UTF-8') as scripts_json_file:
            scripts_json = json.load(scripts_json_file)
        
        with open(file_name, 'w', encoding='UTF-8') as apf_json_file:
            apf_json = {'keywords': keywords_json, 'weights': weights_json, 'scripts': scripts_json}
            json.dump(apf_json, apf_json_file, ensure_ascii=False, indent=2)
        
        page.open(ft.SnackBar(content=ft.Text('Сценарии сохранены.'), show_close_icon=True, bgcolor=ft.Colors.PRIMARY, action='Показать в папке', on_action=lambda e: os.system(f'explorer {os.path.dirname(file_name)}')))



    def open_doc(text_name):
        docs_markdown_renderer.value=text_name
        docs_markdown_renderer.update()

    docs_label = ft.Text('Документация', size=24, weight=ft.FontWeight.BOLD)

    about_app_docs_button=ft.TextButton(content=ft.Container(content=ft.Text('Основы', size=24, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center_left, padding=ft.padding.only(left=5)),
            width=170,
            height=50,
            on_click=lambda e: open_doc(about_app_markdown_text)
    )

    settings_docs_button=ft.TextButton(content=ft.Container(content=ft.Text('Настройки', size=24, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center_left, padding=ft.padding.only(left=5)),
            width=170,
            height=50,
            on_click=lambda e: open_doc(settings_markdown_text)
    )

    sсripts_docs_button=ft.TextButton(content=ft.Container(content=ft.Text('Сценарии', size=24, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center_left, padding=ft.padding.only(left=5)),
            width=170,
            height=50,
            on_click=lambda e: open_doc(scripts_markdown_text)
    )

    functions_docs_button=ft.TextButton(content=ft.Container(content=ft.Text('Функции', size=24, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center_left, padding=ft.padding.only(left=5)),
            width=170,
            height=50,
            on_click=lambda e: open_doc(functions_markdown_text)
    )

    keywords_docs_button=ft.TextButton(content=ft.Container(content=ft.Text('Команды', size=24, weight=ft.FontWeight.BOLD), alignment=ft.alignment.center_left, padding=ft.padding.only(left=5)),
            width=170,
            height=50,
            on_click=lambda e: open_doc(keywords_markdown_text)
    )



    docs_markdown_renderer=ft.Markdown(value=about_app_markdown_text, md_style_sheet=ft.MarkdownStyleSheet(p_text_style=ft.TextStyle(size=16), h2_text_style=ft.TextStyle(color="#FFB781"), h1_text_style=ft.TextStyle(color="#FFB781"), h1_padding=ft.padding.only(top=10), h2_padding=ft.padding.only(top=7)), selectable=True)

    docs_side_column=ft.Column(controls=[docs_label, about_app_docs_button, settings_docs_button, sсripts_docs_button, functions_docs_button, keywords_docs_button])

    def route_change(e):
        if page.route == '/':
            page.views.clear()
            appbar.leading=None
            page.views.append(
                ft.View(
                    '/',
                    [
                        appbar, ft.Row(expand=True, controls=[ft.Container(alignment=ft.alignment.center, content=side_column, padding=7, expand=False), ft.VerticalDivider(width=0.1, color=ft.Colors.GREY_800), home_column])
                    ],
                )
            )

        elif page.route == '/settings':
            page.views.clear()
            appbar.leading=None
            page.views.append(
                ft.View(
                    '/settings',
                    [
                        appbar, ft.Row(expand=True, controls=[ft.Container(alignment=ft.alignment.center, content=side_column, padding=7, expand=False), ft.VerticalDivider(width=0.1, color=ft.Colors.GREY_800), ft.Container(ft.Column([settings_column, ft.Divider(), settings_save_button], alignment=ft.MainAxisAlignment.CENTER, expand=True), alignment=ft.alignment.top_left, expand=True)])
                    ],
                )
            )

        elif page.route == '/scripts':
            page.views.clear()
            make_scripts_blocks(None)
            appbar.leading=None
            page.views.append(
                ft.View(
                    '/scripts',
                    [
                        appbar, ft.Row(expand=True, controls=[ft.Container(alignment=ft.alignment.center, content=side_column, padding=7, expand=False), ft.VerticalDivider(width=0.1, color=ft.Colors.GREY_800), ft.Container(scripts_listview, expand=True)])
                    ],
                )
            )

        elif page.route == '/add_script':
            page.views.clear()
            appbar.leading=ft.Container(ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: page.go(previous)), width=50, height=50, padding=2)
            init_add_script_column()
            page.views.append(
                ft.View(
                    '/add_script',
                    [
                        appbar, add_script_column
                    ],
                )
            )

        elif page.route == '/edit_script':
            page.views.clear()
            appbar.leading=ft.Container(ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: page.go(previous)), width=50, height=50, padding=2)
            init_add_script_column()
            page.views.append(
                ft.View(
                    '/edit_script',
                    [
                        appbar, edit_script_column
                    ],
                )
            )

        elif page.route == "/docs":
            appbar.actions=None
            appbar.leading=ft.Container(ft.IconButton(ft.Icons.ARROW_BACK, on_click=lambda e: page.go(previous)), width=50, height=50, padding=2)
            page.views.append(
                ft.View(
                    "/docs",
                    [
                        appbar, ft.Row(expand=True, controls=[ft.Container(alignment=ft.alignment.center_left, content=docs_side_column, padding=7, expand=False), ft.VerticalDivider(width=0.1, color=ft.Colors.GREY_800), ft.Container(content=ft.Column([docs_markdown_renderer], expand=True, scroll="hidden"), expand=8, alignment=ft.alignment.top_left, padding=ft.padding.only(left=10, bottom=10))])
                    ],
                )
            )

        page.update()

    page.on_route_change = route_change

    page.add(
        appbar, ft.Row(expand=True, controls=[ft.Container(alignment=ft.alignment.center, content=side_column, padding=7, expand=False), ft.VerticalDivider(width=0.1, color=ft.Colors.GREY_800), home_column])
    )
ft.app(target=main, assets_dir='assets')