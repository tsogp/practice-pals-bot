<h1 align="center"> Practice Pals Bot :robot:</h1>

<p align="center">
  <a href="https://github.com/tsogp/practice-pals/blob/main/LICENSE" target="_blank"> <img alt="license" src="https://img.shields.io/github/license/tsogp/practice-pals?style=for-the-badge&labelColor=090909"></a>
  <a href="https://github.com/tsogp/practice-pals/releases/latest" target="_blank"> <img alt="last release" src="https://img.shields.io/github/v/release/tsogp/practice-pals?style=for-the-badge&labelColor=090909"></a>
  <a href="https://github.com/tsogp/practice-pals/commits/main" target="_blank"> <img alt="last commit" src="https://img.shields.io/github/last-commit/tsogp/practice-pals?style=for-the-badge&labelColor=090909"></a>
  <a href="https://github.com/tsogp/practice-pals/graphs/contributors" target="_blank"> <img alt="commit activity" src="https://img.shields.io/github/commit-activity/m/tsogp/practice-pals?style=for-the-badge&labelColor=090909"></a>
</p>

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
       $ git clone https://github.com/tsogp/practice-pals.git
       $ cd practice-pals
       ```
    * Вариант 2 - [Скачать ZIP](https://github.com/tsogp/practice-pals/archive/refs/heads/main.zip)
 
2. Создать виртуальное окружение
```bash
$ python3 -m venv venv
```

3. Активировать виртуальное окружение
```bash
$ source venv/bin/activate
```

4. Установить все зависимости:
```bash
(venv)$ pip install -r ./requirements.txt
```

5. Создать файл `./.env`. В переменной `BOT_TOKEN` должен быть записан токен Вашего Telegram бота, полученный от
[@BotFather](https://t.me/botfather) ([подробнее](https://tlgrm.ru/docs/bots#botfather))
```text
BOT_TOKEN = "your_token"
```

6. Запустить `./src/main.py`

7. Деактивация виртуального окружения:
```bash
(venv)$ deactivate
```

<a id="chapter-5"></a>

## :open_hands: Лицензия

Ставьте звёздочку ⭐️ на репозиторий

GNU General Public License v3.0

Полный текст в [LICENSE](LICENSE)

