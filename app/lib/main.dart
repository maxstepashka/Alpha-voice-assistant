import 'dart:io';
import 'dart:convert';

import 'package:flutter/material.dart';
import 'package:flutter/services.dart' show rootBundle;

import 'package:path/path.dart' as p;
import 'package:window_manager/window_manager.dart';
import 'package:file_picker/file_picker.dart';
import 'package:flutter_markdown_plus/flutter_markdown_plus.dart';
import 'package:url_launcher/url_launcher.dart';

final gitHubURL = Uri.parse('https://github.com/maxstepashka/Alpha-voice-assistant');

const parameterOptions = <String>[
  'open_site',
  'open_app',
  'time.sleep',
  'command_line',
  'python',
];

const optionsMatchShow = <String, String>{
  'new_tab()': 'Новая вкладка',
  'prev_tab()': 'Предыдущая вкладка',
  'next_tab()': 'Следующая вкладка',
  'incognito_tab()': 'Режим инкогнито',
  'rollup()': 'Свернуть окно',
  'unwrap()': 'Развернуть окно',
  'close()': 'Закрыть окно',
  'end()': 'В конец страницы',
  'home()': 'В начало страницы',
  'up()': 'Пролистать вверх',
  'down()': 'Пролистать вниз',
  'open_site': 'Открыть сайт',
  'open_app': 'Открыть приложение',
  'time.sleep': 'Подождать (сек)',
  'command_line': 'Выполнить команду CMD',
  'python': 'Выполнить команду Python',
};

final scriptBlockOptions = optionsMatchShow.entries.map((entry) {
      return DropdownMenuItem(
        value: entry.key,
        child: Text(entry.value.toString()),
      );
    }).toList();

String replaceStrings(String string, List<String> toReplace) {
  for (String line in toReplace) {
    string = string.replaceAll(line, '');
  }
  return string;
}

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await windowManager.ensureInitialized();
  WindowOptions windowOptions = WindowOptions(
    title: 'Голосовой ассистент «Альфа»',
    size: Size(960, 640),
    center: true,
  );
  await windowManager.waitUntilReadyToShow(windowOptions, () async {
    await windowManager.show();
    await windowManager.focus();
  });
  runApp(const AlphaApp());
}

class AlphaApp extends StatelessWidget {
  const AlphaApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Голосовой ассистент «Альфа»',
      theme: ThemeData(
        brightness: Brightness.dark,
        colorScheme: ColorScheme.fromSeed(
          seedColor: Color.fromARGB(255, 255, 136, 0),
          brightness: Brightness.dark,
        ),
      ),
      initialRoute: '/',
      routes: {
        '/': (context) => HomePage(),
        '/settings': (context) => SettingsPage(),
        '/scripts': (context) => ScriptsPage(),
        '/docs': (context) => DocsPage()
      },
    );
  }
}

class HomePage extends StatelessWidget {
  const HomePage({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color.fromARGB(255, 40, 29, 21),
        title: Text(
          'Голосовой ассистент «Альфа»',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
      ),
      body: Row(
        children: <Widget>[
          SideColumn(),
          Padding(
            padding: EdgeInsets.symmetric(vertical: 5),
            child: VerticalDivider(),
          ),
          Column(
            mainAxisAlignment: MainAxisAlignment.center,
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              Padding(
                padding: EdgeInsets.only(left: 5),
                child: Row(
                  children: <Widget>[
                    Image.asset(
                      'assets/alpha.png',
                      width: 80,
                      height: 80,
                    ),
                    Padding(
                      padding: EdgeInsets.only(left: 10),
                      child: Text(
                        'Голосовой ассистент «Альфа»',
                        style: TextStyle(
                          fontSize: 30,
                          fontWeight: FontWeight.bold
                        ),
                      ),
                    )
                  ],
                ),
              ),              
              Padding(
                padding: EdgeInsets.only(top: 10),
                child: Row(
                  children: <Widget>[
                    Padding(
                      padding: EdgeInsets.symmetric(horizontal: 5),
                      child: SizedBox(
                        height: 130,
                        width: 220,
                        child: Card(
                          child: Column(
                            children: <Widget>[
                              Padding(padding: EdgeInsets.only(
                                  left: 10,
                                  right: 10,
                                  top: 4,
                                  bottom: 1
                                ),
                                child: Align(
                                  alignment: Alignment.topLeft,
                                  child: Text(
                                    'Документация',
                                    style: TextStyle(
                                      fontSize: 19,
                                      fontWeight: FontWeight.bold
                                    ),
                                  ),
                                ) 
                              ),
                              Padding(padding: EdgeInsets.only(
                                  left: 10,
                                  right: 10,
                                  top: 6,
                                  bottom: 1
                                ),
                                child: Align(
                                  alignment: Alignment.topLeft,
                                  child: Text(
                                    'Подробная инструкция',
                                    style: TextStyle(
                                      fontSize: 14.5,
                                      fontWeight: FontWeight.bold
                                    ),
                                  ),
                                ) 
                              ),
                              Padding(padding: EdgeInsets.only(
                                  left: 7,
                                  right: 7,
                                  top: 15,
                                  bottom: 2
                                ),
                                child: Align(
                                  alignment: Alignment.bottomRight,
                                  child: TextButton(
                                    onPressed: () {
                                      Navigator.pushNamed(
                                        context,
                                        '/docs',
                                      );
                                    }, 
                                    child: Text(
                                      'Изучить',
                                      style: TextStyle(
                                        fontSize: 15,
                                        fontWeight: FontWeight.bold
                                      ),
                                    )
                                  ),  
                                ) 
                              ),
                            ],
                          ),
                        ),
                      ),
                    ),
                    Padding(
                      padding: EdgeInsets.symmetric(horizontal: 5),
                      child: SizedBox(
                        height: 130,
                        width: 220,
                        child: Card(
                          child: Column(
                            children: <Widget>[
                              Padding(padding: EdgeInsets.only(
                                  left: 10,
                                  right: 10,
                                  top: 4,
                                  bottom: 1
                                ),
                                child: Align(
                                  alignment: Alignment.topLeft,
                                  child: Text(
                                    'GitHub проекта',
                                    style: TextStyle(
                                      fontSize: 19,
                                      fontWeight: FontWeight.bold
                                    ),
                                  ),
                                ) 
                              ),
                              Padding(padding: EdgeInsets.only(
                                  left: 10,
                                  right: 10,
                                  top: 6,
                                  bottom: 1
                                ),
                                child: Align(
                                  alignment: Alignment.topLeft,
                                  child: Text(
                                    'Новости, обновления',
                                    style: TextStyle(
                                      fontSize: 14.5,
                                      fontWeight: FontWeight.bold
                                    ),
                                  ),
                                ) 
                              ),
                              Padding(padding: EdgeInsets.only(
                                  left: 7,
                                  right: 7,
                                  top: 15,
                                  bottom: 2
                                ),
                                child: Align(
                                  alignment: Alignment.bottomRight,
                                  child: TextButton(
                                    onPressed: () async {
                                     await launchUrl(gitHubURL);
                                    }, 
                                    child: Text(
                                      'Перейти',
                                      style: TextStyle(
                                        fontSize: 15,
                                        fontWeight: FontWeight.bold
                                      ),
                                    )
                                  ),  
                                ) 
                              ),
                            ],
                          ),
                        ),
                      ),
                    )
                  ],
                ),
              ),
            ],
          )
        ],
      ),
    );
  }
}

class SettingsPage extends StatefulWidget {
  const SettingsPage({super.key});

  @override
  State<SettingsPage> createState() => SettingsPageState();
}

class SettingsPageState extends State<SettingsPage> {
  late File settingsFile;
  Map<String, dynamic> settings = {};

  late TextEditingController wakewordController;
  late TextEditingController acceptTimeController;

  late String searchSystemValue;
  late String musicSearchSystemValue;
  late String videoSearchSystemValue;
  
  late String voskVersionValue;

  @override
  void initState() {
    super.initState();
    loadData();
  }

  void loadData() {
    File settingsFile = File(
      '${p.dirname(Platform.resolvedExecutable)}\\config\\config.json',
    );

    final settings = json.decode(settingsFile.readAsStringSync());

    wakewordController = TextEditingController(text: settings['wakeword']);

    acceptTimeController = TextEditingController(
      text: settings['accept_time'].toString(),
    );

    searchSystemValue = settings['search_system'];

    musicSearchSystemValue = settings['music_search_system'];

    videoSearchSystemValue = settings['video_search_system'];

    voskVersionValue = settings['vosk_version'];
  }

  void saveSettings() {
    Map settings = <String, String>{
      'wakeword': wakewordController.text,
      'accept_time': acceptTimeController.text,
      'search_system': searchSystemValue,
      'music_search_system': musicSearchSystemValue,
      'video_search_system': videoSearchSystemValue,
      'vosk_version': voskVersionValue,
    };

    final encoder = JsonEncoder.withIndent('  ');
    String settingsString = encoder.convert(settings);
    File settingsFile = File(
      '${p.dirname(Platform.resolvedExecutable)}\\config\\config.json',
    );
    settingsFile.writeAsStringSync(settingsString);

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('Настройки сохранены'),
        backgroundColor: Color.fromARGB(255, 255, 183, 129),
        showCloseIcon: true,
        duration: Duration(seconds: 1, milliseconds: 500),
      )
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color.fromARGB(255, 40, 29, 21),
        title: Text(
          'Голосовой ассистент «Альфа»',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
      ),
      body: Row(
        children: <Widget>[
          SideColumn(),
          Padding(
            padding: EdgeInsets.symmetric(vertical: 5),
            child: VerticalDivider(),
          ),
          Expanded(
            child: Column(
              children: <Widget>[
                Expanded(
                  child: ListView(
                    children: <Widget>[
                      Padding(
                        padding: EdgeInsets.only(
                          left: 10,
                          top: 15,
                          right: 15,
                          bottom: 5,
                        ),
                        child: Text(
                          'Настройки ассистента',
                          style: TextStyle(
                            fontSize: 24,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),

                      Padding(
                        padding: EdgeInsets.only(
                          left: 10,
                          top: 3,
                          right: 15,
                          bottom: 5,
                        ),
                        child: Text(
                          'Основные',
                          style: TextStyle(
                            fontSize: 22,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),

                      Padding(
                        padding: EdgeInsets.only(
                          left: 10,
                          top: 5,
                          right: 15,
                          bottom: 5,
                        ),
                        child: Text(
                          'Активационная фраза',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Color.fromARGB(255, 255, 183, 129),
                          ),
                        ),
                      ),

                      Padding(
                        padding: EdgeInsets.only(
                          left: 10,
                          top: 7,
                          right: 15,
                          bottom: 5,
                        ),
                        child: Align(
                          alignment: Alignment.centerLeft,
                          child: SizedBox(
                            width: 330,
                            child: TextField(
                              controller: wakewordController,
                              decoration: InputDecoration(
                                border: OutlineInputBorder(
                                  borderSide: BorderSide(color: Colors.black),
                                ),
                                hintText: 'Активационная фраза',
                              ),
                            ),
                          ),
                        ),
                      ),

                      Padding(
                        padding: EdgeInsets.only(
                          left: 10,
                          top: 5,
                          right: 15,
                          bottom: 5,
                        ),
                        child: Text(
                          'Приём команд без активационной фразы',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Color.fromARGB(255, 255, 183, 129),
                          ),
                        ),
                      ),

                      Padding(
                        padding: EdgeInsets.only(
                          left: 10,
                          top: 7,
                          right: 15,
                          bottom: 10,
                        ),
                        child: Align(
                          alignment: Alignment.centerLeft,
                          child: SizedBox(
                            width: 330,
                            child: TextField(
                              controller: acceptTimeController,
                              decoration: InputDecoration(
                                border: OutlineInputBorder(),
                                hintText: 'Время в секундах',
                              ),
                            ),
                          ),
                        ),
                      ),

                      Padding(
                        padding: EdgeInsets.only(right: 15, left: 10),
                        child: Divider(),
                      ),

                      Padding(
                        padding: EdgeInsets.only(
                          left: 10,
                          top: 10,
                          right: 15,
                          bottom: 5,
                        ),
                        child: Text(
                          'Поисковые системы',
                          style: TextStyle(
                            fontSize: 22,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),

                      Padding(
                        padding: EdgeInsets.only(
                          left: 10,
                          top: 5,
                          right: 15,
                          bottom: 5,
                        ),
                        child: Text(
                          'Поиск информации',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Color.fromARGB(255, 255, 183, 129),
                          ),
                        ),
                      ),

                      Padding(
                        padding: EdgeInsets.only(
                          left: 10,
                          top: 7,
                          right: 15,
                          bottom: 5,
                        ),
                        child: Align(
                          alignment: Alignment.centerLeft,
                          child: SizedBox(
                            width: 330,
                            child: DropdownButtonFormField(
                              decoration: InputDecoration(
                                border: OutlineInputBorder(),
                              ),
                              initialValue: searchSystemValue,
                              items: <DropdownMenuItem>[
                                DropdownMenuItem(
                                  value: 'Яндекс',
                                  child: Text('Яндекс'),
                                ),

                                DropdownMenuItem(
                                  value: 'Bing',
                                  child: Text('Bing'),
                                ),

                                DropdownMenuItem(
                                  value: 'DuckDuckGo',
                                  child: Text('DuckDuckGo'),
                                ),
                              ],
                              onChanged: (value) {
                                setState(() {
                                  searchSystemValue = value;
                                });
                              },
                            ),
                          ),
                        ),
                      ),

                      Padding(
                        padding: EdgeInsets.only(
                          left: 10,
                          top: 5,
                          right: 15,
                          bottom: 5,
                        ),
                        child: Text(
                          'Поиск музыки',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Color.fromARGB(255, 255, 183, 129),
                          ),
                        ),
                      ),

                      Padding(
                        padding: EdgeInsets.only(
                          left: 10,
                          top: 7,
                          right: 15,
                          bottom: 5,
                        ),
                        child: Align(
                          alignment: Alignment.centerLeft,
                          child: SizedBox(
                            width: 330,
                            child: DropdownButtonFormField(
                              decoration: InputDecoration(
                                border: OutlineInputBorder(),
                              ),
                              initialValue: musicSearchSystemValue,
                              items: <DropdownMenuItem>[
                                DropdownMenuItem(
                                  value: 'Яндекс Музыка',
                                  child: Text('Яндекс Музыка'),
                                ),

                                DropdownMenuItem(
                                  value: 'Звук',
                                  child: Text('Звук'),
                                ),
                              ],
                              onChanged: (value) {
                                setState(() {
                                  musicSearchSystemValue = value;
                                });
                              },
                            ),
                          ),
                        ),
                      ),

                      Padding(
                        padding: EdgeInsets.only(
                          left: 10,
                          top: 5,
                          right: 15,
                          bottom: 5,
                        ),
                        child: Text(
                          'Поиск видео',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Color.fromARGB(255, 255, 183, 129),
                          ),
                        ),
                      ),

                      Padding(
                        padding: EdgeInsets.only(
                          left: 10,
                          top: 7,
                          right: 15,
                          bottom: 5,
                        ),
                        child: Align(
                          alignment: Alignment.centerLeft,
                          child: SizedBox(
                            width: 330,
                            child: DropdownButtonFormField(
                              decoration: InputDecoration(
                                border: OutlineInputBorder(),
                              ),
                              initialValue: videoSearchSystemValue,
                              items: <DropdownMenuItem>[
                                DropdownMenuItem(
                                  value: 'ВК Видео',
                                  child: Text('ВК Видео'),
                                ),

                                DropdownMenuItem(
                                  value: 'Rutube',
                                  child: Text('Rutube'),
                                ),
                              ],
                              onChanged: (value) {
                                setState(() {
                                  videoSearchSystemValue = value;
                                });
                              },
                            ),
                          ),
                        ),
                      ),

                      Padding(
                        padding: EdgeInsets.only(right: 15, left: 10),
                        child: Divider(),
                      ),

                      Padding(
                        padding: EdgeInsets.only(
                          left: 10,
                          top: 10,
                          right: 15,
                          bottom: 5,
                        ),
                        child: Text(
                          'Конфигурация ассистента',
                          style: TextStyle(
                            fontSize: 22,
                            fontWeight: FontWeight.bold,
                          ),
                        ),
                      ),

                      Padding(
                        padding: EdgeInsets.only(
                          left: 10,
                          top: 5,
                          right: 15,
                          bottom: 5,
                        ),
                        child: Text(
                          'Версия модели Vosk',
                          style: TextStyle(
                            fontSize: 18,
                            fontWeight: FontWeight.bold,
                            color: Color.fromARGB(255, 255, 183, 129),
                          ),
                        ),
                      ),

                      Padding(
                        padding: EdgeInsets.only(
                          left: 10,
                          top: 7,
                          right: 15,
                          bottom: 5,
                        ),
                        child: Align(
                          alignment: Alignment.centerLeft,
                          child: SizedBox(
                            width: 330,
                            child: DropdownButtonFormField(
                              decoration: InputDecoration(
                                border: OutlineInputBorder(),
                              ),
                              initialValue: voskVersionValue,
                              items: <DropdownMenuItem>[
                                DropdownMenuItem(
                                  value: '0.22',
                                  child: Text('0.22'),
                                ),

                                DropdownMenuItem(
                                  value: '0.4',
                                  child: Text('0.4'),
                                ),
                              ],
                              onChanged: (value) {
                                setState(() {
                                  voskVersionValue = value;
                                });
                              },
                            ),
                          ),
                        ),
                      ),
                    ],
                  ),
                ),

                Padding(
                  padding: EdgeInsets.only(right: 15, left: 10),
                  child: Divider(),
                ),

                Padding(
                  padding: EdgeInsets.only(left: 10, top: 5, bottom: 15),
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: ElevatedButton.icon(
                      onPressed: saveSettings,
                      label: Text('Сохранить'),
                      icon: Icon(Icons.save),
                      style: ElevatedButton.styleFrom(
                        padding: EdgeInsets.symmetric(horizontal: 10),
                        alignment: Alignment.centerLeft,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class ScriptsPage extends StatefulWidget {
  const ScriptsPage({super.key});

  @override
  State<ScriptsPage> createState() => ScriptsPageState();
}

class ScriptsPageState extends State<ScriptsPage> {
  TextEditingController searchController = TextEditingController(text: '');
  
  late File keywordsFile;
  late File weightsFile;
  late File scriptsFile;

  late Map<String, dynamic> keywords;
  late Map<String, dynamic> weights;
  late Map<String, dynamic> scriptsConst;
  late Map<String, dynamic> scripts;

  @override
  void initState() {
    super.initState();

    keywordsFile = File(
      '${p.dirname(Platform.resolvedExecutable)}\\config\\keywords.json',
    );
    
    weightsFile = File(
      '${p.dirname(Platform.resolvedExecutable)}\\config\\weights.json',
    );

    scriptsFile = File(
      '${p.dirname(Platform.resolvedExecutable)}\\config\\scripts.json',
    );

    loadData();
    searchController.addListener(() {
      searchScripts(searchController.text);
    });
  }

  void loadData() {
    keywords = json.decode(keywordsFile.readAsStringSync());
    weights = json.decode(weightsFile.readAsStringSync());
    scripts = json.decode(scriptsFile.readAsStringSync());
    scriptsConst=Map.of(scripts);
  }

  void saveData() {
    final encoder = JsonEncoder.withIndent('  ');
    keywordsFile.writeAsStringSync(encoder.convert(keywords));
    weightsFile.writeAsStringSync(encoder.convert(weights));
    scriptsFile.writeAsStringSync(encoder.convert(scripts));
  }

  void editScript(String id) {
    Navigator.push(
      context,
      MaterialPageRoute(
        builder: (context) => EditScriptPage(name: id),
      ),
    );
  }

  void deleteScript(String name) {
    loadData();
    List<dynamic> itemsToDelete = [];
    List<dynamic> wordsToDelete = [];
    

    String keywordString = scripts[name]['keyword'];
    keywordString = keywordString.replaceAll(', ', ',');
    keywordString = keywordString.toLowerCase();
    final keyphrases = keywordString.split(',');

    double wordWeight;
    
    for(var keyphrase in keyphrases) {
      for(var word in keyphrase.split(' ')) {
        for(var item in keywords['script'][word]) {
          if (item['parameter'] == name) {
            itemsToDelete.add(item);
          } 
        }
        for(var item in itemsToDelete) {
          keywords['script'][word].remove(item);
        }
      }
    }
    
    for(var keyphrase in keyphrases) {
      wordWeight = 1/keyphrase.split(' ').length;

      for(var word in keyphrase.split(' ')) {
        for(int i = 0; i < keywords['main'][word].length; i++) {
          if (keywords['main'][word][i]['parameter'] == 'script' && keywords['main'][word][i]['weight'] == wordWeight) {
            keywords['main'][word].removeAt(i);
            break;
          }
        }
      }
    }
    

    itemsToDelete = [];
    for(var keyphrase in keyphrases) {
      for(var word in keyphrase.split(' ')) {
        if(keywords['script'][word].isEmpty) {
          wordsToDelete.add(word);
        }
      }
    }

    for(var word in wordsToDelete) {
      keywords['script'].remove(word);

      for(var item in keywords['main'][word]) {
        if (item['parameter'] == 'script') {
          itemsToDelete.add(item);
        }
      }
      
      for(var item in itemsToDelete) {
        keywords['main'][word].remove(item);
      }
      if (keywords['main'][word].isEmpty) {
        keywords['main'].remove(word);
      }
    }
    
    setState(() {
      scripts.remove(name);
      scriptsConst=scripts;
    });
    
    weights['script'].remove(name);

    final encoder = JsonEncoder.withIndent('  ');
    
    scriptsFile.writeAsStringSync(encoder.convert(scripts));
    weightsFile.writeAsStringSync(encoder.convert(weights));
    keywordsFile.writeAsStringSync(encoder.convert(keywords));
  }

  void searchScripts(String query) {
    List<String> scriptsToRemove = [];
    scripts=Map.from(scriptsConst);
    for(var script in scriptsConst.keys) {
      if (!script.toLowerCase().contains(query.toLowerCase())) {
        scriptsToRemove.add(script);
      }
    }
    setState(() {
      for(var script in scriptsToRemove) {
        scripts.remove(script);
      }
    });
  }

  void exportScripts() async {
    loadData();

    FilePickerResult? pickedFile = await FilePicker.platform.pickFiles();

    final scriptsToExport = {
      'keywords': keywords,
      'weights': weights,
      'scripts': scripts
    };

    late File fileToExport;
    if (pickedFile != null) {
      fileToExport = File(pickedFile.files.single.path!);
    } else {
      return;
    }

    final encoder = JsonEncoder.withIndent('  ');
    fileToExport.writeAsStringSync(encoder.convert(scriptsToExport));

    if (mounted) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Text('Сценарии сохранены.'),
          backgroundColor: Color.fromARGB(255, 255, 183, 129),
          showCloseIcon: true,
          duration: Duration(seconds: 2, milliseconds: 500),
          action: SnackBarAction(
            label: 'Показать в папке', 
            onPressed: () async {
              await Process.start('start', [fileToExport.parent.path], runInShell: true);
            }
          ),
        )
      );
    }
  }

  void importScripts() async {
    FilePickerResult? pickedFile = await FilePicker.platform.pickFiles();

    late File fileToImport;
    if (pickedFile != null) {
      fileToImport = File(pickedFile.files.single.path!);
    } else {
      return;
    }

    try {
      final scriptsToImport = json.decode(fileToImport.readAsStringSync());

      keywords = scriptsToImport['keywords'];

      weights = scriptsToImport['weights'];

      setState(() {
        scripts = scriptsToImport['scripts'];
      });

      scriptsConst=Map.of(scripts);
      
      saveData();

      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Сценарии загружены.'),
            backgroundColor: Color.fromARGB(255, 255, 183, 129),
            showCloseIcon: true,
            duration: Duration(seconds: 1, milliseconds: 500),
          )
        );
      }
    } catch (exception) {
      if (mounted) {
        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('Ошибка: неправильный формат файла.'),
            backgroundColor: Colors.red,
            showCloseIcon: true,
            duration: Duration(seconds: 3),
          )
        );
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color.fromARGB(255, 40, 29, 21),
        title: Text(
          'Голосовой ассистент «Альфа»',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
      ),

      body: Row(
        children: <Widget>[
          SideColumn(),
          Padding(
            padding: EdgeInsets.symmetric(vertical: 5),
            child: VerticalDivider(),
          ),

          Expanded(
            child: ListView(
              children: <Widget>[
                Padding(
                  padding: EdgeInsets.only(
                    left: 10,
                    top: 15,
                    right: 15,
                    bottom: 5,
                  ),
                  child: Text(
                    'Сценарии',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                ),

                Row(
                  children: <Widget>[
                    Padding(
                      padding: EdgeInsets.only(
                        left: 10,
                        top: 7,
                        right: 10,
                        bottom: 5,
                      ),
                      child: Align(
                        alignment: Alignment.centerLeft,
                        child: SizedBox(
                          width: 490,
                          child: TextField(
                            controller: searchController,
                            decoration: InputDecoration(
                              border: OutlineInputBorder(
                                borderSide: BorderSide(color: Colors.black),
                              ),
                              hintText: 'Поиск сценариев',
                            ),
                          ),
                        ),
                      ),
                    ),

                    Padding(
                      padding: EdgeInsets.only(left: 5),
                      child: ElevatedButton.icon(
                        onPressed: () {
                          searchController.text='';
                        },
                        label: Text('Очистить'),
                        icon: Icon(Icons.clear),
                        style: ElevatedButton.styleFrom(
                          padding: EdgeInsets.symmetric(horizontal: 10),
                          alignment: Alignment.centerLeft,
                        ),
                      ),
                    ),
                  ],
                ),

                Padding(
                  padding: EdgeInsets.only(right: 15, left: 10),
                  child: Divider(),
                ),

                Row(
                  children: <Widget>[
                    Padding(
                      padding: EdgeInsets.only(
                        left: 10,
                        right: 5,
                        top: 5,
                        bottom: 5,
                      ),
                      child: ElevatedButton.icon(
                        onPressed: () {
                          Navigator.push(
                            context,
                            MaterialPageRoute(
                              builder: (context) => AddScriptPage(),
                            ),
                          );
                        },

                        label: Text('Добавить'),
                        icon: Icon(Icons.add),
                        style: ElevatedButton.styleFrom(
                          padding: EdgeInsets.symmetric(horizontal: 10),
                          alignment: Alignment.centerLeft,
                        ),
                      ),
                    ),

                    Padding(
                      padding: EdgeInsets.only(
                        left: 5,
                        right: 5,
                        top: 5,
                        bottom: 5,
                      ),
                      child: ElevatedButton.icon(
                        onPressed: importScripts,
                        label: Text('Загрузить из файла'),
                        icon: Icon(Icons.upload),
                        style: ElevatedButton.styleFrom(
                          padding: EdgeInsets.symmetric(horizontal: 10),
                          alignment: Alignment.centerLeft,
                        ),
                      ),
                    ),

                    Padding(
                      padding: EdgeInsets.only(
                        left: 5,
                        right: 5,
                        top: 5,
                        bottom: 5,
                      ),
                      child: ElevatedButton.icon(
                        onPressed: exportScripts,
                        label: Text('Сохранить в файл'),
                        icon: Icon(Icons.download),
                        style: ElevatedButton.styleFrom(
                          padding: EdgeInsets.symmetric(horizontal: 10),
                          alignment: Alignment.centerLeft,
                        ),
                      ),
                    ),
                  ],
                ),

                Padding(
                  padding: EdgeInsets.only(left: 10, right: 15),
                  child: Divider(),
                ),

                ScriptsListView(
                  scripts: scripts,
                  editScript: editScript,
                  deleteScript: deleteScript,
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class ScriptsListView extends StatelessWidget {
  String processLineShow(String line) {
    if (line.startsWith('open_app')) {
      line = '$line.END';
      line = 'Открыть ${replaceStrings(line, ['open_app(r\'', '\').END'])}';
    } else if (line.startsWith('open_site')) {
      line = '$line.END';
      line = 'Открыть ${replaceStrings(line, ['open_site(r\'', '\').END'])}';
    } else if (line.startsWith('time.sleep')) {
      line = '$line.END';
      line = 'Подождать ${replaceStrings(line, ['time.sleep(', ').END'])} секунд';
    } else if (line.startsWith('command_line')) {
      line = '$line.END';
      line = 'Выполнить команду CMD: ${replaceStrings(line, ['command_line(r\'', '\').END'])}';
    } else if (line.startsWith('python')) {
      line = '$line.END';
      line = 'Выполнить команду Python: ${replaceStrings(line, ['python(r\'', '\').END'])}';
    } else {
      line = optionsMatchShow[line]!;
    }

    return line;
  }

  final Map<String, dynamic> scripts;
  final Function(String) deleteScript;
  final Function(String) editScript;

  const ScriptsListView({
    super.key,
    required this.scripts,
    required this.deleteScript,
    required this.editScript,
  });

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      shrinkWrap: true,
      itemCount: scripts.length,
      itemBuilder: (BuildContext context, int index) {
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Padding(
              padding: EdgeInsets.only(left: 10, top: 5, bottom: 5),
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                children: <Widget>[
                  Padding(
                    padding: EdgeInsets.only(bottom: 5),
                    child: Text(
                      scripts.keys.toList()[index],
                      style: TextStyle(
                        fontSize: 23,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),

                  Padding(
                    padding: EdgeInsets.only(top: 5, bottom: 5),
                    child: Text(
                      'Ключевая фраза: ${scripts[scripts.keys.toList()[index]]['keyword']}',
                      style: TextStyle(
                        fontSize: 19,
                        fontWeight: FontWeight.bold,
                      ),
                    ),
                  ),

                  Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children:
                        scripts[scripts.keys.toList()[index]]['actions']
                            .map<Widget>(
                              (line) => Padding(
                                padding: EdgeInsets.only(top: 2, bottom: 2),
                                child: Text(
                                  processLineShow(line),
                                  style: TextStyle(
                                    fontSize: 18,
                                    fontWeight: FontWeight.bold,
                                    color: Color(0xFFFFB781),
                                  ),
                                ),
                              ),
                            )
                            .toList(),
                  ),

                  Row(
                    children: <Widget>[
                      Padding(
                        padding: EdgeInsets.only(right: 7, top: 7, bottom: 5),
                        child: ElevatedButton.icon(
                          onPressed:
                              () => editScript(scripts.keys.toList()[index]),
                          label: Text('Изменить'),
                          icon: Icon(Icons.edit),
                          style: ElevatedButton.styleFrom(
                            padding: EdgeInsets.symmetric(horizontal: 10),
                            alignment: Alignment.centerLeft,
                          ),
                        ),
                      ),

                      Padding(
                        padding: EdgeInsets.only(right: 7, top: 7, bottom: 5),
                        child: ElevatedButton.icon(
                          onPressed:
                              () => deleteScript(scripts.keys.toList()[index]),
                          label: Text(
                            'Удалить',
                            style: TextStyle(
                              fontWeight: FontWeight.bold,
                              color: Colors.red,
                            ),
                          ),
                          icon: Icon(Icons.delete),
                          style: ElevatedButton.styleFrom(
                            iconColor: Colors.red,
                            padding: EdgeInsets.symmetric(horizontal: 10),
                            alignment: Alignment.centerLeft,
                          ),
                        ),
                      ),
                    ],
                  ),
                ],
              ),
            ),

            Padding(
              padding: EdgeInsets.only(left: 10, right: 15),
              child: Divider(),
            ),
          ],
        );
      },
    );
  }
}

class AddScriptPage extends StatefulWidget {
  const AddScriptPage({super.key});

  @override
  State<AddScriptPage> createState() => AddScriptPageState();
}

class AddScriptPageState extends State<AddScriptPage> {

  late TextEditingController nameController;
  late TextEditingController keywordController;
  
  late File keywordsFile;
  late File weightsFile;
  late File scriptsFile;

  late Map<String, dynamic> keywords;
  late Map<String, dynamic> weights;
  late Map<String, dynamic> scripts;

  List<ScriptBlockData> blocks = [
    ScriptBlockData(category: 'open_site', parameter: ''),
  ];

  @override
  void initState() {
    super.initState();


    nameController = TextEditingController(text: '');

    keywordController = TextEditingController(text: '');

    keywordsFile = File(
      '${p.dirname(Platform.resolvedExecutable)}\\config\\keywords.json',
    );

    weightsFile = File(
      '${p.dirname(Platform.resolvedExecutable)}\\config\\weights.json',
    );

    scriptsFile = File(
      '${p.dirname(Platform.resolvedExecutable)}\\config\\scripts.json',
    );
  }

  void loadData() {
    keywords = json.decode(keywordsFile.readAsStringSync());
    weights = json.decode(weightsFile.readAsStringSync());
    scripts = json.decode(scriptsFile.readAsStringSync());
  }

  void addBlock() {
    setState(() {
      blocks.add(ScriptBlockData(category: 'open_site', parameter: ''));
    });
  }

  void deleteBlock(int index) {
    setState(() {
      blocks.removeAt(index);
    });
  }

  void addScript() {
    loadData();
    List<String> scriptActions = [];
    for (var block in blocks) {
      switch (block.category)  {
        case 'open_site':
          scriptActions.add('open_site(r\'${block.parameter}\')');
        case 'open_app':
          scriptActions.add('open_app(r\'${block.parameter}\')');
        case 'time.sleep':
          scriptActions.add('time.sleep(${block.parameter.replaceAll(',', '.')})');
        case 'command_line':
          scriptActions.add('command_line(r\'${block.parameter}\')');
        case 'python':
          scriptActions.add('python(r\'${block.parameter}\')');
        default:
          scriptActions.add(block.category);
      }
    }
    scripts = {nameController.text: {'actions': scriptActions, 'keyword': keywordController.text}, ...scripts};
    
    weights['script'][nameController.text] = 0;

    String keywordString = keywordController.text;
    keywordString = keywordString.replaceAll(', ', ',');
    keywordString = keywordString.toLowerCase();
    final keyphrases = keywordString.split(',');
    
    double wordWeight;

    for (var keyphrase in keyphrases) {
      wordWeight = 1/keyphrase.split(' ').length;
      for(var word in keyphrase.split(' ')) {
        if (keywords['script'][word] != null) {
          keywords['script'][word].add({'parameter': nameController.text, 'weight': wordWeight});
        } else {
          keywords['script'][word] = [{'parameter': nameController.text, 'weight': wordWeight}];
        }

        if (keywords['main'][word] != null) {
          keywords['main'][word].add({'parameter': 'script', 'weight': wordWeight});
        } else {
          keywords['main'][word] = [{'parameter': 'script', 'weight': wordWeight}];
        }
      }
    }
    
    final encoder = JsonEncoder.withIndent('  ');
    
    scriptsFile.writeAsStringSync(encoder.convert(scripts));
    weightsFile.writeAsStringSync(encoder.convert(weights));
    keywordsFile.writeAsStringSync(encoder.convert(keywords));

    Navigator.pushNamedAndRemoveUntil(
      context,
      '/scripts',
      (route) => false,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color.fromARGB(255, 40, 29, 21),
        title: Text(
          'Голосовой ассистент «Альфа»',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
      ),

      body: Row(
        children: <Widget>[
          SideColumn(),
          Padding(
            padding: EdgeInsets.symmetric(vertical: 5),
            child: VerticalDivider(),
          ),

          Expanded(
            child: ListView(
              children: <Widget>[
                Padding(
                  padding: EdgeInsets.only(
                    left: 10,
                    top: 15,
                    right: 15,
                    bottom: 5,
                  ),
                  child: Text(
                    'Добавление сценария',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                ),

                Padding(
                  padding: EdgeInsets.only(left: 10, right: 15),
                  child: Divider(),
                ),

                Padding(
                  padding: EdgeInsets.only(
                    left: 10,
                    top: 10,
                    right: 15,
                    bottom: 5,
                  ),
                  child: Text(
                    'Параметры',
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                  ),
                ),

                Padding(
                  padding: EdgeInsets.only(
                    left: 10,
                    top: 5,
                    right: 15,
                    bottom: 5,
                  ),
                  child: Text(
                    'Имя',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Color.fromARGB(255, 255, 183, 129),
                    ),
                  ),
                ),

                Padding(
                  padding: EdgeInsets.only(
                    left: 10,
                    top: 7,
                    right: 15,
                    bottom: 5,
                  ),
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: SizedBox(
                      width: 330,
                      child: TextField(
                        controller: nameController,
                        decoration: InputDecoration(
                          border: OutlineInputBorder(
                            borderSide: BorderSide(color: Colors.black),
                          ),
                          hintText: 'Имя',
                        ),
                      ),
                    ),
                  ),
                ),

                Padding(
                  padding: EdgeInsets.only(
                    left: 10,
                    top: 5,
                    right: 15,
                    bottom: 5,
                  ),
                  child: Text(
                    'Ключевая фраза',
                    style: TextStyle(
                      fontSize: 18,
                      fontWeight: FontWeight.bold,
                      color: Color.fromARGB(255, 255, 183, 129),
                    ),
                  ),
                ),

                Padding(
                  padding: EdgeInsets.only(
                    left: 10,
                    top: 7,
                    right: 15,
                    bottom: 10,
                  ),
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: SizedBox(
                      width: 330,
                      child: TextField(
                        controller: keywordController,
                        decoration: InputDecoration(
                          border: OutlineInputBorder(
                            borderSide: BorderSide(color: Colors.black),
                          ),
                          hintText: 'Ключевая фраза',
                        ),
                      ),
                    ),
                  ),
                ),

                Padding(
                  padding: EdgeInsets.only(left: 10, right: 15),
                  child: Divider(),
                ),

                Padding(
                  padding: EdgeInsets.only(
                    left: 10,
                    top: 5,
                    right: 15,
                    bottom: 5,
                  ),
                  child: Text(
                    'Действия',
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                  ),
                ),

                AddScriptListView(
                  key: ValueKey(blocks.length),
                  blocks: blocks,
                  deleteBlock: deleteBlock
                ),

                Padding(
                  padding: EdgeInsets.only(left: 10, top: 5, bottom: 10),
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: ElevatedButton.icon(
                      onPressed: addBlock,
                      label: Text('Добавить'),
                      icon: Icon(Icons.add),
                      style: ElevatedButton.styleFrom(
                        padding: EdgeInsets.symmetric(horizontal: 10),
                        alignment: Alignment.centerLeft,
                      ),
                    ),
                  ),
                ),

                Padding(
                  padding: EdgeInsets.only(left: 10, top: 0, bottom: 15),
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: ElevatedButton.icon(
                      onPressed: addScript,
                      label: Text('Сохранить'),
                      icon: Icon(Icons.save),
                      style: ElevatedButton.styleFrom(
                        padding: EdgeInsets.symmetric(horizontal: 10),
                        alignment: Alignment.centerLeft,
                      ),
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class AddScriptListView extends StatelessWidget {
  final List<ScriptBlockData> blocks;
  final Function(int) deleteBlock;

  const AddScriptListView({
    super.key,
    required this.blocks,
    required this.deleteBlock,
  });

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      shrinkWrap: true,
      itemCount: blocks.length,
      itemBuilder: (BuildContext context, int index) {
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: <Widget>[
                ScriptBlock(
                  data: blocks[index]
                ),
                Padding(
                  padding: EdgeInsets.only(left: 10, top: 1, bottom: 5),
                  child: ElevatedButton.icon(
                    onPressed:
                        () => deleteBlock(index),
                    label: Text(
                      'Удалить',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.red,
                      ),
                    ),
                    icon: Icon(Icons.delete),
                    style: ElevatedButton.styleFrom(
                      iconColor: Colors.red,
                      padding: EdgeInsets.symmetric(horizontal: 10),
                      alignment: Alignment.centerLeft,
                    ),
                  ),
                ),
              ],
            ),
            Padding(
              padding: EdgeInsets.only(left: 10, right: 15),
              child: Divider(),
            ),
          ],
        );
      },
    );
  }
}

class EditScriptPage extends StatefulWidget {

  final String name;

  const EditScriptPage({
      super.key,
      required this.name
    });

  @override
  State<EditScriptPage> createState() => EditScriptPageState();
}

class EditScriptPageState extends State<EditScriptPage> {
  late File scriptsFile;

  late Map<String, dynamic> scripts;

  List<ScriptBlockData> blocks = [];

  ScriptBlockData processLineShow(String line) {
    String category;
    String parameter;

    if (line.startsWith('open_app')) {
      line = '$line.END';
      category = 'open_app';
      parameter = replaceStrings(line, ['open_app(r\'', '\').END']);
    } else if (line.startsWith('open_site')) {
      line = '$line.END';
      category = 'open_site';
      parameter = replaceStrings(line, ['open_site(r\'', '\').END']);
    } else if (line.startsWith('time.sleep')) {
      line = '$line.END';
      category = 'time.sleep';
      parameter = replaceStrings(line, ['time.sleep(', ').END']);
    } else if (line.startsWith('command_line')) {
      line = '$line.END';
      category = 'command_line';
      parameter = replaceStrings(line, ['command_line(r\'', '\').END']);
    } else if (line.startsWith('python')) {
      line = '$line.END';
      category = 'python';
      parameter = replaceStrings(line, ['python(r\'', '\').END']);
    } else {
      category = line;
      parameter = '';
    }

    return ScriptBlockData(category: category, parameter: parameter);
  }
  
  void loadData() {
    scripts = json.decode(scriptsFile.readAsStringSync());
  }

  @override
  void initState() {
    super.initState();

    scriptsFile = File(
      '${p.dirname(Platform.resolvedExecutable)}\\config\\scripts.json',
    );

    loadData();

    List<dynamic> script = scripts[widget.name]['actions'];
    for(var line in script) {
      blocks.add(processLineShow(line));
    }
  }

  void addBlock() {
    setState(() {
      blocks.add(ScriptBlockData(category: 'open_site', parameter: ''));
    });
  }

  void deleteBlock(int index) {
    setState(() {
      blocks.removeAt(index);
    });
  }

  void editScript() {
    loadData();
    List<String> scriptActions = [];
    for (var block in blocks) {
      switch (block.category)  {
        case 'open_site':
          scriptActions.add('open_site(r\'${block.parameter}\')');
        case 'open_app':
          scriptActions.add('open_app(r\'${block.parameter}\')');
        case 'time.sleep':
          scriptActions.add('time.sleep(${block.parameter.replaceAll(',', '.')})');
        case 'command_line':
          scriptActions.add('command_line(r\'${block.parameter}\')');
        case 'python':
          scriptActions.add('python(r\'${block.parameter}\')');
        default:
          scriptActions.add(block.category);
      }
    }

    scripts[widget.name]['actions'] = scriptActions;

    final encoder = JsonEncoder.withIndent('  ');
    
    scriptsFile.writeAsStringSync(encoder.convert(scripts));

    Navigator.pushNamedAndRemoveUntil(
      context,
      '/scripts',
      (route) => false,
    );
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color.fromARGB(255, 40, 29, 21),
        title: Text(
          'Голосовой ассистент «Альфа»',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
      ),
      body: Row(
        children: <Widget>[
          SideColumn(),
          Padding(
            padding: EdgeInsets.symmetric(vertical: 5),
            child: VerticalDivider(),
          ),

          Expanded(
            child: ListView(
              children: <Widget>[
                Padding(
                  padding: EdgeInsets.only(
                    left: 10,
                    top: 15,
                    right: 15,
                    bottom: 5,
                  ),
                  child: Text(
                    'Редактирование сценария «${widget.name}»',
                    style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                  ),
                ),

                Padding(
                  padding: EdgeInsets.only(left: 10, right: 15),
                  child: Divider(),
                ),
                Padding(
                  padding: EdgeInsets.only(
                    left: 10,
                    top: 5,
                    right: 15,
                    bottom: 5,
                  ),
                  child: Text(
                    'Действия',
                    style: TextStyle(fontSize: 22, fontWeight: FontWeight.bold),
                  ),
                ),

                EditScriptListView(
                  key: ValueKey(blocks.length),
                  blocks: blocks,
                  deleteBlock: deleteBlock
                ),

                Padding(
                  padding: EdgeInsets.only(left: 10, top: 5, bottom: 10),
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: ElevatedButton.icon(
                      onPressed: addBlock,
                      label: Text('Добавить'),
                      icon: Icon(Icons.add),
                      style: ElevatedButton.styleFrom(
                        padding: EdgeInsets.symmetric(horizontal: 10),
                        alignment: Alignment.centerLeft,
                      ),
                    ),
                  ),
                ),

                Padding(
                  padding: EdgeInsets.only(left: 10, top: 0, bottom: 15),
                  child: Align(
                    alignment: Alignment.centerLeft,
                    child: ElevatedButton.icon(
                      onPressed: editScript,
                      label: Text('Сохранить'),
                      icon: Icon(Icons.save),
                      style: ElevatedButton.styleFrom(
                        padding: EdgeInsets.symmetric(horizontal: 10),
                        alignment: Alignment.centerLeft,
                      ),
                    ),
                  ),
                ),
              ]
            )
          )
        ]
      )
    );
  }
}

class EditScriptListView extends StatelessWidget {
  final List<ScriptBlockData> blocks;
  final Function(int) deleteBlock;

  const EditScriptListView({
    super.key,
    required this.blocks,
    required this.deleteBlock,
  });

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      shrinkWrap: true,
      itemCount: blocks.length,
      itemBuilder: (BuildContext context, int index) {
        return Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: <Widget>[
            Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: <Widget>[
                ScriptBlock(
                  data: blocks[index]
                ),
                Padding(
                  padding: EdgeInsets.only(left: 10, top: 1, bottom: 5),
                  child: ElevatedButton.icon(
                    onPressed:
                        () => deleteBlock(index),
                    label: Text(
                      'Удалить',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: Colors.red,
                      ),
                    ),
                    icon: Icon(Icons.delete),
                    style: ElevatedButton.styleFrom(
                      iconColor: Colors.red,
                      padding: EdgeInsets.symmetric(horizontal: 10),
                      alignment: Alignment.centerLeft,
                    ),
                  ),
                ),
              ],
            ),
            Padding(
              padding: EdgeInsets.only(left: 10, right: 15),
              child: Divider(),
            ),
          ],
        );
      },
    );
  }
}

class ScriptBlockData {
  String category = '';
  String parameter = '';

  ScriptBlockData({required this.category, required this.parameter});
}

class ScriptBlock extends StatefulWidget {
  final ScriptBlockData data;

  const ScriptBlock({super.key, required this.data});

  @override
  State<ScriptBlock> createState() => ScriptBlockState();
}

class ScriptBlockState extends State<ScriptBlock> {
  late String categoryValue;
  late TextEditingController parameterController;
  bool isVisible = true;
  String parameterHintText = '';

  void validateDropdown() {
    if (parameterOptions.contains(categoryValue)) {
      switch (categoryValue) {
        case 'open_site':
          setState(() {
            parameterHintText = 'Ссылка';
          });
        case 'open_app':
          setState(() {
            parameterHintText = 'Путь';
          });
        case 'time.sleep':
          setState(() {
            parameterHintText = 'Время в секундах';
          });
        case 'command_line':
          setState(() {
            parameterHintText = 'Команда CMD';
          });
        case 'python':
          setState(() {
            parameterHintText = 'Команда Python';
          });
      }
      setState(() {
        isVisible = true;
      });
    } else {
      setState(() {
        isVisible = false;
      });
    }
  }

  @override
  void initState() {
    super.initState();
    categoryValue = widget.data.category;
    parameterController = TextEditingController(text: widget.data.parameter);

    validateDropdown();
    
    parameterController.addListener(() {
      widget.data.parameter = parameterController.text;
    });
  }

  @override
  Widget build(BuildContext context) {
    return Column(
      children: <Widget>[
        Padding(
          padding: EdgeInsets.only(left: 10, top: 15, right: 15, bottom: 10),
          child: SizedBox(
            width: 330,
            child: DropdownButtonFormField(
              decoration: InputDecoration(border: OutlineInputBorder()),
              initialValue: categoryValue,
              items: scriptBlockOptions,
              onChanged: (value) {
                widget.data.category = value!;
                categoryValue = value;
                validateDropdown();
              },
            ),
          ),
        ),
        Visibility(
          visible: isVisible,
          child: Padding(
            padding: EdgeInsets.only(left: 10, top: 0, right: 15, bottom: 10),
            child: SizedBox(
              width: 330,
              child: TextField(
                controller: parameterController,
                decoration: InputDecoration(
                  border: OutlineInputBorder(
                    borderSide: BorderSide(color: Colors.black),
                  ),
                  hintText: parameterHintText,
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }
}

class DocsPage extends StatefulWidget {

  const DocsPage({super.key});

  @override
  State<DocsPage> createState() => DocsPageState();
}

class DocsPageState extends State<DocsPage> {
  late String selectedParagraph;

  @override
  void initState() {
    super.initState();
    selectedParagraph = 'docs/about_app.md';
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        backgroundColor: Color.fromARGB(255, 40, 29, 21),
        title: Text(
          'Голосовой ассистент «Альфа»',
          style: TextStyle(fontWeight: FontWeight.bold),
        ),
      ),
      body: Row(
        children: <Widget>[
          Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: <Widget>[
              Padding(
                padding: EdgeInsets.only(left: 20, top: 15, right: 15, bottom: 5),
                child: Text(
                  'Документация',
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
              ),

              Padding(
                padding: EdgeInsets.only(left: 16, right: 16, top: 5, bottom: 5),
                child: SizedBox(
                  width: 170,
                  height: 50,
                  child: TextButton(
                    onPressed: () {
                      setState(() {
                        selectedParagraph = 'docs/about_app.md';
                      });
                    },
                    child: Align(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        'Основы',
                        style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                ),
              ),

              Padding(
                padding: EdgeInsets.only(left: 16, right: 16, top: 5, bottom: 5),
                child: SizedBox(
                  width: 170,
                  height: 50,
                  child: TextButton(
                    onPressed: () {
                      setState(() {
                        selectedParagraph = 'docs/settings.md';
                      });
                    },
                    child: Align(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        'Настройки',
                        style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                ),
              ),

              Padding(
                padding: EdgeInsets.only(left: 16, right: 16, top: 5, bottom: 5),
                child: SizedBox(
                  width: 170,
                  height: 50,
                  child: TextButton(
                    onPressed: () {
                      setState(() {
                        selectedParagraph = 'docs/scripts.md';
                      });
                    },
                    child: Align(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        'Сценарии',
                        style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                ),
              ),

              Padding(
                padding: EdgeInsets.only(left: 16, right: 16, top: 5, bottom: 5),
                child: SizedBox(
                  width: 170,
                  height: 50,
                  child: TextButton(
                    onPressed: () {
                      setState(() {
                        selectedParagraph = 'docs/functions.md';
                      });
                    },
                    child: Align(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        'Функции',
                        style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                ),
              ),
              Padding(
                padding: EdgeInsets.only(left: 16, right: 16, top: 5, bottom: 5),
                child: SizedBox(
                  width: 170,
                  height: 50,
                  child: TextButton(
                    onPressed: () {
                      setState(() {
                        selectedParagraph = 'docs/keywords.md';
                      });
                    },
                    child: Align(
                      alignment: Alignment.centerLeft,
                      child: Text(
                        'Команды',
                        style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                      ),
                    ),
                  ),
                ),
              ),
            ],
          ),

          Padding(
            padding: EdgeInsets.symmetric(vertical: 5),
            child: VerticalDivider(),
          ),
          Expanded(
            child: FutureBuilder(
              key: ValueKey(selectedParagraph),
              future: rootBundle.loadString(selectedParagraph),
              builder: (context, snapshot) {
                if (snapshot.hasData) {
                  return Align(
                    alignment: Alignment.topLeft,
                    child: Markdown(
                      padding: EdgeInsets.only(
                        left: 8,
                        right: 10,
                        top: 14,
                        bottom: 14
                      ),
                      shrinkWrap: true, 
                      styleSheet: MarkdownStyleSheet(
                        p: TextStyle(fontSize: 16),
                        h1: TextStyle(color: Color.fromARGB(255, 255, 183, 129)),
                        h1Padding: EdgeInsets.only(top: 3),

                        h2: TextStyle(color: Color.fromARGB(255, 255, 183, 129)),
                        h2Padding: EdgeInsets.only(top: 7),

                        listBullet: TextStyle(fontSize: 20)

                      ),
                      data: snapshot.data!
                    ),
                  );
                }
                return const Center(child: CircularProgressIndicator());
              },
            )
          )
        ]
      )
    ); 
  }
}

class SideColumn extends StatelessWidget {
  const SideColumn({super.key});

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: <Widget>[
        Padding(
          padding: EdgeInsets.only(left: 20, top: 15, right: 15, bottom: 5),
          child: Text(
            'Управление',
            style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
          ),
        ),

        Padding(
          padding: EdgeInsets.only(left: 16, right: 16, top: 5, bottom: 5),
          child: SizedBox(
            width: 170,
            height: 50,
            child: ElevatedButton(
              style: ElevatedButton.styleFrom(
                padding: EdgeInsets.symmetric(horizontal: 16),
                alignment: Alignment.centerLeft,
              ),
              onPressed: () async {
                await Process.start('start', ['alpha_core.exe'], runInShell: true);
              },
              child: Text(
                'Запустить',
                style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
              ),
            ),
          ),
        ),

        Padding(
          padding: EdgeInsets.only(left: 16, right: 16, top: 5, bottom: 5),
          child: SizedBox(
            width: 170,
            height: 50,
            child: TextButton(
              onPressed: () {
                Navigator.pushNamedAndRemoveUntil(
                  context,
                  '/',
                  (route) => false,
                );
              },
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'Главная',
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
              ),
            ),
          ),
        ),

        Padding(
          padding: EdgeInsets.only(left: 16, right: 16, top: 5, bottom: 5),
          child: SizedBox(
            width: 170,
            height: 50,
            child: TextButton(
              onPressed: () {
                Navigator.pushNamedAndRemoveUntil(
                  context,
                  '/settings',
                  (route) => false,
                );
              },
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'Настройки',
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
              ),
            ),
          ),
        ),

        Padding(
          padding: EdgeInsets.only(left: 16, right: 16, top: 5, bottom: 5),
          child: SizedBox(
            width: 170,
            height: 50,
            child: TextButton(
              onPressed: () {
                Navigator.pushNamedAndRemoveUntil(
                  context,
                  '/scripts',
                  (route) => false,
                );
              },
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'Сценарии',
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
              ),
            ),
          ),
        ),

        Padding(
          padding: EdgeInsets.only(left: 16, right: 16, top: 5, bottom: 5),
          child: SizedBox(
            width: 170,
            height: 50,
            child: TextButton(
              onPressed: () {
                Navigator.pushNamed(
                  context,
                  '/docs',
                );
                
              },
              child: Align(
                alignment: Alignment.centerLeft,
                child: Text(
                  'Справка',
                  style: TextStyle(fontSize: 24, fontWeight: FontWeight.bold),
                ),
              ),
            ),
          ),
        ),
      ],
    );
  }
}
