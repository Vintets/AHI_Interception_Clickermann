
# Проект  AHI_Interception_Clickermann

Working with AHI_Interception in Clickermann via Python

---------------------------------------------------------


## Description

С помощью модуля на Python и библиотеки interception-python прокидываем команды в Clickermann.
Обмен команд между Clickermann и Python идёт посредством отправки сообщений окну (POSTMESSAGE).


## Зависимости Requirements

![Python version](https://img.shields.io/badge/python-3.9%2B-blue)
> Требуется Python 3.9.7+

Установка зависимостей:
```sh
pip3 install -r requirements.txt
```
(added only interception-python module)


## Установка драйвера AHI Interception
Драйвер-перехватчик Interception
https://github.com/oblitum/Interception
Для удобства, в данном проекте уже скачан архив Interception_v1.0.1.7z

- установить драйвер (запускать в консоли, от имени администратора):
```sh
command line installer/install-interception.exe /install
```

Если запустить install-interception.exe без каких-либо аргументов в консоли, выдаст инструкции по установке.

- перезагрузиться


## Конфигурирование Configuration

- В настройках Clickermann ``Clickermann\data\config.ini`` должно быть установлено  
Код сообщения, на которое должена реагировать ф-ция GetMessage  
``msg_hook = 1024``

- В скрипте
    ```sh
    $AHI_wnd_title_py = "AHI_Interception_py"
    ```
    ``$AHI_wnd_title_py`` : заголовок создаваемого питоновского окна


### Состав файлов

- `CM_AHI_Interception_exemple.cms` - пример использования в своём скрипте
- `AHI_Interception_lib.cms` - библиотека для Clickermann
- `AHI_Interception.py` - Python модуль
- `Base_Demo_AHI_Interception.py` - демо работы драйвера на чистом python (для проверки работы самого драйвера)

____


## License

:license:  
/*******************************************************
 * Copyright 2023 Vintets <programmer@vintets.ru> - All Rights Reserved
 *
 * Unauthorized copying of this file, via any medium is strictly prohibited
 * Proprietary and confidential
 * Written by Vintets <programmer@vintets.ru>, Octember 2023
 *
 * This file is part of AHI_Interception_Clickermann project.
 * AHI_Interception_Clickermann can not be copied and/or distributed without the express
 * permission of Vintets
*
 * This program is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY;
 * without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.
*******************************************************/
