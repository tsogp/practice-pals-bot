<h1 align="center"> Practice Pals Bot :robot:</h1>

## Навигация

* [Описание проекта](#chapter-0)
* [Как начать](#chapter-1)
* [Лицензия](#chapter-5)

<a id="chapter-0"></a>

## :page_facing_up: Описание проекта

**Practice Pals Bot** ([@practice_pals_bot](https://t.me/practice_pals_bot)) - Telegram-бот сервиса [Practice Pals](https://t.me/practicepals), главная цель
которого - помочь каждому найти себе друзей по интересам.

<a id="chapter-1"></a>

## :hammer: Как начать

1. Скачать данный репозиторий
    * Вариант 1
        1. Установить [Git](https://git-scm.com/download)
        2. Клонировать репозиторий
       ```bash
       git clone https://github.com/tsogp/practice-pals.git
       cd practice-pals
       ```
    * Вариант 2 - [Скачать ZIP](https://github.com/tsogp/practice-pals/archive/refs/heads/main.zip)

2. Установить все зависимости:

```commandline
pip install -r ./requirements.txt
```

3. Создать в папке `./src` файл **bottoken.py**

```python
TOKEN = ""  # Your bot's token from @BotFather
```

Где в переменной `TOKEN` должен быть записан токен Вашего Telegram бота, полученный от
[@BotFather](https://t.me/botfather). [Подробнее](https://tlgrm.ru/docs/bots#botfather)

4.Запустить `./main.py`

<a id="chapter-5"></a>

## :open_hands: Лицензия

Ставьте звёздочку ⭐️ на репозиторий

GNU General Public License v3.0

Полный текст в [LICENSE](LICENSE)

